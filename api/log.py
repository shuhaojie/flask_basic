# app/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# 创建全局日志记录器
_logger = None


def init_logger():
    global _logger
    if _logger is not None:
        return _logger

    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'api.log')

    # 创建格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 设置文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 设置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 创建并配置日志记录器
    _logger = logging.getLogger('app')
    _logger.setLevel(logging.INFO)

    # 清除所有现有的处理器
    for handler in _logger.handlers[:]:
        _logger.removeHandler(handler)

    # 添加新的处理器
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger


# 初始化全局日志记录器
logger = init_logger()