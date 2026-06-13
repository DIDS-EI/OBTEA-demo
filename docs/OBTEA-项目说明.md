# 基于人类指令的意图理解与行为树最优规划 (OBTEA)

## 一、简介

本项目提出了一个两阶段的行为树生成框架，旨在解决家庭或工业环境中机器人执行任务时对适应性和可靠性的需求。该框架利用大型语言模型（LLMs）来解释高级指令中的目标，并通过最优行为树扩展算法（OBTEA）构建高效的目标特定行为树。该框架将目标表示为一阶逻辑中的良好形式公式，有效地桥接了意图理解和最优行为规划。

本项目已发表论文，见 (IJCAI-2024) Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human instructions 

## 二、所在目录

项目文件结构如下：

```text
OBTEA-demo/
│
├─btpg/                     # 行为树生成程序的核心模块
│  ├─agent/                 # 行为树代理模块
│  ├─algos/                 # 算法实现模块
│  │  ├─bt_planning/        # 行为树规划算法（ReactivePlanning / BTExpansion / OBTEA / HOBTEA）
│  │  └─llm_client/         # 大型语言模型客户端，用于意图理解
│  ├─behavior_tree/         # 行为树结构和节点定义
│  ├─envs/                  # 环境模拟模块
│  │  ├─RobotHow/           # RobotHow 环境模拟
│  │  ├─RobotHow_Small/     # RobotHow 小规模环境模拟
│  │  ├─RoboWaiter/         # RoboWaiter 环境模拟
│  │  └─VirtualHome/        # 虚拟家庭环境模拟
│  └─utils/                 # 工具类和辅助函数
│
├─docs/                     # 文档（项目说明、HTML 版 README）
├─images/                   # README 使用的插图
├─simulators/               # 模拟环境代码（需另行下载）
├─output/                   # 所有运行生成物（btml/dot/png/svg）统一存放
│
├─test_demo/                # 自定义任务的最小可运行示例
│  └─run_demo_task.py
│
└─test_exp/                 # 测试实验模块
    ├─main.py               # 交互式演示主程序入口（easy/medium/hard）
    ├─main_VH_easy.py       # VirtualHome 简单实验
    ├─main_VH_medium.py     # VirtualHome 中等实验
    ├─main_VH_hard.py       # VirtualHome 困难实验
    └─data/                 # 测试数据存放目录
```

## 三、运行环境

- **操作系统**：支持Windows, macOS, Linux
- **Python版本**：Python 3.10或更高版本
- **依赖库**：graphviz、numpy、tabulate 

## 四、安装、运行步骤

### 1. 安装步骤：

**创建 conda 环境**

```shell
conda create --name BTPG python=3.10
conda activate BTPG
```

**安装 BTPG**

```shell
cd BTPG
pip install -e .
```

### 2. Demo 运行步骤

```shell
cd OBTEA/test_exp
python main.py
```

生成的行为树文件（`.btml` 文本，以及 `.dot`/`.png`/`.svg` 可视化）统一输出到项目根目录的 `output/` 文件夹下。


## 六、致谢

我们感谢所有使用和支持本项目的社区成员。

## 七、引用

本项目配套论文发表于 **IJCAI 2024**。如果本项目对你的研究或开发有帮助，欢迎引用：

> Xinglin Chen, Yishuai Cai, Yunxin Mao, Minglong Li, Wenjing Yang, Weixia Xu, and Ji Wang.
> **Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions.**
> In *Proceedings of the 33rd International Joint Conference on Artificial Intelligence (IJCAI)*, pages 6832–6840, 2024.

```bibtex
@inproceedings{chen2024obtea,
  title     = {Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions},
  author    = {Chen, Xinglin and Cai, Yishuai and Mao, Yunxin and Li, Minglong and Yang, Wenjing and Xu, Weixia and Wang, Ji},
  booktitle = {Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence (IJCAI)},
  pages     = {6832--6840},
  year      = {2024},
  doi       = {10.24963/ijcai.2024/755},
  url       = {https://www.ijcai.org/proceedings/2024/0755.pdf}
}
```

相关链接：[论文（IJCAI）](https://www.ijcai.org/proceedings/2024/0755.pdf) · [arXiv:2405.07474](https://arxiv.org/abs/2405.07474) · [DOI](https://doi.org/10.24963/ijcai.2024/755)

## 八、版权与许可

本项目基于 **MIT License** 开源，详见仓库根目录的 `LICENSE` 文件。

Copyright © 2024 DIDS-EI. All rights reserved.

