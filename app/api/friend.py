from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
from utils import friend
import utils.other as other
from app.models import DatabaseUser
from config import Config
from utils.web import WebUser
from utils.web import send_notification_to_user, send_chat_message
import time
import json
from datetime import datetime
from utils import friend
import os
from app import db

from app.api import api

@api.route("/get_chat_histroy", methods=["POST"])
@login_required
def get_chat_histroy():
    data = request.get_json()
    target_user_name = data["target_user_name"]
    target_user_id = database.get_user_id_by_username(target_user_name)["user_id"]
    user = database.get_user(int(target_user_id))
    
    if user["success"]:
        t = friend.clear_message_light(target_user_id)
        if t["success"]:
            return jsonify(
                {
                    "success": True,
                    "chat_histroy": friend.get_chat_histroy(int(target_user_id))
                }
            )
        else:
            return jsonify({"success": False, "message": "User not found"})
    else:
        return jsonify({"success": False, "message": "User not found"})
    

@api.route("/search_user", methods=["POST"])
@login_required
def search_user():
    datas = request.get_json()
    username = datas.get("username")
    
    user_id = database.get_user_id_by_username(username)
    
    if user_id["success"]:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    

@api.route("/friend_request", methods=["POST"])
def friend_request():
    datas = request.get_json()
    username = datas.get("username")
    is_agree = datas.get("is_agree")
    user_id = database.get_user_id_by_username(username)
    if user_id["success"]:
        user_id = user_id["user_id"]
        # 清除好友请求
        friend.clear_friend_request(user_id)
        if is_agree:
            friend.add_friend(user_id)
            
            send_notification_to_user(user_id, {
                "title": "新朋友",
                "content": f"{current_user.username} 同意了你的好友请求，点击这里去和Ta聊天吧~",
                "fuc": "jump_to_other_page_with_ui('/friend')"
            })
            
            
            target_user_param = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": "同意好友请求",
                "content": f"<a href='/user_space/{current_user.username}' class='notification_item_a'>{current_user.username}</a> 同意了你的好友请求。",
            }
            other.write_notifications(user_id, "friend", target_user_param)

            # 删除我方对对方的好友请求

            user_datas = database.get_user(user_id)
            if user_datas["success"]:
                user_datas = user_datas["user"]

                if str(current_user.user_id) in user_datas["friend_request"]:
                    del user_datas["friend_request"][str(current_user.user_id)]
                    
                    del user_datas["user_datas"]["password"]
                    del user_datas["user_datas"]["next_level_need_days"]
                    del user_datas["user_space_info"]["praise_count"]
                    del user_datas["other"]

                    user_folder = os.path.join(Config.USER_INFO_DIR, str(user_id))
                    user_file_path = os.path.join(user_folder, "user_info.json")

                    with open(user_file_path, "w", encoding="utf-8") as file:
                        json.dump(user_datas, file, ensure_ascii=False, indent=4)
            



            
            return jsonify(
                {
                    "success": True,
                    "friend_request_list": friend.get_friend_request_list()
                }
            )
        else:
            
            send_notification_to_user(user_id, {
                "title": "有新的未读消息",
                "content": f"{current_user.username} 拒绝了你的好友请求。",
                "fuc": "jump_to_other_page_with_ui('/notification')"
            })
            
            
            target_user_param = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": "拒绝好友请求",
                "content": f"<a href='/user_space/{current_user.username}' class='notification_item_a'>{current_user.username}</a> 拒绝了你的好友请求。",
            }
            other.write_notifications(user_id, "friend", target_user_param)
            
            return jsonify(
                {
                    "success": True,
                    "friend_request_list": friend.get_friend_request_list()
                }
            )
        
    return jsonify(
        {
            "success": False,
            "friend_request_list": friend.get_friend_request_list()
        }
    )


@api.route("/add_friend", methods=['POST'])
def add_friend():
    datas = request.get_json()
    username = datas.get('username')
    text = datas.get('text')
    user_id = database.get_user_id_by_username(username)
    
    if user_id["success"]:
        user_id = user_id["user_id"]

        user_datas = database.get_user(user_id)["user"]

        target_user_friend_list = user_datas["friend_request"]

        if current_user.user_id == user_datas["user_datas"]["user_id"]:
            return jsonify({
                "success": False, 
                "msg" : "can_add_self"
            })
        
        if str(current_user.user_id) in target_user_friend_list:
            return jsonify({
                "success": False, 
                "msg" : "request_already"
            })
        
        if str(current_user.user_id) in user_datas["friends"]:
            return jsonify({
                "success": False, 
                "msg" : "friend_already"
            })
        
        send_notification_to_user(user_id, {
            "title" : "有新的好友申请",
            "content" : f"{current_user.username} 请求添加你为好友，点击跳转到好友请求页面", 
            "fuc" : "jump_to_other_page_with_ui('/friend_request')"
        } )

        other.write_notifications(user_id, "friend", {
            "time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "title": "你有新的好友申请",
            "content" : f"<a href='/user_space/{current_user.username}' class='notification_item_a'>{current_user.username}</a> 请求添加你为好友，快去好友界面处理一下吧~", 
        })


        del user_datas["user_datas"]["password"]
        del user_datas["user_datas"]["next_level_need_days"]
        del user_datas["user_space_info"]["praise_count"]
        del user_datas["other"]

        user_datas["friend_request"][str(current_user.user_id)] = text

        user_folder = os.path.join(Config.USER_INFO_DIR, str(user_id))
        user_file_path = os.path.join(user_folder, "user_info.json")

        with open(user_file_path, "w", encoding="utf-8") as file:
            json.dump(user_datas, file, ensure_ascii=False, indent=4)

        return jsonify({
            "success": True,
        })

    else:
        return jsonify({
            "success": False, 
            "msg" : "no_user"
        })
    

@api.route("/delete_friend", methods=["POST"])
def delete_friend():
    datas = request.get_json()
    username = datas.get("username")
    user_id = database.get_user_id_by_username(username)
    if user_id["success"]:
        user_id = user_id["user_id"]
        friend.delete_friend(user_id)
        
        user_datas = database.get_user(current_user.user_id)["user"]
        
        
        return jsonify(
            {
                "success": True,
                "friend_list": other.get_user_datas()[1]["friends"]
            }
            )
    
    return jsonify({"success": False})

@api.route("/send_message", methods=["POST"])
def send_message():
    datas = request.get_json()
    target_user_name = datas.get("target_user_name")
    message = datas.get("message")
    user_id = database.get_user_id_by_username(target_user_name)
    if user_id["success"]:
        user_id = user_id["user_id"]
    
    t = friend.write_message(user_id, message)
    if t["success"]:
        send_chat_message(user_id, message)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
    