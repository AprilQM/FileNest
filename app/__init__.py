from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
from utils.init import init
import utils.web as web
import utils.database as database
from app.models import DatabaseUser

def create_app():
    app = Flask(__name__)
    app.secret_key = 'filenest_secret_key'
    app.config.from_object(Config)
    app.session_cookie_name = 'filenest_session'

    init(app)
    Session(app)
    
    # 身份验证
    login_manager = LoginManager()
    login_manager.login_view = '/auth'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        p = database.get_user(user_id)["user"]
        return web.WebUser(p["user_datas"]["user_id"], p["user_datas"]["username"])

    # 注册UI路由
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册API路由
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app
