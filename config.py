import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API 配置
    API_TITLE = 'Flask Backend API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL',
        'sqlite:///dev.db'
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/prod_db'
    )


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}