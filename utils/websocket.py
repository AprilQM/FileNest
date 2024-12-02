from app import socketio, app

@socketio.on("connect", namespace="/broadcast")
def on_connect():
    pass
    
@socketio.on("disconnect", namespace="/broadcast")
def on_disconnect():
    pass
    
def send_broadcast_message(title, content, fuc=''):
    socketio.emit("broadcast", {'title':title, 'content': content, 'fuc':fuc}, namespace="/broadcast")