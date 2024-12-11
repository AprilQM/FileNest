from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# 修改名字表单
class ChangName(FlaskForm):
    first = StringField("name", validators=[DataRequired()], render_kw={"placeholder": "新昵称", "class": "input"})

# 修改邮箱表单
class ChangeMail(FlaskForm):
    first = StringField("mail", validators=[DataRequired()], render_kw={"placeholder": "新邮箱", "class": "input"})

# 修改邮箱表单
class ChangePassowrd(FlaskForm):
    first = StringField("old_password", validators=[DataRequired()], render_kw={"placeholder": "原密码", "class": "input", "type": "password"})
    second = StringField("new_password", validators=[DataRequired()], render_kw={"placeholder": "新密码", "class": "input", "type": "password"})