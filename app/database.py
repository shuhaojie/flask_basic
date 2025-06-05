from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化扩展（但不绑定应用）
db = SQLAlchemy()
migrate = Migrate()
