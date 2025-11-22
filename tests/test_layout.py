"""
测试底部面板显示的脚本

主要功能:
- test_layout: 测试界面布局，特别是底部三个面板的显示

主要函数:
- test_layout: 布局测试函数
"""

import tkinter as tk
from tkinter import ttk

def test_layout():
    root = tk.Tk()
    root.title("布局测试")
    root.geometry("1200x900")
    root.resizable(True, True)
    
    # 主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 配置权重
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(4, weight=1)
    
    # 标题
    title = ttk.Label(main_frame, text="测试界面", font=("Arial", 18, "bold"))
    title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    # 画布框架
    canvas_frame = ttk.LabelFrame(main_frame, text="测试画布", padding="10")
    canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
    
    canvas = tk.Canvas(canvas_frame, width=1000, height=350, bg="#E6F3FF")
    canvas.pack(padx=10, pady=10)
    
    # 控制面板
    control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="15")
    control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
    
    ttk.Button(control_frame, text="按钮1").pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="按钮2").pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="按钮3").pack(side=tk.LEFT, padx=5)
    
    # 信息面板容器
    info_container = ttk.Frame(main_frame)
    info_container.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
    
    # 配置容器行列权重
    info_container.grid_columnconfigure(0, weight=1)
    info_container.grid_columnconfigure(1, weight=1)
    info_container.grid_columnconfigure(2, weight=1)
    info_container.grid_rowconfigure(0, weight=1)
    
    # 三个测试面板
    speed_frame = ttk.LabelFrame(info_container, text="⚡ 速度控制", padding="15")
    speed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
    
    ttk.Label(speed_frame, text="速度滑块测试").pack(anchor=tk.W)
    ttk.Scale(speed_frame, from_=0.1, to=3.0, orient=tk.HORIZONTAL).pack(fill=tk.X)
    ttk.Label(speed_frame, text="速度值: 1.0x").pack(anchor=tk.W)
    
    stats_frame = ttk.LabelFrame(info_container, text="📊 统计信息", padding="15")
    stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
    
    ttk.Label(stats_frame, text="比较次数: 0").pack(anchor=tk.W)
    ttk.Label(stats_frame, text="交换次数: 0").pack(anchor=tk.W)
    ttk.Label(stats_frame, text="进度: 0%").pack(anchor=tk.W)
    ttk.Progressbar(stats_frame, length=200, mode='determinate').pack(fill=tk.X)
    
    status_frame = ttk.LabelFrame(info_container, text="📈 状态信息", padding="15")
    status_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
    
    ttk.Label(status_frame, text="状态: 就绪").pack(anchor=tk.W)
    ttk.Label(status_frame, text="当前操作: 无").pack(anchor=tk.W)
    ttk.Label(status_frame, text="排序状态: 未开始").pack(anchor=tk.W)
    ttk.Label(status_frame, text="动画状态: 空闲").pack(anchor=tk.W)
    
    print("测试界面已创建")
    print("请检查底部三个面板是否完全显示")
    print("窗口大小: 1200x900")
    print("画布高度: 350")
    print("如果还有问题，可能需要进一步调整窗口大小或画布高度")
    
    root.mainloop()

if __name__ == "__main__":
    test_layout()