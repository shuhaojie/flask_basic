from flask import Blueprint
from api.app.user.routes import user_bp
from api.app.post.routes import post_bp
# 创建API蓝图
api_bp = Blueprint('api', __name__, url_prefix="/api")

api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(post_bp)