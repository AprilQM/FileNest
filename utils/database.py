from app import db
from app.models import DatabaseUser
import utils.other as other
import os
from config import Config
import json
from datetime import datetime
import utils.other as other
import time

# 增加用户
def create_user(username, email, password):
    try:
        # 检查是否已存在相同的用户名或邮箱
        existing_user = DatabaseUser.query.filter(
            (DatabaseUser.username == username) | (DatabaseUser.email == email)
        ).first()
        if existing_user:
            return {"success": False, "message": "Username or email already exists"}

        encrypted_password = other.hash_encrypt(password)

        # 创建新用户对象并保存到数据库
        new_user = DatabaseUser(username=username, email=email, password=encrypted_password)
        db.session.add(new_user)
        db.session.commit()  # 提交到数据库以生成 user_id

        # 创建用户对应的文件信息
        other.create_user_info(new_user)

        return {"success": True, "message": "User created successfully", "user_id": new_user.user_id}

    except Exception as e:
        db.session.rollback()  # 回滚事务
        return {"success": False, "message": str(e)}

# 查询用户
def get_user(user_id):
    user = DatabaseUser.query.get(user_id)
    if user:
        file_user_data = json.loads(open(os.path.join(Config.USER_INFO_DIR, str(user_id), "user_info.json"), "r", encoding="utf-8").read())
        file_user_data["user_datas"]["password"] = user.password
        return {"success": True, "user": file_user_data}
    return {"success": False, "message": "User not found"}

# 修改用户信息
def update_user(user_id, key, value):
    try:
        # 查找用户
        user = DatabaseUser.query.filter_by(user_id=user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}

        # 如果字段在数据库中，更新数据库
        if hasattr(user, key):
            setattr(user, key, value)
            db.session.commit()  # 提交到数据库
        
        # 更新用户文件（不管字段是否在数据库中）
        update_user_file(user_id, key, value)

        # 如果更新的是密码，进行加密
        if key == "password":
            value = other.hash_encrypt(value)

        return {"success": True, "message": f"User {key} updated successfully"}
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return {"success": False, "message": str(e)}

# 更新用户文件
def update_user_file(user_id, key, value):
    user_folder = os.path.join(Config.USER_INFO_DIR, str(user_id))
    
    if os.path.exists(user_folder):
        user_file_path = os.path.join(user_folder, "user_info.json")
        if os.path.exists(user_file_path):
            with open(user_file_path, "r", encoding="utf-8") as file:
                user_info = json.load(file)
            
            # 更新文件中的字段（如果存在于 user_datas 或 user_space_info 中）
            if key in user_info["user_datas"]:
                user_info["user_datas"][key] = value
            elif key in user_info["user_space_info"]:
                user_info["user_space_info"][key] = value
            else:
                return {"success": False, "message": f"Field '{key}' not found in user file"}

            # 更新修改时间
            user_info["last_modified_time"] = int(time.time())

            # 写回更新后的信息
            with open(user_file_path, "w", encoding="utf-8") as file:
                json.dump(user_info, file, ensure_ascii=False, indent=4)
        else:
            return {"success": False, "message": "User file not found"}
    else:
        return {"success": False, "message": "User folder not found"}

# 删除用户
def delete_user(user_id):
    user = DatabaseUser.query.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    try:
        file_user_data = json.loads(open(os.path.join(Config.USER_INFO_DIR, str(user_id), "user_info.json"), "r", encoding="utf-8").read())
        file_user_data["user_datas"]["is_cancellation"] = True
        with open(os.path.join(Config.USER_INFO_DIR, str(user_id), "user_info.json"), "w", encoding="utf-8") as file:
            json.dump(file_user_data, file, ensure_ascii=False, indent=4)
        return {"success": True, "message": "User deleted successfully"}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

# 用用户名查找用户id
def get_user_id_by_username(username):
    user = DatabaseUser.query.filter_by(username=username).first()
    if user:
        return {"success": True, "user_id": user.user_id}
    return {"success": False, "message": "User not found"}

# 用邮箱查找用户id
def get_user_id_by_email(email):
    user = DatabaseUser.query.filter_by(email=email).first()
    if user:
        return {"success": True, "user_id": user.user_id}
    return {"success": False, "message": "User not found"}