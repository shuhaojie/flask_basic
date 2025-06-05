from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.log import setup_logging

# 创建扩展对象（不绑定应用）
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def register_db(app):
    db.init_app(app)


def register_migrate(app):
    migrate.init_app(app, db)


def create_app(config):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config)

    # 初始化建立数据库连接
    register_db(app)

    # 初始化数据库迁移
    register_migrate(app)

    # 导入日志模块
    setup_logging(app)

    # 初始化jwt
    jwt.init_app(app)

    # 注册蓝图
    from api.app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
