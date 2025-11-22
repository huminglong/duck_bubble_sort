"""
小鸭子冒泡排序可视化动画项目 - 运行脚本
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入并运行主程序
from main import main

if __name__ == "__main__":
    main()