from flask_login import UserMixin
from app import socketio, app
from flask_login import current_user
from flask_socketio import join_room, leave_room, send
from utils.database import get_user

# region 当前用户
class WebUser(UserMixin):
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_id(self):
        return self.user_id

# endregion

# region websocket
@socketio.on("connect", namespace="/broadcast")
def on_connect():
    pass
    
@socketio.on("disconnect", namespace="/broadcast")
def on_disconnect():
    pass
    
def send_broadcast_message(title, content, fuc=''):
    socketio.emit("broadcast", {'title':title, 'content': content, 'fuc':fuc}, namespace="/broadcast")

def send_fuc_to_user( _to, fuc):
    socketio.emit("fuc", fuc, room=str(_to), namespace="/broadcast")
    
@socketio.on("connect", namespace="/chat")
def on_connect():
    if current_user.is_authenticated:
        join_room(str(current_user.user_id))
        
@socketio.on("disconnect", namespace="/chat")
def on_disconnect():
    if current_user.is_authenticated:
        leave_room(str(current_user.user_id))
        
def send_message_to_user(_from, _to, data):
    username = get_user(_from)["user"]["user_datas"]["username"]
    socketio.emit("message", {'from': username, 'data': data}, room=str(_to), namespace="/chat")

# endregion