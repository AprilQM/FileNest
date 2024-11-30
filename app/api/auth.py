from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
import utils.other as other
from utils.web import WebUser
import os

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
    if user_data["user_datas"]["is_cancellation"]:
        back["massage"] = "no_user"
        return jsonify(back)
    if user_data["user_datas"]["is_banned"]:
        back["massage"] = "banned"
        return jsonify(back)
    if other.hash_encrypt(password) == user_data["user_datas"]["password"]:
        back["success"] = True
        login_user(WebUser(user_id, user_data["user_datas"]["username"]))
        back["next_url"] = next_url
        return jsonify(back)
    else:
        back["message"] = "password_error"
        return jsonify(back)

@api.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/home")