# 初始化文件

import os
from app import db
from app.models import DatabaseUser
import utils.database as database_utils
from config import Config
import utils.other as other_utils
import json

def init(app):
    # 主函数
    database_init(app)
    print("数据库初始化完成")
    folder_init()
    print("文件夹初始化完成")
    check_file_db_consistency(app)
    print("文件与数据库一致性检查完成")
    
# 数据库初始化
def database_init(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# 文件夹初始化
def folder_init():
    # 用户数据文件夹
    if os.path.exists(Config.USER_INFO_DIR):
        if os.path.isdir(Config.USER_INFO_DIR):
            pass
        else:
            os.remove(Config.USER_INFO_DIR)
            os.mkdir(Config.USER_INFO_DIR)
    else:
        os.mkdir(Config.USER_INFO_DIR)
    
    # 日志文件夹
    if os.path.exists(Config.LOG_DIR):
        if os.path.isdir(Config.LOG_DIR):
            pass
        else:
            os.remove(Config.LOG_DIR)
            os.mkdir(Config.LOG_DIR)
    else:
        os.mkdir(Config.LOG_DIR)

    

# 校验文件与数据库一致性
def check_file_db_consistency(app):
    # 获取所有用户
    with app.app_context():
        user_list = DatabaseUser.query.all()
        # 创建用户文件夹和json文件
        for user in user_list:
            other_utils.create_user_info(user)
