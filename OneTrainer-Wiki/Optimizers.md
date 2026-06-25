# 分解优化器

![image](https://github.com/Nerogar/OneTrainer/assets/132208482/0b40c78e-7ad3-4c9c-988a-0efee36f30da)

关于优化器有三个重要说明。
* 您可以按三个点（...）打开该优化器的设置。
* 默认设置是优化器的默认值，可能不是训练扩散模型的最佳选择。
* OneTrainer 会存储您为每个优化器设置的最后设置，您可以通过按"加载默认值"来恢复默认设置。

***

### 标准优化器：
* Adagrad - 自适应梯度算法
* ADAM - 自适应矩估计
* ADAMW - 带权重衰减的自适应矩估计
* ADOPT - 改进的 Adam，可以以最佳速率收敛任何 beta2。此优化器声称在扩散模型的小批量大小上比 ADAMW 表现更好
* LAMB - 用于批量训练的逐层自适应矩优化器
* LARS - 逐层自适应速率缩放
* LION - 神经元线性积分
* RMSPROP - 均方根传播
* SGD - 随机梯度下降

所有标准优化器也有 8 位版本。

如果您不被复杂的数学公式所困扰，这里有一个很好的介绍性技术视频，讨论了其中一些优化器：[这里](https://www.youtube.com/watch?v=NE88eqLngkg)

_**注意：8 位版本通过使用 8 位量化来节省 VRAM。这样做会有质量上的权衡。**_

***

### DAdapt 优化器系列
（带参数化时间步的分布式自适应衰减适应）。
这些优化器是标准优化器的自适应版本
* DADAPT_ADA_GRAD
* DADAPT_ADAM
* DADAPT_ADAN
* DADAPT_LION
* DADATP_SGD

***

### 独特的自适应优化器
* Prodigy - 一个特殊的优化器，也是最受欢迎的，因为它易于使用，但也很难获得您正在寻找的确切结果。虽然纯 ADAM 或 ADAMW 可以提供更好的结果，但如果您不知道应该使用什么学习率或需要多少步骤，Prodigy 是一个很好的起点。Prodigy 占用大量 VRAM（特别是对于 1024x 模型），可能只能用于 LoRA 或嵌入训练，除非您有大量 VRAM。Prodigy 本质上是 ADAMW。Tensorboard 可用于查看 Prodigy 稳定在什么学习率，以便在 AdamW 或 AdamW 8bit 中使用。
### 更独特的自适应优化器
* Prodigy Plus - Prodigy Plus 是一个试图将所有优化器的最佳功能融入自身的优化器。Prodigy Plus 的主要好处是能够将 Prodigy 用作带有融合反向传播和随机舍入的无调度优化器，以及许多许多其他功能。

***
### 特殊的
* Adafactor - Adafactor 可以用作带有恒定（或其他）调度器的低内存 ADAMW，或者用作带有 Adafactor 调度器的自适应优化器。


***

### Prodigy 特定设置详情
首先，请注意 Prodigy 来自 https://github.com/konstmish/prodigy
在那里的顶级 README 中有一些使用它的优秀细节。

列出了 OneTrainer 默认值。如果适用，推荐值列在默认值之后
| |  |
|-----------------------------------------------------------|---------------------------------------------------------|
| Beta1: 0.9                 | Beta2: 0.999, ****推荐 0.99 到 0.999**** |
| Beta3: 空白                                          | EPS: 1e-08                                      |
| Weight Decay: 0.0 _**推荐 0.001 到 0.01**_ | Decouple: True                                  |
| Bias Correction: False **_推荐 True_** （除非是恒定调度器/sdxl？）| Safeguard Warmup: False  **_推荐 True?_**    |
| Initial D: 1e-06     | D coefficient: 1.0 _**推荐见注释**_                       |
| Growth Rate: inf   | FSDP in use: False                      |
| Slice parameters: 11（对于嵌入设置为 1） |                       |

**学习率必须为 1**，并且文本编码器和 unet 都必须相同。否则，lora 将不起作用。`学习率缩放器`选项也应保留在默认值 `NONE`。考虑不使用任何训练预热步骤，因为 Prodigy 有自己的预热方法。Prodigy 的开发者建议配合使用余弦，但您可以尝试任何其他方法。

对于 Safeguard 预热，对于短训练设置为 true 可能更好，但对于较长（epoch=100）训练，可以是 true/false。
对于 Bias Correction：遗憾的是，这是另一个最佳选择真的是"视情况而定，两者都试试"的设置 :(

Prodigy 获得了相当显著的 VRAM 优化（自定义功能）。它默认启用，但如果您想禁用它，请在优化器设置中将"Slice parameters"设置为 1。如果您将 Beta1 设置为 0，VRAM 使用量会进一步减少。但这可能会产生更差的结果，类似于 ADAFACTOR 的默认设置。

要调整 Prodigy 计算的 LR，您应该使用 D 系数，它充当 LR 乘数。使用 0.5 的 D 系数会减慢 Prodigy，而 2 的 D 系数会加快它。使用余弦函数（或任何衰减的函数）可以帮助 Prodigy 在训练运行结束时学习细节，因为 Prodigy 永远不会自己降低学习率。使用 0.99 的 Beta 2 已被证明有助于 Prodigy 更好地收敛。使用权重衰减可以帮助 Prodigy 不过度训练。其他技术包括 LoRA 的 dropout（在 LoRA 选项卡上找到）。启用 Bias correction 有助于 Prodigy 更像 ADAM 一样工作。

<img width="323" alt="Capture d'écran 2024-05-02 133822" src="https://github.com/Nerogar/OneTrainer/assets/129741936/95b3691c-ed07-4bcf-98fc-55d121df3e8b">

D 系数对带余弦的 LR 的影响
* 蓝色：1.2
* 黑色：1
* 黄色：0.5


***

### Prodigy Plus 特定设置详情
首先，请注意 Prodigy Plus 来自 https://github.com/LoganBooker/prodigy-plus-schedule-free

Prodigy Plus 有许多实验性功能。它们只会在这里被提及。目前尚不清楚它们是否会有帮助、伤害甚至有效，我们恳请您自行承担使用风险。

列出了 OneTrainer 默认值。如果适用，推荐值列在默认值之后（进行中）
| |  |
|-----------------------------------------------------------|---------------------------------------------------------|
| Beta1: 0.9                 | Beta2: 0.99 |
| Beta3: 空白                                          | Weight Decay: 0.0                                      |
| Weight_decay_by_lr: True | Bias Correction: False (True?)                                  |
| Initial D: 1e-06（微调为 1e-08）| D Coefficient: 1.0    |
| Prodigy Steps: 0    | use speed: disabled（实验性）                    |
| EPS: 1e-08  | split groups: Enabled                      |
| split_groups_mean: Enabled   |  factored: enabled                     |
| factored_fp32: Enabled   |  fused Back Pass: disabled（在低 VRAM 系统上为微调启用）       |
| use_stableadamw: Enabled   |  use_muon_pp: disabled（实验性）      |
| use_cautious: disabled   |  use_grams: disabled（实验性）      |
| use_cautious: disabled（实验性）   |  use_focus: disabled（实验性）      |
| Stochastic Rounding: Enabled   |      |

Prodigy Plus 注意事项：
* 学习率应为 1
* 调度器应为恒定（无调度）
* 梯度裁剪应禁用（在训练选项卡上清除选项）
* 仅限于 BF16/FP32 使用，可能是模型权重。已测试 SDXL 的 FP32 Lora 和 FP16 训练数据类型正常。
* Prodigy Plus 可以为不同组设置不同的学习率（split groups 设置）
* Prodigy Plus 可以与微调一起使用。将初始 LR 设置为 1e-8 以确保它找到正确的低 LR。（已用 SDXL 测试，微调/合并的微调 - Bond 5.0）
* Prodigy Plus 包括二阶近似（如 Adafactor）。作者表示您的体验可能会因功能而异。此功能由 Factored 设置控制。如果您处于 VRAM 限制的边缘，您也可以将 factored_fp32 设置为 false 以使用 bf16。然而，这可能会导致训练不稳定。
* Prodigy Plus 似乎不喜欢累积步骤，它确实减慢了寻找 LR 的过程（需要更多测试）
* Prodigy steps 设置将在达到给定步骤后禁用 Prodigy 计算，释放 VRAM 和计算时间。这也将防止标准 prodigy 行为的 LR 稳定增加，尽管作者表示 schedulefree 也应该对抗这一点。
* 如果您想使用小于 .9 的 D 系数，似乎您需要关闭 d_limiter（Prodigy Plus 2.0 测试）

***


### Adafactor 特定设置详情（自适应）
列出了默认值。如果适用，推荐值列在默认值之后
|  | |
|-----------------------------------------------------------|---------------------------------------------------------|
| EPS: 1e-30                    | EPS2: .001                |
| Clip Threshold: 1.0           | Decay Rate: -0.8          |
| Beta 1: 空白（留空，除非您真的知道这是做什么的）                | Weight Decay: 0.0        |
| Scale Parameter: True         | Relative Step: True       |
| Warmup Initialization: False  | Stochastic Rounding: True |
| Fuse Back Pass: False  |  |

自适应模式下的 Adafactor 注意事项：
* 它会忽略任何 LR 值。
* 带有 relative step 和 scale parameter 的 Adafactor 为微调设置的学习率太高。如果您想将 adafactor 用于微，请参阅下一个设置。将 Adafactor 调度器与这些设置一起使用以进行自适应学习。relative step 下的 Adafactor 较慢，因为它需要做更多计算来确定下一步。为 adafactor 输入 Beta 1 的值将由于启用了 EMA 类型功能而显著增加 VRAM 使用。启用"Fused Back Pass"可以显著减少 VRAM 使用而不会有任何质量损失，但此选项与梯度累积不兼容。

***

### Adafactor 特定设置详情（低内存 ADAMW）
列出了默认值。如果适用，推荐值列在默认值之后
|  | |
|-----------------------------------------------------------|---------------------------------------------------------|
| EPS: 1e-30                    | EPS2: .001                |
| Clip Threshold: 1.0           | Decay Rate: -0.8          |
| Beta 1: 空白（留空，除非您真的知道这是做什么的）                    | Weight Decay: 0.0 _**推荐 0.0 到 0.01**_      |
| Scale Parameter: True _**必须为 FALSE**_        | Relative Step: True  _**必须为 FALSE**_     |
| Warmup Initialization: False  | Stochastic Rounding: True |
| Fuse Back Pass: False  |  |

恒定模式下的 Adafactor 注意事项：在此模式下，adafactor 必须使用标准调度器（恒定、余弦等）。使用与 AdamW 类似的学习率或您训练任务的默认值。此模式下的 Adafactor 使用的 VRAM 比 ADAMW 少，但比 ADAMW 8bit 多，没有 8 位量化的质量损失。为 adafactor 输入 Beta 1 的值将由于启用了 EMA 类型功能而显著增加 VRAM 使用。启用"Fused Back Pass"可以显著减少 VRAM 使用而不会有任何质量损失，但此选项与梯度累积不兼容。

***

### ADAM(W) 特定设置详情

***

### 所有选项
* adam_w_mode: 是否对 Adam 优化器使用权重衰减校正。类型：布尔值
* alpha: RMSprop 和其他的平滑参数。类型：浮点
* amsgrad: 是否对 Adam 使用 AMSGrad 变体。类型：布尔
* Beta1: optimizer_momentum 项。类型：浮点
* Beta2: 计算梯度运行平均值的系数。类型：浮点
* Beta3: 计算 Prodigy 步长的系数。类型：浮点
* bias_correction: 是否在 Adam 等优化算法中使用偏差校正。类型：布尔
* block_wise: 是否执行逐块模型更新。类型：布尔
* capturable: 优化器的某些属性是否可以被捕获。类型：布尔
* centered: 是否在缩放之前将梯度居中。对于稳定训练过程非常好。类型：布尔
* clip_threshold: 梯度的裁剪值。类型：浮点
* Initial D: D 适应的初始 D 估计。类型：浮点
* D Coefficient: d 估计表达式中的系数。类型：浮点
* Dampening: optimizer_momentum 的阻尼。类型：浮点
* Decay Rate: 矩估计的衰减率。类型：浮点
* Decouple: 使用 AdamW 风格的 optimizer_decoupled 权重衰减。类型：布尔
* Differentiable: 优化函数是否是 optimizer_differentiable 的。类型：布尔
* EPS: 防止除以零的小值。类型：浮点
* EPS 2: 防止除以零的小值。类型：浮点
* ForEach: 是否使用 foreach 实现（如果可用）。此实现通常更快。类型：布尔
* FSDP in Use: 使用分片参数的标志。类型：布尔
* Fused: 是否使用融合实现（如果可用）。此实现通常更快且需要更少的内存。类型：布尔
* Growth Rate: D 估计增长率的限制。类型：浮点
* Initial Accumulator Value: Adagrad 优化器的初始值。类型：浮点
* Is Paged: 优化器的内部状态是否应该分页到 CPU。类型：布尔
* Log Every: 日志记录应该发生的间隔。类型：整数
* LR Decay: 学习率下降的速率。类型：浮点}
* Max Unorm: 按范数裁剪梯度的最大值。类型：浮点
* Maximize: 是否 optimizer_maximize 优化函数。类型：布尔
* Min 8bit Size: 8 位量化的最小张量大小。类型：整数
* Optimizer Momentum: 在相关方向上加速 SGD 的因子。类型：浮点
* Nesterov: 是否启用 Nesterov optimizer_momentum。类型：布尔
* No Prox: 是否使用邻近更新。类型：布尔
* Optim Bits: 用于优化的位数。类型：整数
* Percentile Clipping: 基于百分位值的梯度裁剪。类型：浮点
* Relative Step: 是否使用相对步长。类型：布尔
* Safeguard Warmup: 避免预热阶段的问题。类型：布尔
* Scale Parameter: 是否缩放参数。类型：布尔
* Stochastic Rounding: 权重更新的随机舍入。使用 bfloat16 权重时提高质量。类型：布尔
* Bias Correction: 打开 Adam 的偏差校正。类型：布尔
* Use Triton: 是否应使用 Triton 优化。类型：布尔
* Warmup Initialization: 是否预热优化器初始化。类型：布尔
* Weight Decay: 防止过拟合的正则化。类型：浮点

***
### 高级优化器

这些是配备了学术研究论文中最新、**高级**技术和方法的**优化器**。

| 优化器 | 描述 | 最适合 |
|-----------|-------------|----------|
| `Adam_Adv` | 高级 Adam 实现 | 通用 |
| `Adopt_Adv` | 具有独立 beta2 的 Adam 变体 | 小批量大小制度的稳定训练 |
| `Prodigy_Adv` | 带 D 适应的 Prodigy | 带自动 LR 调优的 Adam |
| `Simplified_AdEMAMix` | 带累加器动量的 Adam 变体 | 正确调优时的小/大批量训练 |
| `Lion_Adv` | 高级 Lion 实现 | 通用 |
| `Prodigy_Lion_Adv` | Prodigy + Lion 组合 | 带自动 LR 调优的 Lion |

由于有很多信息需要涵盖，它们在专门的 [页面](https://github.com/Nerogar/OneTrainer/wiki/Advanced-Optimizers) 中有详细描述。
