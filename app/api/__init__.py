from flask import Blueprint

api = Blueprint('api', __name__)

# 导入该蓝图下的路由
from app.api import auth
