"""
小鸭子冒泡排序可视化动画项目 - 动画器模块

该模块包含各种专门的动画器类，用于处理不同类型的动画效果。
每个动画器负责特定类型的动画实现。
"""

import math
import time
from typing import List, Tuple, Optional, Callable
from duck_bubble_sort.animation.animation_engine import Animation, AnimationType, AnimationEngine


class DuckAnimator:
    """鸭子动画器，处理单个鸭子的动画效果"""
    
    def __init__(self, duck, engine: AnimationEngine):
        """
        初始化鸭子动画器
        
        Args:
            duck: 鸭子对象
            engine: 动画引擎
        """
        self.duck = duck
        self.engine = engine
        
    def move_to(self, target_x: float, target_y: float, duration: float = 1.0) -> Animation:
        """
        创建移动动画
        
        Args:
            target_x: 目标x坐标
            target_y: 目标y坐标
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的移动动画
        """
        start_pos = (self.duck.x, self.duck.y)
        end_pos = (target_x, target_y)
        
        return self.engine.create_move_animation(
            self.duck, start_pos, end_pos, duration
        )
        
    def highlight(self, duration: float = 0.5) -> Animation:
        """
        创建高亮动画
        
        Args:
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的高亮动画
        """
        return self.engine.create_highlight_animation(self.duck, duration)
        
    def bounce(self, height: float = 20, duration: float = 0.5) -> Animation:
        """
        创建弹跳动画
        
        Args:
            height: 弹跳高度
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的弹跳动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        start_y = self.duck.y
        
        def update_progress(progress: float):
            # 使用正弦函数创建弹跳效果
            bounce_height = height * math.sin(progress * math.pi * 2)
            self.duck.move_to(self.duck.x, start_y - bounce_height)
            
        animation.on_update = update_progress
        return animation
        
    def shake(self, intensity: float = 5, duration: float = 0.3) -> Animation:
        """
        创建摇晃动画
        
        Args:
            intensity: 摇晃强度
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的摇晃动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        start_x = self.duck.x
        
        def update_progress(progress: float):
            # 使用正弦函数创建摇晃效果
            offset = intensity * math.sin(progress * math.pi * 4)  # 4次摇晃
            self.duck.move_to(start_x + offset, self.duck.y)
            
        def reset_position():
            self.duck.move_to(start_x, self.duck.y)
            
        animation.on_update = update_progress
        animation.on_complete = reset_position
        return animation


class SwapAnimator:
    """交换动画器，处理两只鸭子交换位置的动画"""
    
    def __init__(self, engine: AnimationEngine):
        """
        初始化交换动画器
        
        Args:
            engine: 动画引擎
        """
        self.engine = engine
        
    def swap_ducks(self, duck1, duck2, duration: float = 1.0) -> Animation:
        """
        创建两只鸭子交换位置的动画
        
        Args:
            duck1: 第一只鸭子
            duck2: 第二只鸭子
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的交换动画
        """
        animation = Animation(AnimationType.SWAP, duration)
        
        # 保存起始位置
        start1_x, start1_y = duck1.x, duck1.y
        start2_x, start2_y = duck2.x, duck2.y
        
        # 计算中间点（用于弧形移动）
        mid_x = (start1_x + start2_x) / 2
        mid_y = min(start1_y, start2_y) - 50  # 增加向上弧形的高度，给更多空间避免重叠
        
        # 计算鸭子之间的安全距离，防止重叠
        # 使用完整的鸭子大小而不是一半，确保完全避免重叠
        safe_distance = (duck1.size + duck2.size) / 2 + 20  # 增加额外间距确保安全
        
        # 计算两个不同的中间点，防止鸭子在移动过程中重叠
        # 使用更大的偏移量确保鸭子不会相遇
        if abs(start1_x - start2_x) > abs(start1_y - start2_y):
            # 水平距离大于垂直距离，使用垂直偏移
            offset = safe_distance * 1.2  # 增加偏移量
            mid1_x = mid_x
            mid1_y = mid_y - offset/2  # 第一个中间点更高
            mid2_x = mid_x
            mid2_y = mid_y + offset/2  # 第二个中间点更低
        else:
            # 垂直距离大于水平距离，使用水平偏移
            offset = safe_distance * 1.2  # 增加偏移量
            mid1_x = mid_x - offset  # 第一个中间点更左
            mid1_y = mid_y
            mid2_x = mid_x + offset  # 第二个中间点更右
            mid2_y = mid_y
        
        def update_progress(progress: float):
            if progress < 0.5:
                # 前半段：移动到各自的中间点
                sub_progress = progress * 2
                # 鸭子1移动到第一个中间点
                x1 = start1_x + (mid1_x - start1_x) * sub_progress
                y1 = start1_y + (mid1_y - start1_y) * sub_progress
                duck1.move_to(x1, y1)
                
                # 鸭子2移动到第二个中间点
                x2 = start2_x + (mid2_x - start2_x) * sub_progress
                y2 = start2_y + (mid2_y - start2_y) * sub_progress
                duck2.move_to(x2, y2)
            else:
                # 后半段：从中间点到目标位置
                sub_progress = (progress - 0.5) * 2
                # 鸭子1从第一个中间点到鸭子2的起始位置
                x1 = mid1_x + (start2_x - mid1_x) * sub_progress
                y1 = mid1_y + (start2_y - mid1_y) * sub_progress
                duck1.move_to(x1, y1)
                
                # 鸭子2从第二个中间点到鸭子1的起始位置
                x2 = mid2_x + (start1_x - mid2_x) * sub_progress
                y2 = mid2_y + (start1_y - mid2_y) * sub_progress
                duck2.move_to(x2, y2)
                
        animation.on_update = update_progress
        return animation


class HighlightAnimator:
    """高亮动画器，处理高亮效果"""
    
    def __init__(self, engine: AnimationEngine):
        """
        初始化高亮动画器
        
        Args:
            engine: 动画引擎
        """
        self.engine = engine
        
    def pulse(self, duck, duration: float = 1.0, scale_factor: float = 1.2) -> Animation:
        """
        创建脉冲高亮动画
        
        Args:
            duck: 目标鸭子
            duration: 动画持续时间
            scale_factor: 缩放因子
            
        Returns:
            Animation: 创建的脉冲动画
        """
        animation = Animation(AnimationType.HIGHLIGHT, duration)
        original_size = duck.size
        
        def update_progress(progress: float):
            # 使用正弦函数创建脉冲效果
            scale = 1 + (scale_factor - 1) * math.sin(progress * math.pi * 2)
            new_size = original_size * scale
            
            # 更新鸭子大小（如果支持）
            if hasattr(duck, 'size'):
                duck.size = new_size
                duck.draw()  # 重新绘制
                
        def reset_size():
            duck.size = original_size
            duck.draw()
            
        animation.on_update = update_progress
        animation.on_complete = reset_size
        return animation
        
    def sequential_highlight(self, ducks: List, duration: float = 0.5) -> List[Animation]:
        """
        创建顺序高亮动画
        
        Args:
            ducks: 鸭子列表
            duration: 每只鸭子的高亮持续时间
            
        Returns:
            List[Animation]: 创建的高亮动画列表
        """
        animations = []
        
        for duck in ducks:
            highlight_anim = self.engine.create_highlight_animation(duck, duration)
            animations.append(highlight_anim)
            
        return animations


class MotherDuckAnimator:
    """母鸭动画器，处理大母鸭的特殊动作"""
    
    def __init__(self, mother_duck, engine: AnimationEngine):
        """
        初始化母鸭动画器
        
        Args:
            mother_duck: 母鸭对象
            engine: 动画引擎
        """
        self.mother_duck = mother_duck
        self.engine = engine
        
    def point_to(self, target_x: float, target_y: float, duration: float = 0.5) -> Animation:
        """
        创建指向动画
        
        Args:
            target_x: 目标x坐标
            target_y: 目标y坐标
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的指向动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        
        def update_progress(progress: float):
            # 计算指向角度
            angle = math.atan2(target_y - self.mother_duck.y, target_x - self.mother_duck.x)
            
            # 这里可以添加旋转动画，目前简化为高亮
            if progress > 0.5 and not self.mother_duck.is_highlighted:
                self.mother_duck.highlight(True)
                
        def reset_point():
            self.mother_duck.highlight(False)
            
        animation.on_update = update_progress
        animation.on_complete = reset_point
        return animation
        
    def nod(self, duration: float = 0.5) -> Animation:
        """
        创建点头动画
        
        Args:
            duration: 动画持续时间
            
        Returns:
            Animation: 创建的点头动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        start_y = self.mother_duck.y
        
        def update_progress(progress: float):
            # 使用正弦函数创建点头效果
            if progress < 0.5:
                # 前半段：向下点头
                nod_offset = 10 * math.sin(progress * math.pi * 2)
                self.mother_duck.move_to(self.mother_duck.x, start_y + nod_offset)
            else:
                # 后半段：回到原位
                nod_offset = 10 * math.sin(progress * math.pi * 2)
                self.mother_duck.move_to(self.mother_duck.x, start_y + nod_offset)
                
        animation.on_update = update_progress
        return animation
        
    def walk_to(self, target_x: float, target_y: float, duration: float = 2.0) -> Animation:
        """
        创建行走动画

        Args:
            target_x: 目标x坐标
            target_y: 目标y坐标
            duration: 动画持续时间

        Returns:
            Animation: 创建的行走动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        start_x, start_y = self.mother_duck.x, self.mother_duck.y
        
        # 添加边界检查，确保目标位置在画布范围内
        try:
            canvas_width = self.engine.canvas.winfo_width()
            canvas_height = self.engine.canvas.winfo_height()
            if canvas_width == 1:  # 如果winfo_width返回1，则使用默认值
                canvas_width = 1000
                canvas_height = 400
        except:
            canvas_width = 1000  # 默认画布宽度
            canvas_height = 400  # 默认画布高度
        
        # 确保目标位置在有效范围内（留出边距）
        margin = 80  # 边距
        safe_target_x = max(margin, min(canvas_width - margin, target_x))
        safe_target_y = max(margin, min(canvas_height - margin, target_y))

        def update_progress(progress: float):
            # 计算当前位置
            current_x = start_x + (safe_target_x - start_x) * progress
            current_y = start_y + (safe_target_y - start_y) * progress

            # 添加行走时的摇摆效果
            wobble = 2 * math.sin(progress * math.pi * 8)  # 8次摇摆
            current_y += wobble
            
            # 确保当前位置也在边界内
            current_x = max(margin, min(canvas_width - margin, current_x))
            current_y = max(margin, min(canvas_height - margin, current_y))

            self.mother_duck.move_to(current_x, current_y)

        animation.on_update = update_progress
        return animation
        
    def celebrate(self, duration: float = 2.0) -> Animation:
        """
        创建庆祝动画

        Args:
            duration: 动画持续时间

        Returns:
            Animation: 创建的庆祝动画
        """
        animation = Animation(AnimationType.CUSTOM, duration)
        start_x, start_y = self.mother_duck.x, self.mother_duck.y
        
        # 添加边界检查
        try:
            canvas_width = self.engine.canvas.winfo_width()
            canvas_height = self.engine.canvas.winfo_height()
            if canvas_width == 1:
                canvas_width = 1000
                canvas_height = 400
        except:
            canvas_width = 1000
            canvas_height = 400
        
        margin = 80  # 边距

        def update_progress(progress: float):
            # 组合多种动作：跳跃、旋转、摇摆
            jump_height = 20 * abs(math.sin(progress * math.pi * 2))
            rotation = progress * math.pi * 2  # 旋转一圈
            wobble = 3 * math.sin(progress * math.pi * 6)

            new_x = start_x + wobble
            new_y = start_y - jump_height
            
            # 确保庆祝动作不会超出边界
            new_x = max(margin, min(canvas_width - margin, new_x))
            new_y = max(margin, min(canvas_height - margin, new_y))

            self.mother_duck.move_to(new_x, new_y)

        def reset_position():
            # 确保重置位置也在边界内
            safe_x = max(margin, min(canvas_width - margin, start_x))
            safe_y = max(margin, min(canvas_height - margin, start_y))
            self.mother_duck.move_to(safe_x, safe_y)

        animation.on_update = update_progress
        animation.on_complete = reset_position
        return animation


class ComparisonAnimator:
    """比较动画器，处理比较过程的动画效果"""
    
    def __init__(self, engine: AnimationEngine):
        """
        初始化比较动画器
        
        Args:
            engine: 动画引擎
        """
        self.engine = engine
        
    def compare_ducks(self, mother_duck, duck1, duck2, duration: float = 1.5) -> List[Animation]:
        """
        创建比较动画序列

        Args:
            mother_duck: 母鸭对象
            duck1: 第一只鸭子
            duck2: 第二只鸭子
            duration: 总动画持续时间

        Returns:
            List[Animation]: 创建的动画序列
        """
        animations = []

        # 1. 母鸭移动到比较位置
        # 使用更稳定的坐标计算，基于当前鸭子的实际位置，但加入边界检查
        mid_x = (duck1.x + duck2.x) / 2
        # 使用固定的母鸭高度，而不是基于当前鸭子位置的计算，以确保母鸭移动到正确的位置
        mid_y = 100  # 固定的母鸭高度 - 这是母鸭在画布上的标准位置

        # 添加边界检查，确保母鸭不会移动到画布外
        # 从canvas获取实际宽度和高度
        try:
            canvas_width = self.engine.canvas.winfo_width()
            canvas_height = self.engine.canvas.winfo_height()
            if canvas_width == 1:  # 如果winfo_width返回1，则使用默认值
                canvas_width = 1000
                canvas_height = 400
        except:
            canvas_width = 1000  # 默认画布宽度
            canvas_height = 400  # 默认画布高度

        # 保持在画布边界内，但允许一定的边距
        # 母鸭的大小约为80像素，所以需要留出足够的边距
        margin = mother_duck.size / 2 + 20  # 母鸭大小的一半加上额外边距
        min_x = margin   # 左边界
        max_x = canvas_width - margin  # 右边界
        min_y = margin   # 上边界
        max_y = canvas_height - margin  # 下边界
        
        # 确保目标位置在有效范围内
        safe_mid_x = max(min_x, min(max_x, mid_x))
        safe_mid_y = max(min_y, min(max_y, mid_y))
        
        # 额外的安全检查：如果两只鸭子距离很远，限制母鸭的移动范围
        duck_distance = abs(duck1.x - duck2.x)
        if duck_distance > 400:  # 如果鸭子间距超过400像素
            # 限制母鸭在更安全的中心区域
            center_x = canvas_width / 2
            safe_range = 300  # 安全范围半径
            safe_mid_x = max(center_x - safe_range, min(center_x + safe_range, safe_mid_x))

        mother_animator = MotherDuckAnimator(mother_duck, self.engine)
        walk_anim = mother_animator.walk_to(safe_mid_x, safe_mid_y, duration * 0.3)
        animations.append(walk_anim)

        # 2. 母鸭指向两只鸭子
        point_anim1 = mother_animator.point_to(duck1.x, duck1.y, duration * 0.2)
        animations.append(point_anim1)

        # 3. 高亮比较的鸭子
        highlight_anim1 = self.engine.create_highlight_animation(duck1, duration * 0.2)
        highlight_anim2 = self.engine.create_highlight_animation(duck2, duration * 0.2)
        animations.append(highlight_anim1)
        animations.append(highlight_anim2)

        # 4. 母鸭点头表示理解
        nod_anim = mother_animator.nod(duration * 0.3)
        animations.append(nod_anim)

        return animations