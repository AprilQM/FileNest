from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
import utils.other as other
from utils.web import WebUser
from config import Config
import os
import time

from app.api import api

@api.route("/check_in", methods=["POST"])
def check_in():
    back = {
        'success': False
    }
    user_datas = database.get_user(current_user.user_id)["user"]
    if int(time.time()) - user_datas["user_datas"]['last_check_time'] > 86400:
        database.update_user(current_user.user_id, "check_in_days", user_datas["user_datas"]['check_in_days'] + 1)
        database.update_user(current_user.user_id, "last_check_time", int(time.time()))
        database.update_user(current_user.user_id, "level", other.figout_user_level(user_datas["user_datas"]['check_in_days'] + 1))
        back['success'] = True
        next_level_need_days_list = [0, 5, 15, 35, 65, 105]
        user_datas = database.get_user(current_user.user_id)["user"]
        if user_datas["user_datas"]["level"] >= 6:
            next_level_need_days = "∞"
        else:
            next_level_need_days = next_level_need_days_list[user_datas["user_datas"]["level"]]
        back["level"] = user_datas["user_datas"]['level']
        back["check_in_days"] = user_datas["user_datas"]['check_in_days']
        back["next_level_need_days"] = next_level_need_days
    
    return back
