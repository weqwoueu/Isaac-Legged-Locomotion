# 🤖 Isaac-Legged-Locomotion
> 基于 NVIDIA Isaac Lab 的足式机器人（人形/四足）端到端强化学习控制与抗扰动部署

![Isaac Lab](https://img.shields.io/badge/NVIDIA-Isaac_Lab-76B900?logo=nvidia)
![RL](https://img.shields.io/badge/RL-RSL__RL-0052CC)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch)
![Hardware](https://img.shields.io/badge/Hardware-Unitree_G1_|_H1_|_Go1-red)

## 📖 项目简介
足式机器人（尤其是双足人形机器人）属于典型的高维度、强欠驱动（Underactuated）、非线性动态系统。传统基于精确模型的控制算法在面对复杂地形和外部扰动时极易发散崩溃。

本项目基于 **NVIDIA Omniverse / Isaac Lab** 大规模并行张量仿真框架，针对目前工业界最前沿的足式平台（**Unitree G1/H1 人形机器人, Unitree Go1 / ANYmal-C 机器狗**）进行了强化学习 (PPO) 步态策略的从零训练。项目深度介入了**域随机化 (Domain Randomization)** 与 **面向硬件的奖励塑形 (Hardware-Aware Reward Shaping)**，成功实现了机器人无需视觉输入、仅靠本体感觉（Proprioception）即可在崎岖地形（Rough Terrain）与极限冰面下保持动态平衡的鲁棒控制。

## 🎬 核心成果演示 (Demos)

### 🚶 1. 人形双足机器人和机器狗崎岖地形行走 
| Unitree Go1 复杂崎岖地形越野 (Rough Terrain) | Unitree H1 全尺寸人形崎岖地形盲走 |
| :---: | :---: |
| <img src="docs/gif/unitree_go1_rough_chase.gif" width="400"> | <img src="docs/gif/h1_rough.gif" width="400"> |
| **难点**: 极小支撑多边形、高质心动态平衡 | **难点**: 全尺寸大惯量、无视觉地形自适应 |

### 🐕 2. 四足机器人抗扰动与大规模并行 (Quadruped Robustness)
| Unitree Go1 冰面极限打滑求生 ($\mu=0.1$) | ANYmal-C 大规模张量化并行训练阵列 |
| :---: | :---: |
| <img src="docs/gif/unitree_go1_flat_ice_r_v.gif" width="400"> | <img src="docs/gif/unitree_go1_rough.gif" width="400"> |
| **技术点**: 极低附着力、涌现高频代偿碎步 | **技术点**: GPU Zero-Copy, 4096 并行宇宙 |

## 🛠️ 技术深度与工程突破

### 1. 人形机器人的时序信用分配与欠驱动控制
- 针对 G1/H1 人形机器人重心极高、支撑面积极小的物理特性，优化了 `base_orientation_penalty`（躯干姿态惩罚）和 `feet_air_time`（脚部离地时间）的 Reward 权重。
- 克服了双足模型在复杂地形下极易陷入局部最优（原地死站）的难题，成功涌现出稳定的交替迈步与动态平衡恢复能力。

### 2. 极端域随机化 (Extreme Domain Randomization)
- 为弥合 Sim-to-Real Gap，在底层 `env_cfg` 中注入严苛的物理约束突变。
- **低附着力极限测试**: 将 Go1 所在环境的地面摩擦系数随机下限突破至极端的 $\mu \in[0.1, 0.2]$（模拟结冰路面）。策略网络自主舍弃大跨步，涌现 (Emergence) 出高频碎步 (High-frequency Trotting) 以维持质心 (CoM) 投影。

### 3. 面向机械硬件寿命的奖励重构 (Hardware-Aware Reward)
- 发挥机械动力学专业优势，拒绝“只要跑得快就行”的盲目优化。在 Reward 函数中深度耦合了硬件物理极限：
- 增加对 `dof_torques_l2` (关节输出扭矩峰值) 与 `action_rate_l2` (高频控制指令震荡) 的二次项惩罚。
- **工程意义**：强制网络输出平滑的 PD 控制器目标角度，**最大化保护真实机器人的减速器与电机驱动板免受过载烧毁**，大幅提升实机部署（Deployment）的可行性。

### 4. HPC 超算容器化极速部署
- 突破超算节点权限与底层驱动限制，利用 Apptainer 虚拟化技术，手动注入 Vulkan 与 NVIDIA GLX 动态库，打通无头模式 (Headless) 物理渲染链路。
- 在双 RTX 4090 算力节点上开启大规模并行宇宙，将百万步交互数据收集压缩至分钟级。

## 📂 核心代码目录
Isaac-Legged-Locomotion/
├── custom_configs/          # 自定义配置文件目录，包含不同机器人的环境配置和部署脚本
│   ├── config/              # 机器人环境配置文件
│   └── deploy_scripts/      # 部署相关的脚本文件
├── docs/                    # 文档与演示资源目录
│   ├── gif/                 # GIF 格式的演示文件
│   └── video/               # MP4 格式的演示视频
├── trained_models/          # 预训练模型权重文件目录
└── README.md                # 项目说明文档





