from flask import request, jsonify, current_app
from flask_login import current_user,login_required
from app.api import api
from app.models import DatabaseUser
from utils.database import get_user, update_user
from config import Config
import json

@api.route('/get_notification', methods=['POST'])
@login_required
def get_notification():
    
    datas = request.get_json()
    notification_type = datas.get('type')
    
    
    notification = json.loads(open(Config.USER_INFO_DIR + str(current_user.user_id) + f"/notification/{notification_type}.json", "r", encoding="utf-8").read())
    return jsonify({
        "success": True,
        "notification": notification
    })