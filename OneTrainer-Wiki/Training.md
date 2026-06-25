### 章节
注意：由于 OT 持续获得增强，截图可能不是最新的，每个参数都有工具提示。

![image](https://github.com/user-attachments/assets/797e375a-d449-4a1c-8af5-d518f8b4972c)

## 优化器信息
有关优化器的更多信息可以在 [这里](https://github.com/Nerogar/OneTrainer/wiki/Optimizers) 找到

## 训练文本编码器（1 和 2）
如果设置了文本编码器 LR，它会覆盖基础 LR。

SDXL 包含 2 个文本编码器（TENC1 - CLIP-ViT/L 和 TENC2 - OpenCLIP-ViT/G）。有人认为 TENC1 更适合标签，TENC2 更适合自然语言，但这尚未得到证实，更多是基于测试观察和感觉。尝试确定让文本编码器协同工作以获得您想要的结果的最佳方式是 SDXL 微调的最大挑战之一。大多数成功案例都使用了商业级硬件，而不是消费级硬件。[作为参考，这里是原始 CLIP 模型的硬件信息。](https://github.com/Nerogar/OneTrainer/assets/132208482/8e5ecdc2-fc63-47ab-9c74-691902fe681b)。


## 训练 UNet
如果设置了 unet 编码器 LR，它会覆盖基础 LR。

[文本和 Unet 编码器](https://rentry.org/59xed3#text-encoder-learning-rate)

## 掩码训练
使用掩码训练，您可以指示模型专注于训练图像的某些部分。例如，如果您想训练一个主体，但较少训练背景或某些特定部分，此设置会有所帮助。要启用掩码训练，您需要为每张需要它的训练图像添加掩码，并非所有图像都需要有掩码。此掩码是一个黑白图像文件，其中白色区域定义了应该获得关注的部分，黑色区域则较少。文件需要与图像同名，并添加 "-masklabel.png" 扩展名。掩码必须是 png 格式。这些掩码可以在工具部分创建，可以自动创建或使用绘画功能。进行掩码训练时，OneTrainer 会在掩码所在位置减少注意力（请查看此 [讨论](https://github.com/Nerogar/OneTrainer/discussions/347#discussioncomment-9807611) 以更好地了解掩码训练）。

掩码训练可用的选项有：
_未掩码概率_：不使用掩码运行的步数。应该理解为百分比。值：0 到 1。默认值：.1

_未掩码权重_：掩码区域在未掩码训练期间的加权损失值。应该理解为百分比。值：0 到 1。默认值：.1

_归一化掩码区域损失_：一个开关（开/关），应在掩码区域非常大时使用（例如：珠宝）。对于较小尺寸的掩码，这会增加平滑损失，这可能是不需要的。例如，开启此功能的运行会使平滑损失从 .06 增加到 .12，而掩码不到图像的 50%。

## 验证

验证是一种确定训练何时开始过拟合的技术方法。对验证概念中的每张图像进行预测，并在概念内对损失进行平均。有关损失和验证作用的更多信息可以在 [这里](https://github.com/Nerogar/OneTrainer/wiki/How-Validation-works) 找到。

启用它的快速步骤：

* 在通用选项卡中启用验证，并设置验证计算的间隔（如样本）。
* 添加验证概念，标记为验证概念，并像在任何图像生成程序中一样添加描述。
* 对于验证概念，不要使用您的训练图像——这似乎显而易见，但值得一提。您也可以在另一个概念中使用完全不同的图像来获取其他信息（验证损失应该缓慢增长）。
* 验证概念（标记为这样的）不会影响训练。
* 结果可以在 Tensorboard 中看到：每个验证概念的验证损失图。

另请参阅此 [页面](https://github.com/Nerogar/OneTrainer/wiki/How-to-setup-and-evaluate-validation-datasets) 了解详细配置和用法。



## 主要设置
您需要调整的最重要设置是学习率、学习率最小因子、调度器和优化器。然后是 epoch、批量大小和累积步骤。其他设置一开始可以保持默认。

训练分辨率默认根据基础模型设置。您可以通过在分辨率字段中指定逗号分隔的数字列表来同时训练多个分辨率。每一步将从列表中随机选择一个分辨率进行训练。

多分辨率值示例（思路是上下调整 64px）：
* SD1.5: 384,448,512,576,640
* SDXL: 896,960,1024,1088,1152

另请参阅 [多分辨率训练](https://github.com/Nerogar/OneTrainer/wiki/Lessons-Learnt-and-Tutorials#multi-resolution-training) 了解更多信息，并可选择在概念上使用 [分辨率覆盖](https://github.com/Nerogar/OneTrainer/wiki/Concepts#image-augmentation-tab)。

注意：您也可以在特定分辨率（如 896x1152）下训练，但在这种情况下只支持一个训练分辨率。

### EMA（指数移动平均）
![image](https://github.com/user-attachments/assets/e2d619e6-662a-4e2f-ad9c-0a7784cac5a3)

移动平均是一种确定趋势方向的统计工具。指数移动平均是移动平均的一种，它对最近的数据点比对过去发生的数据点施加更多权重。

仅对具有多个概念的较大数据集有用，因为 EMA 会减少多样性，EMA 越多，多样性越少。
如果您的数据集不太复杂且变化不大，请保持关闭。如果关闭 EMA 无法获得好结果，请尝试启用它。对于数百或数千张图像的数据集，将 EMA Decay 设置为 0.9999。对于较小的数据集，将其设置为 0.999 或甚至 0.998。

有一些说法认为它也需要根据 LR 进行调整 https://arxiv.org/pdf/2312.02696

EMA 在训练选项卡中有三个设置：
* EMA（默认：关闭）：使用 CPU、GPU 启用 EMA，或禁用（关闭）
* EMA Decay（默认：.999）：控制将平均多少步。较大的数据集应使用 .9999，较小的数据集可以使用 .999 或 .998
* EMA 更新步长间隔（默认：5）：EMA 更新计算的执行频率。1 是最好的，但仅建议您可以用 GPU 管理 EMA 时使用。5 是 CPU 计算 EMA 的一个很好的折衷值。


### 梯度检查点
减少内存使用但增加训练时间。

有三个可用选项：
* 关闭：最高的 VRAM 使用但最快的训练速度。
* 开启：减少 VRAM 使用，对训练速度有一些影响。
* CPU 卸载：通过使用系统内存减少 VRAM，对训练速度有一些影响。

使用 CPU 卸载模式时：
要启用它，请将"梯度检查点"设置为 CPU_OFFLOADED，然后将"层卸载分数"设置为 0 到 1 之间的值。较高的值将使用更多的系统 RAM 而不是 VRAM。

重要注意事项：
* 训练 SD1.5 或 SDXL 等 unet 模型时，VRAM 使用量减少不多
* 训练 Flux 或 SD3.5-M 并使用接近 0.5 的卸载分数时，VRAM 使用仍然不是最佳
* 使用 CPU 卸载进行微调时，累积步骤必须设置为 1，因为 Fused Back Pass 不支持累积步骤

使用 CPU 卸载进行微调需要支持 Fused Back Pass 的优化器：
* ADAMW
* ADAM
* ADAFACTOR
* CAME

[Reddit 发布](https://www.reddit.com/r/StableDiffusion/comments/1gi2w2e/onetrainer_now_supports_efficient_ram_offloading/) 关于此功能，如果您在 Discord 服务器上搜索更多信息，技术名称是 RAM 卸载。技术信息在 [Github](https://github.com/Nerogar/OneTrainer/blob/master/docs/RamOffloading.md) 上。

### 优化器

请参阅此 [页面](https://github.com/Nerogar/OneTrainer/wiki/Optimizers)


### 学习率调度器
调度器方法将根据初始学习率值（在学习率字段中设置）计算学习进度。

学习率最小因子决定最终学习率的值。例如：如果设置为 0.1，最终 LR 将是初始 LR 的 10%，设置为 0 时对计算的 LR 没有任何改变。

余弦示例：蓝色曲线是学习率最小因子 = 0，红色是学习率最小因子 = 0.3。

![LRminFactor1](https://github.com/user-attachments/assets/e994d512-19a6-4119-b451-9bdafb673dda)

注意：除了基础学习率（简称为学习率）之外，还有几个学习率字段。这些是用于文本编码器、Unet 和嵌入（用于额外嵌入）的，如果它们为空，将使用基础 LR，如果设置了，它们将覆盖基础 LR 值。

* 恒定：固定学习率。
* 线性：从初始学习率到 0 的线性学习率衰减。
<img width="227" alt="linear" src="https://github.com/Nerogar/OneTrainer/assets/129741936/95237662-3f87-4383-b7f7-850a4da54e76">

* 余弦

此调度器在开始时衰减快，在结束时慢。

<img width="233" alt="cosine" src="https://github.com/Nerogar/OneTrainer/assets/129741936/1dbcd622-5964-4421-b9e8-4270554d8ed6">

* 带重启的余弦

* 带硬重启的余弦

* REX：从初始学习率开始并以 0 结束的反向指数学习率衰减。也称为"brute"，在某些情况下可以执行非常快速的训练。

<img width="233" alt="REX" src="https://github.com/Nerogar/OneTrainer/assets/129741936/6c6d1ed9-4983-4dd4-aaea-44ae64a279ff">

* 自定义调度器

自定义调度信息可以在这里找到：https://github.com/Nerogar/OneTrainer/wiki/Custom-Scheduler

### 训练数据类型
在内部，这会设置通过模型进行前向传播时的混合精度数据类型。此设置在训练期间以精度换取速度。并非所有数据类型都在所有 GPU 上受支持。实际上，float16 只会略微降低质量，同时提供显著的速度提升。但为了最佳质量，请使用 float32（降低速度）。

### Epochs / 批量 / 累积步骤

* Epochs：一个 epoch 是所有图像都被训练的一个周期。根据批量大小和数据集，它可以使用一次或多次迭代。
* 批量大小：发送到 GPU 进行处理的图像数量。
* 累积步骤：批量大小的乘数。例如：如果您想要 16 的批量但限制为 4，请将累积步骤设置为 4。

### 层过滤器

选择要训练的层，这适用于全微调和 Lora。可能的值取决于训练类型（Lora 或全微调）和基础模型。默认是简单的子字符串匹配，如果启用则是正则表达式。我们建议坚持使用预设附带的默认值，但您始终可以选择另一个值，甚至"自定义"并指定您自己的值，用逗号分隔，空白值将训练所有层。

这可以改进较新模型的全微调，因为某些层可能不打算被训练。对于某些模型，有一个名为"blocks"的新预设，它几乎训练整个模型，但排除了一些可能有问题的层。

对于 Lora，"attn-mlp" 和 "attn-only" 是安全的选择。

### 损失权重函数

我们建议对 SD1.5 和 SDXL 使用值为 5 的 `min_snr_gamma`。对于其他模型，您需要向人们和谷歌询问。

### 重新缩放噪声调度器

这为模型启用 V-pred 和 ZTSNR。如果您选择启用重新缩放噪声调度器，请不要启用 `min_snr_gamma`，因为它很快会导致样本变灰。这是使 NAIv3 与 SDXL 相比具有显著更好保真度生成的功能。https://arxiv.org/abs/2409.15997

### 强制循环填充
如果您希望训练无缝游戏纹理，请启用此功能。否则请保持关闭。
