"""
测试鸭子重叠修复效果的程序
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from graphics import DuckFactory
from animation.animators import SwapAnimator, ComparisonAnimator
from animation.animation_engine import AnimationEngine


def test_swap_animation():
    """测试交换动画，确保鸭子不会重叠"""
    root = tk.Tk()
    root.title("鸭子重叠修复测试")
    root.geometry("1000x400")
    
    canvas = tk.Canvas(root, width=1000, height=400, bg="lightblue")
    canvas.pack()
    
    # 创建动画引擎
    engine = AnimationEngine(canvas)
    
    # 创建两只小鸭子，位置相近
    ducks = DuckFactory.create_baby_ducks(canvas, 400, 250, 80, [3, 5])
    
    # 创建母鸭
    mother_duck = DuckFactory.create_mother_duck(canvas, 500, 100)
    
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


def test_comparison_animation():
    """测试比较动画，确保母鸭不会超出边界"""
    root = tk.Tk()
    root.title("母鸭边界检查测试")
    root.geometry("1000x400")
    
    canvas = tk.Canvas(root, width=1000, height=400, bg="lightblue")
    canvas.pack()
    
    # 创建动画引擎
    engine = AnimationEngine(canvas)
    
    # 创建两只小鸭子，位置在画布边缘
    ducks = DuckFactory.create_baby_ducks(canvas, 50, 250, 800, [2, 8])
    
    # 创建母鸭
    mother_duck = DuckFactory.create_mother_duck(canvas, 500, 100)
    
    # 创建比较动画器
    comparison_animator = ComparisonAnimator(engine)
    
    # 测试比较动画
    comparison_anims = comparison_animator.compare_ducks(mother_duck, ducks[0], ducks[1], duration=3.0)
    for anim in comparison_anims:
        engine.add_animation(anim)
    
    # 添加信息标签
    info_label = tk.Label(root, text="测试：母鸭移动到边缘位置比较，应该不会超出边界", font=("Arial", 12))
    info_label.pack()
    
    # 启动动画引擎
    engine.play()
    
    root.mainloop()


def test_multiple_swaps():
    """测试多次交换动画"""
    root = tk.Tk()
    root.title("多次交换测试")
    root.geometry("1000x400")
    
    canvas = tk.Canvas(root, width=1000, height=400, bg="lightblue")
    canvas.pack()
    
    # 创建动画引擎
    engine = AnimationEngine(canvas)
    
    # 创建多只小鸭子
    ducks = DuckFactory.create_baby_ducks(canvas, 200, 250, 100, [5, 2, 8, 1, 9])
    
    # 创建母鸭
    mother_duck = DuckFactory.create_mother_duck(canvas, 500, 100)
    
    # 创建交换动画器
    swap_animator = SwapAnimator(engine)
    
    # 测试多次交换
    swap_anim1 = swap_animator.swap_ducks(ducks[0], ducks[1], duration=1.5)
    swap_anim2 = swap_animator.swap_ducks(ducks[2], ducks[3], duration=1.5)
    
    engine.add_animation(swap_anim1)
    engine.add_animation(swap_anim2)
    
    # 添加信息标签
    info_label = tk.Label(root, text="测试：同时进行多次交换，鸭子之间不应该重叠", font=("Arial", 12))
    info_label.pack()
    
    # 启动动画引擎
    engine.play()
    
    root.mainloop()


if __name__ == "__main__":
    print("开始测试鸭子重叠修复效果...")
    
    print("1. 测试交换动画...")
    test_swap_animation()
    
    print("2. 测试比较动画...")
    test_comparison_animation()
    
    print("3. 测试多次交换...")
    test_multiple_swaps()
    
    print("所有测试完成！")