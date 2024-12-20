from flask import request, current_app
from flask_login import current_user
from utils import database
import json
import os
from config import Config

def add_friend(target_user_id):
    # 添加好友
    if current_user.is_authenticated:
        
        # 我方创建好友
        user_datas = database.get_user(current_user.user_id)
        
        if user_datas["success"]:
            user_data = user_datas["user"]
            if str("target_user_id") in user_data["friends"]:
                return {"success": False, "message": "exist"}
            
            user_data["friends"][str(target_user_id)] = False
            
            user_folder = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id))
            user_file_path = os.path.join(user_folder, "user_info.json")
            

            del user_data["user_datas"]["password"]
            del user_data["user_datas"]["next_level_need_days"]
            del user_data["user_space_info"]["praise_count"]
            del user_data["other"]

            with open(user_file_path, "w", encoding="utf-8") as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)
            
            os.mkdir(os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id)))
            with open(os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id), "1"), "w+", encoding="utf-8") as f:
                f.write("")
        
        # 对象创建好友
        user_datas = database.get_user(target_user_id)

        if user_datas["success"]:
            user_data = user_datas["user"]
            if str(current_user.user_id) in user_data["friends"]:
                return {"success": False, "message": "exist"}

            user_data["friends"][str(current_user.user_id)] = False

            user_folder = os.path.join(Config.USER_INFO_DIR, str(target_user_id))
            user_file_path = os.path.join(user_folder, "user_info.json")

            del user_data["user_datas"]["password"]
            del user_data["user_datas"]["next_level_need_days"]
            del user_data["user_space_info"]["praise_count"]
            del user_data["other"]


            with open(user_file_path, "w", encoding="utf-8") as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)

            os.mkdir(os.path.join(Config.USER_INFO_DIR, str(target_user_id), "chat", str(current_user.user_id)))
            with open(os.path.join(Config.USER_INFO_DIR, str(target_user_id), "chat", str(current_user.user_id), "1"), "w+", encoding="utf-8") as f:
                f.write("")

        return {"success": True, "message": "success"}
        
    return {"success": False, "message": "User not found"}


def clear_message_light(target_user_id):
    # 清除消息提醒
    if current_user.is_authenticated:
        user_datas = database.get_user(current_user.user_id)
        if user_datas["success"]:
            user_data = user_datas["user"]
            if str(target_user_id) in user_data["friends"]:
                user_data["friends"][str(target_user_id)] = False
                
                del user_data["user_datas"]["password"]
                del user_data["user_datas"]["next_level_need_days"]
                del user_data["user_space_info"]["praise_count"]
                del user_data["other"]

                user_folder = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id))
                user_file_path = os.path.join(user_folder, "user_info.json")
                
                with open(user_file_path, "w", encoding="utf-8") as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)

                return {"success": True, "message": "success"}
            
    return {"success": False, "message": "User not found"}

# 清除好友请求
def clear_friend_request(target_user_id):
    if current_user.is_authenticated:
        user_datas = database.get_user(current_user.user_id)
        if user_datas["success"]:
            user_data = user_datas["user"]
            if str(target_user_id) in user_data["friend_request"]:
                del user_data["friend_request"][str(target_user_id)]
                
                del user_data["user_datas"]["password"]
                del user_data["user_datas"]["next_level_need_days"]
                del user_data["user_space_info"]["praise_count"]
                del user_data["other"]

                user_folder = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id))
                user_file_path = os.path.join(user_folder, "user_info.json")
                
                with open(user_file_path, "w", encoding="utf-8") as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)

                return {"success": True, "message": "success"}

    return {"success": False, "message": "User not found"}

# 获取好友请求列表
def get_friend_request_list():
    user_datas = database.get_user(current_user.user_id)["user"]
    friend_request_list = user_datas["friend_request"]
    friend_request_uername_list = {}
    for i in friend_request_list:
        this_user_datas = database.get_user(int(i))["user"]
        this_username = this_user_datas["user_datas"]["username"]
        friend_request_uername_list[this_username] = friend_request_list[i]
        
    return friend_request_uername_list