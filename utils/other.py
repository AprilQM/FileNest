import base64
from config import Config
import os
import json
from datetime import datetime
import hashlib
import utils.database as database
from PIL import Image
import io
import random
import smtplib
from email.mime.text import MIMEText
import logging
from logging.handlers import TimedRotatingFileHandler
import time
from flask import request, current_app
from flask_login import current_user
from urllib.parse import urlparse
import re




# region 加密
def hash_encrypt(plain_text, salt=None):
    """
    对明文使用哈希算法进行加密。
    
    :param plain_text: 要加密的明文
    :param salt: 可选的盐值，用于增强安全性
    :return: 哈希值（十六进制字符串）
    """
    # 如果提供了盐值，将其拼接到明文前
    if salt:
        plain_text = salt + plain_text
    
    # 使用 SHA-256 计算哈希值
    hash_object = hashlib.sha256(plain_text.encode('utf-8'))
    return hash_object.hexdigest()

# endregion

# region 用户文件
def create_user_info(user):
    user_id = str(user.user_id)
    # 如果存在用户文件夹且文件夹内容正确才为通过
    
    #判断用户文件夹是否存在
    if user_id in os.listdir(Config.USER_INFO_DIR):
        # 判断是否为文件夹
        if os.path.isdir(os.path.join(Config.USER_INFO_DIR, user_id)):
            # 判断是否存在user_info.json
            if "user_info.json" in os.listdir(os.path.join(Config.USER_INFO_DIR, user_id)):
                # 判断是否为文件
                if os.path.isfile(os.path.join(Config.USER_INFO_DIR, user_id, "user_info.json")):
                    # 检查文件正确性
                    flag = False
                    
                    try:
                        file_user_info = json.loads(open(os.path.join(Config.USER_INFO_DIR, user_id, "user_info.json"), "r", encoding="utf-8").read())
                        # 判断是否为正确的用户信息 id 用户名 邮箱
                        if file_user_info["user_datas"]["user_id"] != user.user_id or file_user_info["user_datas"]["username"] != user.username or file_user_info["user_datas"]["email"] != user.email:
                            flag = True
                    
                        for i in ["last_modified_time", "user_datas", "user_space_info", "friends", "setting", "friend_request"]:
                            if i not in file_user_info:
                                flag = True
                            
                        # user_datas子字典的整形判断
                        for i in ["user_id", "color", "level", "check_in_days", "last_check_time"]:
                            if type(file_user_info["user_datas"][i]) != int:
                                flag = True
                        
                        # 判断等级范围
                        if not 0 <= file_user_info["user_datas"]["level"] <= 6:
                            flag = True

                        # user_datas子字典的字符串判断
                        for i in ["username", "email", "register_time", "logined_time"]:
                            if type(file_user_info["user_datas"][i]) != str:
                                flag = True
                        
                        # user_datas子字典的布尔判断
                        for i in ["is_consent_agreement", "is_banned", "is_admin", "unread_message"]:
                            if type(file_user_info["user_datas"][i]) != bool:
                                flag = True
                    
                        # user_space_info的字符串判断
                        for i in ["slogan","avatar_file", "background_file"]:
                            if type(file_user_info["user_space_info"][i]) != str:
                                flag = True
                        
                        # user_space_info的praise列表内容判断
                        for i in file_user_info["user_space_info"]["praise"]:
                            if type(i) != int:
                                flag = True
                        
                        # friends的好友消息的布尔判断
                        for i in file_user_info["friends"]:
                            if type(file_user_info["friends"][i]) != bool:
                                flag = True

                        if "tag" not in file_user_info["user_space_info"]:
                            flag = True
                            
                        # setting的整形判断
                        for i in ["visit_my_space"]:
                            if type(file_user_info["setting"][i]) != int:
                                flag = True

                    except:
                        flag = True
                        
                    if flag:
                        print(f"ID为{user_id}的用户信息文件格式错误，重新创建文件")
                        create_user_info_json(user)
                else:
                    create_user_info_json(user)
            else:
                create_user_info_json(user)
        else:
            os.remove(os.path.join(Config.USER_INFO_DIR, user_id))
            os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id))
            create_user_info_json(user)
    else:   
        # 创建文件夹
        os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id))
        create_user_info_json(user)
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "avatar")):
        os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id, "avatar"))
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "chat")):
        os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id, "chat"))
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "background")):
        os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id, "background"))
    
    # 创建邮件消息文件
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "notification")):
        os.mkdir(os.path.join(Config.USER_INFO_DIR, user_id, "notification"))
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "login.json")):
        with open(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "login.json"), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "friend.json")):
        with open(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "friend.json"), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "server.json")):
        with open(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "server.json"), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    if not os.path.exists(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "other.json")):
        with open(os.path.join(Config.USER_INFO_DIR, user_id, "notification", "other.json"), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)


def create_user_info_json(user):
    init_user_info = {
            "last_modified_time": int(time.time()),
            "user_datas":{
                "user_id": user.user_id, 
                "username": user.username, 
                "email": user.email, 
                "level": 1, 
                "color": 0,
                "check_in_days": 0,
                "last_check_time": int(time.time()),
                "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "logined_time": "", 
                "is_consent_agreement": False, 
                "is_banned": False,
                "is_admin": False,
                "unread_message": False
            },
            "user_space_info":{
                "slogan":"这个人很懒，什么都没有留下。",
                "avatar_file": "",
                "background_file": "",
                "praise": [],
                "tag": []
            },
            "friend_request":{},
            "setting":{
                # 公开 好友 不公开
                "visit_my_space": 0,
            },
            "friends" : {}
        }
    with open(f"./{Config.USER_INFO_DIR}/{user.user_id}/user_info.json", "w", encoding="utf-8") as f:
        json.dump(init_user_info, f, ensure_ascii=False, indent=4)
# endregion

# region 前端工具
def get_user_theme(username=""):
    if username == "":
        if current_user.is_authenticated:
            user_data = database.get_user(current_user.user_id)
            if user_data["success"]:
                user_data = user_data["user"]
                color_index = user_data["user_datas"]["color"]
                return Config.WEBCONFIG["front"]["themes"][color_index]
            else:
                return KeyError(f"未知ID: {current_user.user_id}")
        else:
            return Config.WEBCONFIG["front"]["themes"][0]
    else:
        user_id = database.get_user_id_by_username(username)["user_id"]
        user_data = database.get_user(user_id)
        if user_data["success"]:
            user_data = user_data["user"]
            if user_data["setting"]["visit_my_space"] == 0 or (user_data["setting"]["visit_my_space"] == 1 and str(current_user.user_id) in user_data["friends"])  or current_user.user_id == user_id:
                color_index = user_data["user_datas"]["color"]
                return Config.WEBCONFIG["front"]["themes"][color_index]
            else:
                if current_user.is_authenticated:
                    user_data = database.get_user(current_user.user_id)
                    if user_data["success"]:
                        user_data = user_data["user"]
                        color_index = user_data["user_datas"]["color"]
                        return Config.WEBCONFIG["front"]["themes"][color_index]
                    else:
                        return KeyError(f"未知ID: {current_user.user_id}")
                else:
                    return Config.WEBCONFIG["front"]["themes"][0]
        else:
            return KeyError(f"未知ID: {user_id}")

def get_user_datas(username=None):
    if username:
        user_id = database.get_user_id_by_username(username)["user_id"]
    
        user_datas = database.get_user(user_id)
        
        if user_datas["user"]["setting"]["visit_my_space"] == 0 or (user_datas["user"]["setting"]["visit_my_space"] == 1 and str(current_user.user_id) in user_datas["user"]["friends"])  or current_user.user_id == user_id:
            user_datas = database.get_user(user_id)
            if user_datas["success"]:
                user_datas = user_datas["user"]
                del user_datas["last_modified_time"]
                
                usename = user_datas["user_datas"]["username"]
                level = user_datas["user_datas"]["level"]
                
                del user_datas["user_datas"]
                
                user_datas["user_datas"] = {}
                user_datas["user_datas"]["user_id"] = user_id
                user_datas["user_datas"]["level"] = level
                user_datas["user_datas"]["username"] = usename
                
                
                if current_user.is_authenticated:
                    user_datas["is_praise"] = current_user.user_id in user_datas["user_space_info"]["praise"]
                else:
                    user_datas["is_praise"] = False
                    
                
                del user_datas["other"]
                user_datas["is_friend"] = str(current_user.user_id) in user_datas["friends"]
                del user_datas["friends"]
                del user_datas["setting"]
                
                
                return True, user_datas
        
        return False, {
            "user_datas":{
                "user_id": 0,
                "username": "游客",
                "level": 0
            },
            "user_space_info":{
                "tag": []
            }
        }
    if current_user.is_authenticated:
        user_datas = database.get_user(current_user.user_id)
        if user_datas["success"]:
            user_datas = user_datas["user"]
            del user_datas["last_modified_time"]
            del user_datas["user_datas"]["password"]
            del user_datas["user_datas"]["is_consent_agreement"]
            del user_datas["user_datas"]["is_banned"]
            del user_datas["user_datas"]["is_admin"]
            
            friends_id_dict = user_datas["friends"]
            del user_datas["friends"]
            friends_username_dict = {}
            for i in friends_id_dict:
                this_user_datas = database.get_user(i)["user"]
                friends_username_dict[this_user_datas["user_datas"]["username"]] = [friends_id_dict[i], this_user_datas["user_space_info"]["slogan"]]
            user_datas["friends"] = friends_username_dict
            
            return True, user_datas
    else:
        return False, {
            "user_datas":{
                "user_id": 0,
                "username": "游客",
                "level": 0
            },
            "user_space_info":{
                "tag": []
            }
        }
    

def make_png(avatar_path, max_width=150, max_height=150):
    # 打开头像文件
    with Image.open(avatar_path) as img:
        # 如果图片是 GIF 动图，提取第一帧
        if img.format == 'GIF' and getattr(img, "is_animated", False):
            img.seek(0)  # 定位到第一帧

        # 检查图片模式，如果不是 RGB 模式则进行转换
        if img.mode in ("RGBA", "P"):  # 包括透明和调色板模式
            img = img.convert("RGB")  # 转换为 RGB 模式以支持 JPEG

        # 获取原始图片的宽度和高度
        width, height = img.size

        # 计算缩放比例，保持等比缩放
        ratio = min(max_width / width, max_height / height)

        # 根据计算出的比例调整图片大小
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 将压缩后的图片保存到内存流
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)  # 调整质量参数 (0-100)
        img_io.seek(0)

        return img_io

# region 日志
def re_analyze_log(log):
    log_re = r'\[(?P<time>[^\]]+)\] \[(?P<method>[^\]]+)\] \[(?P<type>[^\]]+)\] \(\s*ID : (?P<user_id>[^\)]+)\s*\) - (?P<request_path>[^\s]+)'

    response = re.match(log_re, log)
    response = response.groupdict()
    response["type"] = response["type"].upper()
    response["request_path"] = urlparse(response["request_path"]).path
    response["method"] = response["method"].upper()
    response["user_id"] = int(response["user_id"])
    
    return response



def analyze_log(log_nema, group_by="time"):
    log_dict = {}
    
    # 读取日志文件
    with open(Config.LOG_DIR + log_nema, "r", encoding="utf-8") as file:
        for line in file.readlines():
            this_log = re_analyze_log(line)
            
            # 根据group_by参数进行分组
            if group_by == "time":
                group_key = int(this_log["time"].split(":")[0])  # 按小时分组
            elif group_by == "method":
                group_key = this_log["method"]  # 按请求方法分组
            elif group_by == "user_id":
                group_key = this_log["user_id"]  # 按用户ID分组
            elif group_by == "request_path":
                group_key = this_log["request_path"]  # 按请求路径分组
            else:
                raise ValueError(f"Unsupported group_by value: {group_by}")
            
            # 初始化该分组的统计数据
            if group_key not in log_dict:
                log_dict[group_key] = {
                    'time': {},
                    'method': {},
                    'type': {},
                    'user_id': {},
                    'request_path': {}
                }
            
            # 访问时间统计
            this_time = this_log["time"].split(":")[0]
            if this_time not in log_dict[group_key]["time"]:
                log_dict[group_key]["time"][this_time] = 1
            else:
                log_dict[group_key]["time"][this_time] += 1
            
            # 访问方法统计
            if this_log["method"] not in log_dict[group_key]["method"]:
                log_dict[group_key]["method"][this_log["method"]] = 1
            else:
                log_dict[group_key]["method"][this_log["method"]] += 1
                
            # 访问类型统计
            if this_log["type"] not in log_dict[group_key]["type"]:
                log_dict[group_key]["type"][this_log["type"]] = 1
            else:
                log_dict[group_key]["type"][this_log["type"]] += 1
                
            # 访问用户ID统计
            if this_log["user_id"] not in log_dict[group_key]["user_id"]:
                log_dict[group_key]["user_id"][this_log["user_id"]] = 1
            else:
                log_dict[group_key]["user_id"][this_log["user_id"]] += 1
                
            # 访问路径统计
            if this_log["request_path"] not in log_dict[group_key]["request_path"]:
                log_dict[group_key]["request_path"][this_log["request_path"]] = 1
            else:
                log_dict[group_key]["request_path"][this_log["request_path"]] += 1
    
    return log_dict

# endregion

#region 其他
def create_code(length=16, state=0):
    s = ""
    for i in range(length):
        if state == 0:
            s += chr(random.randint(33, 126))
        elif state == 1:
            up = chr(random.randint(65, 90))
            low = chr(random.randint(97, 122))
            num = str(random.randint(0, 9))
            choice = (up, low, num)
            s += random.choice(choice)
        elif state == 2:
            s += str(random.randint(0, 9))
    return s

# 发送验证码
def send_code(mail):
    try:
        code = create_code(6, 2)
        content = f"您的验证码为:{code}，时效为5分钟。\n\n如果不是本人操作，请忽略此信息。"
        message = MIMEText(content, "plain", "utf-8")
        message["From"] = Config.mail_config["send_by"]
        message["To"] = mail
        message["Subject"] = "【文栖验证码】"
        # 使用第三方服务发送
        smtp = smtplib.SMTP_SSL(Config.mail_config["mail_host"], Config.mail_config["mail_port"], "utf-8")
        smtp.login(Config.mail_config["send_by"], Config.mail_config["mail_password"])
        smtp.sendmail(Config.mail_config["send_by"], mail, message.as_string())
        print(code)
        return code
    except Exception as e:
        print(e)
    
    
# 日志记录

def figout_user_level(days):
    next_level_need_days_list = [0, 5, 15, 35, 65, 105]
    new_level = 105
    for i in next_level_need_days_list:
        if days >= i:
            new_level = next_level_need_days_list.index(i) + 1
    return new_level
    
# 获取用户的消息
def get_notifications(user_id):
    notifications_path = f"{Config.USER_INFO_DIR}/{user_id}/notification"
    b = {}
    for i in ["friend", "login", "other", "server"]:
        b[i] = json.loads(open(f"{notifications_path}/{i}.json", "r", encoding="utf-8").read())
    return b

# 写入消息
def write_notifications(user_id, notification_type, notification_content):
    notifications_path = f"{Config.USER_INFO_DIR}/{user_id}/notification"
    with open(f"{notifications_path}/{notification_type}.json", "r", encoding="utf-8") as f:
        a = json.loads(f.read())
    a.append(notification_content)
    with open(f"{notifications_path}/{notification_type}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(a))
    
    
# endregion