"""
小鸭子冒泡排序可视化动画项目 - 启动脚本

该脚本提供程序的简单入口点，包含环境检查和错误处理。
"""

import sys
import os
import traceback
from typing import Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def check_python_version() -> bool:
    """
    检查Python版本是否满足要求
    
    Returns:
        bool: 版本是否满足要求
    """
    # 检查Python版本（需要3.6+）
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True


def check_dependencies() -> bool:
    """
    检查必要的依赖是否已安装
    
    Returns:
        bool: 依赖是否满足要求
    """
    try:
        # 检查tkinter是否可用
        import tkinter
        print("√ tkinter已安装")

        # 检查其他标准库模块
        import random
        import threading
        import time
        import math
        from typing import List, Optional, Callable, Tuple

        print("√ 所有标准库模块可用")
        return True
        
    except ImportError as e:
        print(f"错误: 缺少必要的依赖 - {e}")
        return False


def check_project_structure() -> bool:
    """
    检查项目结构是否完整
    
    Returns:
        bool: 项目结构是否完整
    """
    required_files = [
        "src/main.py",
        "src/graphics.py",
        "src/logger.py",
        "algorithms/bubble_sort.py",
        "animation/animation_engine.py",
        "animation/animators.py",
        "animation/sort_animation_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("错误: 缺少必要的项目文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("√ 项目结构完整")
    return True


def initialize_environment() -> bool:
    """
    初始化运行环境
    
    Returns:
        bool: 环境初始化是否成功
    """
    try:
        # 设置环境变量
        os.environ["PYTHONPATH"] = project_root
        
        # 创建必要的目录（如果不存在）
        directories = ["logs"]
        for directory in directories:
            dir_path = os.path.join(project_root, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"√ 创建目录: {directory}")
        
        return True
        
    except Exception as e:
        print(f"错误: 环境初始化失败 - {e}")
        return False


def run_application() -> Optional[int]:
    """
    运行主应用程序
    
    Returns:
        Optional[int]: 退出代码，None表示正常退出
    """
    try:
        print("正在启动小鸭子冒泡排序可视化动画...")
        print("=" * 50)
        
        # 导入并运行主程序
        from src.main import main
        
        print("√ 成功导入主程序模块")
        print("启动应用程序...")
        print("=" * 50)
        
        # 运行主程序
        main()
        
        return None
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        return 130
        
    except ImportError as e:
        print(f"错误: 无法导入必要的模块 - {e}")
        traceback.print_exc()
        return 1
        
    except Exception as e:
        print(f"错误: 程序运行时发生异常 - {e}")
        traceback.print_exc()
        return 1


def main() -> int:
    """
    主函数，负责环境检查和程序启动
    
    Returns:
        int: 退出代码
    """
    print("小鸭子冒泡排序可视化动画 - 启动检查")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return 1
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 检查项目结构
    if not check_project_structure():
        return 1
    
    # 初始化环境
    if not initialize_environment():
        return 1
    
    print("=" * 50)
    print("所有检查通过，准备启动程序...")
    print("=" * 50)
    
    # 运行应用程序
    exit_code = run_application()
    
    if exit_code is None:
        print("程序正常退出")
        return 0
    else:
        print(f"程序异常退出，代码: {exit_code}")
        return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)