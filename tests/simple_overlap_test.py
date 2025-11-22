"""
简化的鸭子重叠修复测试程序
"""

import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graphics import DuckFactory
from animation.animators import SwapAnimator
from animation.animation_engine import AnimationEngine


def simple_test():
    """简单的测试程序"""
    root = tk.Tk()
    root.title("鸭子重叠修复测试")
    root.geometry("1000x400")
    
    canvas = tk.Canvas(root, width=1000, height=400, bg="lightblue")
    canvas.pack()
    
    # 创建动画引擎
    engine = AnimationEngine(canvas)
    
    # 创建两只小鸭子，位置相近
    ducks = DuckFactory.create_baby_ducks(canvas, 400, 250, 80, [3, 5])
    
    # 创建交换动画器
    swap_animator = SwapAnimator(engine)
    
    # 测试交换动画
    swap_anim = swap_animator.swap_ducks(ducks[0], ducks[1], duration=2.0)
    engine.add_animation(swap_anim)
    
    # 添加信息标签
    info_label = tk.Label(root, text="测试：两只鸭子交换位置，应该不会重叠", font=("Arial", 12))
    info_label.pack()
    
    # 启动动画引擎
    engine.play()
    
    root.mainloop()


if __name__ == "__main__":
    simple_test()