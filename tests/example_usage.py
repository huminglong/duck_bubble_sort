"""
小鸭子冒泡排序可视化动画项目 - 使用示例

该程序展示如何使用冒泡排序算法与鸭子图形系统集成，
包括基本用法、回调设置和状态监控。
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bubble_sort import BubbleSort
from src.graphics import BabyDuck, DuckFactory
import tkinter as tk


class MockDuck:
    """模拟鸭子类，用于演示算法逻辑（不需要图形界面）"""
    
    def __init__(self, value: int):
        self.value = value
        self.x = 0
        self.y = 0
        self.is_highlighted = False
        self.is_comparing = False
        self.is_sorted = False
    
    def move_to(self, new_x: float, new_y: float) -> None:
        """模拟移动方法"""
        self.x = new_x
        self.y = new_y
    
    def highlight(self, highlight: bool = True) -> None:
        """模拟高亮方法"""
        self.is_highlighted = highlight
    
    def set_comparing(self, comparing: bool = True) -> None:
        """模拟比较状态设置"""
        self.is_comparing = comparing
    
    def set_sorted(self, sorted: bool = True) -> None:
        """模拟排序状态设置"""
        self.is_sorted = sorted


def example_basic_usage():
    """示例1：基本用法"""
    print("=== 示例1：基本用法 ===")
    
    # 创建模拟鸭子列表
    values = [5, 2, 8, 1, 9, 3]
    ducks = [MockDuck(value) for value in values]
    
    print(f"原始序列: {[duck.value for duck in ducks]}")
    
    # 创建冒泡排序实例
    bubble_sort = BubbleSort(ducks)
    
    # 逐步执行排序
    step_count = 0
    while not bubble_sort.is_completed():
        step_count += 1
        bubble_sort.step()
        
        # 每3步打印一次状态
        if step_count % 3 == 0 or bubble_sort.is_completed():
            current_values = [duck.value for duck in ducks]
            progress = bubble_sort.get_progress()
            print(f"步骤 {step_count}: {current_values} (进度: {progress:.1%})")
    
    print(f"排序完成! 最终序列: {[duck.value for duck in ducks]}")
    print(f"总比较次数: {bubble_sort.get_comparisons_count()}")
    print(f"总交换次数: {bubble_sort.get_swaps_count()}")
    print()


def example_with_callbacks():
    """示例2：使用回调函数"""
    print("=== 示例2：使用回调函数 ===")
    
    # 创建模拟鸭子列表
    values = [4, 7, 2, 5, 1, 3]
    ducks = [MockDuck(value) for value in values]
    
    print(f"原始序列: {[duck.value for duck in ducks]}")
    print("排序过程:")
    
    # 定义回调函数
    def on_compare(index1, index2):
        duck1, duck2 = ducks[index1], ducks[index2]
        duck1.set_comparing(True)
        duck2.set_comparing(True)
        print(f"  比较: 鸭子{index1}(值{duck1.value}) 和 鸭子{index2}(值{duck2.value})")
    
    def on_swap(index1, index2):
        duck1, duck2 = ducks[index1], ducks[index2]
        duck1.set_comparing(False)
        duck2.set_comparing(False)
        duck1.highlight(True)
        duck2.highlight(True)
        print(f"  交换: 鸭子{index1}(值{duck1.value}) 和 鸭子{index2}(值{duck2.value})")
        
        # 短暂延迟以观察效果
        time.sleep(0.1)
        
        duck1.highlight(False)
        duck2.highlight(False)
    
    def on_complete():
        print("  排序完成!")
        # 标记所有鸭子为已排序
        for duck in ducks:
            duck.set_sorted(True)
    
    # 创建冒泡排序实例并设置回调
    bubble_sort = BubbleSort(ducks)
    bubble_sort.set_callbacks(
        on_compare=on_compare,
        on_swap=on_swap,
        on_complete=on_complete
    )
    
    # 执行排序
    while not bubble_sort.is_completed():
        bubble_sort.step()
    
    print(f"最终序列: {[duck.value for duck in ducks]}")
    print()


def example_pause_resume():
    """示例3：暂停和继续功能"""
    print("=== 示例3：暂停和继续功能 ===")
    
    # 创建模拟鸭子列表
    values = [9, 5, 2, 7, 1, 4, 3]
    ducks = [MockDuck(value) for value in values]
    
    print(f"原始序列: {[duck.value for duck in ducks]}")
    
    # 创建冒泡排序实例
    bubble_sort = BubbleSort(ducks)
    
    # 执行几步
    print("执行前5步:")
    for i in range(5):
        if bubble_sort.step():
            current_values = [duck.value for duck in ducks]
            print(f"  步骤{i+1}: {current_values}")
    
    # 暂停
    bubble_sort.pause()
    print(f"\n暂停状态: {bubble_sort.is_paused()}")
    
    # 尝试继续执行（应该被忽略）
    print("尝试在暂停状态下执行3步:")
    for i in range(3):
        result = bubble_sort.step()
        print(f"  步骤{i+6}: 执行结果={result}")
    
    # 恢复并继续执行
    bubble_sort.resume()
    print(f"\n恢复后暂停状态: {bubble_sort.is_paused()}")
    print("继续执行直到完成:")
    
    step_count = 0
    while not bubble_sort.is_completed():
        step_count += 1
        if bubble_sort.step():
            current_values = [duck.value for duck in ducks]
            print(f"  步骤{step_count}: {current_values}")
    
    print(f"最终序列: {[duck.value for duck in ducks]}")
    print()


def example_state_monitoring():
    """示例4：状态监控"""
    print("=== 示例4：状态监控 ===")
    
    # 创建模拟鸭子列表
    values = [6, 3, 8, 2, 5, 1, 7, 4]
    ducks = [MockDuck(value) for value in values]
    
    print(f"原始序列: {[duck.value for duck in ducks]}")
    
    # 创建冒泡排序实例
    bubble_sort = BubbleSort(ducks)
    
    # 监控排序过程
    print("排序过程监控:")
    step_count = 0
    while not bubble_sort.is_completed():
        step_count += 1
        bubble_sort.step()
        
        # 每隔几步打印详细状态
        if step_count % 4 == 0 or bubble_sort.is_completed():
            current_values = [duck.value for duck in ducks]
            comparison = bubble_sort.get_current_comparison()
            swap = bubble_sort.get_current_swap()
            sorted_indices = bubble_sort.get_sorted_indices()
            progress = bubble_sort.get_progress()
            
            print(f"步骤 {step_count}:")
            print(f"  当前序列: {current_values}")
            print(f"  当前比较: {comparison}")
            print(f"  当前交换: {swap}")
            print(f"  已排序索引: {sorted_indices}")
            print(f"  进度: {progress:.1%}")
            print(f"  比较次数: {bubble_sort.get_comparisons_count()}")
            print(f"  交换次数: {bubble_sort.get_swaps_count()}")
            print()
    
    print(f"排序完成! 最终序列: {[duck.value for duck in ducks]}")
    print()


def example_with_real_ducks():
    """示例5：与真实鸭子对象集成（需要图形界面）"""
    print("=== 示例5：与真实鸭子对象集成 ===")
    
    try:
        # 创建Tkinter窗口（但不显示）
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 创建画布
        canvas = tk.Canvas(root, width=800, height=200)
        
        # 创建真实的小鸭子（12只，按项目要求）
        values = [8, 3, 5, 2, 9, 1, 7, 4, 6, 11, 10, 12]
        ducks = DuckFactory.create_baby_ducks(canvas, 50, 100, 60, values)
        
        print(f"原始序列: {values}")
        print("开始排序...")
        
        # 定义回调函数
        def on_compare(index1, index2):
            ducks[index1].set_comparing(True)
            ducks[index2].set_comparing(True)
        
        def on_swap(index1, index2):
            ducks[index1].set_comparing(False)
            ducks[index2].set_comparing(False)
            ducks[index1].highlight(True)
            ducks[index2].highlight(True)
            
            # 短暂延迟以观察效果
            time.sleep(0.05)
            
            ducks[index1].highlight(False)
            ducks[index2].highlight(False)
        
        def on_complete():
            for duck in ducks:
                duck.set_sorted(True)
            print("排序完成!")
        
        # 创建冒泡排序实例并设置回调
        bubble_sort = BubbleSort(ducks)
        bubble_sort.set_callbacks(
            on_compare=on_compare,
            on_swap=on_swap,
            on_complete=on_complete
        )
        
        # 执行排序
        while not bubble_sort.is_completed():
            bubble_sort.step()
        
        # 检查结果
        sorted_values = [duck.value for duck in ducks]
        print(f"排序后序列: {sorted_values}")
        print(f"排序正确: {sorted_values == sorted(values)}")
        print(f"总比较次数: {bubble_sort.get_comparisons_count()}")
        print(f"总交换次数: {bubble_sort.get_swaps_count()}")
        
        # 清理
        root.destroy()
        
    except Exception as e:
        print(f"测试真实鸭子对象时出错: {e}")
        print("这可能是由于缺少图形环境，但算法逻辑仍然正确。")
    
    print()


def main():
    """主函数，运行所有示例"""
    print("小鸭子冒泡排序算法使用示例")
    print("=" * 50)
    
    # 运行所有示例
    example_basic_usage()
    example_with_callbacks()
    example_pause_resume()
    example_state_monitoring()
    example_with_real_ducks()
    
    print("=" * 50)
    print("所有示例运行完成!")
    print("\n使用说明:")
    print("1. 创建鸭子对象列表（每个鸭子必须有value属性）")
    print("2. 创建BubbleSort实例: bubble_sort = BubbleSort(ducks)")
    print("3. 可选：设置回调函数来处理比较、交换和完成事件")
    print("4. 逐步执行: bubble_sort.step()")
    print("5. 检查状态: bubble_sort.is_completed(), bubble_sort.get_progress() 等")
    print("6. 控制执行: bubble_sort.pause(), bubble_sort.resume(), bubble_sort.reset()")


if __name__ == "__main__":
    main()