from flask import request, current_app
from flask_login import current_user
from utils import database
from utils import web
from utils import other
import json
import os
import shutil
from datetime import datetime
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

# 删除好友
def delete_friend(target_user_id):
    if current_user.is_authenticated:
        flag = False
        user_datas = database.get_user(current_user.user_id)
        if user_datas["success"]:
            user_data = user_datas["user"]
            if str(target_user_id) in user_data["friends"]:
                del user_data["friends"][str(target_user_id)]

                del user_data["user_datas"]["password"]
                del user_data["user_datas"]["next_level_need_days"]
                del user_data["user_space_info"]["praise_count"]
                del user_data["other"]
                
                user_folder = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id))
                user_file_path = os.path.join(user_folder, "user_info.json")

                with open(user_file_path, "w", encoding="utf-8") as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)

                # 删除一整个文件夹
                shutil.rmtree(os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id)))
                
                flag  = True
                
        user_datas = database.get_user(target_user_id)
        if user_datas["success"] and flag:
            user_data = user_datas["user"]
            if str(current_user.user_id) in user_data["friends"]:
                del user_data["friends"][str(current_user.user_id)]

                del user_data["user_datas"]["password"]
                del user_data["user_datas"]["next_level_need_days"]
                del user_data["user_space_info"]["praise_count"]
                del user_data["other"]
                
                user_folder = os.path.join(Config.USER_INFO_DIR, str(target_user_id))
                user_file_path = os.path.join(user_folder, "user_info.json")

                with open(user_file_path, "w", encoding="utf-8") as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)

                # 删除一整个文件夹
                shutil.rmtree(os.path.join(Config.USER_INFO_DIR, str(target_user_id), "chat", str(current_user.user_id)))
                
                web.send_notification_to_user(target_user_id, {
                    "title" : "有新的未读消息",
                    "content": "点击查看新的未读消息",
                    "fuc": "jump_to_other_page_with_ui('/notification')"
                })
                
                other.write_notifications(target_user_id, "friend", {
                    "title": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "title" : "删除好友",
                    "content": f"您的好友 <a href='/user_space/{current_user.username}' class='notification_item_a'>{current_user.username}</a> 解除了和您的好友关系"
                })
                
                return {"success": True, "message": "success"}
                

    return {"success": False, "message": "User not found"}
                

def write_message(target_user_id, message):
    if current_user.is_authenticated:
        
        # 不需要调用config中的非法字符，只需要排除一些特殊字符即可
        message = message.replace("\n", "\\n")
            
                
        if len(message) == 0:
            return {"success": False, "message": "Message is empty"}
        
        user_folder_list = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id))
        last_message_file = 1
        for i in os.listdir(user_folder_list):
            if i.isdigit() and int(i) > last_message_file:
                last_message_file = int(i)
        last_message_file_path = os.path.join(user_folder_list, str(last_message_file))
        old_message = open(last_message_file_path, "r", encoding="utf-8").readlines()
        
        # 在原来内容基础上加新消息和消息id
        old_message.append(f"{(last_message_file - 1) * 100 + len(old_message) + 1} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 0 {message}\n")
        
        
        if len(old_message) > 100:
            # 创建新的消息文件
            new_message_file = open(os.path.join(user_folder_list, str(last_message_file+1)), "w+", encoding="utf-8")
            new_message_file.write(f"{(last_message_file - 1) * 100 + len(old_message) + 1} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 0 {message}\n")
            new_message_file.close()
            
            
        else:
            # 写入消息
            with open(last_message_file_path, "w", encoding="utf-8") as f:
                f.write("".join(old_message))
                
                
        # 同理在对方的消息列表中写入消息
        user_folder_list = os.path.join(Config.USER_INFO_DIR, str(target_user_id), "chat", str(current_user.user_id))
        last_message_file = 1
        for i in os.listdir(user_folder_list):
            if i.isdigit() and int(i) > last_message_file:
                last_message_file = int(i)
        last_message_file_path = os.path.join(user_folder_list, str(last_message_file))
        old_message = open(last_message_file_path, "r", encoding="utf-8").readlines()
        
        # 在原来内容基础上加新消息
        old_message.append(f"{(last_message_file - 1) * 100 + len(old_message) + 1} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 1 {message}\n")
        
        
        if len(old_message) > 100:
            # 创建新的消息文件
            new_message_file = open(os.path.join(user_folder_list, str(last_message_file+1)), "w+", encoding="utf-8")
            new_message_file.write(f"{(last_message_file - 1) * 100 + len(old_message) + 1} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 1 {message}\n")
            new_message_file.close()
            
            
        else:
            # 写入消息
            with open(last_message_file_path, "w", encoding="utf-8") as f:
                f.write("".join(old_message))
                
        return {"success": True, "message": "success"}
    return {"success": False, "message": "User not found"}

def get_chat_histroy(target_user_id):
    if current_user.is_authenticated:
        chat_histroy_list = []
        user_folder_list = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id))
        chat_histroy_list_temp = open(os.path.join(user_folder_list, str(len(os.listdir(user_folder_list)))), "r", encoding="utf-8").readlines()
        for chat_content in chat_histroy_list_temp:
            chat_content = chat_content.split()
            content = ""
            for i in chat_content[4:]:
                content += i + " "
            if content:
                content = content.replace("\\n", "\n")
                chat_histroy_list.append([chat_content[3], content[:-1]])
        return chat_histroy_list, len(os.listdir(user_folder_list))
    
def set_unread(my_user_id, target_user_id):
    user_datas = database.get_user(my_user_id)
    if user_datas["success"]:
        user_data = user_datas["user"]
        
        user_data["friends"][str(target_user_id)] = True
        
        del user_data["user_datas"]["password"]
        del user_data["user_datas"]["next_level_need_days"]
        del user_data["user_space_info"]["praise_count"]
        del user_data["other"]
        
        with open(os.path.join(Config.USER_INFO_DIR, str(my_user_id), "user_info.json"), "w+", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)
            
def get_last_message_page(current_history_page, target_user_name):
    target_user_id = database.get_user_id_by_username(target_user_name)["user_id"]
    
    chat_histroy_list = []
    user_folder_list = os.path.join(Config.USER_INFO_DIR, str(current_user.user_id), "chat", str(target_user_id))
    chat_histroy_list_temp = open(os.path.join(user_folder_list, str(int(current_history_page) - 1)), "r", encoding="utf-8").readlines()
    for chat_content in chat_histroy_list_temp:
        chat_content = chat_content.split()
        content = ""
        for i in chat_content[4:]:
            content += i + " "
        if content:
            content = content.replace("\\n", "\n")
            chat_histroy_list.append([chat_content[3], content[:-1]])
            
    # 由于前段是倒着渲染的 所以在这里奖聊天内容进行翻转
    chat_histroy_list.reverse()
    
    return chat_histroy_list, int(current_history_page) - 1