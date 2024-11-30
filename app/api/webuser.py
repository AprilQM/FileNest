from flask import Blueprint, jsonify, request, send_from_directory, abort, request, current_app, redirect, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import safe_join
import utils.database as database
import utils.other as other
from utils.web import WebUser
from config import Config
import os

from app.api import api

@api.route("/get_user_avatar_small")
def get_user_avatar_small():
    if current_user.is_authenticated:
        user_id = current_user.user_id
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
    else:
        return send_from_directory(Config.STATIC_DIR, "default_avatar.png")