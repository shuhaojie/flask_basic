from flask import Blueprint

# 创建API蓝图
user_bp = Blueprint('user', __name__, url_prefix="/user")

# 导入视图函数以触发路由注册
from api.app.user import views  # noqa
from api.app.post import views  # noqa