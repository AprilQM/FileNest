from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from config import Config
import os
import json
from datetime import datetime
import hashlib
import utils.database as database


# region 加密
# 定义加密和解密函数
def aes_encrypt(plain_text, key = Config.PASSWORD_SALT):
    # 将明文转换为字节数据
    plain_text_bytes = plain_text.encode('utf-8')
    # 确保密钥是16字节、24字节或32字节长（AES的密钥长度限制）
    key = key.ljust(32)[:32].encode('utf-8')
    
    # 生成随机的初始化向量 (IV)
    iv = get_random_bytes(16)
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    # 加密数据
    cipher_text = cipher.encrypt(plain_text_bytes)
    # 返回IV和密文的组合，并进行Base64编码
    return base64.b64encode(iv + cipher_text).decode('utf-8')


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
                    
                        for i in ["last_modified_time", "user_datas", "user_space_info"]:
                            if i not in file_user_info:
                                flag = True
                            
                        # user_datas子字典的整形判断
                        for i in ["user_id", "color"]:
                            if type(file_user_info["user_datas"][i]) != int:
                                flag = True
                        
                        # user_datas子字典的字符串判断
                        for i in ["username", "email", "register_time", "logined_time"]:
                            if type(file_user_info["user_datas"][i]) != str:
                                flag = True
                        
                        # user_datas子字典的布尔判断
                        for i in ["is_consent_agreement", "is_banned", "is_admin", "is_cancellation"]:
                            if type(file_user_info["user_datas"][i]) != bool:
                                flag = True
                    
                        # user_space_info的字符串判断
                        for i in ["slogan","avatar_path", "background_path"]:
                            if type(file_user_info["user_space_info"][i]) != str:
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
def create_user_info_json(user):
    init_user_info = {
            "last_modified_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_datas":{
                "user_id": user.user_id, 
                "username": user.username, 
                "email": user.email, 
                "level": 1, 
                "color": 0,
                "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "logined_time": "", 
                "is_consent_agreement": False, 
                "is_banned": False,
                "is_admin": False,
                "is_cancellation": False
            },
            "user_space_info":{
                "slogan":"这个人很懒，什么都没有留下。",
                "avatar_path": "",
                "background_path":""
            }
        }
    with open(f"./{Config.USER_INFO_DIR}/{user.user_id}/user_info.json", "w", encoding="utf-8") as f:
        json.dump(init_user_info, f, ensure_ascii=False, indent=4)
# endregion

# region 前端工具
def get_user_theme(current_user):
    if current_user.is_authenticated:
        user_data = database.get_user(current_user.user_id)
        if user_data["success"]:
            user_data = user_data["user"]
            color_index = user_data["user_datas"]["color"]
            if user_data["user_datas"]["is_cancellation"]:
                color_index = 0
            return Config.WEBCONFIG["front"]["themes"][color_index]
        else:
            return KeyError(f"未知ID: {current_user.user_id}")
    else:
        return Config.WEBCONFIG["front"]["themes"][0]
# endregion