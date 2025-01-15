from flask_login import UserMixin
from app import socketio, app
from flask_login import current_user
from flask_socketio import join_room, leave_room, send, rooms
from utils.database import get_user
from utils import database
from config import Config
import os
import json

# region 当前用户
class WebUser(UserMixin):
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_id(self):
        return self.user_id

# endregion

# region websocket
# 连接部分
socketio.broadcast_room_count = {}
socketio.notification_room_count = {}
@socketio.on("connect", namespace="/broadcast")
def on_connect():
    if current_user.is_authenticated:
        if str(current_user.user_id) not in socketio.broadcast_room_count:
            socketio.broadcast_room_count[str(current_user.user_id)] = 0
        socketio.broadcast_room_count[str(current_user.user_id)] += 1
        join_room(str(current_user.user_id))
    
@socketio.on("disconnect", namespace="/broadcast")
def on_disconnect():
    if current_user.is_authenticated:
        if str(current_user.user_id) not in socketio.broadcast_room_count:
            socketio.broadcast_room_count[str(current_user.user_id)] = 0
        socketio.broadcast_room_count[str(current_user.user_id)] -= 1
        leave_room(str(current_user.user_id))
        
@socketio.on("connect", namespace="/notification")
def on_connect():
    if current_user.is_authenticated:
        if str(current_user.user_id) not in socketio.notification_room_count:
            socketio.notification_room_count[str(current_user.user_id)] = 0
        socketio.notification_room_count[str(current_user.user_id)] += 1
        
        join_room(str(current_user.user_id))
        
        user_datas = get_user(current_user.user_id)["user"]
        if user_datas["user_datas"]["unread_message"]:
            database.update_user(current_user.user_id, "unread_message", False)
            send_notification_to_user(current_user.user_id, {"title": "您有新的消息", "content": "点击查看新的未读消息", "fuc": "jump_to_other_page_with_ui('/notification')"})
        
    
@socketio.on("disconnect", namespace="/notification")
def on_disconnect():
    if current_user.is_authenticated:
        if str(current_user.user_id) not in socketio.notification_room_count:
            socketio.notification_room_count[str(current_user.user_id)] = 0
        socketio.notification_room_count[str(current_user.user_id)] -= 1
        leave_room(str(current_user.user_id))

# 函数部分
def send_broadcast_message(title, content, fuc=''):
    socketio.emit("message", {'title':title, 'content': content, 'fuc':fuc}, namespace="/broadcast")

def send_fuc_to_user( _to, fuc):
    socketio.emit("fuc", fuc, room=str(_to), namespace="/broadcast")


def send_notification_to_user(_to, data):
    # 判断room内是否有用户
    try:
        if socketio.notification_room_count[str(_to)] == 0:
            # 如果没有则将该用户的未读消息布尔改为true
            database.update_user(int(_to), "unread_message", True)
            return
    except:
        database.update_user(int(_to), "unread_message", True)
        return
    # 发送通知
    socketio.emit("message", {'data': data}, room=str(_to), namespace="/notification")
    
def send_chat_notification(_to):
    def set_unread(_to):
        user_datas = database.get_user(_to)
        if user_datas["success"]:
            user_data = user_datas["user"]
            
            user_data["friends"][str(current_user.user_id)] = True
            
            del user_data["user_datas"]["password"]
            del user_data["user_datas"]["next_level_need_days"]
            del user_data["user_space_info"]["praise_count"]
            del user_data["other"]
            
            with open(os.path.join(Config.USER_INFO_DIR, str(_to), "user_info.json"), "w+", encoding="utf-8") as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
    try:
        if socketio.notification_room_count[str(_to)] != 0:
            socketio.emit("chat_notification", {'sender_username': current_user.username}, room=str(_to), namespace="/notification")
        else:
            set_unread(_to)
    except:
        set_unread(_to)


@socketio.on("connect", namespace="/chat")
def on_connect():
    join_room(str(current_user.user_id))
        
    
@socketio.on("disconnect", namespace="/chat")
def on_disconnect():
    leave_room(str(current_user.user_id))

def send_chat_message(_to, message):
    socketio.emit("message", {'_from': current_user.username, 'content': message}, room=str(_to), namespace="/chat")
    
# endregion