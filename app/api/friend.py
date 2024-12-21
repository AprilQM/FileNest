from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
from utils import friend
import utils.other as other
from app.models import DatabaseUser
from config import Config
from utils.web import WebUser
from utils.web import send_notification_to_user
import time
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
        friend.clear_message_light(target_user_id)
        return friend.clear_message_light(target_user_id)
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