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
    # JWT配置
    JWT_SECRET_KEY = "jwt-secret"


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:805115148@localhost/flask_basic"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:805115148@localhost/flask_basic_test"
