## 1. 框架结构

### （1）整体结构

项目整体架构如下：

```bash
.
├── api
│   ├── __init__.py
│   ├── routes.py
│   └── user
│       ├── __init__.py
│       ├── models.py
│       ├── routes.py
│       └── views.py
├── config.py
├── migrate.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── a66cbf654a28_initial_migration.py
├── run.py
└── tests
    └── test_user.py
```

### （2）模块作用

- `run.py`：项目入口文件

```python
from api.config import DevConfig
from api import create_app

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

- `config.py`：用来写配置，这个是flask独有的，在后面导入里面的配置

```python
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


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:805115148@localhost/flask_basic"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:805115148@localhost/flask_basic_test"
```

- `migrate.py`：用来执行迁移，后面会说明如何执行迁移

```python
from api import create_app, db
from api.config import DevConfig
from flask_migrate import Migrate

# 创建应用实例
app = create_app(DevConfig)

# 初始化迁移扩展
migrate = Migrate(app, db)
```

- `app/__init__.py`：重点，这里定义了启动框架，连接路由，建立数据库连接等

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建扩展对象（不绑定应用）
db = SQLAlchemy()
migrate = Migrate()


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

    # 注册蓝图
    from api.app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
```

- `app/routes.py`：路由集中注册的入口模块

```python
from flask import Blueprint
from api.app.user.routes import user_bp

# 创建API蓝图
api_bp = Blueprint('api', __name__, url_prefix="/api")

api_bp.register_blueprint(user_bp)
```

## 2. flask使用mysql

### （1）建立连接

比较简单，在启动框架的时候，建立连接即可

### （2）数据迁移

- 文件准备：首先需要一个migrate.py文件

```python
from api import create_app, db
from api.config import DevConfig
from flask_migrate import Migrate

# 创建应用实例
app = create_app(DevConfig)

# 初始化迁移扩展
migrate = Migrate(app, db)
```

- 执行迁移，首次执行的时候，需要做一次初始化

```bash
export FLASK_APP=migrate.py 
flask db init 
```

这样会生成一个migrations文件夹，然后再执行迁移即可

```bash
flask db migrate -m "Initial migration"
flask db upgrade
```

## 3. 日志模块

- 创建日志初始化模块

```python
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'api.log')

    # 设置日志等级
    app.logger.setLevel(logging.INFO)

    # 设置文件日志处理器（带轮转）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # 设置控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 注册处理器到 Flask 的 logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info("日志系统初始化完成")
```

- 初始化日志模块

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.log import setup_logging  # 添加导入

db = SQLAlchemy()
migrate = Migrate()


def register_db(app):
    db.init_app(app)


def register_migrate(app):
    migrate.init_app(app, db)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # 初始化日志
    setup_logging(app)

    register_db(app)
    register_migrate(app)

    from api.app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
```

- 使用日志

```python
from flask import current_app

def some_function():
    current_app.logger.info("这是在函数中的日志")
```

## 4. 权限认证

flask提供了jwt_required这个装饰器来做鉴权

```python
from flask_jwt_extended import jwt_required
@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Hello, {current_user}!"})
```

不过这个需要在启动flask框架的时候导入配置

```python
from flask_jwt_extended import JWTManager
jwt = JWTManager()

def create_app(config):
    """应用工厂函数"""
    app = Flask(__name__)

    # 初始化jwt
    jwt.init_app(app)
```

并且在配置中必须有一个`JWT_SECRET_KEY`

```
class Config:
    # JWT配置
    JWT_SECRET_KEY = "jwt-secret"
```

仿照这个我们可以写一个装饰器，让某些接口只允许admin访问

```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return jsonify({"error": "Admins only!"}), 403
        return fn(*args, **kwargs)

    return wrapper
```

这个需要在登录的接口里，加一个额外参数

```python
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.username,
                                           additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401
```

