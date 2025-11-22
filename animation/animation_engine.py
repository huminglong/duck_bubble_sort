"""
小鸭子冒泡排序可视化动画项目 - 动画引擎模块

该模块包含动画引擎的核心实现，负责管理所有动画效果、
动画队列和动画播放控制。
"""

import time
from typing import List, Dict, Callable, Optional, Any
from enum import Enum
import threading
import tkinter as tk


class AnimationState(Enum):
    """动画状态枚举"""
    IDLE = "idle"       # 空闲状态
    PLAYING = "playing" # 播放中
    PAUSED = "paused"   # 已暂停
    STOPPED = "stopped" # 已停止


class AnimationType(Enum):
    """动画类型枚举"""
    MOVE = "move"           # 移动动画
    SWAP = "swap"           # 交换动画
    HIGHLIGHT = "highlight" # 高亮动画
    COMPARE = "compare"     # 比较动画
    COMPLETE = "complete"   # 完成动画
    CUSTOM = "custom"       # 自定义动画


class Animation:
    """动画基类，定义动画的基本属性和方法"""
    
    def __init__(self, animation_type: AnimationType, duration: float = 1.0):
        """
        初始化动画
        
        Args:
            animation_type: 动画类型
            duration: 动画持续时间（秒）
        """
        self.type = animation_type
        self.duration = duration
        self.start_time = 0
        self.is_completed = False
        self.on_complete: Optional[Callable] = None
        self.on_update: Optional[Callable[[float], None]] = None  # 进度更新回调
        
    def start(self) -> None:
        """开始动画"""
        self.start_time = time.time()
        self.is_completed = False
        
    def update(self) -> bool:
        """
        更新动画状态
        
        Returns:
            bool: 动画是否已完成
        """
        if self.is_completed:
            return True
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # 调用进度更新回调
        if self.on_update:
            self.on_update(progress)
        
        # 检查动画是否完成
        if progress >= 1.0:
            self.is_completed = True
            if self.on_complete:
                self.on_complete()
            return True
            
        return False
    
    def set_duration(self, duration: float) -> None:
        """设置动画持续时间"""
        self.duration = max(0.1, duration)  # 最小0.1秒


class AnimationEngine:
    """动画引擎类，管理所有动画效果和动画队列"""
    
    def __init__(self, canvas: tk.Canvas):
        """
        初始化动画引擎
        
        Args:
            canvas: Tkinter画布对象
        """
        self.canvas = canvas
        self.state = AnimationState.IDLE
        self.animation_queue: List[Animation] = []
        self.current_animation: Optional[Animation] = None
        self.speed_multiplier = 1.0  # 速度倍数
        self.is_running = False
        
        # 动画线程
        self.animation_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # 回调函数
        self.on_animation_start: Optional[Callable[[Animation], None]] = None
        self.on_animation_complete: Optional[Callable[[Animation], None]] = None
        self.on_queue_empty: Optional[Callable[[], None]] = None
        
    def add_animation(self, animation: Animation) -> None:
        """
        添加动画到队列
        
        Args:
            animation: 要添加的动画对象
        """
        # 调整动画持续时间以匹配速度设置
        animation.set_duration(animation.duration / self.speed_multiplier)
        self.animation_queue.append(animation)
        
    def add_animation_front(self, animation: Animation) -> None:
        """
        添加动画到队列前端（优先执行）
        
        Args:
            animation: 要添加的动画对象
        """
        # 调整动画持续时间以匹配速度设置
        animation.set_duration(animation.duration / self.speed_multiplier)
        self.animation_queue.insert(0, animation)
        
    def clear_queue(self) -> None:
        """清空动画队列"""
        self.animation_queue.clear()
        
    def play(self) -> None:
        """开始播放动画"""
        from logger import get_logger
        logger = get_logger()
        
        # 检查是否在动画线程中调用
        current_thread = threading.current_thread()
        is_in_animation_thread = (self.animation_thread and 
                                  current_thread.ident == self.animation_thread.ident)
        
        # 如果在动画线程中调用，只需更新状态
        if is_in_animation_thread:
            logger.debug("在动画线程中调用play()，只更新状态")
            self.state = AnimationState.PLAYING
            self.is_running = True
            return
        
        # 如果已经在播放状态
        if self.state == AnimationState.PLAYING and self.animation_thread and self.animation_thread.is_alive():
            logger.debug("动画已在播放中，无需重新启动")
            return
            
        # 🔧 关键修复：如果已有动画线程但线程已结束，直接重启，不要调用stop()
        # 因为stop()会清空队列，导致刚添加的动画丢失
        if self.animation_thread and self.animation_thread.is_alive():
            logger.debug("停止旧的动画线程（不清空队列）")
            # 只设置停止标志，不清空队列
            self.state = AnimationState.STOPPED
            self.is_running = False
            self.stop_event.set()
            self.animation_thread.join(timeout=0.5)
            
        logger.debug("启动新的动画线程")
        self.state = AnimationState.PLAYING
        self.is_running = True
        self.stop_event.clear()
        
        # 启动动画线程
        self.animation_thread = threading.Thread(target=self._animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def pause(self) -> None:
        """暂停动画"""
        if self.state == AnimationState.PLAYING:
            self.state = AnimationState.PAUSED
            
    def resume(self) -> None:
        """继续播放动画"""
        if self.state == AnimationState.PAUSED:
            self.state = AnimationState.PLAYING
            
    def stop(self) -> None:
        """停止动画"""
        self.state = AnimationState.STOPPED
        self.is_running = False
        self.stop_event.set()
        
        # 等待动画线程结束
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=0.5)
            
        self.current_animation = None
        self.clear_queue()
        
    def set_speed(self, speed_multiplier: float) -> None:
        """
        设置动画速度倍数
        
        Args:
            speed_multiplier: 速度倍数（1.0为正常速度，2.0为2倍速）
        """
        self.speed_multiplier = max(0.1, speed_multiplier)
        
    def is_playing(self) -> bool:
        """检查动画是否正在播放"""
        return self.state == AnimationState.PLAYING
        
    def is_paused(self) -> bool:
        """检查动画是否已暂停"""
        return self.state == AnimationState.PAUSED
        
    def is_idle(self) -> bool:
        """检查动画引擎是否空闲"""
        return self.state == AnimationState.IDLE
        
    def get_queue_length(self) -> int:
        """获取动画队列长度"""
        return len(self.animation_queue)
        
    def _animation_loop(self) -> None:
        """动画主循环（在单独线程中运行）"""
        from logger import get_logger
        logger = get_logger()
        logger.debug("动画线程启动")
        
        loop_count = 0
        while self.is_running and not self.stop_event.is_set():
            loop_count += 1
            logger.debug(f"动画循环 #{loop_count} - 状态: {self.state}, 运行中: {self.is_running}, 队列长度: {len(self.animation_queue)}, 当前动画: {self.current_animation is not None}")
            
            # 处理暂停状态
            if self.state == AnimationState.PAUSED:
                logger.debug("动画已暂停，等待恢复")
                time.sleep(0.1)
                continue
                
            # 获取下一个动画
            if not self.current_animation and self.animation_queue:
                logger.debug(f"从队列获取新动画，队列长度: {len(self.animation_queue)}")
                self.current_animation = self.animation_queue.pop(0)
                self.current_animation.start()
                logger.debug(f"开始播放动画: {self.current_animation.type}")
                
                # 调用动画开始回调
                if self.on_animation_start:
                    try:
                        self.on_animation_start(self.current_animation)
                        logger.debug("动画开始回调执行成功")
                    except Exception as e:
                        logger.error(f"动画开始回调执行失败: {str(e)}")
            
            # 更新当前动画
            if self.current_animation:
                logger.debug(f"更新动画: {self.current_animation.type}")
                
                # 🔧 修复：确保 current_animation 不为 None
                current_anim = self.current_animation
                if current_anim is not None:
                    try:
                        is_completed = current_anim.update()
                        
                        if is_completed:
                            logger.debug(f"动画完成: {current_anim.type}")
                            # 调用动画完成回调
                            if self.on_animation_complete:
                                try:
                                    self.on_animation_complete(current_anim)
                                    logger.debug("动画完成回调执行成功")
                                except Exception as e:
                                    logger.error(f"动画完成回调执行失败: {str(e)}")
                            
                            self.current_animation = None
                            logger.debug("当前动画已清空")
                            
                            # 🔧 修复：只有在队列为空且没有外部请求停止时才设置IDLE状态
                            if not self.animation_queue and self.is_running:
                                logger.debug("动画队列为空且仍在运行，设置状态为IDLE")
                                self.state = AnimationState.IDLE

                                # 🔧 修复：立即调用队列空回调，而不是延迟调用
                                # 这样可以确保在回调中可以正确地重新启动动画
                                if self.on_queue_empty:
                                    try:
                                        logger.debug("执行队列空回调")
                                        self.on_queue_empty()
                                        logger.debug("队列空回调执行成功")
                                    except Exception as e:
                                        logger.error(f"队列空回调执行失败: {str(e)}")
                            else:
                                logger.debug(f"队列中还有 {len(self.animation_queue)} 个动画或动画已停止")
                    except Exception as e:
                        logger.error(f"更新动画时发生错误: {str(e)}")
                        self.current_animation = None
                else:
                    logger.warning("current_animation 变为 None，跳过更新")
                    self.current_animation = None
            else:
                # 没有当前动画时的处理
                if not self.animation_queue:
                    # 队列为空，但不立即退出，给排序算法时间添加新动画
                    if self.state == AnimationState.IDLE:
                        # 🔧 关键修复：增加等待时间，给排序算法更多时间来添加新动画
                        logger.debug("等待新动画...")
                        # 使用更长的等待时间，确保异步调度有足够时间执行
                        time.sleep(0.05)  # 增加到50ms
                        if not self.animation_queue:  # 再次检查
                            logger.debug("没有新动画，准备退出循环")
                            break
                    else:
                        # 状态不是IDLE但队列为空，短暂休眠
                        logger.debug("队列为空，短暂休眠")
                        time.sleep(0.05)  # 增加等待时间
                else:
                    # 队列中有动画但没有当前动画，短暂休眠
                    logger.debug("队列中有动画但没有当前动画，短暂休眠")
                    time.sleep(0.01)  # 稍微增加休眠时间
                
        logger.debug(f"动画线程结束，总循环次数: {loop_count}")
                
    def set_callbacks(self,
                     on_animation_start: Optional[Callable[[Animation], None]] = None,
                     on_animation_complete: Optional[Callable[[Animation], None]] = None,
                     on_queue_empty: Optional[Callable[[], None]] = None) -> None:
        """
        设置回调函数
        
        Args:
            on_animation_start: 动画开始回调
            on_animation_complete: 动画完成回调
            on_queue_empty: 队列为空回调
        """
        self.on_animation_start = on_animation_start
        self.on_animation_complete = on_animation_complete
        self.on_queue_empty = on_queue_empty
        
    def create_move_animation(self, 
                            target: Any, 
                            start_pos: tuple, 
                            end_pos: tuple, 
                            duration: float = 1.0) -> Animation:
        """
        创建移动动画
        
        Args:
            target: 移动目标对象
            start_pos: 起始位置 (x, y)
            end_pos: 结束位置 (x, y)
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的移动动画对象
        """
        animation = Animation(AnimationType.MOVE, duration)
        
        def update_progress(progress: float):
            # 计算插值位置
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
            
            # 更新目标位置
            if hasattr(target, 'move_to'):
                target.move_to(x, y)
                
        animation.on_update = update_progress
        return animation
        
    def create_highlight_animation(self, 
                                 target: Any, 
                                 duration: float = 0.5) -> Animation:
        """
        创建高亮动画
        
        Args:
            target: 高亮目标对象
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的高亮动画对象
        """
        animation = Animation(AnimationType.HIGHLIGHT, duration)
        
        def start_highlight():
            if hasattr(target, 'highlight'):
                target.highlight(True)
                
        def end_highlight():
            if hasattr(target, 'highlight'):
                target.highlight(False)
                
        animation.on_update = lambda progress: None
        animation.on_complete = end_highlight
        
        # 立即开始高亮
        start_highlight()
        
        return animation
        
    def create_compare_animation(self, 
                               mother_duck: Any, 
                               target1: Any, 
                               target2: Any, 
                               duration: float = 1.0) -> Animation:
        """
        创建比较动画
        
        Args:
            mother_duck: 母鸭对象
            target1: 第一个比较目标
            target2: 第二个比较目标
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的比较动画对象
        """
        animation = Animation(AnimationType.COMPARE, duration)
        
        def start_compare():
            # 设置比较状态
            if hasattr(target1, 'set_comparing'):
                target1.set_comparing(True)
            if hasattr(target2, 'set_comparing'):
                target2.set_comparing(True)
                
            # 母鸭指向目标
            if hasattr(mother_duck, 'point_to'):
                mother_duck.point_to(target1.x, target1.y)
                
        def end_compare():
            # 清除比较状态
            if hasattr(target1, 'set_comparing'):
                target1.set_comparing(False)
            if hasattr(target2, 'set_comparing'):
                target2.set_comparing(False)
                
        animation.on_update = lambda progress: None
        animation.on_complete = end_compare
        
        # 立即开始比较
        start_compare()
        
        return animation
        
    def create_complete_animation(self, 
                                targets: List[Any], 
                                duration: float = 2.0) -> Animation:
        """
        创建完成动画
        
        Args:
            targets: 目标对象列表
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的完成动画对象
        """
        animation = Animation(AnimationType.COMPLETE, duration)
        
        def start_complete():
            # 设置所有目标为已排序状态
            for target in targets:
                if hasattr(target, 'set_sorted'):
                    target.set_sorted(True)
                    
        animation.on_update = lambda progress: None
        animation.on_complete = lambda: None
        
        # 立即开始完成动画
        start_complete()
        
        return animation