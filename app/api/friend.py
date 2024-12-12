from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
from utils import friend
import utils.other as other
from app.models import DatabaseUser
from config import Config
from utils.web import WebUser
import time
from datetime import datetime
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
    
    