# LoRA 选项选项卡
仅当您将模式设置为 LoRA（右上角下拉菜单）时，此选项卡才可见

此选项卡上有几个选项。

![image](https://github.com/user-attachments/assets/ddcbd806-ec5c-4423-835d-950badabeb41)

* 类型（默认：`LoRA`）：您想要使用的参数高效微调形式。您的选择是 LoRA（传统）和 LoHa（由 Lycoris 项目引入）以及 OFTv2（正交微调）。
* LoRA 基础模型（默认：`空白`）：这允许您加载一个 LoRA 来继续处理它（即恢复）。或者，可以使用备份文件夹，但请注意，加载备份文件夹时，您可以做的事情更有限。
* LoRA 秩（默认：`16`）：这是决定您的 LoRA 将有多少层的值。层越多，您需要的 VRAM 越多，但可以存储的数据也越多。
* LoRA alpha（默认：`1.0`）：一个可调超参数。alpha 值除以秩将乘以您的学习率。例如，默认值将为您的学习率提供 .0625 乘数（1/16）。自适应优化器（dAdapt、Prodigy）将顾名思义，适应您的 alpha 值。
* 分解权重（默认：`关闭`）：仅对 LoRA 有效。执行幅度/方向权重分解。这通常被称为 **DoRA**，与传统技术相比，可以带来更好的学习和更快的收敛。如果您选择此选项，您必须将 dropout 概率大幅降低到常规 LoRA 设置的 1/10。
* Dropout 概率（默认 - 0.0）：一种通过在每个训练步骤随机忽略一定百分比的训练节点来帮助防止过拟合的技术。一个指南（下面链接的那个）建议值在 .1 和 .5 之间。如果您想了解更多，请查看该指南。
* LoRA 权重数据类型（默认：`float32`）：将 LoRA 加载到内存时使用的精度。您几乎不应该更改此设置
* 捆绑嵌入（默认：开启）：如果您训练额外的嵌入，这会将它们捆绑到 LoRA 文件中。此选项仅在 Automatic1111 和 SD.Next 中受支持；ComfyUI 不读取这些。


## Lora Alpha 值
Lora Alpha 值和秩在 Discord 上引发了很多讨论，Discord 是获取更多信息以及搜索维基中没有的信息的好地方！

## 有关 LoRA 的更多信息
[如果您有兴趣阅读更多关于 LoRA 的信息，这里有一个链接，您可以访问 CivitAI 上的指南。](https://civitai.com/articles/3105/essential-to-advanced-guide-to-training-a-lora)

## OFTv2
OFT（正交微调）是一种尝试解决 Lora 带来的一些挑战的方法，即过拟合和原始模型知识的丢失。

OFTv2 比原始版本在内存和速度上有显著提升。

为了在 ComfyUI 中使用 OneTrainer 的 OFTv2 safetensor 输出，您需要使用自定义节点来修补 ComfyUI，直到它有原生支持。自定义节点可以在 [这里](https://github.com/Koratahiu/ComfyUI-OFTv2) 找到。

关于 OFT 和 OFTv2 的信息
* [OFT](https://github.com/zqiu24/oft)
* [OFTv2](https://github.com/huggingface/peft/pull/2575#issue-3128673603)
* [OneTrainer PR](https://github.com/Nerogar/OneTrainer/pull/1073)
