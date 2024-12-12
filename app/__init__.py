from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, render_template
from datetime import datetime
import os


db = SQLAlchemy()
from app.models import DatabaseUser
from config import Config
from utils.other import get_user_theme as get_user_theme
from utils.other import get_user_datas as get_user_datas

app = Flask(__name__)
app.secret_key = 'filenest_secret_key'
app.config.from_object(Config)
app.session_cookie_name = 'filenest_session'

# region 日志部分
# 创建一个日志记录器
logger = logging.getLogger('flask_logger')
logger.setLevel(logging.DEBUG)

# 定义日志文件的路径，日志会按天切分，每天生成一个新的日志文件
log_handler = TimedRotatingFileHandler(
    os.path.join(Config.LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log"),
    when='midnight',
    interval=1,
    encoding="utf-8"
)
log_handler.setLevel(logging.INFO)  # 设置日志等级为INFO，可以根据需求调整
formatter = logging.Formatter('%(message)s')
log_handler.setFormatter(formatter)

# 添加 handler 到 logger
logger.addHandler(log_handler)


# 其他
@app.before_request
def log_request_info():
    user_id = 0
    if current_user.is_authenticated:
        user_id = current_user.user_id
    if "/static/" not in request.path and request.method != "OPTIONS":
        now_time = datetime.now().strftime("%H:%M:%S")
        type = "NORMAL"
        if "/api/" in request.path:
            type = "API"
            if Config.FILTRATION_API:
                return
        logger.info(f"[{now_time}] [{request.method}] [{type}] (ID : {user_id}) - {request.path}")
        
# endregion 


Session(app)

socketio = SocketIO(app)

# 身份验证
login_manager = LoginManager()
login_manager.login_view = '/auth'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    p = database.get_user(user_id)["user"]
    return web.WebUser(p["user_datas"]["user_id"], p["user_datas"]["username"])



# 捕获所有错误
if not Config.WEBCONFIG["rear"]["debug"]:
    @app.errorhandler(Exception)
    def handle_exception(e):
        # 检查是否是 HTTPException 类型
        if hasattr(e, 'code'):
            # 针对 HTTP 错误返回对应的错误页面
            return render_template("error.html", error_code=e.code, error_message=e.description, theme=get_user_theme(), user_datas=get_user_datas()[1]), e.code
        else:
            print(e)
            # 针对非 HTTP 错误返回通用错误页面
            return render_template("error.html", error_code=500, error_message="Internal Server Error", theme=get_user_theme(), user_datas=get_user_datas()[1]), 500



# 注册UI路由
from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)

# 注册API路由
from app.api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

# 工具类导入
from utils.init import init
import utils.web as web
import utils.other as other
import utils.database as database

# 初始化
init(app)

