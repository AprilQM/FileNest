from flask import request, jsonify, current_app
from flask_login import current_user,login_required
from app.api import api
from app.models import DatabaseUser

from utils.database import get_user, update_user
from config import Config


@api.route("/change_ui_color", methods=["POST"])
@login_required
def change_ui_color():
    data = request.get_json()
    color = data.get("color")
    color_name_dict = {
        "艳红": 0,
        "橘橙": 1,
        "米黄": 2,
        "铜绿": 3,
        "钴青": 4,
        "星阁": 5,
        "樱紫": 6,
        "黑白": 7,
        "黑金": 8
    }
    user_datas = get_user(current_user.user_id)["user"]["user_datas"]
    
    if user_datas["is_admin"] and color_name_dict[color] == 8:
        with current_app.app_context():
            update_user(current_user.user_id, "color", color_name_dict[color])
        return jsonify(
                {
                    "success": True, 
                    "colors": Config.WEBCONFIG["front"]["themes"][8]
                }
            )
        
    if user_datas["level"]  == 6 and color_name_dict[color] in [6, 7]:
        with current_app.app_context():
            update_user(current_user.user_id, "color", color_name_dict[color])
        return jsonify(
                {
                    "success": True, 
                    "colors": Config.WEBCONFIG["front"]["themes"][color_name_dict[color]]
                }
            )
    
    if user_datas["level"] <= color_name_dict[color]:
        return jsonify(
                {
                    "success": False
                }
            )
    else:
        with current_app.app_context():
            update_user(current_user.user_id, "color", color_name_dict[color])
        return jsonify(
                {
                    "success": True, 
                    "colors": Config.WEBCONFIG["front"]["themes"][color_name_dict[color]]
                }
            )
    
@api.route("/change_privacy_mode", methods=["POST"])
@login_required
def change_privacy_mode():
    try:
        user_datas = get_user(current_user.user_id)["user"]
        visit_my_space = user_datas["setting"]["visit_my_space"]
        update_user(current_user.user_id, "visit_my_space", not visit_my_space)

        return jsonify({
            "success": True,
            "state": not visit_my_space
        })
    except:
        return jsonify(
            {
                "success": True
            }
        )
        
@api.route("/change_name", methods=["POST"])
@login_required
def change_name():
    data = request.get_json()
    values = data.get("values")
    new_name = values[0]
    
    if DatabaseUser.query.filter_by(username=new_name).first():
        return jsonify({
            "success": False,
            "message": "用户名存在"
        })
        
    with current_app.app_context():
        update_user(current_user.user_id, "username", new_name)
    
    return jsonify({
        "success": True,
        "message": "修改成功！"
    })