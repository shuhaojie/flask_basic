from flask import Flask
from config import config
from app.database import db, migrate


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.user.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # 初始化数据库（仅开发用）
    if app.config.get('DEBUG'):
        with app.app_context():
            db.create_all()

    return app
