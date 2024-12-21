from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
import utils.other as other
import utils.web as web
from utils.web import WebUser
from config import Config
import os
import time
from datetime import datetime


from app.api import api

@api.route("/get_user_avatar_small/<username>")
def get_user_avatar_small(username):
    if username == "游客":
        return send_from_directory(Config.STATIC_DIR, "default_avatar.png")
    user_id = database.get_user_id_by_username(username)["user_id"]
    with current_app.app_context():
        user_datas = database.get_user(user_id)["user"]
        avatar_file = user_datas["user_space_info"]["avatar_file"]
        
        # 构建头像文件路径，使用 os.path.join 正确拼接
        avatar_path = os.path.join(Config.USER_INFO_DIR, str(user_id),"avatar", avatar_file)

        
        # 检查文件是否存在
        if not os.path.exists(avatar_path) or avatar_file == "":
            return send_from_directory(Config.STATIC_DIR, "default_avatar.png")

        # 返回处理后的图片
        return send_file(other.make_png(avatar_path), mimetype='image/jpeg')
    
@api.route("/get_user_avatar/<username>")
@login_required
def get_user_avatar(username):
    if username == "游客":
        return send_from_directory(Config.STATIC_DIR, "default_avatar.png")
    user_id = database.get_user_id_by_username(username)["user_id"]
    with current_app.app_context():
        user_datas = database.get_user(user_id)["user"]
        avatar_file = user_datas["user_space_info"]["avatar_file"]
        
        # 构建头像文件路径，使用 os.path.join 正确拼接
        avatar_path = os.path.join(Config.USER_INFO_DIR, str(user_id),"avatar", avatar_file)

        
        # 检查文件是否存在
        can_visit = other.get_user_datas(username)[0]
        if not os.path.exists(avatar_path) or avatar_file == "" or not can_visit:
            return send_from_directory(Config.STATIC_DIR, "default_avatar.png")

        # 返回处理后的图片
        return send_file("." + avatar_path, mimetype='image/jpeg')
    

@api.route("/get_user_background/<username>")
@login_required
def get_user_background(username):
    if username == "游客":
        return send_from_directory(Config.STATIC_DIR, "default_background.png")
    user_id = database.get_user_id_by_username(username)["user_id"]
    with current_app.app_context():
        user_datas = database.get_user(user_id)["user"]
        background_file = user_datas["user_space_info"]["background_file"]
        
        # 构建头像文件路径，使用 os.path.join 正确拼接
        background_path = os.path.join(Config.USER_INFO_DIR, str(user_id),"background", background_file)

        
        # 检查文件是否存在
        can_visit = other.get_user_datas(username)[0]
        if not os.path.exists(background_path) or background_file == "" or not can_visit:
            return send_from_directory(Config.STATIC_DIR, "default_background.png")

        # 返回处理后的图片
        return send_file("." + background_path, mimetype='image/jpeg')
    


@api.route("/get_user_lv_img/<username>")
@login_required
def get_user_lv_img(username):
    if username == "游客":
        abort(404)
    user_id = database.get_user_id_by_username(username)["user_id"]
    with current_app.app_context():
        user_datas = database.get_user(user_id)["user"]
        level = user_datas["user_datas"]["level"]
        return send_from_directory(Config.STATIC_DIR, f"lv_img/lv{level}.svg")

@api.route("/check_in", methods=["POST"])
@login_required
def check_in():
    back = {
        'success': False
    }
    user_datas = database.get_user(current_user.user_id)["user"]
    if int(time.time()) - user_datas["user_datas"]['last_check_time'] > 43200:
        database.update_user(current_user.user_id, "check_in_days", user_datas["user_datas"]['check_in_days'] + 1)
        database.update_user(current_user.user_id, "last_check_time", int(time.time()))
        database.update_user(current_user.user_id, "level", other.figout_user_level(user_datas["user_datas"]['check_in_days'] + 1))
        back['success'] = True
        next_level_need_days_list = [0, 5, 15, 35, 65, 105]
        user_datas = database.get_user(current_user.user_id)["user"]
        if user_datas["user_datas"]["level"] >= 6:
            next_level_need_days = user_datas["user_datas"]["check_in_days"]
        else:
            next_level_need_days = next_level_need_days_list[user_datas["user_datas"]["level"]]
        back["level"] = user_datas["user_datas"]['level']
        back["check_in_days"] = user_datas["user_datas"]['check_in_days']
        back["next_level_need_days"] = next_level_need_days
    
    return back

@api.route("/praise_user", methods=['POST'])
@login_required
def praise_user():
    back = {
        'success': False
    }
    datas = request.get_json()
    target_id = int(datas.get('target_id'))
    web.send_notification_to_user(target_id, {
        "title": "有人赞了你",
        "content": f"{current_user.username} 赞了你,点击跳转到访客列表界面。",
        "fuc": "jump_to_other_page_with_ui('/praise_list')"
    })
    param = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        "title": "有人赞了你", 
        "content": f"<a href='/user_space/{current_user.username}' class='notification_item_a'>{current_user.username}</a> 赞了你, 快去Ta的主页回赞吧~"
        }
    other.write_notifications(target_id, "other", param)
    
    target_user_datas = database.get_user(target_id)["user"]
    
    if current_user.user_id in target_user_datas["user_space_info"]["praise"]:
        back["message"] = "already_praise"
        return jsonify(back)
    else:
        back["success"] = True
        back["praise_count"] = target_user_datas["user_space_info"]["praise_count"] + 1
        database.update_user(target_id, "praise", [current_user.user_id] + target_user_datas["user_space_info"]["praise"])
        return jsonify(back)

@api.route("/change_slogan", methods=['POST'])
@login_required
def change_slogan():
    datas = request.get_json()
    slogan = datas.get('slogan')
    database.update_user(current_user.user_id, "slogan", slogan)
    
    return jsonify({
        "success" : True
    })
        