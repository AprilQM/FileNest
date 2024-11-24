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
    
    WEBCONFIG = {
        "rear": {
            "port": 5000,
            "host": "0.0.0.0",
            "debug": True
        },
        "front": {
            # 主色调
            # 辅助色
            # 文本色
            # 背景色
            # 背景冲突色
            # 成功色
            # 警告色
            # 错误色
            # 悬停色
            # 点击色
            "theme_color": {
                "艳红": [
                    "#ED5A65",
                    "#F7B2AB",
                    "#3C3C3C",
                    "#FFFFFF",
                    "#ED5A65",
                    "#28A745",
                    "#FFC107",
                    "#DC3545",
                    "#C84850",
                    "#B23A42"
                ],
                "琥珀黄": [
                    "#FEBA07",
                    "#FEE28B",
                    "#4A4A4A",
                    "#F9F9F9",
                    "#FEBA07",
                    "#28A745",
                    "#FFC107",
                    "#DC3545",
                    "#E1A006",
                    "#C58805"
                ],
                "蛙绿": [
                    "#45B787",
                    "#A7DFC1",
                    "#3E3E3E",
                    "#F8F8F8",
                    "#45B787",
                    "#28A745",
                    "#FFC107",
                    "#DC3545",
                    "#3BA678",
                    "#2D8F63"
                ],
                "瀑布蓝": [
                    "#51C4D3",
                    "#A7E3EA",
                    "#3E3E3E",
                    "#F7F7F7",
                    "#51C4D3",
                    "#2BAF84",
                    "#F7B731",
                    "#D64545",
                    "#47B3C1",
                    "#3998A6"
                ],
                "暗黑": [
                    "#000000",
                    "#1C1C1E",
                    "#FFFFFF",
                    "#121212",
                    "#FEFEFE",
                    "#2BAF84",
                    "#F7B731",
                    "#D64545",
                    "#575757",
                    "#333333"
                ]
            }
        }        
    }
    
