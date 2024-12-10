from flask import request, jsonify, current_app
from flask_login import current_user,login_required
from app.api import api

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
        "樱紫": 5,
        "黑白": 6,
        "黑金": 7
    }
    user_datas = get_user(current_user.user_id)["user"]["user_datas"]
    
    if user_datas["is_admin"] and color_name_dict[color] == 7:
        with current_app.app_context():
            update_user(current_user.user_id, "color", color_name_dict[color])
        return jsonify(
                {
                    "success": True, 
                    "colors": Config.WEBCONFIG["front"]["themes"][7]
                }
            )
        
    if user_datas["level"] == 6 and color_name_dict[color] == 6:
        with current_app.app_context():
            update_user(current_user.user_id, "color", color_name_dict[color])
        return jsonify(
                {
                    "success": True, 
                    "colors": Config.WEBCONFIG["front"]["themes"][6]
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