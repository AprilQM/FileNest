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
            # 主色
            # 次色
            # 次次色
            # 文本色
            # 背景色
            # 背景冲突色
            # 悬停色
            # 点击色
            "theme_color": {
                "red": [
                    "#ED5A65",
                    "#F48B94",
                    "#FAD1D4",
                    "#333333",
                    "#FFFFFF",
                    "#ED5A65",
                    "#D7444F",
                    "#B5353E"
                ],
                "yellow": [
                    "#FEBA07",
                    "#FFD355",
                    "#FFF0C2",
                    "#333333",
                    "#FFFFFF",
                    "#FEBA07",
                    "#E5A506",
                    "#C58805"
                ],
                "green": [
                    "#45B787",
                    "#76D2AC",
                    "#C2EBDD",
                    "#333333",
                    "#FFFFFF",
                    "#45B787",
                    "#379A6F",
                    "#2D7D5C"
                ],
                "blue": [
                    "#51C4D3",
                    "#84D8E1",
                    "#D2F2F6",
                    "#333333",
                    "#FFFFFF",
                    "#51C4D3",
                    "#3FA9B6",
                    "#2F8490"
                ]
            }
        }        
    }
    
