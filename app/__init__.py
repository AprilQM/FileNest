from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
from utils.init import init
from app.models import DatabaseUser

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init(app)

    # 注册UI路由
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册API路由
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    import utils.database as database
    
    with app.app_context():
        database.delete_user(1)
    return app
