# 🦆 小鸭子冒泡排序可视化动画

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

一个使用Python + Tkinter开发的冒泡排序算法可视化教学工具，通过12只不同大小的小鸭子和一只大母鸭的动画演示，帮助用户直观理解冒泡排序算法的工作原理。

## ✨ 特性

- 🎨 **生动的可视化**：使用可爱的小鸭子图形表示排序元素
- 🎬 **流畅的动画**：逐步展示冒泡排序的比较和交换过程
- 🎮 **交互式控制**：支持开始、暂停、重置和速度调节
- 📊 **实时统计**：显示比较次数、交换次数和执行时间
- 🎵 **音效反馈**：为比较和交换操作添加音效（可选）
- 📝 **详细日志**：记录排序过程的每个步骤
- 🎯 **教学友好**：适合算法教学和自学

## 🚀 快速开始

### 环境要求

- Python 3.6 或更高版本
- Tkinter（通常随Python一起安装）

### 安装与运行

1. **克隆项目**

   ```bash
   git clone git clone ssh://git@ssh.github.com:443/huminglong/duck_bubble_sort.git
   cd duck-bubble-sort
   ```

2. **运行程序**

   ```bash
   python scripts/run.py
   ```

   或者使用主模块：

   ```bash
   python -m src.main
   ```

3. **开始使用**
   - 点击"开始排序"按钮观看动画演示
   - 使用速度滑块调节动画速度
   - 点击"重置"按钮重新开始

## 📖 使用指南

### 基本操作

| 操作 | 说明 |
|------|------|
| 🎬 开始排序 | 开始冒泡排序动画演示 |
| ⏸️ 暂停/继续 | 暂停或继续当前排序过程 |
| 🔄 重置 | 重新生成随机序列并重置状态 |
| ⚡ 速度调节 | 调整动画播放速度（1-10级） |
| 🔊 音效开关 | 开启或关闭操作音效 |

### 界面说明

- **主画布区域**：显示12只小鸭子和1只大母鸭
- **控制面板**：包含所有控制按钮和速度调节
- **统计信息**：实时显示比较次数、交换次数和执行时间
- **状态栏**：显示当前操作状态和提示信息

## 🏗️ 项目架构

```
duck_bubble_sort/
├── src/                    # 核心源代码
│   ├── main.py            # 主应用程序入口
│   ├── graphics.py        # 鸭子图形绘制
│   └── logger.py          # 日志系统
├── algorithms/            # 排序算法实现
│   └── bubble_sort.py     # 冒泡排序算法
├── animation/             # 动画系统
│   ├── animation_engine.py    # 动画引擎
│   ├── animators.py           # 动画效果
│   └── sort_animation_integration.py  # 排序动画集成
├── scripts/               # 启动脚本
│   ├── run.py            # 主启动脚本
│   └── run_app.py        # 应用启动脚本
├── tests/                 # 测试文件
├── docs/                  # 文档
└── logs/                  # 日志文件
```

### 核心组件

- **DuckBubbleSortApp**：主应用程序类，负责GUI界面和系统集成
- **BubbleSort**：冒泡排序算法实现，支持逐步执行和状态跟踪
- **AnimationEngine**：动画引擎，管理所有动画效果和播放控制
- **Duck系列类**：鸭子图形对象，包括小鸭子和大母鸭

## 🎯 教学价值

这个工具特别适合：

- 📚 **算法教学**：在课堂上直观演示冒泡排序的工作原理
- 🎓 **自学理解**：帮助初学者理解排序算法的执行过程
- 🔍 **代码分析**：展示算法状态管理和动画集成的实现方式
- 💡 **项目参考**：作为Python GUI和动画开发的参考项目

## 🔧 技术实现

### 关键特性

- **线程安全**：使用线程锁确保动画和排序过程的同步
- **状态管理**：完整的排序状态跟踪和恢复机制
- **动画队列**：高效的动画调度和执行系统
- **事件驱动**：基于Tkinter事件系统的用户交互处理

### 解决的技术挑战

- **线程死锁**：解决了动画线程自join导致的死锁问题
- **动画流畅性**：优化了重绘逻辑，确保动画流畅
- **状态同步**：实现了排序算法与动画状态的精确同步
- **资源管理**：合理的内存和CPU资源使用

## 🧪 测试

项目包含完整的测试套件：

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_ui.py
python tests/example_usage.py
```

## 📝 开发日志

详细的开发过程和问题解决记录请参考：

- [架构设计文档](docs/architecture_design.md)
- [问题总结](docs/问题总结.md)
- [界面优化总结](docs/界面优化总结.md)

## 🤝 贡献

欢迎提交问题报告和功能请求！如果您想贡献代码，请：

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有为算法可视化教育事业做出贡献的开发者
- 特别感谢Martin Fowler的《重构》一书提供的代码质量指导
- 感谢Tkinter社区提供的优秀GUI框架支持

---

<div align="center">
  <p>用可爱的小鸭子让算法学习变得更有趣！🦆✨</p>
</div>
