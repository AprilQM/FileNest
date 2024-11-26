import json

class Config:
    PASSWORD_SALT = 'filenestWQD153ieq'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///FileNest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
    session_cookie_name = "FileNest"
    mail_config = {
        "send_by": "2173840670@qq.com",
        "mail_password": "zysdlrricebjdihe",
        "mail_host": "smtp.qq.com",
        "mail_port": 465
        }
    USER_INFO_DIR = "./userdatas"
    CONFIG_JSON_PATH = "./config.json"
    WEBCONFIG = {
        "rear": {
            "port": 5000,
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
                        "text": "#333333"
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
                        "text": "#333333"
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
                        "text": "#333333"
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
                        "text": "#333333"
                    }
                },
                {
                    "name": "暗黑",
                    "colors": {
                        "main": "#111111",
                        "secondary1": "#333333",
                        "secondary2": "#222222",
                        "prominent": "#f9f871",
                        "background": "#202224",
                        "background2": "#171717",
                        "background_conflict": "#f0f0f0",
                        "text": "#f0f0f0"
                    }
                }
            ]
            
        }    
    }
