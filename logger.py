"""
小鸭子冒泡排序可视化动画项目 - 日志记录模块

该模块提供统一的日志记录功能，用于记录应用程序运行状态、
排序步骤、动画事件等信息。
"""

import logging
import os
from datetime import datetime
from typing import Optional


def get_logger(name: str = "duck_bubble_sort", log_level: int = logging.DEBUG) -> logging.Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称
        log_level: 日志级别

    Returns:
        logging.Logger: 日志记录器实例
    """
    logger = logging.getLogger(name)

    # 如果logger已经有处理器，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 创建文件处理器
    log_file = os.path.join(log_dir, f"duck_bubble_sort_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_sort_step(operation: str, details: str) -> None:
    """
    记录排序步骤

    Args:
        operation: 操作类型
        details: 详细信息
    """
    logger = get_logger()
    logger.debug(f"排序步骤: {operation} - {details}")


def log_animation_event(event_type: str, details: str) -> None:
    """
    记录动画事件

    Args:
        event_type: 事件类型
        details: 详细信息
    """
    logger = get_logger()
    logger.debug(f"动画事件: {event_type} - {details}")


def log_user_action(action: str, details: str) -> None:
    """
    记录用户操作

    Args:
        action: 操作名称
        details: 详细信息
    """
    logger = get_logger()
    logger.info(f"用户操作: {action} - {details}")


def log_error(error: Exception, context: str) -> None:
    """
    记录错误信息

    Args:
        error: 错误对象
        context: 上下文信息
    """
    logger = get_logger()
    logger.error(f"错误发生: {context} - {str(error)}", exc_info=True)