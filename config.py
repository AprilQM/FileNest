import json

class Config:
    SECRET_KEY = "FileNestFileNest"
    SESSION_TYPE = 'filesystem'  # 或 'redis'，'sqlalchemy' 等
    SESSION_FILE_DIR = './flask_session'
    SESSION_KEY_PREFIX = 'filenest_'
    PASSWORD_SALT = 'filenestWQ'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///FileNest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
    session_cookie_name = "FileNest"
    mail_config = {
        "send_by": "2173840670@qq.com",
        "mail_password": "xsvyvafzgzyedijc",
        "mail_host": "smtp.qq.com",
        "mail_port": 465
        }
    USER_INFO_DIR = "./userdatas/"
    LOG_DIR = "./logs/"
    STATIC_DIR = "../static/"
    USER_FILES_DIR = "./userfiles/"
    NOTICE_DIR = "./notice/"
    PROJECT_DIR = "./projects/"
    FORUM_DIR = "./forums/"
    CONFIG_JSON_PATH = "./config.json"
    ILLEGAL_CHARACTERS = [
        '/', '\\', ':', '*', '?', '"', "'", '<', '>', '|', ';',  # 路径和文件系统符号
        '?', '&', '#', '%', '=', '+',  # URL相关符号
        '<', '>', '"', "'", '/',  # HTML和JavaScript相关符号
        '(', ')', '[', ']', '{', '}', '^', '$', '.', '*', '+', '?', '|',  # 正则表达式符号
        '~', '$',  # 操作系统相关符号
        '\r', '\n', '\t',  # 控制字符
        ' ', ',', '@'  # 其他危险字符
    ]
    FILTRATION_API = True
    WEBCONFIG = {
        "rear": {
            "port": 56895,
            "host": "0.0.0.0",
            "debug": True
        },
        "front": {
            "themes": [
                {
                    "name": "艳红",
                    "colors": {
                        "main": "#ed5a65",
                        "secondary1": "#faaead",
                        "secondary2": "#ffe4e2",
                        "prominent": "#54b9ca",
                        "background": "#fef6f6",
                        "background2": "#ffffff",
                        "background_conflict": "#ed5a65",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "淡橘橙",
                    "colors": {
                        "main": "#fba414",
                        "secondary1": "#fdc456",
                        "secondary2": "#fee6a2",
                        "prominent": "#007461",
                        "background": "#FFF5E6",
                        "background2": "#ffffff",
                        "background_conflict": "#fba414",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "炒米黄",
                    "colors": {
                        "main": "#f4ce69",
                        "secondary1": "#f9e39c",
                        "secondary2": "#fef0c5",
                        "prominent": "#f9f871",
                        "background": "#FDF7E7",
                        "background2": "#ffffff",
                        "background_conflict": "#f4ce69",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "铜绿",
                    "colors": {
                        "main": "#2bae85",
                        "secondary1": "#64d0a0",
                        "secondary2": "#a4f1d3",
                        "prominent": "#f9f871",
                        "background": "#EBFAF5",
                        "background2": "#ffffff",
                        "background_conflict": "#2bae85",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "钴青",
                    "colors": {
                        "main": "#1a94bc",
                        "secondary1": "#71cde3",
                        "secondary2": "#d3f1f6",
                        "prominent": "#f9f871",
                        "background": "#E9F7FC",
                        "background2": "#ffffff",
                        "background_conflict": "#1a94bc",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "樱草紫",
                    "colors": {
                        "main": "#c06f98",
                        "secondary1": "#d898b3",
                        "secondary2": "#f1ccdc",
                        "prominent": "#f9f871",
                        "background": "#F7EDF2",
                        "background2": "#ffffff",
                        "background_conflict": "#c06f98",
                        "text": "#333333",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "黑白",
                    "colors": {
                        "main": "#111111",
                        "secondary1": "#333333",
                        "secondary2": "#222222",
                        "prominent": "#fae9a0",
                        "background": "#202224",
                        "background2": "#171717",
                        "background_conflict": "#f0f0f0",
                        "text": "#f0f0f0",
                        "text2": "#ffffff",
                        "text3": "#777777",
                        "other": "#ffffff"
                    }
                },
                {
                    "name": "黑金",
                    "colors": {
                        "main": "#111111",
                        "secondary1": "#333333",
                        "secondary2": "#222222",
                        "prominent": "#f0f0f0",
                        "background": "#202224",
                        "background2": "#171717",
                        "background_conflict": "#fae9a0",
                        "text": "#f0f0f0",
                        "text2": "#fae9a0",
                        "text3": "#e3bf71",
                        "other": "#fae9a0"
                    }
                }
            ]
            
        }    
    }
