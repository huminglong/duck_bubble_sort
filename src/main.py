"""
小鸭子冒泡排序可视化动画项目 - 主程序

该模块包含主应用程序类DuckBubbleSortApp，负责：
- 创建和管理GUI界面
- 集成鸭子图形系统、排序算法和动画系统
- 处理用户交互和控制

主要功能:
- DuckBubbleSortApp: 小鸭子冒泡排序可视化主应用程序类
- 提供GUI界面和用户交互功能
- 集成排序算法和动画系统

主要类:
- DuckBubbleSortApp: 主应用程序类
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import threading
import math
from typing import List, Optional
from tkinter import Canvas

from src.graphics import DuckFactory, BabyDuck, MotherDuck
from algorithms.bubble_sort import BubbleSort
from animation.animation_engine import AnimationEngine
from animation.sort_animation_integration import SortAnimationIntegration
from src.logger import get_logger, log_user_action, log_error


class DuckBubbleSortApp:
    """小鸭子冒泡排序可视化主应用程序类"""
    
    def __init__(self, root: tk.Tk):
        # 添加线程锁
        self.sort_lock = threading.Lock()
        """
        初始化应用程序
        
        Args:
            root: Tkinter根窗口对象
        """
        # 初始化日志记录器
        self.logger = get_logger()
        self.logger.info("开始初始化小鸭子冒泡排序可视化应用程序")
        
        self.root = root
        self.root.title("小鸭子冒泡排序可视化动画")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        
        # 设置现代化主题
        self.root.configure(bg='#F0F8FF')
        self._setup_styles()
        
        # 应用程序状态
        self.is_running = False
        self.is_paused = False
        self.animation_speed = 1.0
        
        # 鸭子和排序相关对象
        self.baby_ducks: List[BabyDuck] = []
        self.mother_duck: Optional[MotherDuck] = None
        self.bubble_sort: Optional[BubbleSort] = None
        self.animation_engine: Optional[AnimationEngine] = None
        self.sort_animation_integration: Optional[SortAnimationIntegration] = None
        
        try:
            # 设置样式
            self._setup_styles()
            
            # 创建GUI界面
            self._create_gui()
            self.logger.info("GUI界面创建成功")
            
            # 初始化鸭子
            self._initialize_ducks()
            self.logger.info(f"初始化了 {len(self.baby_ducks)} 只小鸭子")
            
            # 设置排序算法和动画系统
            self._setup_sort_and_animation()
            self.logger.info("排序算法和动画系统设置完成")
            
            # 绑定窗口关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            self.logger.info("应用程序初始化完成")
        except Exception as e:
            self.logger.error(f"应用程序初始化失败: {str(e)}")
            log_error(e, "应用程序初始化")
            raise
        
    def _create_gui(self) -> None:
        """创建GUI界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架行列权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)  # 确保信息面板有足够空间
        
        # 创建渐变背景效果
        self._create_gradient_background(main_frame)
        
        # 创建标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # 创建装饰性标题
        title_label = ttk.Label(
            title_frame, 
            text="🦆 小鸭子冒泡排序可视化动画 🦆", 
            font=("Microsoft YaHei", 20, "bold"),
            foreground="#2E8B57"
        )
        title_label.pack()
        
        # 创建副标题
        subtitle_label = ttk.Label(
            title_frame,
            text="观看大母鸭如何帮助小鸭子们按大小排队！",
            font=("Microsoft YaHei", 12),
            foreground="#4682B4"
        )
        subtitle_label.pack(pady=(3, 0))
        
        # 创建画布框架
        canvas_frame = ttk.LabelFrame(main_frame, text="排序场景", padding="5")
        canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # 创建画布容器
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建画布
        self.canvas = Canvas(canvas_container, width=1000, height=320, 
                           bg="#E6F3FF", highlightthickness=2, highlightbackground="#87CEEB")
        self.canvas.pack(padx=5, pady=5)
        
        # 添加装饰性边框
        self._add_canvas_decorations()
        
        # 创建控制面板框架
        control_frame = ttk.LabelFrame(main_frame, text="🎮 控制面板", padding="10")
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 创建控制按钮
        self._create_control_buttons(control_frame)
        
        # 创建信息面板容器
        info_container = ttk.Frame(main_frame)
        info_container.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # 配置容器行列权重
        info_container.grid_columnconfigure(0, weight=1)
        info_container.grid_columnconfigure(1, weight=1)
        info_container.grid_columnconfigure(2, weight=1)
        info_container.grid_rowconfigure(0, weight=1)
        
        # 创建速度控制框架
        speed_frame = ttk.LabelFrame(info_container, text="⚡ 速度控制", padding="10")
        speed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 创建速度控制滑块
        self._create_speed_control(speed_frame)
        
        # 创建统计信息框架
        stats_frame = ttk.LabelFrame(info_container, text="📊 统计信息", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 创建统计信息显示
        self._create_statistics_display(stats_frame)
        
        # 创建状态信息框架
        status_frame = ttk.LabelFrame(info_container, text="📈 状态信息", padding="10")
        status_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 创建状态信息显示
        self._create_status_display(status_frame)
        
    def _create_control_buttons(self, parent: ttk.Frame) -> None:
        """
        创建控制按钮
        
        Args:
            parent: 父框架
        """
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.pack()
        
        # 创建按钮样式
        button_style = {
            'width': 14,
            'padding': (10, 8)
        }
        
        # 创建主要操作按钮
        primary_frame = ttk.Frame(button_frame)
        primary_frame.pack(pady=(0, 10))
        
        self.start_button = ttk.Button(
            primary_frame, 
            text="▶️ 开始排序", 
            command=self._start_sort,
            **button_style
        )
        self.start_button.grid(row=0, column=0, padx=8, pady=5)
        
        self.pause_button = ttk.Button(
            primary_frame, 
            text="⏸️ 暂停", 
            command=self._pause_sort,
            state=tk.DISABLED,
            **button_style
        )
        self.pause_button.grid(row=0, column=1, padx=8, pady=5)
        
        self.resume_button = ttk.Button(
            primary_frame, 
            text="▶️ 继续", 
            command=self._resume_sort,
            state=tk.DISABLED,
            **button_style
        )
        self.resume_button.grid(row=0, column=2, padx=8, pady=5)
        
        # 创建辅助操作按钮
        secondary_frame = ttk.Frame(button_frame)
        secondary_frame.pack()
        
        self.reset_button = ttk.Button(
            secondary_frame, 
            text="🔄 重置", 
            command=self._reset_sort,
            **button_style
        )
        self.reset_button.grid(row=0, column=0, padx=8, pady=5)
        
        self.step_button = ttk.Button(
            secondary_frame, 
            text="⏭️ 单步执行", 
            command=self._step_sort,
            **button_style
        )
        self.step_button.grid(row=0, column=1, padx=8, pady=5)
        
        self.new_ducks_button = ttk.Button(
            secondary_frame, 
            text="🐥 新的小鸭子", 
            command=self._generate_new_ducks,
            **button_style
        )
        self.new_ducks_button.grid(row=0, column=2, padx=8, pady=5)
        
    def _create_speed_control(self, parent: ttk.Frame) -> None:
        """
        创建速度控制滑块
        
        Args:
            parent: 父框架
        """
        # 速度标签
        speed_label = ttk.Label(parent, text="动画速度:", font=("Microsoft YaHei", 11, "bold"))
        speed_label.pack(anchor=tk.W, pady=(0, 8))
        
        # 速度滑块容器
        slider_container = ttk.Frame(parent)
        slider_container.pack(fill=tk.X, pady=5)
        
        # 慢速标签
        slow_label = ttk.Label(slider_container, text="🐢 慢", font=("Microsoft YaHei", 9))
        slow_label.pack(side=tk.LEFT)
        
        # 速度滑块
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_slider = ttk.Scale(
            slider_container,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self._on_speed_change,
            length=150
        )
        self.speed_slider.pack(side=tk.LEFT, padx=10)
        
        # 快速标签
        fast_label = ttk.Label(slider_container, text="快 🚀", font=("Microsoft YaHei", 9))
        fast_label.pack(side=tk.LEFT)
        
        # 速度值标签
        self.speed_value_label = ttk.Label(parent, text="1.0x", font=("Microsoft YaHei", 12, "bold"), 
                                        foreground="#2E8B57")
        self.speed_value_label.pack(anchor=tk.W, pady=(8, 0))
        
    def _create_statistics_display(self, parent: ttk.Frame) -> None:
        """
        创建统计信息显示
        
        Args:
            parent: 父框架
        """
        # 添加图标装饰
        stats_title = ttk.Label(parent, text="实时数据监控", font=("Microsoft YaHei", 11, "bold"),
                              foreground="#4682B4")
        stats_title.pack(anchor=tk.W, pady=(0, 10))
        
        # 创建统计信息网格
        stats_grid = ttk.Frame(parent)
        stats_grid.pack(fill=tk.X, pady=(0, 10))
        
        # 比较次数
        comp_frame = ttk.Frame(stats_grid)
        comp_frame.pack(fill=tk.X, pady=3)
        comp_icon = ttk.Label(comp_frame, text="🔍", font=("Microsoft YaHei", 10))
        comp_icon.pack(side=tk.LEFT)
        self.comparisons_label = ttk.Label(comp_frame, text="比较次数: 0", font=("Microsoft YaHei", 10))
        self.comparisons_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 交换次数
        swap_frame = ttk.Frame(stats_grid)
        swap_frame.pack(fill=tk.X, pady=3)
        swap_icon = ttk.Label(swap_frame, text="🔄", font=("Microsoft YaHei", 10))
        swap_icon.pack(side=tk.LEFT)
        self.swaps_label = ttk.Label(swap_frame, text="交换次数: 0", font=("Microsoft YaHei", 10))
        self.swaps_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 进度
        progress_frame = ttk.Frame(stats_grid)
        progress_frame.pack(fill=tk.X, pady=3)
        progress_icon = ttk.Label(progress_frame, text="📊", font=("Microsoft YaHei", 10))
        progress_icon.pack(side=tk.LEFT)
        self.progress_label = ttk.Label(progress_frame, text="进度: 0%", font=("Microsoft YaHei", 10))
        self.progress_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 进度条容器
        progress_container = ttk.Frame(parent)
        progress_container.pack(fill=tk.X, pady=(10, 0))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            progress_container,
            length=250,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X)
        
        # 进度百分比标签
        self.progress_percent_label = ttk.Label(progress_container, text="0%", 
                                             font=("Microsoft YaHei", 10, "bold"),
                                             foreground="#2E8B57")
        self.progress_percent_label.pack(anchor=tk.E, pady=(3, 0))
        
    def _create_status_display(self, parent: ttk.Frame) -> None:
        """
        创建状态信息显示
        
        Args:
            parent: 父框架
        """
        # 状态标签
        self.status_label = ttk.Label(parent, text="状态: 就绪", font=("Microsoft YaHei", 11, "bold"))
        self.status_label.pack(anchor=tk.W, pady=2)
        
        # 当前操作
        self.current_operation_label = ttk.Label(parent, text="当前操作: 无", font=("Microsoft YaHei", 10))
        self.current_operation_label.pack(anchor=tk.W, pady=2)
        
        # 排序状态
        self.sort_status_label = ttk.Label(parent, text="排序状态: 未开始", font=("Microsoft YaHei", 10))
        self.sort_status_label.pack(anchor=tk.W, pady=2)
        
        # 动画状态
        self.animation_status_label = ttk.Label(parent, text="动画状态: 空闲", font=("Microsoft YaHei", 10))
        self.animation_status_label.pack(anchor=tk.W, pady=2)
    
    def _setup_styles(self) -> None:
        """设置现代化样式"""
        style = ttk.Style()
        
        # 设置主题
        style.theme_use('clam')
        
        # 配置标签框架样式
        style.configure('TLabelFrame', 
                       background='#F0F8FF', 
                       borderwidth=2,
                       relief='solid')
        style.configure('TLabelFrame.Label', 
                       background='#F0F8FF',
                       font=('Microsoft YaHei', 12, 'bold'))
        
        # 配置按钮样式
        style.configure('TButton',
                       background='#4CAF50',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Microsoft YaHei', 10, 'bold'))
        style.map('TButton',
                 background=[('active', '#45a049'),
                           ('disabled', '#cccccc')])
        
        # 配置标签样式
        style.configure('TLabel',
                       background='#F0F8FF',
                       font=('Microsoft YaHei', 10))
        
        # 配置进度条样式
        style.configure('TProgressbar',
                       background='#4CAF50',
                       troughcolor='#E0E0E0')
    
    def _create_gradient_background(self, parent) -> None:
        """创建渐变背景效果"""
        # 创建渐变效果的装饰性元素
        gradient_frame = tk.Frame(parent, bg='#F0F8FF', height=5)
        gradient_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 添加装饰性线条
        for i in range(5):
            color_intensity = 200 + i * 10
            color = f'#{color_intensity:02x}{color_intensity:02x}FF'
            line = tk.Frame(gradient_frame, bg=color, height=1)
            line.pack(fill=tk.X, pady=1)
    
    def _add_canvas_decorations(self) -> None:
        """为画布添加装饰性元素"""
        # 添加底部装饰波浪线
        wave_points = []
        for x in range(0, 1000, 15):
            y = 300 + 8 * math.sin(x * 0.015)
            wave_points.extend([x, y])
        
        if len(wave_points) >= 4:
            wave = self.canvas.create_line(wave_points, fill='#4682B4', width=3, smooth=True)
            self.canvas.tag_lower(wave)  # 将波浪线置于底层
        
        # 添加顶部装饰波浪线
        wave_points_top = []
        for x in range(0, 1000, 15):
            y = 20 + 6 * math.sin(x * 0.02 + math.pi/2)
            wave_points_top.extend([x, y])
        
        if len(wave_points_top) >= 4:
            wave_top = self.canvas.create_line(wave_points_top, fill='#87CEEB', width=2, smooth=True)
            self.canvas.tag_lower(wave_top)
        
        # 添加角落装饰
        corner_size = 30
        corners = [
            (10, 10),  # 左上
            (960, 10),  # 右上
            (10, 280),  # 左下
            (960, 280)  # 右下
        ]
        
        for x, y in corners:
            # 外框
            corner_outer = self.canvas.create_rectangle(
                x, y, x + corner_size, y + corner_size,
                outline='#4682B4', width=3, fill=''
            )
            # 内框
            corner_inner = self.canvas.create_rectangle(
                x + 5, y + 5, x + corner_size - 5, y + corner_size - 5,
                outline='#87CEEB', width=1, fill=''
            )
            self.canvas.tag_lower(corner_outer)
            self.canvas.tag_lower(corner_inner)
        
        # 添加装饰性圆点
        for i in range(5):
            x = 50 + i * 200
            y = 200
            dot = self.canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill='#B0C4DE', outline=''
            )
            self.canvas.tag_lower(dot)
        
    def _initialize_ducks(self) -> None:
        """初始化鸭子"""
        # 清除现有鸭子
        self.canvas.delete("all")
        self.baby_ducks.clear()
        
        # 生成12个随机数值（1-100）
        values = random.sample(range(1, 101), 12)
        
        # 创建小鸭子
        start_x = 100
        start_y = 200
        spacing = 70
        
        self.baby_ducks = DuckFactory.create_baby_ducks(
            self.canvas, start_x, start_y, spacing, values
        )
        
        # 创建大母鸭
        mother_x = 500
        mother_y = 100
        self.mother_duck = DuckFactory.create_mother_duck(self.canvas, mother_x, mother_y)
        
        # 更新状态
        self._update_status("状态: 就绪")
        self._update_sort_status("排序状态: 未开始")
        
    def _setup_sort_and_animation(self) -> None:
        """设置排序算法和动画系统"""
        if not self.baby_ducks or not self.mother_duck:
            return
            
        # 创建冒泡排序算法
        self.bubble_sort = BubbleSort(self.baby_ducks)
        
        # 创建动画引擎
        self.animation_engine = AnimationEngine(self.canvas)
        
        # 创建排序动画集成
        self.sort_animation_integration = SortAnimationIntegration(
            self.bubble_sort,
            self.baby_ducks,
            self.mother_duck,
            self.animation_engine
        )
        
        # 设置动画速度
        self.sort_animation_integration.set_animation_speed(self.animation_speed)
        
    def _start_sort(self) -> None:
        """开始排序"""
        log_user_action("开始排序", "用户点击开始排序按钮")
        self.logger.info("开始执行排序操作")
        
        if not self.bubble_sort or not self.sort_animation_integration:
            error_msg = "排序系统未初始化，请检查鸭子创建和动画系统设置"
            self.logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
            return
            
        try:
            # 重置排序状态
            self.bubble_sort.reset()
            self.logger.info("排序状态已重置")
            
            # 清空动画队列
            self.animation_engine.clear_queue()
            self.logger.info("动画队列已清空")
            
            # 更新按钮状态
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.step_button.config(state=tk.DISABLED)
            self.new_ducks_button.config(state=tk.DISABLED)
            
            # 更新状态
            self.is_running = True
            self.is_paused = False
            self._update_status("状态: 排序中")
            self._update_sort_status("排序状态: 进行中")
            self._update_animation_status("动画状态: 播放中")
            
            # 开始动画排序
            self.sort_animation_integration.start_animation()
            self.logger.info("动画排序已开始")
            
            # 启动统计更新
            self._start_statistics_update()
            self.logger.info("统计更新已启动")
        except Exception as e:
            self.logger.error(f"开始排序时发生错误: {str(e)}")
            log_error(e, "开始排序")
            messagebox.showerror("错误", f"开始排序时发生错误: {str(e)}")
        
    def _pause_sort(self) -> None:
        """暂停排序"""
        log_user_action("暂停排序", "用户点击暂停按钮")
        self.logger.info("暂停排序操作")
        
        if not self.sort_animation_integration:
            self.logger.error("排序动画集成对象不存在，无法暂停")
            return
            
        try:
            # 暂停动画
            self.sort_animation_integration.pause_animation()
            self.logger.info("动画已暂停")
            
            # 更新按钮状态
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            
            # 更新状态
            self.is_paused = True
            self._update_status("状态: 已暂停")
            self._update_sort_status("排序状态: 已暂停")
            self._update_animation_status("动画状态: 已暂停")
        except Exception as e:
            self.logger.error(f"暂停排序时发生错误: {str(e)}")
            log_error(e, "暂停排序")
        
    def _resume_sort(self) -> None:
        """继续排序"""
        log_user_action("继续排序", "用户点击继续按钮")
        self.logger.info("继续排序操作")
        
        if not self.sort_animation_integration:
            self.logger.error("排序动画集成对象不存在，无法继续")
            return
            
        try:
            # 继续动画
            self.sort_animation_integration.resume_animation()
            self.logger.info("动画已继续")
            
            # 更新按钮状态
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            
            # 更新状态
            self.is_paused = False
            self._update_status("状态: 排序中")
            self._update_sort_status("排序状态: 进行中")
            self._update_animation_status("动画状态: 播放中")
        except Exception as e:
            self.logger.error(f"继续排序时发生错误: {str(e)}")
            log_error(e, "继续排序")
        
    def _reset_sort(self) -> None:
        """重置排序"""
        if not self.sort_animation_integration:
            return
            
        # 停止动画
        self.sort_animation_integration.stop_animation()
        
        # 重置鸭子状态
        for duck in self.baby_ducks:
            duck.set_sorted(False)
            duck.set_comparing(False)
            duck.highlight(False)
        
        # 更新按钮状态
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.step_button.config(state=tk.NORMAL)
        self.new_ducks_button.config(state=tk.NORMAL)
        
        # 更新状态
        self.is_running = False
        self.is_paused = False
        self._update_status("状态: 就绪")
        self._update_sort_status("排序状态: 未开始")
        self._update_animation_status("动画状态: 空闲")
        self._update_current_operation("当前操作: 无")
        
        # 重置统计信息
        self._update_statistics()
        
    def _step_sort(self) -> None:
        """单步执行排序"""
        if not self.sort_animation_integration:
            return
            
        # 如果排序已完成，先重置
        if self.bubble_sort.is_completed():
            self._reset_sort()
            
        # 执行单步
        self.sort_animation_integration.step_sort()
        
        # 更新状态
        if not self.is_running:
            self.is_running = True
            self._update_status("状态: 单步执行")
            self._update_sort_status("排序状态: 进行中")
            
        # 更新统计信息
        self._update_statistics()
        
        # 检查是否完成
        if self.bubble_sort.is_completed():
            self._on_sort_complete()
            
    def _generate_new_ducks(self) -> None:
        """生成新的小鸭子"""
        # 停止当前排序
        if self.is_running:
            self._reset_sort()
            
        # 重新初始化鸭子
        self._initialize_ducks()
        
        # 重新设置排序和动画系统
        self._setup_sort_and_animation()
        
        # 重置统计信息
        self._update_statistics()
        
    def _on_speed_change(self, value: str) -> None:
        """
        速度滑块变化回调
        
        Args:
            value: 新的速度值
        """
        self.animation_speed = float(value)
        self.speed_value_label.config(text=f"{self.animation_speed:.1f}x")
        
        # 更新动画速度
        if self.sort_animation_integration:
            self.sort_animation_integration.set_animation_speed(self.animation_speed)
            
    def _on_sort_complete(self) -> None:
        """排序完成回调"""
        # 更新按钮状态
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.step_button.config(state=tk.DISABLED)
        self.new_ducks_button.config(state=tk.NORMAL)
        
        # 更新状态
        self.is_running = False
        self.is_paused = False
        self._update_status("状态: 排序完成 🎉")
        self._update_sort_status("排序状态: 已完成 ✅")
        self._update_animation_status("动画状态: 空闲")
        self._update_current_operation("当前操作: 排序完成 🏆")
        
        # 添加完成动画效果
        self._celebrate_completion()
        
        # 显示完成消息
        messagebox.showinfo("恭喜！", "🎊 小鸭子们已经按大小排好队了！\n\n🏆 排序动画演示完成！\n\n🦆 大母鸭做得很棒！")
        
    def _start_statistics_update(self) -> None:
        """启动统计信息更新"""
        def update():
            if self.is_running and not self.is_paused:
                self._update_statistics()
                
                # 如果排序还在进行，继续更新
                if not self.bubble_sort.is_completed():
                    self.root.after(100, update)
                    
        # 开始更新
        self.root.after(100, update)
        
    def _update_statistics(self) -> None:
        """更新统计信息显示"""
        if not self.bubble_sort:
            return
            
        # 获取统计信息
        comparisons = self.bubble_sort.get_comparisons_count()
        swaps = self.bubble_sort.get_swaps_count()
        progress = self.bubble_sort.get_progress()
        
        # 计算百分比
        progress_percent = progress * 100
        
        # 更新标签
        self.comparisons_label.config(text=f"比较次数: {comparisons}")
        self.swaps_label.config(text=f"交换次数: {swaps}")
        self.progress_label.config(text=f"进度: {progress_percent:.1f}%")
        
        # 更新进度条
        self.progress_bar['value'] = progress_percent
        
        # 更新进度百分比标签
        self.progress_percent_label.config(text=f"{progress_percent:.0f}%")
        
        # 根据进度改变颜色
        if progress_percent >= 100:
            self.progress_percent_label.config(foreground="#32CD32")  # 绿色
        elif progress_percent >= 75:
            self.progress_percent_label.config(foreground="#FFD700")  # 金色
        elif progress_percent >= 50:
            self.progress_percent_label.config(foreground="#FF8C00")  # 橙色
        else:
            self.progress_percent_label.config(foreground="#2E8B57")  # 深绿色
        
        # 更新当前操作
        current_comparison = self.bubble_sort.get_current_comparison()
        current_swap = self.bubble_sort.get_current_swap()
        
        if current_swap != (-1, -1):
            self._update_current_operation(f"🔄 交换位置 {current_swap[0]+1} 和 {current_swap[1]+1}")
        elif current_comparison != (-1, -1):
            self._update_current_operation(f"🔍 比较位置 {current_comparison[0]+1} 和 {current_comparison[1]+1}")
        else:
            self._update_current_operation("⏸️ 等待操作...")
            
    def _update_status(self, status: str) -> None:
        """
        更新状态标签
        
        Args:
            status: 状态文本
        """
        self.status_label.config(text=status)
        
        # 添加状态变化时的视觉反馈
        if "排序中" in status:
            self.status_label.config(foreground="#FF8C00")
        elif "完成" in status:
            self.status_label.config(foreground="#32CD32")
        elif "暂停" in status:
            self.status_label.config(foreground="#FF6347")
        else:
            self.status_label.config(foreground="#2E8B57")
        
    def _update_sort_status(self, status: str) -> None:
        """
        更新排序状态标签
        
        Args:
            status: 排序状态文本
        """
        self.sort_status_label.config(text=status)
        
    def _update_animation_status(self, status: str) -> None:
        """
        更新动画状态标签
        
        Args:
            status: 动画状态文本
        """
        self.animation_status_label.config(text=status)
        
    def _update_current_operation(self, operation: str) -> None:
        """
        更新当前操作标签
        
        Args:
            operation: 操作文本
        """
        self.current_operation_label.config(text=operation)
        
    def _celebrate_completion(self) -> None:
        """添加排序完成的庆祝效果"""
        # 为所有小鸭子添加庆祝动画
        for i, duck in enumerate(self.baby_ducks):
            # 创建跳跃动画
            self._animate_duck_jump(duck, i * 100)  # 错开时间
        
        # 母鸭点头庆祝
        if self.mother_duck:
            self._animate_mother_duck_celebration()
    
    def _animate_duck_jump(self, duck, delay_ms: int) -> None:
        """让小鸭子跳跃庆祝"""
        def jump():
            original_y = duck.y
            # 向上跳
            duck.move_to(duck.x, original_y - 30)
            # 落回原位
            self.root.after(200, lambda: duck.move_to(duck.x, original_y))
        
        # 延迟执行
        self.root.after(delay_ms, jump)
    
    def _animate_mother_duck_celebration(self) -> None:
        """母鸭庆祝动画"""
        if not self.mother_duck:
            return
            
        # 连续点头3次
        for i in range(3):
            self.root.after(i * 300, self.mother_duck.nod)
    
    def _on_closing(self) -> None:
        """窗口关闭事件处理"""
        # 停止动画
        if self.sort_animation_integration:
            self.sort_animation_integration.stop_animation()
            
        # 关闭窗口
        self.root.destroy()


def main():
    """主函数"""
    # 创建根窗口
    root = tk.Tk()
    
    # 创建应用程序
    app = DuckBubbleSortApp(root)
    
    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()