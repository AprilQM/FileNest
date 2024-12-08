from flask import Blueprint

api = Blueprint('api', __name__)

# 导入该蓝图下的路由
from app.api import auth
from app.api import webuser
from app.api import cloud
from app.api import project
from app.api import forum
from app.api import setting
