import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'api.log')

    # 设置日志等级
    app.logger.setLevel(logging.INFO)

    # 清除默认的处理器（解决日志重复打印问题）
    app.logger.handlers.clear()

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
