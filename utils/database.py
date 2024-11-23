from app import db
from app.models import DatabaseUser
import os
import json

from utils.other import aes_encrypt, aes_decrypt


# region 用户表单管理
# 增加新用户
def add_user(user):
    # 创建数据库表
    db.create_all()
    # 创建用户文件夹和json文件
    
    
    
    # 写入数据库
    db.session.add(user)
    db.session.commit() 


# 删除用户
def delete_user(user_id):
    # 删除数据库表
    db.session.query(DatabaseUser).filter_by(user_id=user_id).delete()
    db.session.commit()
    # 删除用户文件夹
    os.rmdir(f"./userdatas/{user_id}")
    
# 更新用户信息
def update_user_info(user_id, new_data_name, new_data_value):
    # 三项数据库修改内容
    if new_data_name in ["email", "username", "password"]:
        user = DatabaseUser.query.filter_by(user_id=user_id).first()
        if new_data_name == "email":
            user.email = new_data_value
        elif new_data_name == "username":
            user.username = new_data_value
        elif new_data_name == "password":
            user.password = aes_encrypt(new_data_value)
            db.session.commit()
            # 如果是修改的密码就不用修改用户数据了，直接返回
            return
        db.session.commit()
    # 修改用户信息文件
    with open(f"./userdatas/{user_id}/user_info.json", "r", encoding="utf-8") as f:
        user_folder_info = json.load(f)

    if new_data_name in user_folder_info["user_datas"].keys():
        user_folder_info["user_datas"][new_data_name] = new_data_value
    if new_data_name in user_folder_info["user_space_info"].keys():
        user_folder_info["user_space_info"][new_data_name] = new_data_value
    
    # 写入文件
    with open(f"./userdatas/{user_id}/user_info.json", "w", encoding="utf-8") as f:
        json.dump(user_folder_info, f, ensure_ascii=False, indent=4)

# 查询用户信息
def query_user_info(user_id):
    
    user_datas = json.loads(open(f"./userdatas/{user_id}/user_info.json", "r", encoding="utf-8").read())
    user_datas["user_datas"]["password"] = aes_decrypt(DatabaseUser.query.filter_by(user_id=user_id).first().password)
    return user_datas
    

# endregion