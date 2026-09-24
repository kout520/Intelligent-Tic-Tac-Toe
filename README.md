# Intelligent-Tic-Tac-Toe · 智能井字棋
> **OpenMV 视觉识别 + Minimax AI 下棋 + STM32 步进电机落子** 的智能井字棋系统 —— OpenMV 实时识别棋盘局面，AI 决策落子，STM32 驱动步进电机自动摆棋，实现全自动人机对弈！
[![OpenMV](https://img.shields.io/badge/Vision-OpenMV-blue.svg)](https://openmv.io/)
[![STM32](https://img.shields.io/badge/MCU-STM32F103%20HAL-green.svg)](https://www.st.com/)
[![AI](https://img.shields.io/badge/AI-Minimax-orange.svg)]()

---
## 📖 项目简介
本项目是一套**智能井字棋（人机对弈）**系统，采用 **双端协同** 架构：

- **视觉 + AI 决策端（OpenMV）**：`main.py` 通过摄像头实时识别 3×3 棋盘上的棋子分布（基于 ROI 灰度统计检测），`chess.py` 内置 **Minimax 极小化极大** AI 算法计算最优落子，再经串口把落子位置下发给主控。
- **主控执行端（STM32F103VCT6 · HAL）**：`A_SZQ/` 为 STM32CubeMX 工程，接收 OpenMV 下发的落子坐标，通过 **步进电机（PWM 驱动）** 自动将棋子摆放到指定棋盘格，并 OLED 实时显示状态。

系统支持 **玩家先手 / AI 先手** 两种模式，AI 具备完整的胜负判断（胜 / 平 / 负）与最优策略，配合步进电机机械落子，实现全自动的井字棋对弈体验。✨

---
## ✨ 核心特性
- 🤖 **Minimax AI 决策**：极小化极大算法 + 深度搜索，AI 永不失误，先手首步即占中心
- 👁️ **OpenMV 棋子识别**：9 宫格 ROI + 子 ROI 灰度统计，多帧多数投票提升识别鲁棒性
- ⚙️ **步进电机自动落子**：STM32 接收落子坐标，PWM 驱动步进电机移动到目标格摆放棋子
- 🖥️ **OLED 状态显示**：实时显示落子位置 / 对弈状态
- 📡 **UART 双端通信**：OpenMV（UART3 115200）⇄ STM32（USART1）串口协议下发落子
- 🎮 **双模式对弈**：AI 先手（执 X）/ 玩家先手（执任意色）可切换

---
## 🧩 已集成模块清单
### 👁️ OpenMV 视觉与 AI（根目录）
| 文件 | 功能说明 |
| :--- | :--- |
| main.py | 主程序：摄像头棋子识别、多数投票、对弈状态机、串口下发落子 |
| chess.py | 井字棋 AI：胜负/平局判断、Minimax 极小化极大算法、落子决策 |
| qz_find.py | 棋子识别：9 宫格 ROI 与子 ROI 定义、灰度统计判棋子有无 |

### ⚙️ STM32F103VCT6 主控（A_SZQ/）
| 模块名称 | 功能说明 | 接口 |
| :--- | :--- | :--- |
| bj_motor | 步进电机驱动（速度 / 距离 / 步进回调） | PWM/TIM |
| oled | OLED 显示（落子位置 / 状态） | I2C2 |
| UserUsart1 | USART1 通信（接收 OpenMV 落子指令） | USART1 |
| fun | 落子坐标控制（lcd_show / black_points / QZ_points） | —— |
| font | 字库数据 | —— |

---
## 🚀 快速上手
### 1. 环境要求
- **视觉端**：OpenMV Cam（H7），MicroPython
- **主控**：STM32F103VCT6，STM32CubeMX + Keil MDK（HAL 库）
- **执行机构**：步进电机 + 驱动（PWM 控制）

### 2. 部署步骤
1.  克隆本仓库到本地：
    ```bash
    git clone https://github.com/kout520/Intelligent-Tic-Tac-Toe.git
    ```
2.  **OpenMV 端**：用 OpenMV IDE 打开 `main.py`，把 `chess.py`、`qz_find.py` 一起放到 SD 卡，连接 OpenMV 摄像头运行
3.  **STM32 端**：用 STM32CubeMX 打开 `A_SZQ/A_SZQ.ioc`，或直接用 Keil 打开 `A_SZQ/MDK-ARM/` 工程，编译烧录到 STM32F103VCT6
4.  接线：OpenMV（UART3）⇄ STM32（USART1）波特率一致（115200），步进电机 PWM 接到对应定时器通道
5.  上电对弈：OpenMV 识别局面 → AI 算落子 → 串口下发 → STM32 步进电机摆棋 → 循环直到分出胜负

### 3. 对弈流程
```
OpenMV 识别棋盘 → 判读当前局面 → chess.minimax 计算 AI 最优落子
        │
        ▼  UART 下发落子坐标
STM32 步进电机移动到目标格 → 摆放棋子
        │
        ▼  循环
OpenMV 重新识别 → 判断胜负/平局 → 结束或继续
```
- 模式切换：`flag = 1`（AI 先手执 X）/ `flag = 2`（玩家先手）在 `main.py` 中设置

---
## 📂 项目结构
```
Intelligent-Tic-Tac-Toe/
├── main.py                # OpenMV 主程序（识别 + 对弈状态机 + 串口下发）
├── chess.py               # 井字棋 AI（Minimax 极小化极大）
├── qz_find.py             # 棋子识别（ROI 灰度统计）
├── A_SZQ/                 # STM32F103VCT6 主控（CubeMX）
│   ├── A_SZQ.ioc          # STM32CubeMX 工程配置
│   ├── code/              # 业务模块（bj_motor / oled / UserUsart1 / fun / font）
│   ├── Core/  Drivers/    # 主程序、HAL 驱动
│   └── MDK-ARM/           # Keil MDK 工程
└── README.md              # 项目说明文档
```

---
## 📄 开源协议
本项目**未指定开源许可证**，如需对外开源请自行添加 `LICENSE` 文件。

---
## 🎉 致谢
感谢 OpenMV 与 STMicroelectronics 提供的优秀开发平台，祝各位在电子设计竞赛中取得优异成绩！
---
