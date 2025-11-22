"""
测试界面显示的简单脚本
"""

import tkinter as tk
from tkinter import ttk

# 创建测试窗口
root = tk.Tk()
root.title("界面测试")
root.geometry("800x400")

# 创建主框架
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 配置权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

# 创建信息面板容器
info_container = ttk.Frame(main_frame)
info_container.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

# 配置容器行列权重
info_container.grid_columnconfigure(0, weight=1)
info_container.grid_columnconfigure(1, weight=1)
info_container.grid_columnconfigure(2, weight=1)

# 创建三个测试框架
speed_frame = ttk.LabelFrame(info_container, text="⚡ 速度控制", padding="15")
speed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

stats_frame = ttk.LabelFrame(info_container, text="📊 统计信息", padding="15")
stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)

status_frame = ttk.LabelFrame(info_container, text="📈 状态信息", padding="15")
status_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

# 添加一些测试控件
tk.Label(speed_frame, text="速度滑块测试").pack()
tk.Scale(speed_frame, from_=0.1, to=3.0, orient=tk.HORIZONTAL).pack(fill=tk.X)

tk.Label(stats_frame, text="统计信息测试").pack()
tk.Label(stats_frame, text="比较次数: 0").pack()
tk.Label(stats_frame, text="交换次数: 0").pack()

tk.Label(status_frame, text="状态信息测试").pack()
tk.Label(status_frame, text="状态: 就绪").pack()
tk.Label(status_frame, text="当前操作: 无").pack()

print("测试界面已创建，请检查是否正常显示三个面板")
root.mainloop()