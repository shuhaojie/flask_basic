import os
from app.server import create_app

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    # 启动开发服务器
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5001)),
        debug=app.config['DEBUG']
    )
