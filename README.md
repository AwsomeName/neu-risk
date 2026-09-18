# 神经生物学与人工学习系统研究

本项目并行研究 Transformer 架构与生物神经系统，围绕共同计算问题寻找可借鉴机制，通过架构改进降低连续感知任务中的运行能耗。原有 Hebbian 等调研作为研究材料。

**术语约定：** 本项目的“现代大模型”专指 Transformer 系列。当前已确认主线是生物启发的 Transformer 架构节能，以连续视觉环境理解为主、可结合流式 ASR，保持任务能力与实时性，先在与目标大模型结构对应的小模型上验证，再扩大规模。具体约定见 [AGENTS.md](/Users/lc/Desktop/neu-risk/AGENTS.md)。

当前目标、任务场景、方案与五阶段计划，见[研究方向讨论备忘第 13 节](/Users/lc/Desktop/neu-risk/2026-09-09-研究方向讨论备忘.md)。2026-09-10 用户已确认研究方向与阶段计划；具体任务、模型、硬件和生物机制仍待确定。备忘前文保留早期路线、VLA 及参数和功率预算讨论，不是本地实测结果。

**当前状态（2026-09-09）：** 已修订原有 12 篇文档。这里是研究资料库，尚无本地模型实现或实验复现结果；文献中的成绩不代表本项目已经验证。旧文档中的普遍能力上限、无定义百分比和缺少来源的预测已撤回或改为待核验。

## 从哪里开始

硬件约束与三年展望的当前入口：[机器人能源与端侧算力重新调研](/Users/lc/Desktop/neu-risk/2026-09-10-机器人能源与端侧算力重新调研.md)。覆盖 BYD、CATL 等主要电池路线及多类端侧计算平台，区分规格、测试、送样和路线图；以完整电池包、固定/动态计算开销重新评估 2029 年模型、载荷和续航约束。附[可复算脚本](/Users/lc/Desktop/neu-risk/research-data/robot-energy-2029/calculate.py)与[情景数据](/Users/lc/Desktop/neu-risk/research-data/robot-energy-2029/scenarios.csv)，不代表本地模型实验。

此前的[硬件约束初稿](/Users/lc/Desktop/neu-risk/2026-09-10-机器人电池载荷与端侧算力物理约束.md)和[三年预测初稿](/Users/lc/Desktop/neu-risk/2026-09-10-电池与端侧AI芯片三年回顾及2029预测.md)保留用于回溯；综合结论与数值规划以重新调研报告为准。

近期专题：[流式观测世界模型调研](/Users/lc/Desktop/neu-risk/2026-09-10-流式观测世界模型调研.md)，比较 DreamerV3、LingBot-VA 系列与 Streaming-WAM 的状态更新和闭环方式。

生物侧专题：[生物神经系统开源项目广度调研](/Users/lc/Desktop/neu-risk/2026-09-10-生物神经系统开源项目广度调研.md)，按架构、活动及仿真整理开放数据、工具和研究模型。先广度比较，尚未选定深入项目或进行复现。

1. 了解研究动机：[大脑如何学习](/Users/lc/Desktop/neu-risk/神经网络/0728-大脑是如何学习的-神经生物学给AI的启示.md)。
2. 理清基本概念：[Hebbian 入门](/Users/lc/Desktop/neu-risk/神经网络/0731-Hebbian学习理论与实验验证-v2.0.md) → [规则、架构与结构可塑性](/Users/lc/Desktop/neu-risk/Hebbian学习-学习规则vs网络架构-完整解析.md)。
3. 查证据：[生物实验笔记](/Users/lc/Desktop/neu-risk/神经网络/0731-Hebbian学习理论与实验验证.md) → [现代方法与结果](/Users/lc/Desktop/neu-risk/Hebbian学习的现代实现-专题调研.md)。
4. 准备研究或复现：[架构摘录](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构完整调研报告.md) → [记录规范](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构详细调研.md) → [待核验台账](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构补充调研.md)。

## 文档职责

| 文档 | 用途 |
|---|---|
| [研究状态](/Users/lc/Desktop/neu-risk/调研报告.md) | 已完成与尚未完成事项 |
| [研究总览](/Users/lc/Desktop/neu-risk/【已发布】生物神经网络与人工神经网络交叉研究调研报告.md) | 研究范围、主要问题与证据边界 |
| [阅读框架](/Users/lc/Desktop/neu-risk/神经网络/0728-神经生物学阅读笔记.md) | 阅读计划与问题记录 |
| [研究思路文章](/Users/lc/Desktop/neu-risk/神经网络/0728-大脑是如何学习的-神经生物学给AI的启示.md) | 从生物启发形成可检验假说 |
| [概念主文档](/Users/lc/Desktop/neu-risk/Hebbian学习-学习规则vs网络架构-完整解析.md) | 规则、架构、动力学、结构与信号来源 |
| [生物证据主文档](/Users/lc/Desktop/neu-risk/神经网络/0731-Hebbian学习理论与实验验证.md) | 实验来源、模型及解释边界 |
| [简明入口](/Users/lc/Desktop/neu-risk/神经网络/0731-Hebbian学习理论与实验验证-v2.0.md) | 入门摘要；内容版本已更新，文件名兼容旧链接 |
| [讨论层次](/Users/lc/Desktop/neu-risk/神经网络/0806-Hebbian现象vsHebbian学习-核心区分.md) | 假说、现象、模型和算法的区分 |
| [工程方法主文档](/Users/lc/Desktop/neu-risk/Hebbian学习的现代实现-专题调研.md) | 代表方法、结果来源与比较限制 |
| [架构主文档](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构完整调研报告.md) | 静态配置核对，尚非完整复现规格 |
| [实验记录规范](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构详细调研.md) | 复现和比较需记录的字段 |
| [待核验台账](/Users/lc/Desktop/neu-risk/Hebbian学习-网络架构补充调研.md) | 未解决的文献、架构和协议缺口 |

性能数字集中维护在工程方法主文档；架构尺寸集中维护在架构主文档。摘要引用主文档，避免多处复制后相互矛盾。

## 如何理解证据状态

“论文报告”“源码静态核对”“项目运行验证”分别记录；本项目尚没有第三类结果。来源存在不表示支持所有解读，代码存在不表示已经成功复现。研究设想应标明尚未验证，并说明可能的反例。

## 历史与修订

- [原文评估](/Users/lc/Desktop/neu-risk/2026-09-09-已有文档与结论评估.md)：针对修订前材料的 18 项问题；历史引用已指向快照。
- [修订记录](/Users/lc/Desktop/neu-risk/2026-09-09-文档修订记录.md)：本轮修改及验证边界。
- [修订前快照](/Users/lc/Desktop/neu-risk/历史归档/2026-09-09修订前/README.md)：原有 12 篇文档及配图，保留原始字节与校验清单，**仅用于回溯，不作为当前事实依据**。

文件名中的日期、v2.0、“完整”“已发布”等部分保留了历史命名；以正文状态为准。“已发布”文件本次仅在本地修订，未同步外部渠道。
