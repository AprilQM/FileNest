from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
import utils.other as other
from app.models import DatabaseUser
from config import Config
from utils.web import WebUser, send_notification_to_user
import time
from datetime import datetime
import os
import json
import re
from app import db

from app.api import api

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    next_url = data.get('next_url')
    if not next_url:
        next_url = '/home'
    username = data.get('username')
    password = data.get('password')
    user_data = database.get_user(username)
    back = {
        "success": False
    }
    with current_app.app_context():
        user_id = database.get_user_id_by_username(username)
        if user_id["success"]:
            user_id = user_id["user_id"]
        else:
            back["massage"] = "no_user"
            return jsonify(back)
    user_data = database.get_user(user_id)["user"]
    if other.hash_encrypt(password) == user_data["user_datas"]["password"]:
        back["success"] = True
        database.update_user(user_id, "logined_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        login_user(WebUser(user_id, user_data["user_datas"]["username"]))
        back["next_url"] = next_url
        
        # 记录登录

        # 定义正则表达式
        os_pattern = r"\(([^;]+(?:; [^;)]+)*)\)"  # 匹配操作系统信息
        browser_pattern = r"(Chrome/\d+\.\d+\.\d+\.\d+|Safari/\d+\.\d+|Firefox/\d+\.\d+)"  # 添加 Firefox 支持

        # 提取操作系统
        os_match = re.search(os_pattern, request.headers.get('User-Agent'))
        os_info = os_match.group(1) if os_match else "未知操作系统"

        # 提取浏览器
        browser_match = re.search(browser_pattern, request.headers.get('User-Agent'))
        browser_info = browser_match.group(1) if browser_match else "未知浏览器"
        
        login_hsitory = json.loads(open(Config.USER_INFO_DIR + f"/{user_id}/notification/login.json", "r", encoding="utf-8").read())
        login_hsitory.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "os": os_info,
            "browser": browser_info
        })
        
        with open(Config.USER_INFO_DIR + f"{user_id}/notification/login.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(login_hsitory))
        
        # 给该账号的其他设备发送登录提醒
        send_notification_to_user(user_id, {
            "title": "有设备登录了该账号",
            "content": "有设备登录了该账号，点击查看详细信息。",
            "fuc": "jump_to_other_page_with_ui('/notification')"
        })
        
        return jsonify(back)
    else:
        back["message"] = "password_error"
        return jsonify(back)

@api.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/home")


@api.route('/register_1', methods=['POST'])
def register_1():
    datas = request.get_json()
    email = datas.get('email')
    username = datas.get('username').replace(" ", "")
    password = datas.get('password')
    if len(DatabaseUser.query.filter_by(email=email).all()) > 0:
        return jsonify({
            "massage":"fail",
            "reason": "email_exist"
        })
    # 验证用户名不存在
    if len(DatabaseUser.query.filter_by(username=username).all()) > 0:
        return jsonify({
            "massage":"fail",
            "reason": "username_exist"
        })
    # 验证用户名长度
    if not 3 <= len(username) <= 12:
        return jsonify({
            "massage":"fail",
            "reason": "username_length_error"
        }) 
    # 验证密码长度
    if len(password) < 6:
        return jsonify({
            "massage":"fail",
            "reason": "password_length_error"
        })
    # 验证用户名是否包含非法字符
    flag = False
    for i in username:
        if i in Config.ILLEGAL_CHARACTERS:
            flag = True
            break
    if flag:
        return jsonify({
            "massage":"fail",
            "reason": "username_illegal_character"
        })
    
    session['temp_email'] = email
    session['temp_username'] = username
    session['temp_password'] = password
    session['temp_code'] = (other.send_code(email), time.time())
    return jsonify({
        "massage":"success",
        "reason": ""
    })
    
@api.route('/register_2', methods=['POST'])
def register_2():
    datas = request.get_json()
    code = datas.get('code')
    try:
        if session['temp_code'][0] != code:
            return jsonify({
                "massage":"fail",
                "reason": "code_error"
            })
    except:
        return jsonify({
            "massage":"fail",
            "reason": "code_error"
        })
    if time.time() - session['temp_code'][1] > 300:
        session.pop('temp_email', None)
        session.pop('temp_username', None)
        session.pop('temp_password', None)
        session.pop('temp_code', None)
        return jsonify({
            "massage":"fail",
            "reason": "code_timeout"
        })
        
    if len(DatabaseUser.query.filter_by(email=session["temp_email"]).all()) > 0:
        return jsonify({
            "massage":"fail",
            "reason": "email_exist"
        })
    if len(DatabaseUser.query.filter_by(username=session["temp_username"]).all()) > 0:
        return jsonify({
            "massage":"fail",
            "reason": "username_exist"
        })
    with current_app.app_context():
        user_id = database.create_user(session["temp_username"], session["temp_email"], session["temp_password"])["user_id"]
    login_user(WebUser(user_id, session["temp_username"]))
    session.pop('temp_email', None)
    session.pop('temp_username', None)
    session.pop('temp_password', None)
    session.pop('temp_code', None)
    return jsonify({
        "massage":"success",
        "reason": ""
    })