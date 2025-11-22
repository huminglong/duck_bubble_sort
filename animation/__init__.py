"""
小鸭子冒泡排序可视化动画项目 - 动画模块

该模块包含动画系统的所有组件，包括动画引擎、动画器和排序动画集成。
"""

from .animation_engine import (
    AnimationEngine,
    Animation,
    AnimationState,
    AnimationType
)

from .animators import (
    DuckAnimator,
    SwapAnimator,
    HighlightAnimator,
    MotherDuckAnimator,
    ComparisonAnimator
)

from .sort_animation_integration import SortAnimationIntegration

__all__ = [
    # 动画引擎
    'AnimationEngine',
    'Animation',
    'AnimationState',
    'AnimationType',
    
    # 动画器
    'DuckAnimator',
    'SwapAnimator',
    'HighlightAnimator',
    'MotherDuckAnimator',
    'ComparisonAnimator',
    
    # 集成接口
    'SortAnimationIntegration'
]