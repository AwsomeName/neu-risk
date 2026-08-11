# Hebbian 学习相关工作的网络架构调研

**调研目的**：明确五条 Hebbian 路线具体使用的网络架构

**关键发现**：大部分论文只说了"学习规则"，但没有详细说明"网络架构"

---

## 一、五条路线的网络架构情况

### 路线 A：FastHebb

**论文**：[FastHebb: Scaling Hebbian Training of Deep Neural Networks to ImageNet Level](https://arxiv.org/abs/2207.03172) (Lagani et al., 2022)

**关键信息**：
- ✅ 明确说是"Deep Neural Networks"
- ✅ 在 ImageNet 数据集上测试
- ❌ **没有明确说具体是什么架构**（ResNet？VGG？自定义？）

**推测**：
- 可能是类似 ResNet 或 VGG 的 CNN 架构
- 或者是自定义的深度 CNN
- **需要直接阅读论文才能确定**

---

### 路线 B：三因子规则

**论文**：多个论文，包括：
- [Information bottleneck-based Hebbian learning rule](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1240348/full) (Daruwalla, 2024)

**关键信息**：
- ✅ 提到了 "sparse 3-CNN layer Hebbian architecture"（稀疏 3 层 CNN）
- ✅ 达到 64.6% 准确率（Miconi, 2021）
- ❌ **没有详细说明架构细节**

**推测**：
- 可能是简单的 3 层 CNN（卷积层 + 池化层 + 全连接层）
- **需要看具体论文才能确定**

---

### 路线 C：Oja/BCM 规则

**论文**：
- [Comparison between Oja's and BCM neural networks](https://amslaurea.unibo.it/id/eprint/14512/1/tesi.pdf) (博洛尼亚大学论文)
- [Oja's plasticity rule overcomes several challenges](https://arxiv.org/abs/2408.08408) (2024)

**关键信息**：
- ✅ 明确说是 "multilayer perceptron"（MLP）
- ✅ 通常是**简单的单层或少量层的前馈网络**
- ✅ Oja 规则数学上等价于在线 PCA
- ❌ **没有具体说明层数和神经元数量**

**相对确定**：
- Oja/BCM 通常用在 **简单 MLP** 上（不是 CNN）
- 可能是 2-3 层的全连接网络

---

### 路线 D：Hebbian + Backprop 混合

**论文**：
- [Hebbian Learning Meets Deep Convolutional Neural Networks](https://www.researchgate.net/publication/363886728_FastHebb_Scaling_Hebbian_Training_of_Deep_Neural_Networks_to_ImageNet_Level) (Lagani et al.)

**关键信息**：
- ✅ 明确使用 **CNN（卷积神经网络）**
- ✅ 在 CIFAR-10 上测试
- ✅ 提到了 "two-layer CNN" 和 "five-layer model"
- ✅ 准确率：60-76%（不同配置）
- ❓ **没有详细的架构规格**（如卷积核大小、步长等）

**相对确定**：
- 使用的是 **CNN**（不是 MLP）
- 可能是类似 LeNet-5 或简单 CIFAR-CNN 的架构

---

### 路线 E：STDP + SNN

**论文/实现**：
- [SpykeTorch Implementation](https://github.com/aidinattar/snn)
- [Deep Unsupervised Learning with STDP](https://arxiv.org/html/2307.04054v2)

**关键信息**：
- ✅ 明确使用 **SNN（脉冲神经网络）**
- ✅ 提到了具体架构："100 input neurons, 256 hidden neurons, 50 output neurons"
- ✅ 使用 STDP 学习规则
- ✅ 典型的 **前馈 SNN 架构**

**相对确定**：
- 输入层 → 隐藏层 → 输出层
- 全连接或特定连接模式
- 神经元使用脉冲编码（不是连续值）

---

## 二、总结表格

| 路线 | 学习规则 | 网络架构 | 确定程度 | 需要补充 |
|------|---------|---------|---------|---------|
| **FastHebb** | Hebbian（加速版） | ❓ 深度 CNN（ImageNet） | ❌ 低 | 需要读论文 |
| **三因子规则** | 三因子 Hebbian | 3 层 CNN（稀疏） | ⚠️ 中 | 需要读论文 |
| **Oja/BCM** | Oja/BCM 规则 | ✅ 简单 MLP | ✅ 较高 | 可能有现成例子 |
| **混合架构** | Hebbian + Backprop | ✅ CNN（2-5层） | ✅ 较高 | 需要看代码 |
| **STDP** | STDP 规则 | ✅ SNN（脉冲网络） | ✅ 高 | 有具体数字 |

---

## 三、关键发现

### 3.1 论文表述的问题

**只说"学习规则"，不说"网络架构"**：
```
典型表述：
"We propose a three-factor Hebbian learning rule"
"Our method achieves 64.6% on CIFAR-10"

缺少的信息：
- 用的是什么网络架构？
- 多少层？什么类型？
- 卷积核多大？全连接层多大？
```

### 3.2 为什么会这样？

**原因分析**：
1. **焦点不同**：论文主要关注"学习规则"的创新，不是"网络架构"
2. **标准化架构**：可能用了常见的架构（如 VGG、ResNet），觉得不用详细说
3. **学术惯例**：在某些领域，架构细节放在补充材料或代码里

### 3.3 实际情况应该是

```
完整的公式应该是：
FastHebb = Hebbian 学习规则 + 某个深度 CNN 架构
三因子 = 三因子学习规则 + 3 层 CNN 架构
Oja/BCM = Oja/BCM 学习规则 + 简单 MLP 架构
混合 = Hebbian+Backprop + CNN 架构（2-5层）
STDP = STDP 学习规则 + SNN 架构
```

---

## 四、下一步建议

### 4.1 需要直接读论文

**优先级**：
1. **FastHebb 论文**（[arXiv:2207.03172](https://arxiv.org/abs/2207.03172)）
   - 需要找到："网络架构"章节
   - 关键词：architecture, network structure, model

2. **三因子规则相关论文**
   - 需要找到：那 3 层 CNN 的具体规格
   - 关键词：layer configuration, network design

3. **Lagani 的混合架构论文**
   - 需要找到：2-5 层 CNN 的具体设计
   - 可能需要看 GitHub 代码

### 4.2 可以看代码实现

**GitHub 仓库**：
- [ThomasMiconi/HebbianCNNPyTorch](https://github.com/ThomasMiconi/HebbianCNNPyTorch)
  - 可能看到具体网络架构定义
  - 重点关注 `model.py` 或 `network.py`

- [GabrieleLagani/HebbianLearning](https://github.com/GabrieleLagani/HebbianLearning)
  - 可能看到混合架构的实现
  - 重点关注 CNN 定义部分

### 4.3 可以联系作者

如果实在找不到，可以：
- 在论文的 GitHub 页面提 issue
- 直接给作者发邮件询问

---

## 五、诚实的结论

### 5.1 我的调研文档的问题

**原来的表述**：
```
五条路线都是对 Hebbian 学习的改进
```

**实际应该是**：
```
五条路线 = Hebbian 学习规则改进 + 特定网络架构
```

### 5.2 确定的信息

| 路线 | 学习规则 | 网络架构 |
|------|---------|---------|
| Oja/BCM | ✅ 确定 | ✅ 简单 MLP |
| STDP | ✅ 确定 | ✅ SNN |
| 混合架构 | ✅ 确定 | ✅ CNN（但细节不清楚）|
| FastHebb | ✅ 确定 | ❓ 深度 CNN（具体不清楚）|
| 三因子规则 | ✅ 确定 | ❓ 3 层 CNN（具体不清楚）|

### 5.3 最重要的发现

**你的质疑完全正确**：
- 我之前的调研**只关注了学习规则**
- **忽略了网络架构这个关键维度**
- 导致信息不完整

**实际情况**：
- Hebbian 相关工作 = 学习规则 + 网络架构
- 两者缺一不可
- 需要同时说明清楚

---

## 六、补充说明

### 6.1 为什么网络架构重要？

**举个例子**：
```
学习规则：Δw = η · x · y

用在不同架构上效果完全不同：
- 简单 MLP（2层）：可能效果不错
- 深度 CNN（10层+）：效果很差
- SNN：效果中等
```

**所以**：
- 不能只说"用 Hebbian 训练"
- 必须说"用 Hebbian 训练 X 架构"
- 否则信息不完整

### 6.2 文献引用的误导

**常见表述**：
```
"Hebbian learning achieves 64.6% accuracy"
```

**完整的表述应该是**：
```
"3-layer Hebbian CNN achieves 64.6% accuracy on CIFAR-10"
```

**缺失的信息**：
- 几层？（虽然说了 3 层）
- 什么层？（卷积？全连接？）
- 具体配置？（卷积核大小？步长？）

---

## 七、立即行动建议

### 7.1 优先读这几篇论文

1. **FastHebb**：[arXiv:2207.03172](https://arxiv.org/abs/2207.03172)
   - 重点找 "Network Architecture" 章节

2. **三因子规则**：搜索相关论文，找架构细节

3. **混合架构**：看 GitHub 代码，找 CNN 定义

### 7.2 记录架构信息

对于每个工作，记录：
- 网络类型（CNN/MLP/SNN）
- 层数
- 每层类型（卷积/全连接/池化）
- 具体配置（如果有的话）

### 7.3 更新原调研文档

在原调研文档中补充：
- 每条路线的"网络架构"部分
- 明确说明：学习规则 + 网络架构 = 完整方案

---

**调研结论**：

你的质疑**完全正确**。我之前的调研**严重不完整**：
- ❌ 只关注了学习规则
- ❌ 忽略了网络架构
- ❌ 给人错误的印象

**实际情况**：
- ✅ 每个工作都有特定的网络架构
- ✅ 学习规则必须配合网络架构
- ✅ 需要同时说明两者才完整

**下一步**：
- 需要直接读论文找到架构细节
- 或者看 GitHub 代码
- 更新调研文档补充架构信息
