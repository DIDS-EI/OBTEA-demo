# 基于人类指令的意图理解与行为树最优规划 (OBTEA)

## 一、简介

本项目提出了一个两阶段的行为树生成框架，旨在解决家庭或工业环境中机器人执行任务时对适应性和可靠性的需求。该框架利用大型语言模型（LLMs）来解释高级指令中的目标，并通过最优行为树扩展算法（OBTEA）构建高效的目标特定行为树。该框架将目标表示为一阶逻辑中的良好形式公式，有效地桥接了意图理解和最优行为规划。

本项目已发表论文，见 (IJCAI-2024) Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human instructions 

## 二、所在目录

项目文件结构如下：

```text
# OBTEA/
│
├─btpg/            # 行为树生成程序的核心模块
│  ├─agent/        # 行为树代理模块
│  ├─algos/         # 算法实现模块
│  │  ├─bt_planning/       # 行为树规划算法
│  │  └─llm_client/         # 大型语言模型客户端，用于意图理解
│  ├─behavior_tree/         # 行为树结构和节点定义
│  ├─envs/                 # 环境模拟模块
│  │  ├─RobotHow/           # RobotHow环境模拟
│  │  ├─RobotHow_Small/      # RobotHow小规模环境模拟
│  │  ├─RoboWaiter/         # RoboWaiter环境模拟
│  │  └─VirtualHome/        # 虚拟家庭环境模拟
│  └─utils/                # 工具类和辅助函数
│
├─simulators/        # 模拟环境代码
│
└─test_exp/          # 测试实验模块
    ├─main.py        # 测试实验主程序入口
    ├─data/          # 测试数据存放目录
    └─outputs/       # 测试结果和输出文件存放目录
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

输出的 BT 文件以 ptml 格式 和 pdf 格式分别输出在 outputs 文件架下。

## 五、联系方式（邮箱）

如果您有任何问题或建议，请通过以下邮箱联系我们：

- **技术支持**：caiyishuai@nudt.edu.cn
- **原论文主要作者**：chenxinglin@nudt.edu.cn ，caiyishuai@nudt.edu.cn

## 六、致谢

我们感谢所有使用和支持本项目的社区成员。





