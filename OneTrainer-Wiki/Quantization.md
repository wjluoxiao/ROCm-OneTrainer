# 使用量化和编译的 LoRA 训练

<img width="1060" height="186" alt="image" src="https://github.com/user-attachments/assets/dda74b57-9e49-4640-8d73-cc45756b170d" />


## 建议
这些建议随着技术的发展和测试的进行而不断演变，请经常回来查看或在 Discord 中了解最新动态。

### 目标：准确性
为了获得最佳准确性，推荐使用 `bfloat16` 或带有 Q8 `.gguf` 文件的 `GGUF`。其他所有选项都在质量和速度之间有权衡。

### 目标：速度
为了获得最佳训练速度，请使用 `int W8A8` 或 `GGUF A8 int`。`int W8A8` 比 `GGUF A8 int` 更快。但是，如果您使用较小的 GGUF，如较大模型的 `Q4_K_S`，如果这减少了 CPU 卸载，`GGUF A8 int` 总体上可能更快。

### 伪影
某些模型在使用 `int W8A8` 的样本中可能有可见的伪影。在测试的模型中，Qwen 和 Z-Image 似乎受到影响。可以通过启用 `SVDQuant` 或改用 `float W8A8` 来修复。`float W8A8` 更准确但比 `int W8A8` 慢。带有 `SVDQuant` 的 `int W8A8` 仍然比 `float W8A8` 快，并且似乎足够准确。

<img width="969" height="331" alt="image" src="https://github.com/user-attachments/assets/834c289d-ae7a-43d3-a4b0-034750ae413f" />

Qwen INT 8 vs INT 8 SVDQuant vs BF16

对于 Qwen-Image-2512，推荐使用 `float W8A8` 或 `GGUF int A8`。`SVDQuant` 不能完全消除此模型的伪影。

对于 Z-Image Turbo，`int W8A8` 似乎效果很好，但对于 Z-Image 非 Turbo 则不行。要么使用带有高 SVDQuant 秩的 `int W8A8`（例如 128），`float W8A8`，或者干脆使用 `bfloat16`，因为它尺寸小。

### 其他注意事项
所有带有 `A8` 的选项只有在同时启用 `编译 transformer 块` 时才更快。使用浮点 `A8` 类型之一需要 Nvidia `RTX 40xx` 或更高的显卡。int `A8` 类型需要 `RTX 30xx` 或更高的显卡。

对于大多数模型，使用带有预设 `blocks` 的 `量化层过滤器`。某些模型可能不会受到 `full` 量化的影响，但其他模型会。

** 基于有限测试的陈述 / 需要更多测试

## 数据类型（技术描述）

### float8 (W8)
基线。
速度与 `bfloat16` 相似，但 VRAM 更少。对于大多数模型来说足够准确，但仍然推荐使用 `量化层过滤器`。

技术：权重的张量级量化，采用 float8 e4m3。训练期间反量化到您的 `训练数据类型`。

### nfloat4
速度与 `bfloat16` 相似。
对于大多数模型来说不够准确。可以使用 `SVDQuant` 提高准确性，然后可能与其他数据类型相当，但这尚未经过测试，因为 GGUF 模型更适合低位量化。

技术：权重的块级量化。训练期间反量化到 `训练数据类型`。

### float W8A8
快得多。理论上比 float8 不准确，但测试显示相似的训练行为。

技术：权重的张量级量化，采用 float8 e4m3。激活在训练期间按 token 级量化，Linear 层矩阵乘法在 float8 中执行。

需要 Nvidia `RTX40xx` 卡或更新版本。

### int W8A8
甚至比 `float W8A8` 更快。
在某些模型上没有问题，但使用 Qwen 时有可见的伪影。可以使用 `SVDQuant` 以非常小的性能影响移除伪影（仍然比 `float W8A8` 快）。否则训练行为相似。

技术：权重的张量级量化，采用 int8。激活在训练期间按 token 级量化，Linear 层矩阵乘法在 int8 中执行。

需要 Nvidia `RTX30xx` 卡或更新版本。

### GGUF

从 GGUF 文件按原样加载量化模型。比 `bfloat16` 慢，但使用 `编译 transformer 块` 时以相似速度运行**。
`量化层过滤器` 没有效果：GGUF 文件决定哪些层被量化。不能使用 `SVDQuant`。

技术：根据 GGUF 文件进行权重量化，训练期间反量化到 `训练数据类型`。


### GGUF A8 int

从 GGUF 文件按原样加载量化模型。在相似准确性下快得多。
`量化层过滤器` 仅影响哪些层使用激活量化，而不是哪些层被量化 - 这仍然根据 GGUF 文件。

技术：根据 GGUF 文件进行权重量化。权重从 GGUF 重新量化为 int8 轴级。激活也在训练期间按轴级（token 级）量化，Linear 层矩阵乘法在 int8 中执行。

### GGUF A8 float

类似于 `GGUF A8 int`，但更慢且训练行为更差**。通常不推荐，但对于某些模型可能有用。

技术：根据 GGUF 文件进行权重量化。权重从 GGUF 重新量化为 float8 e4m3 轴级。激活也在训练期间按轴级（token 级）量化，Linear 层矩阵乘法在 float8 中执行。


## SVDQuant

提高量化质量。可以与除 GGUF 之外的所有量化数据类型结合使用。推荐与 `int W8A8` 和 Qwen 一起使用，或者如果您在样本中看到可见伪影，则与其他模型和数据类型一起使用。
`SVDQuant` 数据类型 `bfloat16` 和 `秩` 16 似乎就足够了。

技术：根据 https://arxiv.org/abs/2411.05007 的 SVDQuant 实现
