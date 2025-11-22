"""
小鸭子冒泡排序可视化动画项目 - 排序动画集成模块

该模块提供动画系统与排序算法的集成接口，负责接收排序算法的
状态变化通知并触发相应的动画效果。
"""

from typing import List, Optional, Callable
from duck_bubble_sort.algorithms.bubble_sort import BubbleSort
from duck_bubble_sort.graphics import BabyDuck, MotherDuck
from duck_bubble_sort.animation.animation_engine import AnimationEngine, AnimationState
from duck_bubble_sort.animation.animators import DuckAnimator, SwapAnimator, HighlightAnimator, MotherDuckAnimator, ComparisonAnimator
from duck_bubble_sort.logger import get_logger, log_animation_event


class SortAnimationIntegration:
    """排序动画集成类，连接排序算法和动画系统"""
    
    def __init__(self,
                 bubble_sort: BubbleSort,
                 baby_ducks: List[BabyDuck],
                 mother_duck: MotherDuck,
                 engine: AnimationEngine):
        """
        初始化排序动画集成
        
        Args:
            bubble_sort: 冒泡排序算法对象
            baby_ducks: 小鸭子列表
            mother_duck: 大母鸭对象
            engine: 动画引擎
        """
        self.logger = get_logger()
        self.logger.info("初始化排序动画集成")
        
        self.bubble_sort = bubble_sort
        self.baby_ducks = baby_ducks
        self.mother_duck = mother_duck
        self.engine = engine
        
        # 创建动画器
        self.duck_animators = [DuckAnimator(duck, engine) for duck in baby_ducks]
        self.swap_animator = SwapAnimator(engine)
        self.highlight_animator = HighlightAnimator(engine)
        self.mother_duck_animator = MotherDuckAnimator(mother_duck, engine)
        self.comparison_animator = ComparisonAnimator(engine)
        self.logger.info(f"创建了 {len(self.duck_animators)} 个鸭子动画器")
        
        # 动画配置
        self.animation_speed = 1.0
        self.enable_compare_animation = True
        self.enable_swap_animation = True
        self.enable_highlight_animation = True
        self.enable_complete_animation = True
        
        # 状态跟踪
        self.is_animating = False
        self.animation_queue = []
        
        # 设置排序算法回调
        self._setup_sort_callbacks()
        
        # 设置动画引擎回调
        self._setup_engine_callbacks()
        
        self.logger.info("排序动画集成初始化完成")
        
    def _setup_sort_callbacks(self) -> None:
        """设置排序算法的回调函数"""
        self.bubble_sort.set_callbacks(
            on_compare=self._on_compare,
            on_swap=self._on_swap,
            on_complete=self._on_complete
        )
        
    def _setup_engine_callbacks(self) -> None:
        """设置动画引擎的回调函数"""
        self.engine.set_callbacks(
            on_animation_start=self._on_animation_start,
            on_animation_complete=self._on_animation_complete,
            on_queue_empty=self._on_queue_empty
        )
        
    def _on_compare(self, index1: int, index2: int) -> None:
        """
        比较回调函数，当排序算法比较两个元素时触发
        
        Args:
            index1: 第一个元素的索引
            index2: 第二个元素的索引
        """
        if not self.enable_compare_animation:
            return
            
        # 获取比较的鸭子
        duck1 = self.baby_ducks[index1]
        duck2 = self.baby_ducks[index2]
        
        # 创建比较动画序列
        animations = self.comparison_animator.compare_ducks(
            self.mother_duck, duck1, duck2, 1.5 / self.animation_speed
        )
        
        # 添加到动画队列
        for anim in animations:
            self.engine.add_animation(anim)
            
    def _on_swap(self, index1: int, index2: int) -> None:
        """
        交换回调函数，当排序算法交换两个元素时触发
        
        Args:
            index1: 第一个元素的索引
            index2: 第二个元素的索引
        """
        self.logger.debug(f"交换回调开始 - 索引: {index1}, {index2}")
        self.logger.debug(f"交换前鸭子列表长度: {len(self.baby_ducks)}")
        self.logger.debug(f"交换前动画器列表长度: {len(self.duck_animators)}")
        
        if not self.enable_swap_animation:
            self.logger.debug("交换动画已禁用，跳过交换动画")
            return
            
        # 获取交换的鸭子
        duck1 = self.baby_ducks[index1]
        duck2 = self.baby_ducks[index2]
        
        self.logger.debug(f"创建交换动画: 鸭子 {index1} (值: {duck1.value}) 和 鸭子 {index2} (值: {duck2.value})")
        
        try:
            # 创建交换动画
            swap_anim = self.swap_animator.swap_ducks(
                duck1, duck2, 1.0 / self.animation_speed
            )
            self.logger.debug("交换动画创建成功")
            
            # 添加到动画队列
            self.engine.add_animation(swap_anim)
            self.logger.debug(f"交换动画已添加到队列，当前队列长度: {self.engine.get_queue_length()}")
            log_animation_event("交换动画", f"交换鸭子 {index1} 和 {index2}")

            # 注意：排序算法负责更新鸭子在列表中的顺序，这里不需要重复更新
            # 验证列表一致性
            self.logger.debug(f"交换后鸭子列表: {[duck.value for duck in self.baby_ducks]}")
            self.logger.debug(f"交换后动画器列表长度: {len(self.duck_animators)}")
            
        except Exception as e:
            self.logger.error(f"创建交换动画时发生错误: {str(e)}")
            raise
        
    def _on_complete(self) -> None:
        """完成回调函数，当排序完成时触发"""
        if not self.enable_complete_animation:
            return
            
        # 创建完成动画
        complete_anim = self.engine.create_complete_animation(
            self.baby_ducks, 2.0 / self.animation_speed
        )
        
        # 添加到动画队列
        self.engine.add_animation(complete_anim)
        
        # 母鸭庆祝动画
        celebrate_anim = self.mother_duck_animator.celebrate(2.0 / self.animation_speed)
        self.engine.add_animation(celebrate_anim)
        
    def _on_animation_start(self, animation) -> None:
        """动画开始回调"""
        self.is_animating = True
        
    def _on_animation_complete(self, animation) -> None:
        """动画完成回调"""
        # 可以在这里添加动画完成后的处理逻辑
        pass
        
    def _on_queue_empty(self) -> None:
        """动画队列为空回调"""
        self.logger.debug("动画队列为空回调开始")
        self.logger.debug(f"当前状态 - is_animating: {self.is_animating}, 排序完成: {self.bubble_sort.is_completed()}")

        # 立即设置 is_animating 状态为 False
        self.is_animating = False
        self.logger.debug("设置 is_animating = False")

        # 如果排序还没完成，继续下一步
        if not self.bubble_sort.is_completed():
            self.logger.debug("排序未完成，使用after()调度下一步排序")
            try:
                # 🔧 关键修复：使用canvas.after()在主线程中异步执行下一步
                # 这样可以避免在动画线程中直接调用可能导致线程join自己的问题
                # 使用较小的延迟以确保在动画线程检查前执行，但不要太小
                self.engine.canvas.after(10, self._execute_next_step)  # 增加到10ms
                self.logger.debug("下一步排序已调度")
            except Exception as e:
                self.logger.error(f"调度下一步排序时发生错误: {str(e)}")
                raise
        else:
            self.logger.debug("排序已完成，不继续执行")
    
    def _execute_next_step(self) -> None:
        """执行下一步排序（在主线程中调用）"""
        try:
            self.logger.debug("在主线程中执行下一步排序")
            
            # 🔧 关键修复：先检查排序是否已完成
            if self.bubble_sort.is_completed():
                self.logger.debug("排序已完成，不继续执行")
                self.is_animating = False  # 确保状态被重置
                return
                
            # 🔧 关键修复：检查动画状态，但允许在队列为空时继续执行
            if self.is_animating and self.engine.get_queue_length() > 0:
                self.logger.debug("动画正在执行中且队列不为空，跳过此步骤")
                return
                
            # 重置动画状态，允许执行下一步
            self.is_animating = False
            self.logger.debug("重置is_animating状态，准备执行下一步")
                
            self.step_sort()
            self.logger.debug("下一步排序执行成功")
            
            # 🔧 关键修复：确保动画引擎在播放状态
            # 如果动画队列不为空但引擎不在播放状态，重新启动引擎
            if self.engine.get_queue_length() > 0 and not self.engine.is_playing():
                self.logger.debug("动画队列不为空但引擎未播放，重新启动引擎")
                self.engine.play()
            elif self.engine.get_queue_length() == 0 and not self.bubble_sort.is_completed():
                # 🔧 新增修复：如果队列为空但排序未完成，可能需要手动触发下一步
                self.logger.debug("队列为空但排序未完成，延迟后再次尝试")
                self.engine.canvas.after(50, self._execute_next_step)
        except Exception as e:
            self.logger.error(f"执行下一步排序时发生错误: {str(e)}")
            # 重置状态以便可以手动重试
            self.is_animating = False
            
    def start_animation(self) -> None:
        """开始动画排序"""
        self.logger.info("开始动画排序")
        
        try:
            # 重置排序状态
            self.bubble_sort.reset()
            self.logger.debug("排序状态已重置")
            
            # 清空动画队列
            self.engine.clear_queue()
            self.logger.debug("动画队列已清空")
            
            # 开始播放动画
            self.engine.play()
            self.logger.debug("动画引擎已开始播放")
            
            # 执行第一步
            self.step_sort()
            self.logger.info("动画排序已开始")
        except Exception as e:
            self.logger.error(f"开始动画排序时发生错误: {str(e)}")
            raise
        
    def step_sort(self) -> None:
        """执行排序的一步"""
        self.logger.debug(f"step_sort 开始 - is_animating: {self.is_animating}, 排序完成: {self.bubble_sort.is_completed()}")

        # 添加更严格的状态检查
        if self.is_animating:
            self.logger.debug("动画正在播放中，跳过此步骤")
            return

        # 检查排序是否已完成
        if self.bubble_sort.is_completed():
            self.logger.debug("排序已完成，不继续执行")
            return

        # 临时设置动画状态，防止重复调用
        self.is_animating = True
        self.logger.debug("临时设置 is_animating = True")

        try:
            self.logger.debug("执行排序算法的一步")
            # 执行排序算法的一步
            has_step = self.bubble_sort.step()
            self.logger.debug(f"排序步骤执行结果: {has_step}")

            # 添加额外的数据验证
            self._validate_data_consistency()

            if not has_step:
                # 排序完成
                self.logger.debug("排序算法返回False，触发完成回调")
                self._on_complete()
                # 排序完成后重置状态
                self.is_animating = False
            else:
                self.logger.debug("排序步骤执行成功，继续等待动画完成")

                # 🔧 关键修复：不要立即重置is_animating，等待动画完成后再重置
                # 这样可以防止在动画还没完成时就执行下一步
                # is_animating 会在 _on_queue_empty 中重置
                
                # 确保动画引擎在播放状态
                if not self.engine.is_playing():
                    self.logger.debug("动画引擎未播放，重新启动")
                    self.engine.play()
        except Exception as e:
            self.logger.error(f"执行排序步骤时发生错误: {str(e)}")
            # 发生错误时重置状态
            self.is_animating = False
            raise

    def _validate_data_consistency(self):
        """验证数据一致性"""
        # 验证鸭子列表和动画器列表是否长度一致
        if len(self.baby_ducks) != len(self.duck_animators):
            self.logger.error(f"数据不一致: 鸭子列表长度 {len(self.baby_ducks)}，动画器列表长度 {len(self.duck_animators)}")
            return

        # 验证值的排序状态
        duck_values = [duck.value for duck in self.baby_ducks]
        self.logger.debug(f"当前鸭子值序列: {duck_values}")

        # 检查是否有重复值（虽然不应该有）
        value_counts = {}
        for value in duck_values:
            value_counts[value] = value_counts.get(value, 0) + 1
            if value_counts[value] > 1:
                self.logger.warning(f"发现重复值: {value}")
            
    def pause_animation(self) -> None:
        """暂停动画"""
        self.engine.pause()
        self.bubble_sort.pause()
        
    def resume_animation(self) -> None:
        """恢复动画"""
        self.engine.resume()
        self.bubble_sort.resume()
        
    def stop_animation(self) -> None:
        """停止动画"""
        self.engine.stop()
        self.bubble_sort.reset()
        
        # 重置所有鸭子状态
        for duck in self.baby_ducks:
            duck.set_sorted(False)
            duck.set_comparing(False)
            duck.highlight(False)
            
    def set_animation_speed(self, speed: float) -> None:
        """
        设置动画速度
        
        Args:
            speed: 速度倍数（1.0为正常速度）
        """
        self.animation_speed = max(0.1, speed)
        self.engine.set_speed(self.animation_speed)
        
    def enable_animation(self, 
                        compare: bool = True, 
                        swap: bool = True, 
                        highlight: bool = True, 
                        complete: bool = True) -> None:
        """
        启用或禁用特定类型的动画
        
        Args:
            compare: 是否启用比较动画
            swap: 是否启用交换动画
            highlight: 是否启用高亮动画
            complete: 是否启用完成动画
        """
        self.enable_compare_animation = compare
        self.enable_swap_animation = swap
        self.enable_highlight_animation = highlight
        self.enable_complete_animation = complete
        
    def run_complete_sort(self) -> None:
        """运行完整的排序动画"""
        self.start_animation()
        
        # 持续执行排序步骤直到完成
        def check_and_step():
            if not self.bubble_sort.is_completed() and not self.engine.is_paused():
                self.step_sort()
                # 使用after方法在下一帧继续
                if hasattr(self.engine.canvas, 'after'):
                    self.engine.canvas.after(50, check_and_step)
                    
        # 开始检查循环
        if hasattr(self.engine.canvas, 'after'):
            self.engine.canvas.after(100, check_and_step)
            
    def highlight_duck(self, index: int, duration: float = 0.5) -> None:
        """
        高亮指定的鸭子
        
        Args:
            index: 鸭子索引
            duration: 高亮持续时间
        """
        if 0 <= index < len(self.baby_ducks):
            duck = self.baby_ducks[index]
            highlight_anim = self.highlight_animator.pulse(
                duck, duration / self.animation_speed
            )
            self.engine.add_animation(highlight_anim)
            
    def highlight_range(self, start_index: int, end_index: int, duration: float = 0.5) -> None:
        """
        高亮指定范围内的鸭子
        
        Args:
            start_index: 起始索引
            end_index: 结束索引
            duration: 每只鸭子的高亮持续时间
        """
        start_index = max(0, start_index)
        end_index = min(len(self.baby_ducks) - 1, end_index)
        
        for i in range(start_index, end_index + 1):
            self.highlight_duck(i, duration)
            
    def create_custom_animation_sequence(self, animations: List) -> None:
        """
        添加自定义动画序列
        
        Args:
            animations: 动画列表
        """
        for anim in animations:
            self.engine.add_animation(anim)
            
    def is_animation_playing(self) -> bool:
        """检查动画是否正在播放"""
        return self.engine.is_playing()
        
    def is_sort_completed(self) -> bool:
        """检查排序是否完成"""
        return self.bubble_sort.is_completed()
        
    def get_sort_progress(self) -> float:
        """获取排序进度"""
        return self.bubble_sort.get_progress()
        
    def get_sort_statistics(self) -> dict:
        """获取排序统计信息"""
        return {
            'comparisons': self.bubble_sort.get_comparisons_count(),
            'swaps': self.bubble_sort.get_swaps_count(),
            'progress': self.bubble_sort.get_progress(),
            'completed': self.bubble_sort.is_completed()
        }