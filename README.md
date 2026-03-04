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

## 📂 核心代码目录 (Repository Structure)

本仓库采用**补丁包（Patch Workspace）**结构，仅包含核心的魔改配置、环境初始化脚本以及预训练好的神经网络权重，以便于无缝嵌入标准的 Isaac Lab 官方框架中：

```text
Isaac-Legged-Locomotion/
├── custom_configs/                 # 核心物理法则与奖励函数重塑 (Core RL Configs)
│   ├── config/                     # 各机型专属配置 (Robot-specific Configs)
│   │   ├── anymal_c/
│   │   │   └── flat_env_cfg.py     # ANYmal-C：大规模并行阵列与基础速度追踪
│   │   ├── go1/
│   │   │   ├── flat_env_cfg.py     # 宇树 Go1：冰面打滑极限测试 ($\mu=0.1$) 与无人机跟拍视角
│   │   │   └── rough_env_cfg.py    # 宇树 Go1：崎岖地形越野与暴力飞踢抗扰动
│   │   └── h1/
│   │       └── rough_env_cfg.py    # 宇树 H1：全尺寸人形双足机器人复杂地形自适应
│   └── velocity_env_cfg.py         # 【基类配置】注入硬件寿命保护（极高频震荡惩罚与关节扭矩限幅）
├── deploy_scripts/                 # 底层环境急救脚本 (DevOps & HPC)
│   ├── init_vulkan_535.146.02.sh   # 突破 HPC 容器权限，针对 535 驱动的 Vulkan 注入脚本
│   └── init_vulkan_550.142.sh      # 针对 550 驱动的 Vulkan 注入脚本
├── docs/                           # 演示素材
│   ├── gif/                        # README 核心展示动图
│   └── video/                      # 完整版高帧率仿真录像 (.mp4)
├── trained_models/                 # 经 RTX 4090 阵列并行训练得到的高鲁棒性策略权重 (.pt)
│   ├── anymal_c_flat.pt
│   ├── h1_rough.pt
│   ├── unitree_go1_flat.pt
│   └── unitree_go1_rough.pt
└── README.md
```
## 🚀 快速复现指南 (How to Run & Reproduce)

本仓库采用 **“补丁包 (Patch Workspace)”** 模式组织。请在标准 Isaac Lab 环境下，注入本仓库的配置即可复现全部极限抗扰动效果。

### 1. 基础环境准备 (Prerequisites)
- 请参考官方文档完成 [Isaac Lab (v1.0+)](https://github.com/isaac-sim/IsaacLab) 的安装。
- **HPC/云容器适配**：若在受限的 Docker/Apptainer 节点中出现 Vulkan 驱动丢失或 OOM 报错，请以 `root` 权限执行本仓库提供的急救脚本，强行挂载 NVIDIA 图形渲染管线：
- 目前只支持显卡驱动版本535.146.02和550.142使用前请先查看版本是否对应
  ```bash
  bash deploy_scripts/init_vulkan_550.142.sh(或init_vulkan_535.146.02.sh)
  
### 2. 注入核心配置 (Inject Custom Configs)
- 将本仓库 custom_configs/ 下的文件，覆盖至 Isaac Lab 源码的对应目录：
- 通用配置类：
- 将 velocity_env_cfg.py 覆盖至 source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/
  机型专属配置 (如 Go1, G1, H1)：
- 将 go1_flat_env_cfg.py 等覆盖至 .../velocity/config/go1/flat_env_cfg.py

### 3. 部署预训练模型 (Play Pre-trained Policy)
- 将 trained_models/ 目录下的权重文件（如 unitree_go1_rough.pt）放置于 Isaac Lab 的 logs/rsl_rl/... 目录下，并运行推演脚本（带无人机跟拍运镜）即可生成视频：
code
Bash
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Rough-Unitree-Go1-v0 \
    --num_envs 1 \
    --headless \
    --video \
    --video_length 1000
    
- (注：运行结束后，视频将自动保存在对应 logs 目录下的 videos/ 文件夹中。)

 ## 📬 Contact & Resume
- liuzijian0801@163.com
- 这是本人的具身智能算法实战项目。欢迎各位同仁交流讨论，若对底层动力学控制或 RL 落地感兴趣，期待与您在面试中深入探讨！










