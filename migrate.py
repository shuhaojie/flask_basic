from api import create_app, db
from api.config import DevConfig
from flask_migrate import Migrate

# 创建应用实例
app = create_app(DevConfig)

# 初始化迁移扩展
migrate = Migrate(app, db)