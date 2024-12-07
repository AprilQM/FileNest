import smtplib
from email.mime.text import MIMEText

# 邮件配置
mail_config = {
    "send_by": "2173840670@qq.com",
    "mail_password": "xsvyvafzgzyedijc",  # 使用应用专用密码
    "mail_host": "smtp.qq.com",
    "mail_port": 465
}

# 创建邮件内容
msg = MIMEText("这是邮件正文", "plain", "utf-8")
msg["From"] = mail_config["send_by"]
msg["To"] = "2730391712@qq.com"
msg["Subject"] = "测试邮件"

try:
    # 使用SSL加密连接
    with smtplib.SMTP_SSL(mail_config["mail_host"], mail_config["mail_port"]) as server:
        server.login(mail_config["send_by"], mail_config["mail_password"])
        server.sendmail(mail_config["send_by"], "2730391712@qq.com", msg.as_string())
        print("邮件发送成功！")
except smtplib.SMTPException as e:
    print(f"邮件发送失败: {e}")
