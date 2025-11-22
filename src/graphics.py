"""
小鸭子冒泡排序可视化动画项目 - 图形模块

该模块包含所有鸭子相关的图形类：
- Duck: 鸭子基类
- BabyDuck: 小鸭子类
- MotherDuck: 大母鸭类

使用Tkinter Canvas绘制鸭子图形。
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import math


class Duck(ABC):
    """鸭子基类，定义所有鸭子的基本属性和行为"""
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float, size: float, value: int):
        """
        初始化鸭子
        
        Args:
            canvas: Tkinter画布对象
            x: 鸭子的x坐标
            y: 鸭子的y坐标
            size: 鸭子的大小
            value: 鸭子代表的数值（用于排序）
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.value = value
        self.graphic_elements = []  # 存储鸭子的图形元素
        self.is_highlighted = False  # 是否高亮显示
        self.is_comparing = False  # 是否正在比较
        self.is_sorted = False  # 是否已排序
        
    @abstractmethod
    def draw(self) -> None:
        """绘制鸭子的抽象方法，子类必须实现"""
        pass
    
    def move_to(self, new_x: float, new_y: float) -> None:
        """移动鸭子到新位置，添加边界检查防止鸭子跑出界面外"""
        # 获取画布尺寸
        try:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if canvas_width == 1:  # 画布还未初始化
                canvas_width = 1000
                canvas_height = 400
        except:
            canvas_width = 1000
            canvas_height = 400
            
        # 计算安全边界（考虑鸭子大小）
        margin = self.size / 2 + 10  # 鸭子大小的一半加上额外边距
        
        # 确保新位置在边界内
        safe_x = max(margin, min(canvas_width - margin, new_x))
        safe_y = max(margin, min(canvas_height - margin, new_y))
        
        dx = safe_x - self.x
        dy = safe_y - self.y
        
        for element in self.graphic_elements:
            self.canvas.move(element, dx, dy)
        
        self.x = safe_x
        self.y = safe_y
    
    def highlight(self, highlight: bool = True) -> None:
        """高亮或取消高亮鸭子"""
        self.is_highlighted = highlight
        self._update_appearance()
    
    def set_comparing(self, comparing: bool = True) -> None:
        """设置鸭子是否正在比较状态"""
        self.is_comparing = comparing
        self._update_appearance()
    
    def set_sorted(self, sorted: bool = True) -> None:
        """设置鸭子是否已排序"""
        self.is_sorted = sorted
        self._update_appearance()
    
    def _update_appearance(self) -> None:
        """更新鸭子的外观（子类可以重写）"""
        pass
    
    def clear(self) -> None:
        """从画布上清除鸭子"""
        for element in self.graphic_elements:
            self.canvas.delete(element)
        self.graphic_elements.clear()


class BabyDuck(Duck):
    """小鸭子类，用于表示排序数组中的元素"""
    
    # 小鸭子的颜色方案 - 更柔和现代的配色
    BODY_COLOR = "#FFD700"  # 金黄色
    BEAK_COLOR = "#FF8C00"  # 深橙色
    EYE_COLOR = "#000000"   # 黑色
    WING_COLOR = "#FFA500"  # 橙色
    BODY_OUTLINE = "#8B7500"  # 深金色轮廓
    
    # 状态颜色 - 更丰富的视觉效果
    HIGHLIGHT_COLOR = "#FF69B4"  # 粉红色（高亮）
    COMPARING_COLOR = "#00CED1"  # 深青色（比较中）
    SORTED_COLOR = "#32CD32"     # 绿色（已排序）
    GLOW_COLOR = "#FFFFE0"       # 发光效果颜色
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float, size: float, value: int):
        """
        初始化小鸭子
        
        Args:
            canvas: Tkinter画布对象
            x: 鸭子的x坐标
            y: 鸭子的y坐标
            size: 鸭子的大小（20-50像素）
            value: 鸭子代表的数值
        """
        super().__init__(canvas, x, y, size, value)
        self.draw()
    
    def draw(self) -> None:
        """绘制小鸭子"""
        # 清除之前的图形
        self.clear()
        
        # 计算鸭子各部分的相对位置
        body_width = self.size * 0.8
        body_height = self.size * 0.6
        head_radius = self.size * 0.25
        beak_length = self.size * 0.15
        eye_radius = self.size * 0.05
        
        # 添加阴影效果
        shadow_offset = 3
        shadow = self.canvas.create_oval(
            self.x - body_width/2 + shadow_offset, self.y - body_height/2 + shadow_offset,
            self.x + body_width/2 + shadow_offset, self.y + body_height/2 + shadow_offset,
            fill="#D3D3D3", outline="", stipple="gray50"
        )
        self.graphic_elements.append(shadow)
        
        # 绘制身体（椭圆）- 带有渐变效果
        body = self.canvas.create_oval(
            self.x - body_width/2, self.y - body_height/2,
            self.x + body_width/2, self.y + body_height/2,
            fill=self._get_body_color(), outline=self.BODY_OUTLINE, width=2
        )
        self.graphic_elements.append(body)
        
        # 绘制身体高光
        highlight = self.canvas.create_oval(
            self.x - body_width/4, self.y - body_height/3,
            self.x - body_width/8, self.y - body_height/4,
            fill=self.GLOW_COLOR, outline="", stipple="gray75"
        )
        self.graphic_elements.append(highlight)
        
        # 绘制头部（圆形）
        head_x = self.x + body_width * 0.3
        head_y = self.y - body_height * 0.3
        head = self.canvas.create_oval(
            head_x - head_radius, head_y - head_radius,
            head_x + head_radius, head_y + head_radius,
            fill=self._get_body_color(), outline=self.BODY_OUTLINE, width=2
        )
        self.graphic_elements.append(head)
        
        # 绘制嘴巴（三角形）
        beak_points = [
            head_x + head_radius, head_y,  # 嘴巴根部
            head_x + head_radius + beak_length, head_y,  # 嘴巴尖端
            head_x + head_radius, head_y + beak_length/2  # 嘴巴底部
        ]
        beak = self.canvas.create_polygon(
            beak_points, fill=self.BEAK_COLOR, outline="#000000", width=1
        )
        self.graphic_elements.append(beak)
        
        # 绘制眼睛（更生动的设计）
        eye_x = head_x + head_radius * 0.5
        eye_y = head_y - head_radius * 0.3
        
        # 眼白
        eye_white = self.canvas.create_oval(
            eye_x - eye_radius * 1.5, eye_y - eye_radius * 1.5,
            eye_x + eye_radius * 1.5, eye_y + eye_radius * 1.5,
            fill="white", outline="#000000", width=1
        )
        self.graphic_elements.append(eye_white)
        
        # 眼珠
        eye = self.canvas.create_oval(
            eye_x - eye_radius, eye_y - eye_radius,
            eye_x + eye_radius, eye_y + eye_radius,
            fill=self.EYE_COLOR, outline=""
        )
        self.graphic_elements.append(eye)
        
        # 眼睛高光
        eye_highlight = self.canvas.create_oval(
            eye_x - eye_radius * 0.3, eye_y - eye_radius * 0.3,
            eye_x - eye_radius * 0.1, eye_y - eye_radius * 0.1,
            fill="white", outline=""
        )
        self.graphic_elements.append(eye_highlight)
        
        # 绘制翅膀（小椭圆）
        wing_width = body_width * 0.3
        wing_height = body_height * 0.4
        wing = self.canvas.create_oval(
            self.x - body_width * 0.1, self.y - wing_height/2,
            self.x - body_width * 0.1 + wing_width, self.y + wing_height/2,
            fill=self.WING_COLOR, outline="#000000", width=1
        )
        self.graphic_elements.append(wing)
        
        # 数值背景
        text_bg = self.canvas.create_rectangle(
            self.x - self.size/4, self.y + body_height/2 + 5,
            self.x + self.size/4, self.y + body_height/2 + 20,
            fill="#FFFFFF", outline="#8B7500", width=1
        )
        self.graphic_elements.append(text_bg)
        
        # 显示数值
        text = self.canvas.create_text(
            self.x, self.y + body_height/2 + 12,
            text=str(self.value), font=("Arial", int(self.size/3.5), "bold"),
            fill="#000000"
        )
        self.graphic_elements.append(text)
    
    def _get_body_color(self) -> str:
        """根据状态获取身体颜色"""
        if self.is_sorted:
            return self.SORTED_COLOR
        elif self.is_comparing:
            return self.COMPARING_COLOR
        elif self.is_highlighted:
            return self.HIGHLIGHT_COLOR
        else:
            return self.BODY_COLOR
    
    def _update_appearance(self) -> None:
        """更新小鸭子的外观"""
        if self.graphic_elements:
            # 更新身体颜色
            body_color = self._get_body_color()
            self.canvas.itemconfig(self.graphic_elements[2], fill=body_color)  # 身体
            self.canvas.itemconfig(self.graphic_elements[5], fill=body_color)  # 头部
            
            # 添加闪烁效果
            if self.is_comparing:
                self._add_glow_effect()
            elif self.is_sorted:
                self._add_sorted_effect()
    
    def _add_glow_effect(self) -> None:
        """添加比较时的发光效果"""
        if len(self.graphic_elements) > 10:  # 确保有足够的元素
            # 为身体添加发光边框
            self.canvas.itemconfig(self.graphic_elements[2], width=3)
    
    def _add_sorted_effect(self) -> None:
        """添加排序完成时的特效"""
        if len(self.graphic_elements) > 10:
            # 为已排序的鸭子添加特殊边框
            self.canvas.itemconfig(self.graphic_elements[2], width=4)


class MotherDuck(Duck):
    """大母鸭类，用于执行排序操作"""
    
    # 大母鸭的颜色方案 - 更优雅的配色
    BODY_COLOR = "#8B4513"  # 棕色
    BEAK_COLOR = "#FF6347"  # 番茄红
    EYE_COLOR = "#000000"   # 黑色
    WING_COLOR = "#A0522D"  # 赭色
    CROWN_COLOR = "#FFD700" # 金色皇冠
    BODY_OUTLINE = "#654321" # 深棕色轮廓
    CROWN_GEM = "#FF1493"   # 皇冠宝石
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float):
        """
        初始化大母鸭
        
        Args:
            canvas: Tkinter画布对象
            x: 鸭子的x坐标
            y: 鸭子的y坐标
        """
        # 大母鸭比小鸭子大1.5倍
        size = 60  # 固定大小
        super().__init__(canvas, x, y, size, 0)  # 大母鸭不参与排序，value设为0
        self.draw()
    
    def draw(self) -> None:
        """绘制大母鸭"""
        # 清除之前的图形
        self.clear()
        
        # 计算鸭子各部分的相对位置
        body_width = self.size * 0.8
        body_height = self.size * 0.6
        head_radius = self.size * 0.25
        beak_length = self.size * 0.15
        eye_radius = self.size * 0.05
        crown_height = self.size * 0.2
        
        # 添加阴影效果
        shadow_offset = 4
        shadow = self.canvas.create_oval(
            self.x - body_width/2 + shadow_offset, self.y - body_height/2 + shadow_offset,
            self.x + body_width/2 + shadow_offset, self.y + body_height/2 + shadow_offset,
            fill="#A9A9A9", outline="", stipple="gray50"
        )
        self.graphic_elements.append(shadow)
        
        # 绘制身体（椭圆）- 带有渐变效果
        body = self.canvas.create_oval(
            self.x - body_width/2, self.y - body_height/2,
            self.x + body_width/2, self.y + body_height/2,
            fill=self.BODY_COLOR, outline=self.BODY_OUTLINE, width=3
        )
        self.graphic_elements.append(body)
        
        # 绘制身体高光
        highlight = self.canvas.create_oval(
            self.x - body_width/3, self.y - body_height/2.5,
            self.x - body_width/6, self.y - body_height/3,
            fill="#D2691E", outline="", stipple="gray75"
        )
        self.graphic_elements.append(highlight)
        
        # 绘制头部（圆形）
        head_x = self.x + body_width * 0.3
        head_y = self.y - body_height * 0.3
        head = self.canvas.create_oval(
            head_x - head_radius, head_y - head_radius,
            head_x + head_radius, head_y + head_radius,
            fill=self.BODY_COLOR, outline=self.BODY_OUTLINE, width=3
        )
        self.graphic_elements.append(head)
        
        # 绘制皇冠（更华丽的三角形）
        crown_points = [
            head_x - head_radius * 0.8, head_y - head_radius - crown_height/2,  # 左下
            head_x - head_radius * 0.4, head_y - head_radius - crown_height * 0.8,  # 左中
            head_x, head_y - head_radius - crown_height,  # 顶点
            head_x + head_radius * 0.4, head_y - head_radius - crown_height * 0.8,  # 右中
            head_x + head_radius * 0.8, head_y - head_radius - crown_height/2  # 右下
        ]
        crown = self.canvas.create_polygon(
            crown_points, fill=self.CROWN_COLOR, outline=self.BODY_OUTLINE, width=2
        )
        self.graphic_elements.append(crown)
        
        # 皇冠上的宝石
        gem = self.canvas.create_oval(
            head_x - head_radius * 0.15, head_y - head_radius - crown_height * 0.7,
            head_x + head_radius * 0.15, head_y - head_radius - crown_height * 0.5,
            fill=self.CROWN_GEM, outline="#FFFFFF", width=1
        )
        self.graphic_elements.append(gem)
        
        # 绘制嘴巴（三角形）
        beak_points = [
            head_x + head_radius, head_y,  # 嘴巴根部
            head_x + head_radius + beak_length, head_y,  # 嘴巴尖端
            head_x + head_radius, head_y + beak_length/2  # 嘴巴底部
        ]
        beak = self.canvas.create_polygon(
            beak_points, fill=self.BEAK_COLOR, outline="#000000", width=2
        )
        self.graphic_elements.append(beak)
        
        # 绘制眼睛（更生动的设计）
        eye_x = head_x + head_radius * 0.5
        eye_y = head_y - head_radius * 0.3
        
        # 眼白
        eye_white = self.canvas.create_oval(
            eye_x - eye_radius * 1.5, eye_y - eye_radius * 1.5,
            eye_x + eye_radius * 1.5, eye_y + eye_radius * 1.5,
            fill="white", outline=self.BODY_OUTLINE, width=1
        )
        self.graphic_elements.append(eye_white)
        
        # 眼珠
        eye = self.canvas.create_oval(
            eye_x - eye_radius, eye_y - eye_radius,
            eye_x + eye_radius, eye_y + eye_radius,
            fill=self.EYE_COLOR, outline=""
        )
        self.graphic_elements.append(eye)
        
        # 眼睛高光
        eye_highlight = self.canvas.create_oval(
            eye_x - eye_radius * 0.3, eye_y - eye_radius * 0.3,
            eye_x - eye_radius * 0.1, eye_y - eye_radius * 0.1,
            fill="white", outline=""
        )
        self.graphic_elements.append(eye_highlight)
        
        # 绘制翅膀（大椭圆）
        wing_width = body_width * 0.4
        wing_height = body_height * 0.5
        wing = self.canvas.create_oval(
            self.x - body_width * 0.1, self.y - wing_height/2,
            self.x - body_width * 0.1 + wing_width, self.y + wing_height/2,
            fill=self.WING_COLOR, outline="#000000", width=2
        )
        self.graphic_elements.append(wing)
        
        # 文字背景
        text_bg = self.canvas.create_rectangle(
            self.x - 20, self.y + body_height/2 + 10,
            self.x + 20, self.y + body_height/2 + 30,
            fill="#FFFFFF", outline=self.BODY_OUTLINE, width=2
        )
        self.graphic_elements.append(text_bg)
        
        # 显示"母鸭"文字
        text = self.canvas.create_text(
            self.x, self.y + body_height/2 + 20,
            text="👑 母鸭", font=("Arial", 14, "bold"),
            fill="#8B4513"
        )
        self.graphic_elements.append(text)
    
    def point_to(self, target_x: float, target_y: float) -> None:
        """让母鸭指向目标位置"""
        # 计算指向角度
        angle = math.atan2(target_y - self.y, target_x - self.x)
        
        # 这里可以添加指向动画，暂时简化处理
        self.highlight(True)
    
    def nod(self) -> None:
        """母鸭点头动作"""
        # 保存原始位置
        original_y = self.y
        
        # 向下点头
        self.move_to(self.x, self.y + 10)
        
        # 恢复原位（这里应该使用动画，暂时简化）
        self.move_to(self.x, original_y)


class DuckFactory:
    """鸭子工厂类，用于创建不同类型的鸭子"""
    
    @staticmethod
    def create_baby_ducks(canvas: tk.Canvas, start_x: float, start_y: float, 
                         spacing: float, values: List[int]) -> List[BabyDuck]:
        """
        创建一组小鸭子
        
        Args:
            canvas: Tkinter画布对象
            start_x: 起始x坐标
            start_y: 起始y坐标
            spacing: 鸭子之间的间距
            values: 鸭子代表的数值列表
            
        Returns:
            小鸭子列表
        """
        ducks = []
        min_value = min(values)
        max_value = max(values)
        
        for i, value in enumerate(values):
            # 根据数值计算鸭子大小（20-50像素）
            normalized_value = (value - min_value) / (max_value - min_value) if max_value != min_value else 0.5
            size = 20 + normalized_value * 30  # 20-50像素范围
            
            x = start_x + i * spacing
            duck = BabyDuck(canvas, x, start_y, size, value)
            ducks.append(duck)
        
        return ducks
    
    @staticmethod
    def create_mother_duck(canvas: tk.Canvas, x: float, y: float) -> MotherDuck:
        """
        创建大母鸭
        
        Args:
            canvas: Tkinter画布对象
            x: 母鸭的x坐标
            y: 母鸭的y坐标
            
        Returns:
            大母鸭对象
        """
        return MotherDuck(canvas, x, y)