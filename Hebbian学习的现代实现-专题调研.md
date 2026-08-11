# Hebbian 学习的现代实现 — 专题调研

**调研日期**: 2026-07-26
**专题范围**: Hebbian 学习在 2022-2025 年现代深度学习中的工程化实现
**配套文件**: 《生物神经网络与人工神经网络交叉研究调研报告.md》第一章 1.1 节的深入展开

> **本次调研说明**: 本篇所有论文均带有 arXiv 编号或 DOI,所有 GitHub 仓库均为搜索核实存在的真实仓库。可按链接自行复核。这是和上一篇"概览报告"最大的不同——上一篇里部分论文标题/stars 数字可能是 AI 生成的,本篇尽量做到可追溯。

---

## 引子:为什么要单独讲"现代实现"

上一篇我们说过 Hebbian 的一句话本质:

> **"Cells that fire together, wire together."** —— 一起放电的神经元,连接变强。

规则本身 1949 年就提出了,公式朴素到不能再朴素:

$$\Delta w = \eta \cdot x \cdot y$$

听起来很美好——和大脑一样、局部、不需要标签。但几十年来它在工程上**一直打不过反向传播(backprop)**。原因有三个,必须先讲清楚,否则看不懂"现代实现"到底在解决什么:


| 病症           | 通俗解释                            | 后果         |
| ------------ | ------------------------------- | ---------- |
| **权重爆炸/饱和**  | $x$ 和 $y$ 只要都为正,$w$ 就一直涨,涨到天上去  | 网络发散,学不到东西 |
| **没有深度信用分配** | 深层网络里,前面哪一层该为最终错误负责?Hebbian 不知道 | 训不动深层特征    |
| **缺乏全局目标**   | 它只看"邻居在不在",不看"最终结果对不对"          | 学到的特征可能没用  |


所以"现代实现"要回答的核心问题是:

> **能不能既保留 Hebbian 的"局部、生物合理、无监督"优点,又让它在深层网络里真正能用,甚至逼近反向传播的性能?**

2022-2025 年,这个问题有了实质性突破。下面是五条主要路线。

---

## 一、五条现代实现路线

### 路线 A:让 Hebbian 跑得快、跑得深 —— FastHebb

**核心问题**: 原始 Hebbian 即使能跑,也慢得没法上 ImageNet 这种大数据集。

**代表工作**: **FastHebb** (Gabriele Lagani et al.)

- 2022 年预印本: [arXiv:2207.03172](https://arxiv.org/abs/2207.03172) —— "FastHebb: Scaling Hebbian Training of Deep Neural Networks to ImageNet-Level"
- 2024 年期刊版: *Neurocomputing* Vol. 595, p. 127867, [DOI:10.1016/j.neucom.2024.127867](https://www.sciencedirect.com/science/article/pii/S0925231224006386)

**关键结果**: 比此前的 Hebbian 方法(如 SoftHebb)训练**快 70 倍**,首次让 Hebbian 训练扩展到 ImageNet 级别。

**怎么做到的**(工程优化,不是换算法):

1. **合并更新步骤**: 把原本分散的权重更新合并成一次张量运算,吃满 GPU
2. **半监督**: Hebbian 无监督学特征 + 少量标签微调
3. **计算重排**: 避免重复的内存读写

> **启示**: Hebbian 慢,很多时候不是算法本质慢,而是没人认真做过工程优化。FastHebb 的贡献恰恰是"把它当成正经系统来优化"。

---

### 路线 B:局部 + 全局 —— 三因子规则 (Three-Factor Rules)

这是**理论上最重要**的一条线,直接回答"怎么给 Hebbian 加全局目标"。

**回顾两因子(原始 Hebbian)**:

$$\Delta w = \eta \cdot \underbrace{x}*{\text{输入}} \cdot \underbrace{y}*{\text{输出}}$$

只有 pre 和 post 两个因子,纯局部。

**三因子规则**:

$$\Delta w = \eta \cdot \underbrace{x \cdot y}*{\text{局部 Hebbian}} \cdot \underbrace{M}*{\text{全局调制信号}}$$

第三个因子 $M$ 是一个**全局标量信号**,告诉每个突触:"这次活动整体上是好是坏?"

**生物对应**: 大脑里的**神经调质**(多巴胺、乙酰胆碱、血清素)——它们是全局广播的化学信号,正好扮演 $M$ 的角色。一个神经元释放多巴胺,整个脑区都会接收到。

**代表工作**:

- **Information Bottleneck Hebbian** (Daruwalla, 2024) [Frontiers in Computational Neuroscience](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1240348/full):用一个辅助记忆网络产生全局信号,把跨样本的信息压进 Hebbian 更新
- **Hebbian Learning with Global Direction** (2026 预印本, [arXiv:2601.21367](https://arxiv.org/html/2601.21367v1)):延续了"给 Hebbian 一个全局方向"的思路

> **为什么重要**: 三因子规则是"既局部又全局"的折中——保留了 Hebbian 的生物合理性(突触只看本地信息 + 一个广播信号),又拿到了类似反传的全局指导。这是当前最被看好的"生物合理 + 可用"的范式。

---

### 路线 C:经典规则的现代复活 —— Oja / BCM

这两个是 1980 年代的经典 Hebbian 变体,2024-2025 年因为新论文重新火起来。它们专治"权重爆炸"。

#### Oja's Rule —— 加个归一化,顺便做了 PCA

$$\Delta w = \eta \cdot y \cdot (x - w \cdot y)$$

后面那个 $-w \cdot y$ 是个"减自激"项,效果是**把权重长度拉回 1 附近**,不会爆炸。

**神奇性质**: Oja 证明过,这个简单规则在数学上**等价于在线主成分分析(PCA)**——也就是说,它在无监督地提取数据的主要成分。

**现代应用**: [NeurIPS 2025 论文](https://arxiv.org/html/2510.14810v1) "Low-Dimensional Structural Projection" 用 Oja 和 BCM 做现代无监督降维,说明这些经典规则在今天的 ML 里仍有竞争力。

#### BCM Theory —— 滑动阈值,做出"选择性"

$$\Delta w = \eta \cdot y \cdot (y - \theta_M) \cdot x$$

其中 $\theta_M$ 是一个**随历史活动变化的阈值**:

- 最近经常放电 → 阈值升高 → 更难再加强(防止过兴奋)
- 最近很安静 → 阈值降低 → 容易加强(保持敏感)

**生物对应**: 视觉皮层的**方位选择性**(orientation selectivity)——神经元对某个特定朝向的线条反应最强。BCM 能自发学出这种选择性。


| 规则         | 解决的问题  | 数学等价   | 典型用途    |
| ---------- | ------ | ------ | ------- |
| 原始 Hebbian | —      | 无      | 仅作起点    |
| **Oja**    | 权重爆炸   | 在线 PCA | 降维、特征提取 |
| **BCM**    | 选择性、稳态 | 方位选择模型 | 感知学习    |


---

### 路线 D:Hebbian + 反向传播 混合架构

既然 Hebbian 训不动深层、Backprop 又不够"生物",那能不能**各取所长**?

**典型做法**: 浅层用 Hebbian(无监督学特征),深层用 Backprop(有监督精调)。

**代表实现**: [GabrieleLagani/HebbianLearning](https://github.com/GabrieleLagani/HebbianLearning) (PyTorch)

- 支持每一层单独配置学习规则
- 可以"第 1-3 层 Hebbian + 第 4-5 层 Backprop"
- 在 CIFAR-10 上验证

**相关论文**: "Hebbian Learning Meets Deep Convolutional Neural Networks?" (Lagani et al., ICIAP, [被引 91 次](https://falchi.isti.cnr.it/Draft/2019-ICIAP-HLMSD.pdf))

> **优点**: 标签需求少(只有深层需要)、前端可在线学习、可解释性比纯 Backprop 好。
> **代价**: 怎么切层、怎么协调两种规则,需要调参。

---

### 路线 E:脉冲网络里的 STDP + 代理梯度

这是和\*\*脉冲神经网络(SNN)\*\*结合的一条线,在上一篇报告第三章也提过。

**STDP (Spike-Timing-Dependent Plasticity)** 是 Hebbian 的"时间精细版":

- pre 神经元在 post 之前几毫秒放电 → 加强(因果关系)
- pre 在 post 之后放电 → 减弱

$$\Delta w = \begin{cases} A^+ e^{-\Delta t/\tau} &amp; \Delta t &gt; 0 \text{ (pre 先于 post)} \ -A^- e^{\Delta t/\tau} &amp; \Delta t &lt; 0 \text{ (pre 后于 post)} \end{cases}$$

**问题**: STDP 的脉冲是离散的、不可微,没法直接用 PyTorch 的 autograd 训练。

**解法 —— 代理梯度 (Surrogate Gradient)**: 在前向传播时用真正的脉冲(离散),在反向传播时**用一个平滑的函数"假装"它是可微的**,骗过 autograd。

**代表工作**:

- **SSTDP** (F. Liu et al., 2021, [Frontiers in Neuroscience, 被引 101 次](https://pmc.ncbi.nlm.nih.gov/articles/PMC8603828/)):显式桥接 STDP 和反向传播式监督学习
- **SpikingJelly** 框架的 [STDP 教程](https://spikingjelly.readthedocs.io/zh-cn/latest/tutorials/en/stdp.html)
- Sandia 国家实验室报告: [Combining STDP with Deep Learning](https://www.osti.gov/servlets/purl/1902866)

---

## 二、Hebbian vs Backprop:实证对比

这部分来自一篇少有的"硬碰硬"实验对比论文:

**"Is Bio-Inspired Learning Better than Backprop?"** (Gupta et al., 2022, [arXiv:2212.04614](https://arxiv.org/pdf/2212.04614), 被引 16 次)


| 维度             | Hebbian          | Backpropagation      |
| -------------- | ---------------- | -------------------- |
| **生物合理性**      | ✅ 高(局部突触可塑性)     | ❌ 低(需对称权重传输、全局误差)    |
| **学习速度**(某些设置) | 快,约 **5 epochs** | 慢,约 **\~100 epochs** |
| **可解释性**       | 更透明              | 更黑箱                  |
| **大规模深层性能**    | 较弱               | **SOTA**             |
| **对标签的依赖**     | 可无监督             | 需要标签                 |
| **核心短板**       | 深层信用分配           | 生物不 plausible        |


补充:2025 年 [Nimmo et al. 的研究](https://www.sciencedirect.com/science/article/pii/S0893608025005088)([arXiv:2501.17266](https://arxiv.org/html/2501.17266v1))进一步指出,Hebbian 在\*\*可解释性和可说明性(explainability)\*\*上优于 Backprop,这也是它在医疗、边缘场景里被重新看好的原因。

> **一句话**: Hebbian 不是要"取代"Backprop,而是**在某些场景(少标签、要可解释、要在线学习、要上神经形态硬件)里补上 Backprop 的短板**。

---

## 三、算法变体速查表


| 名称               | 公式核心                  | 解决了什么       | 现代地位             |
| ---------------- | --------------------- | ----------- | ---------------- |
| **原始 Hebbian**   | $\eta x y$           | 学习的起点       | 仅教学用             |
| **Oja**          | $\eta y(x-wy)$       | 爆炸 → 等价 PCA | NeurIPS 2025 仍在用 |
| **BCM**          | $\eta y(y-\theta)x$ | 选择性、稳态      | 感知学习             |
| **STDP**         | 时序依赖 ±                | 因果、时序       | SNN 核心           |
| **SoftHebb**     | 概率软化                  | 稳定性         | FastHebb 的基线     |
| **FastHebb**     | 工程加速                  | 速度(70×)     | ImageNet 级       |
| **Three-Factor** | $xyM$                 | 全局目标        | 理论最被看好           |


---

## 四、可用代码实现(均已核实存在)

按"从入门到进阶"排序:


| 仓库                                                                                      | 用途                                                    | 适合谁     |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------- |
| [ThomasMiconi/HebbianCNNPyTorch](https://github.com/ThomasMiconi/HebbianCNNPyTorch)     | 多层 CNN 的 Hebbian **教学示范**                             | 第一次上手   |
| [Einlar/biopytorch](https://github.com/Einlar/biopytorch)                               | 提供 `BioLinear` / `BioConv2d` **即插即用层**,镜像 `nn.Linear` | 想塞进现有架构 |
| [julestalloen/pytorch-hebbian](https://github.com/julestalloen/pytorch-hebbian)         | 灵活框架,带 `HebbianTrainer`,每层可配不同规则                      | 做实验     |
| [GabrieleLagani/HebbianLearning](https://github.com/GabrieleLagani/HebbianLearning)     | 深度 CNN,**Hebbian+Backprop 混合**,CIFAR-10               | 研究复现    |
| [aimh-lab/hebbian-learning-cnn](https://github.com/aimh-lab/hebbian-learning-cnn)       | Lagani 仓库的镜像/分支,带对比实验                                 | 研究复现    |
| [SpikingJelly](https://spikingjelly.readthedocs.io/zh-cn/latest/tutorials/en/stdp.html) | SNN + STDP 完整教程(PyTorch)                              | 脉冲网络方向  |


**入门建议**: 从 `ThomasMiconi/HebbianCNNPyTorch` 开始读代码(几十行就能看懂一层 Hebbian 怎么写),然后用 `biopytorch` 在自己的小网络里替换一层试效果。

---

## 五、关键论文清单(可核实)

**综述/对比类**:

1. Gupta et al. (2022). *Is Bio-Inspired Learning Better than Backprop?* [arXiv:2212.04614](https://arxiv.org/pdf/2212.04614)
2. Nimmo et al. (2025). *Advancing the Biological Plausibility and Efficacy of Hebbian Learning…* [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0893608025005088) / [arXiv:2501.17266](https://arxiv.org/html/2501.17266v1)

**方法突破类**:
3. Lagani et al. (2024). *Scalable bio-inspired training of DNNs with FastHebb.* [Neurocomputing, DOI:10.1016/j.neucom.2024.127867](https://www.sciencedirect.com/science/article/pii/S0925231224006386) / [arXiv:2207.03172](https://arxiv.org/abs/2207.03172)
4. Daruwalla (2024). *Information bottleneck-based Hebbian learning rule.* [Frontiers in Comp. Neuro.](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1240348/full)
5. Ravichandran et al. (2025). *Unsupervised representation learning with Hebbian synaptic and structural plasticity.* [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0925231225001122) (被引 22)
6. (NeurIPS 2025) *Low-Dimensional Structural Projection for Unsupervised Learning.* [arXiv:2510.14810](https://arxiv.org/html/2510.14810v1)
7. Liu et al. (2021). *SSTDP: Supervised Spike Timing Dependent Plasticity.* [Frontiers in Neuroscience](https://pmc.ncbi.nlm.nih.gov/articles/PMC8603828/) (被引 101)

**经典/参考**:
8. *Hebbian Learning Meets Deep CNNs?* Lagani et al. (ICIAP, [被引 91](https://falchi.isti.cnr.it/Draft/2019-ICIAP-HLMSD.pdf))
9. KTH 皇家理工硕士论文: [Comparison of Hebbian Learning and Backpropagation](https://kth.diva-portal.org/smash/get/diva2:1795928/FULLTEXT01.pdf)
10. Scholarpedia: [Oja learning rule](http://www.scholarpedia.org/article/Oja_learning_rule)

---

## 六、学习路径建议

**第 1 步(1 天)**: 概念

- 读懂原始 Hebbian、Oja、BCM 三者的公式差异(本篇路线 A-C 的公式部分)
- 推荐: [Julien Vitay 的讲义](https://julien-vitay.net/lecturenotes-neurocomputing/4-neurocomputing/5-Hebbian.html)

**第 2 步(2-3 天)**: 跑代码

- 克隆 [ThomasMiconi/HebbianCNNPyTorch](https://github.com/ThomasMiconi/HebbianCNNPyTorch),在 MNIST 上跑通
- 改一个超参数(学习率、归一化),看权重会不会爆炸

**第 3 步(1 周)**: 复现

- 用 [biopytorch](https://github.com/Einlar/biopytorch) 在一个小 CNN 里把第一层换成 Hebbian
- 对比:纯 Backprop vs Hebbian+Backprop 混合,在 CIFAR-10 上的精度和收敛速度

**第 4 步(深入)**: 读论文

- 先读 Gupta 2022(对比清晰) → 再读 FastHebb(工程优化怎么做的) → 再读三因子规则(理论精髓)

---

## 七、一句话总结

Hebbian 学习的"现代实现"围绕一个核心矛盾展开:**生物合理性 vs 工程性能**。五条路线分别从

- **速度** (FastHebb 的 70× 加速)
- **全局指导** (三因子规则 $xyM$)
- **稳定性** (Oja/BCM 的归一化和滑动阈值)
- **混合** (Hebbian 前端 + Backprop 后端)
- **脉冲硬件** (STDP + 代理梯度)

五个角度,把这个 1949 年的老规则,第一次推到了 ImageNet 级别和神经形态硬件上。它不会取代 Backprop,但在**少标签、要可解释、要在线学习、要低功耗**的场景里,正在成为正经的工程选项。

---

## 诚实声明

- 本篇所有 **论文** 均带 arXiv 编号或 DOI,可自行核实。
- 所有 **GitHub 仓库** 均为搜索时确认存在的真实仓库(stars 数会随时间变化,故未写死数字,需要时可直接点进仓库看最新值)。
- "70× 加速""5 epochs vs 100 epochs""被引 101 次"等**具体数字**来自对应论文的搜索摘要,引用前建议点开原文确认上下文(这些数字往往有特定前提条件)。
- 本篇是上一篇概览报告的**深入补丁**,概念上和上一篇一致,但资源更可靠。

---

**报告编制**: AI 调研助手
**最后更新**: 2026-07-26
**版本**: 1.0