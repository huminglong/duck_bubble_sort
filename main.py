"""
小鸭子冒泡排序可视化动画项目 - 主程序

该模块包含主应用程序类DuckBubbleSortApp，负责：
- 创建和管理GUI界面
- 集成鸭子图形系统、排序算法和动画系统
- 处理用户交互和控制
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
from typing import List, Optional

from duck_bubble_sort.graphics import DuckFactory, BabyDuck, MotherDuck
from duck_bubble_sort.algorithms.bubble_sort import BubbleSort
from duck_bubble_sort.animation.animation_engine import AnimationEngine
from duck_bubble_sort.animation.sort_animation_integration import SortAnimationIntegration
from duck_bubble_sort.logger import get_logger, log_user_action, log_error


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
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
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
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建标题
        title_label = ttk.Label(
            main_frame, 
            text="小鸭子冒泡排序可视化动画", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # 创建说明文字
        description_label = ttk.Label(
            main_frame,
            text="观看大母鸭如何帮助小鸭子们按大小排队！",
            font=("Arial", 12)
        )
        description_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # 创建画布框架
        canvas_frame = ttk.LabelFrame(main_frame, text="排序场景", padding="10")
        canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 创建画布
        self.canvas = tk.Canvas(canvas_frame, width=1000, height=400, bg="#E6F3FF")
        self.canvas.pack()
        
        # 创建控制面板框架
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 创建控制按钮
        self._create_control_buttons(control_frame)
        
        # 创建速度控制框架
        speed_frame = ttk.LabelFrame(main_frame, text="速度控制", padding="10")
        speed_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 创建速度控制滑块
        self._create_speed_control(speed_frame)
        
        # 创建统计信息框架
        stats_frame = ttk.LabelFrame(main_frame, text="统计信息", padding="10")
        stats_frame.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 创建统计信息显示
        self._create_statistics_display(stats_frame)
        
        # 创建状态信息框架
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.grid(row=4, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
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
        
        # 创建按钮
        self.start_button = ttk.Button(
            button_frame, 
            text="开始排序", 
            command=self._start_sort,
            width=12
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.pause_button = ttk.Button(
            button_frame, 
            text="暂停", 
            command=self._pause_sort,
            width=12,
            state=tk.DISABLED
        )
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.resume_button = ttk.Button(
            button_frame, 
            text="继续", 
            command=self._resume_sort,
            width=12,
            state=tk.DISABLED
        )
        self.resume_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.reset_button = ttk.Button(
            button_frame, 
            text="重置", 
            command=self._reset_sort,
            width=12
        )
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.step_button = ttk.Button(
            button_frame, 
            text="单步执行", 
            command=self._step_sort,
            width=12
        )
        self.step_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.new_ducks_button = ttk.Button(
            button_frame, 
            text="新的小鸭子", 
            command=self._generate_new_ducks,
            width=12
        )
        self.new_ducks_button.grid(row=0, column=5, padx=5, pady=5)
        
    def _create_speed_control(self, parent: ttk.Frame) -> None:
        """
        创建速度控制滑块
        
        Args:
            parent: 父框架
        """
        # 速度标签
        speed_label = ttk.Label(parent, text="动画速度:")
        speed_label.pack(anchor=tk.W)
        
        # 速度滑块
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_slider = ttk.Scale(
            parent,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self._on_speed_change
        )
        self.speed_slider.pack(fill=tk.X, pady=5)
        
        # 速度值标签
        self.speed_value_label = ttk.Label(parent, text="1.0x")
        self.speed_value_label.pack(anchor=tk.W)
        
    def _create_statistics_display(self, parent: ttk.Frame) -> None:
        """
        创建统计信息显示
        
        Args:
            parent: 父框架
        """
        # 比较次数
        self.comparisons_label = ttk.Label(parent, text="比较次数: 0")
        self.comparisons_label.pack(anchor=tk.W, pady=2)
        
        # 交换次数
        self.swaps_label = ttk.Label(parent, text="交换次数: 0")
        self.swaps_label.pack(anchor=tk.W, pady=2)
        
        # 进度
        self.progress_label = ttk.Label(parent, text="进度: 0%")
        self.progress_label.pack(anchor=tk.W, pady=2)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            parent,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
    def _create_status_display(self, parent: ttk.Frame) -> None:
        """
        创建状态信息显示
        
        Args:
            parent: 父框架
        """
        # 状态标签
        self.status_label = ttk.Label(parent, text="状态: 就绪", font=("Arial", 10, "bold"))
        self.status_label.pack(anchor=tk.W, pady=2)
        
        # 当前操作
        self.current_operation_label = ttk.Label(parent, text="当前操作: 无")
        self.current_operation_label.pack(anchor=tk.W, pady=2)
        
        # 排序状态
        self.sort_status_label = ttk.Label(parent, text="排序状态: 未开始")
        self.sort_status_label.pack(anchor=tk.W, pady=2)
        
        # 动画状态
        self.animation_status_label = ttk.Label(parent, text="动画状态: 空闲")
        self.animation_status_label.pack(anchor=tk.W, pady=2)
        
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
        self._update_status("状态: 排序完成")
        self._update_sort_status("排序状态: 已完成")
        self._update_animation_status("动画状态: 空闲")
        self._update_current_operation("当前操作: 排序完成")
        
        # 显示完成消息
        messagebox.showinfo("恭喜！", "小鸭子们已经按大小排好队了！\n\n排序动画演示完成！")
        
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
        
        # 更新标签
        self.comparisons_label.config(text=f"比较次数: {comparisons}")
        self.swaps_label.config(text=f"交换次数: {swaps}")
        self.progress_label.config(text=f"进度: {progress*100:.1f}%")
        
        # 更新进度条
        self.progress_bar['value'] = progress * 100
        
        # 更新当前操作
        current_comparison = self.bubble_sort.get_current_comparison()
        current_swap = self.bubble_sort.get_current_swap()
        
        if current_swap != (-1, -1):
            self._update_current_operation(f"当前操作: 交换位置 {current_swap[0]+1} 和 {current_swap[1]+1}")
        elif current_comparison != (-1, -1):
            self._update_current_operation(f"当前操作: 比较位置 {current_comparison[0]+1} 和 {current_comparison[1]+1}")
        else:
            self._update_current_operation("当前操作: 无")
            
    def _update_status(self, status: str) -> None:
        """
        更新状态标签
        
        Args:
            status: 状态文本
        """
        self.status_label.config(text=status)
        
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