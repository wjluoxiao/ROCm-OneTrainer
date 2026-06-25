# OneTrainer 中扩散模型的特定模型技术信息
本维基页面提供了有关 OneTrainer 支持的扩散模型的详细技术信息，特别关注 SD1.5、SDXL 和 Flux。这些信息是为相当高级的用户量身定制的。

## SD1.5

### 基础架构
SD1.5 采用具有编码器-解码器结构的 UNet 架构，基于去噪自动编码器的层次结构

### 训练分辨率
最终训练分辨率实际上是 512x512

分词和最大 token 数

* 使用 CLIP 分词器
* OT 中每个描述的最大 token 数：75

LoRA 完整块集 / 层键
SD1.5 LoRA 训练的自定义层集的工作示例是：

```python
down_blocks.1.attentions.0,down_blocks.1.attentions.1,down_blocks.2.attentions.0,down_blocks.2.attentions.1,mid_block.attentions.0
```

SD1.5 的完整块集可以在 [这里](https://raw.githubusercontent.com/ratwithacompiler/diffusers_stablediff_conversion/refs/heads/main/convert_diffusers_to_sd.py) 或 [这里](https://gist.github.com/jachiam/8a5c0b607e38fcc585168b90c686eb05) 参考

VAE 压缩

* 压缩因子：8x8（每个维度 8 倍）
* VAE 在 256px x 256px 分辨率上训练
* 通道数：4

论文：https://arxiv.org/pdf/2112.10752

## Stable Diffusion XL (SDXL)

### 基础架构
SDXL 使用增强的 UNet 架构，明显大于 SD1.5。

### 训练分辨率
SDXL 在更高的分辨率下训练，实际上是 1024x1024。

### 分词和最大 token 数

* 使用两个 CLIP 文本编码器（CLIP ViT-L 和 OpenCLIP ViT-bigG）
* 最大 token 数：在 OneTrainer 中又是 75

### VAE 压缩

* 压缩因子：8x8（每个维度 8 倍）
* VAE 在 256px x 256px 分辨率上训练
* 使用与 SD1.5 相同的 VAE 模型，但使用更大的批量大小并启用 EMA 进行训练

论文：https://arxiv.org/pdf/2307.01952
