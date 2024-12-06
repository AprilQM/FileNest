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
    for i in [Config.USER_INFO_DIR, Config.LOG_DIR, Config.USER_FILES_DIR, Config.NOTICE_DIR, Config.PROJECT_DIR, Config.FORUM_DIR]:
        if os.path.exists(i):
            if os.path.isdir(i):
                pass
            else:
                os.remove(i)
                os.mkdir(i)
        else:
            os.mkdir(i)

# 校验文件与数据库一致性
def check_file_db_consistency(app):
    # 获取所有用户
    with app.app_context():
        user_list = DatabaseUser.query.all()
        # 创建用户文件夹和json文件
        for user in user_list:
            other_utils.create_user_info(user)
