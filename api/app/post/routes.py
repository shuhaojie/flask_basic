from flask import Blueprint

# 创建API蓝图
post_bp = Blueprint('post', __name__, url_prefix="/post")

# 导入视图函数以触发路由注册
from api.app.post import views  # noqa