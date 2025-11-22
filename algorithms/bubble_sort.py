"""
小鸭子冒泡排序可视化动画项目 - 冒泡排序算法模块

该模块包含冒泡排序算法的实现，支持逐步执行和状态跟踪，
用于与小鸭子图形系统集成，实现排序过程的可视化。
"""

from typing import List, Optional, Tuple, Callable
import time
from duck_bubble_sort.logger import get_logger, log_sort_step


class BubbleSort:
    """冒泡排序算法类，封装排序逻辑和状态管理"""
    
    def __init__(self, ducks: List):
        """
        初始化冒泡排序算法
        
        Args:
            ducks: 鸭子对象列表，每个鸭子必须有value属性
        """
        self.logger = get_logger()
        self.logger.info(f"初始化冒泡排序算法，鸭子数量: {len(ducks)}")
        
        self.ducks = ducks
        self.n = len(ducks)
        
        # 排序状态
        self.i = 0  # 外层循环索引
        self.j = 0  # 内层循环索引
        self.completed = False  # 排序是否完成
        self.paused = False  # 是否暂停
        
        # 状态跟踪
        self.current_comparison = (-1, -1)  # 当前比较的两个鸭子索引
        self.current_swap = (-1, -1)  # 当前交换的两个鸭子索引
        self.sorted_indices = []  # 已排序的鸭子索引
        self.comparisons_count = 0  # 比较次数
        self.swaps_count = 0  # 交换次数
        
        # 回调函数
        self.on_compare: Optional[Callable[[int, int], None]] = None  # 比较回调
        self.on_swap: Optional[Callable[[int, int], None]] = None  # 交换回调
        self.on_complete: Optional[Callable[[], None]] = None  # 完成回调
        
        # 历史记录（用于回放或调试）
        self.history = []  # 记录每一步的操作
        
        # 记录初始状态
        initial_values = [duck.value for duck in ducks]
        self.logger.info(f"初始鸭子值序列: {initial_values}")
        
    def step(self) -> bool:
        """
        执行一步排序操作
        
        Returns:
            bool: 是否执行了操作（True表示有操作，False表示排序已完成）
        """
        if self.completed or self.paused:
            return False
        
        # 处理空列表或单元素列表
        if self.n <= 1:
            self._complete_sort()
            return False
            
        # 清除之前的状态
        self.current_comparison = (-1, -1)
        self.current_swap = (-1, -1)
        
        # 执行冒泡排序的一步
        if self.i < self.n - 1:
            if self.j < self.n - self.i - 1:
                # 比较相邻的两个鸭子
                self.current_comparison = (self.j, self.j + 1)
                self.comparisons_count += 1
                
                # 调用比较回调（捕获异常）
                if self.on_compare:
                    try:
                        self.on_compare(self.j, self.j + 1)
                    except Exception:
                        # 忽略回调异常，继续执行
                        pass
                
                # 记录历史
                self.history.append({
                    'type': 'compare',
                    'indices': (self.j, self.j + 1),
                    'values': (self.ducks[self.j].value, self.ducks[self.j + 1].value)
                })
                
                # 如果前一个鸭子比后一个鸭子大，则交换
                if self.ducks[self.j].value > self.ducks[self.j + 1].value:
                    self._swap_ducks(self.j, self.j + 1)
                
                self.j += 1
                return True
            else:
                # 内层循环完成，标记最后一个元素为已排序
                self.sorted_indices.append(self.n - self.i - 1)
                self.i += 1
                self.j = 0
                
                # 如果所有元素都已排序
                if self.i >= self.n - 1:
                    self._complete_sort()
                    return False  # 🔧 修复：排序完成后应返回False
                
                return True
        else:
            self._complete_sort()
            return False
    
    def _swap_ducks(self, index1: int, index2: int) -> None:
        """
        交换两个鸭子的位置

        Args:
            index1: 第一个鸭子的索引
            index2: 第二个鸭子的索引
        """
        # 记录交换信息
        self.current_swap = (index1, index2)
        self.swaps_count += 1

        # 获取要交换的鸭子对象和位置信息（在交换前保存）
        duck1 = self.ducks[index1]
        duck2 = self.ducks[index2]
        pos1_x, pos1_y = duck1.x, duck1.y
        pos2_x, pos2_y = duck2.x, duck2.y

        # 记录交换日志
        self.logger.debug(f"交换鸭子 {index1} 和 {index2}，值: {duck1.value} 和 {duck2.value}")
        self.logger.debug(f"交换前位置: 鸭子{index1}({pos1_x}, {pos1_y}), 鸭子{index2}({pos2_x}, {pos2_y})")

        # 记录历史（在交换前记录原始值）
        self.history.append({
            'type': 'swap',
            'indices': (index1, index2),
            'values': (duck1.value, duck2.value),
            'positions': ((pos1_x, pos1_y), (pos2_x, pos2_y))
        })

        # 调用交换回调（在列表交换前调用，让动画层使用正确的鸭子对象）
        if self.on_swap:
            try:
                self.on_swap(index1, index2)
            except Exception as e:
                self.logger.warning(f"交换回调执行失败: {str(e)}")
                # 忽略回调异常，继续执行
                pass

        # 执行列表中的位置交换
        self.ducks[index1], self.ducks[index2] = duck2, duck1

        # 更新鸭子的图形位置（确保鸭子移动到正确位置）
        if hasattr(duck1, 'move_to') and hasattr(duck2, 'move_to'):
            try:
                # 交换位置：duck1移动到duck2的位置，duck2移动到duck1的位置
                duck1.move_to(pos2_x, pos2_y)
                duck2.move_to(pos1_x, pos1_y)

                self.logger.debug(f"交换后位置: 鸭子{index1}({pos2_x}, {pos2_y}), 鸭子{index2}({pos1_x}, {pos1_y})")
            except Exception as e:
                self.logger.error(f"更新鸭子图形位置失败: {str(e)}")

        # 数据一致性验证
        if self.ducks[index1].x != pos2_x or self.ducks[index2].x != pos1_x:
            self.logger.warning(f"位置更新可能存在不一致，请检查动画实现")

        # 额外的一致性验证
        self._validate_consistency(index1, index2, duck1, duck2)

    def _validate_consistency(self, index1: int, index2: int, original_duck1, original_duck2):
        """
        验证交换后数据的一致性

        Args:
            index1: 交换前的索引1
            index2: 交换前的索引2
            original_duck1: 原始鸭子1对象
            original_duck2: 原始鸭子2对象
        """
        # 验证列表中的鸭子对象是否正确交换
        actual_duck1 = self.ducks[index1]
        actual_duck2 = self.ducks[index2]

        if actual_duck1.value != original_duck2.value:
            self.logger.error(f"列表交换错误: 位置{index1}的鸭子值应该是{original_duck2.value}，但实际是{actual_duck1.value}")

        if actual_duck2.value != original_duck1.value:
            self.logger.error(f"列表交换错误: 位置{index2}的鸭子值应该是{original_duck1.value}，但实际是{actual_duck2.value}")

        # 验证鸭子对象的图形位置是否与列表中的位置一致
        if hasattr(actual_duck1, 'x') and hasattr(actual_duck2, 'x'):
            # 检查实际位置是否与预期一致
            expected_pos1_x = original_duck2.x  # 由于交换，duck1现在应该是原来duck2的位置
            expected_pos2_x = original_duck1.x  # 由于交换，duck2现在应该是原来duck1的位置

            if actual_duck1.x != expected_pos1_x:
                self.logger.warning(f"鸭子{index1}在列表中的位置与图形位置不一致: 列表值{actual_duck1.value}, 预期x={expected_pos1_x}, 实际x={actual_duck1.x}")

            if actual_duck2.x != expected_pos2_x:
                self.logger.warning(f"鸭子{index2}在列表中的位置与图形位置不一致: 列表值{actual_duck2.value}, 预期x={expected_pos2_x}, 实际x={actual_duck2.x}")
    
    def _complete_sort(self) -> None:
        """完成排序，设置最终状态"""
        self.completed = True
        self.sorted_indices = list(range(self.n))  # 所有元素都已排序
        
        # 记录完成日志
        final_values = [duck.value for duck in self.ducks]
        self.logger.info(f"排序完成！最终序列: {final_values}")
        self.logger.info(f"总比较次数: {self.comparisons_count}, 总交换次数: {self.swaps_count}")
        
        # 调用完成回调（捕获异常）
        if self.on_complete:
            try:
                self.on_complete()
            except Exception as e:
                self.logger.warning(f"完成回调执行失败: {str(e)}")
                # 忽略回调异常，继续执行
                pass
        
        # 记录历史
        self.history.append({
            'type': 'complete',
            'message': '排序完成'
        })
    
    def reset(self) -> None:
        """重置排序状态"""
        self.i = 0
        self.j = 0
        self.completed = False
        self.paused = False
        self.current_comparison = (-1, -1)
        self.current_swap = (-1, -1)
        self.sorted_indices = []
        self.comparisons_count = 0
        self.swaps_count = 0
        self.history = []
        
        # 重置所有鸭子的状态
        for duck in self.ducks:
            if hasattr(duck, 'set_sorted'):
                duck.set_sorted(False)
            if hasattr(duck, 'set_comparing'):
                duck.set_comparing(False)
            if hasattr(duck, 'highlight'):
                duck.highlight(False)
    
    def is_completed(self) -> bool:
        """检查排序是否完成"""
        return self.completed
    
    def get_current_comparison(self) -> Tuple[int, int]:
        """获取当前比较的鸭子索引"""
        return self.current_comparison
    
    def get_current_swap(self) -> Tuple[int, int]:
        """获取当前交换的鸭子索引"""
        return self.current_swap
    
    def get_sorted_indices(self) -> List[int]:
        """获取已排序的鸭子索引"""
        return self.sorted_indices
    
    def get_comparisons_count(self) -> int:
        """获取比较次数"""
        return self.comparisons_count
    
    def get_swaps_count(self) -> int:
        """获取交换次数"""
        return self.swaps_count
    
    def get_progress(self) -> float:
        """
        获取排序进度（0.0到1.0）
        
        Returns:
            float: 排序进度百分比
        """
        if self.n <= 1:
            return 1.0
        
        total_comparisons = (self.n - 1) * self.n // 2
        return min(self.comparisons_count / total_comparisons, 1.0)
    
    def pause(self) -> None:
        """暂停排序"""
        self.paused = True
    
    def resume(self) -> None:
        """继续排序"""
        self.paused = False
    
    def is_paused(self) -> bool:
        """检查是否暂停"""
        return self.paused
    
    def set_callbacks(self, 
                     on_compare: Optional[Callable[[int, int], None]] = None,
                     on_swap: Optional[Callable[[int, int], None]] = None,
                     on_complete: Optional[Callable[[], None]] = None) -> None:
        """
        设置回调函数
        
        Args:
            on_compare: 比较回调函数，接收两个鸭子索引
            on_swap: 交换回调函数，接收两个鸭子索引
            on_complete: 完成回调函数
        """
        self.on_compare = on_compare
        self.on_swap = on_swap
        self.on_complete = on_complete
    
    def get_history(self) -> List[dict]:
        """获取操作历史记录"""
        return self.history.copy()
    
    def run_to_completion(self, delay: float = 0.1) -> None:
        """
        运行排序直到完成（用于测试）
        
        Args:
            delay: 每步之间的延迟时间（秒）
        """
        while not self.completed and not self.paused:
            self.step()
            time.sleep(delay)
    
    def get_duck_values(self) -> List[int]:
        """获取当前鸭子值的列表"""
        return [duck.value for duck in self.ducks]
    
    def is_sorted(self) -> bool:
        """检查鸭子列表是否已排序"""
        for i in range(len(self.ducks) - 1):
            if self.ducks[i].value > self.ducks[i + 1].value:
                return False
        return True