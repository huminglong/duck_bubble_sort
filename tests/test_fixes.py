#!/usr/bin/env python3
"""
测试修复效果的简单程序

主要功能:
- test_boundary_check: 测试边界检查
- test_swap_animation: 测试交换动画，确保不会重叠

主要函数:
- test_boundary_check: 边界检查测试函数
- test_swap_animation: 交换动画测试函数
"""

import tkinter as tk
from src.graphics import DuckFactory, BabyDuck, MotherDuck
from animation.animators import SwapAnimator
from animation.animation_engine import AnimationEngine
import time

def test_boundary_check():
    """测试边界检查"""
    print("测试边界检查...")
    
    # 创建窗口
    root = tk.Tk()
    root.title("测试边界检查")
    root.geometry("1000x400")
    
    # 创建画布
    canvas = tk.Canvas(root, width=1000, height=400, bg="#E6F3FF")
    canvas.pack()
    
    # 创建一只小鸭子，位置在边界外
    duck = BabyDuck(canvas, 50, 200, 30, 5)
    
    # 尝试移动到边界外
    print(f"原始位置: ({duck.x}, {duck.y})")
    duck.move_to(-50, 200)  # 尝试移动到左边界外
    print(f"移动到(-50, 200)后的位置: ({duck.x}, {duck.y})")
    
    duck.move_to(1050, 200)  # 尝试移动到右边界外
    print(f"移动到(1050, 200)后的位置: ({duck.x}, {duck.y})")
    
    duck.move_to(500, -50)  # 尝试移动到上边界外
    print(f"移动到(500, -50)后的位置: ({duck.x}, {duck.y})")
    
    duck.move_to(500, 450)  # 尝试移动到下边界外
    print(f"移动到(500, 450)后的位置: ({duck.x}, {duck.y})")
    
    # 测试母鸭子
    mother_duck = MotherDuck(canvas, 500, 100)
    print(f"母鸭子原始位置: ({mother_duck.x}, {mother_duck.y})")
    
    mother_duck.move_to(-50, 100)  # 尝试移动到左边界外
    print(f"母鸭子移动到(-50, 100)后的位置: ({mother_duck.x}, {mother_duck.y})")
    
    print("边界检查测试完成！")
    
    # 显示窗口
    root.update()
    time.sleep(2)
    root.destroy()

def test_swap_animation():
    """测试交换动画，确保不会重叠"""
    print("\n测试交换动画...")
    
    # 创建窗口
    root = tk.Tk()
    root.title("测试交换动画")
    root.geometry("1000x400")
    
    # 创建画布
    canvas = tk.Canvas(root, width=1000, height=400, bg="#E6F3FF")
    canvas.pack()
    
    # 创建两只小鸭子
    duck1 = BabyDuck(canvas, 300, 200, 30, 5)
    duck2 = BabyDuck(canvas, 700, 200, 30, 10)
    
    print(f"鸭子1原始位置: ({duck1.x}, {duck1.y})")
    print(f"鸭子2原始位置: ({duck2.x}, {duck2.y})")
    
    # 创建动画引擎
    engine = AnimationEngine(canvas)
    
    # 创建交换动画器
    swap_animator = SwapAnimator(engine)
    
    # 创建交换动画
    swap_anim = swap_animator.swap_ducks(duck1, duck2, 2.0)
    
    # 添加到动画队列
    engine.add_animation(swap_anim)
    
    # 播放动画
    engine.play()
    
    print("开始交换动画...")
    
    # 显示窗口
    root.update()
    
    # 等待动画完成
    time.sleep(3)
    
    print(f"鸭子1最终位置: ({duck1.x}, {duck1.y})")
    print(f"鸭子2最终位置: ({duck2.x}, {duck2.y})")
    
    # 停止动画引擎
    engine.stop()
    
    print("交换动画测试完成！")
    
    root.destroy()

if __name__ == "__main__":
    test_boundary_check()
    test_swap_animation()
    print("\n所有测试完成！")