本节包含从 Discord 服务器收集的各种信息。顶部的那些是由开发者提供的，其他的（后跟"by 或 from 用户名"）是分享的经验，所以请按其实际情况考虑它们，而不是"一种方法"，并且可能包含误导性信息，如果您发现任何问题，请在 Discord 的 wiki 讨论中报告。

### 样本问题
* 如果您的样本图像是黑色的，请将覆盖 VAE 数据类型设置为 bfloat16 或 float32（模型选项卡）。
* 对于嵌入，如果您的样本图像总是相同的，您要么忘记在样本提示词中放置 `<embedding>`，要么忘记在概念的描述中放置。
### 随机化描述
* 您可以添加多个描述。在 txt 文件中每行一个。它会为每个 epoch 随机选择一个。
### 多分辨率训练
* 您可以通过在分辨率字段中指定逗号分隔的数字列表来同时训练多个分辨率。每一步将从列表中随机选择一个分辨率进行训练。这在某些情况下可能有帮助
* 示例：将训练分辨率设置为 896,960,1024,1088,1152（上下 64px），并添加 5 个相同的概念，准备好至少 1152 分辨率，分辨率覆盖分别设置为 896,960,1024,1088,1152，将您需要的 epoch 除以 5，因为它会使用 5 倍更多的步骤。
* 可选地在概念上使用 [分辨率覆盖](https://github.com/Nerogar/OneTrainer/wiki/Concepts#image-augmentation-tab)。

---


### 数据集、批量大小和训练策略（by Caith）

一般来说，您的批量大小应该约为总数据集大小的 **0.2%**，最大不超过 **512**。  
然而，这个指南主要适用于中等至大型数据集（大约 **10,000** 到 **10,000,000** 张图像）。

#### 小型数据集（1–1,000 张图像）

当您只有一个小型数据集时，事情会变得更复杂。

-   您的批量大小必须保持在总数据集大小的 **10%** 以下，
-   但如果需要，它可以**显著大于** **0.2%**。

### "批量大小"有什么作用？

对于**非常小的数据集**，以下几点特别相关。_（对于较大的数据集，只需坚持大约 0.2%，除非您有充分的理由不这样做。）_

1.  **小批量大小**
    
    -   **优点**：模型更频繁地更新其理解。每个新示例都可以立即影响学习，这有助于抓住小型数据集中的独特细节（例如，特定的风格或物体）。
    -   **缺点**：因为它一次只看到几个示例，所以更新可能是"嘈杂的"。模型可能对那几张图像中的特性反应过度，导致潜在的过拟合（尤其是在 10–100 张图像的数据集上）。

2.  **大批量大小**
    
    -   **优点**：模型在调整之前看到更广泛的图像集，导致更稳定和一致的学习。这就像一次批改一整堆作业，而不是逐张批改——基于单个奇怪的例子过度纠正的可能性更小。
    -   **缺点**：只有 10–1,000 张图像，大批量大小可能意味着整个数据集只需几个批次就处理完了。这减少了更新的次数，可能会阻碍模型捕捉描述中细微差别的能力。（因此我们坚持不超过最大数据集的 10%！）

### 这意味着什么？

-   如果您正在训练一个**单一、非常明显的概念**（比如您自己的脸），**较低的批量大小**实际上可能会有帮助。
-   您包含的**不同概念越多**（只要它们在描述中被一致地标记），您可能需要的批量大小就**越大**，以防止这些概念相互渗透。

---


这些见解来自 Discord 的一次讨论，Caith 在其中解释了他的方法。有关完整的策略和示例，请参阅 Civitai 页面：[Juno for Flux (by Caith) – Overwatch 2](https://civitai.green/models/714292/juno-for-flux-by-caith-overwatch-2)。

![在此处输入图像描述](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/441b9b0e-20d6-42dd-af8d-cdc9be308ef5/width=525/441b9b0e-20d6-42dd-af8d-cdc9be308ef5.jpeg)

**数据集准备**

-   Caith 通常将 30% 的数据集用于特写图像，50% 用于他希望最终输出 resemble 的内容，20% 用于可能与他的 LoRA 或微调一起使用的概念。这有助于模型更有效地适应。
    -   例如，如果角色与赌博相关，那额外的 20% 可能包括纸牌、空赌场、繁忙的赌场、酒吧等图像。
    -   在处理特定风格时，他会添加约 20% 的数据集，其中包含_不_属于该风格的图像（例如，汽车、人物、背景）。这就像有针对性的"正则化"数据，而不是随机填充。

**批量大小**

-   保持在总数据集的 10% 以下，但至少 1%。如果您受 VRAM 限制，可以使用梯度累积（累积步骤）来有效增加批量大小。

**描述和训练策略**

-   这些在 Civitai 页面上有解释（使用 Lokr 和 Simple Tuner），但该过程可以在 OT 上复制，使用 DoRa，或对 SDXL 进行全微调。
-   对于 Flux，您需要足够的正则化数据集，因为您无法使用 Lokr。

---

### 使用 One Trainer 训练 SDXL LoRA 的（个人经验）指南 by [Corleone11](https://www.reddit.com/user/Corleone11/)
Corleone11：本指南涉及训练写实人类 LoRA 的主题——这个概念可能所有 SD 基础模型都已经知道了。这是一个快速教程，介绍我如何创建非常好的结果。我没有编程背景，我也不知道为什么我使用某个设置的来龙去脉。但通过大量测试，我发现了什么有效，什么无效——至少对我来说是这样。:)

[Reddit 链接](https://www.reddit.com/r/StableDiffusion/comments/1gvp073/a_personal_experience_guide_to_training_sdxl/)

### 图像结果差异诊断，来自 Alaiya @ OnePawProductions：
![Ai 错误类型](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/363a2504-4e10-4315-9d0e-68cb56347fea/dgplseb-00038eba-6c9e-4c19-9c7f-1bb2e57de060.png/v1/fit/w_828,h_496,q_70,strp/ai_errors_in_sdxl_lora_training__using_onetrainer_by_onepawproductions_dgplseb-414w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzY4IiwicGF0aCI6IlwvZlwvMzYzYTI1MDQtNGUxMC00MzE1LTlkMGUtNjhjYjU2MzQ3ZmVhXC9kZ3Bsc2ViLTAwMDM4ZWJhLTZjOWUtNGMxOS05YzdmLTFiYjJlNTdkZTA2MC5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.4CnHWHT_nOnNVbr8AlreAl3koI-fzGOYMo_nNNPIuZg)

在这里，我们看到了在采样过程中生成的三种不同的噪声图像示例。

在第一张图像中，输出完全是噪声，您可以从随机性和高度的色彩对比中看出。这表明分辨率不匹配。如果正在训练的 LORA 是 SDXL（分辨率为 1024x1024），而您将采样图像输出设置为 512x512，它将无法生成连贯的图像。

在第二张图像中，我们看到一些有凝聚力的东西，但有噪声。有渐变，既有柔和的也有高对比度的颜色，它作为一张图像起作用，尽管是有噪声的。没有真正可识别的形状。当您的唯一标识符对 AI 来说无法解析时，可能会发生这种情况，例如"lkjasdf"，或"myGreatOC"，或者在这种情况下是"Muse"。当 AI 查看您的数据集并学习将图像和标签与唯一标识符相关联时，它应该在 2-50 个 epoch 之间收敛（解析为与您的数据集相关的可识别和可复制的模式），并变得越来越清晰。

在最后一张图像中，我们看到一张可识别的图像，尽管它非常不正确且与数据集无关。当使用的唯一标识符带有 AI 认为与这些词/那个词相关的其他概念时，可能会发生这种情况。唯一标识符可能是类似"Hannah Bearlet"，或"myElegantCharacterBearnois"，或类似的东西。这张图像来自"Taylor Hebert"，收敛发生得非常早，在第 2 个 epoch，当 AI 意识到 Taylor Hebert 实际上不是一只熊时。

![Ai 不识别数据](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/363a2504-4e10-4315-9d0e-68cb56347fea/dgplib3-32188c19-e92b-4901-ba44-7d061be00dc4.png/v1/fit/w_828,h_372,q_70,strp/onetrainer_troubleshooting_by_onepawproductions_dgplib3-414w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NTc2IiwicGF0aCI6IlwvZlwvMzYzYTI1MDQtNGUxMC00MzE1LTlkMGUtNjhjYjU2MzQ3ZmVhXC9kZ3BsaWIzLTMyMTg4YzE5LWU5MmItNDkwMS1iYTQ0LTdkMDYxYmUwMGRjNC5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.X8p4-sXQSOoomMPRtSQ7h2w3rVJWKdDBpahT4QjK8Do)

在这个 100 个 epoch 的训练运行中，我们看到 AI 没有识别并将数据集连接到图像训练和输出。第一张图像是纯噪声，因为它是 SDXL，它试图包含一些文本。但即使随着 epoch 的推进，图像仍然是有噪声的，尽管分辨率越来越清晰。

这可以通过考虑 OneTrainer 如何读取您的数据来解决。在 OneTrainer > 概念 > 通用中，您会发现：
* 每个样本来自文本文件
* 来自单个文本文件
* 来自图像文件名

来自每个样本的文本文件：这将从与您的图像同名的 .txt 文件中读取数据，例如 image1.png, image1.txt。这让您可以有比使用图像文件名更长的描述和更多与图像相关的标签，图像文件名（至少在 Windows 中）对图像标题的长度有设定的上限。

来自单个文本文件：这将读取单个文本文件并将其应用于所有图像，类似于（我相信）文本反转嵌入的过程

来自图像文件名：这将从图像文件名读取数据，这可能是一个节省工作量的有用措施，但请注意，图像文件名通常有一定的长度限制。如果超过，它可能会损坏您的文件（我的就是这样）。

![Ai 运行良好](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/363a2504-4e10-4315-9d0e-68cb56347fea/dgplm9d-dd97e45e-60dd-4799-ab6f-9268e5d3da16.png/v1/fit/w_828,h_506,q_70,strp/onetrainer_troubleshooting__ai_functioning_well_by_onepawproductions_dgplm9d-414w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzgxIiwicGF0aCI6IlwvZlwvMzYzYTI1MDQtNGUxMC00MzE1LTlkMGUtNjhjYjU2MzQ3ZmVhXC9kZ3BsbTlkLWRkOTdlNDVlLTYwZGQtNDc5OS1hYjZmLTkyNjhlNWQzZGExNi5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.Ry2ChFSalxtZwRRp62OA5tNIqUkIemoDVNrGE_yGdNY)

在这里，我们看到当过程顺利时可以预期的结果。我的采样文本"Muse jumping"起初在早期 epoch（少于 10 个）被 AI 渲染为摇滚乐队 Muse 跳跃。在 epoch 的中期阶段（10-50 个 epoch），我们看到人物开始发展出动物特征，因为数据集由 Muse（粉色印花布吉祥物）的镜头组成。到后期的 epoch，我们看到收敛已经发生，AI 现在识别出标签"Muse"（或者，myMuse）属于数据集中的图像。我们看到了数据集中被标记的投影、灰色背景、风格和特征。


### 关于梯度累积和批量大小的注意事项，by Alaiya @ OnePawProductions

梯度累积和批量大小（即，训练期间引用了多少图像，然后在使用 LORA 期间）可以对 LORA 的输出产生很好的影响，既有积极的也有消极的。您可以随着时间的推移通过使用您的 LORA 看到这种模式，当由于梯度累积为 1（引用的图像是单张图像，而不是许多图像）时，一些图像非常明显地是从一张或另一张特定图像衍生出来的。

梯度累积和批量大小为"1"有优点和缺点：

优点：数据集中相关概念之间的更多差异化，例如，我正在为 Taylor Hebert 制作一个 LORA...但是哪个 Taylor？漂亮的！Taylor？经典！Taylor？工匠 Taylor，还是来自某部特定同人小说的变体？梯度累积为 1 时，每次我运行生成会话（使用组合提示扩展，我强烈建议用于数据集多样化），我都会得到大量不同的图像，每张都来自单个图像。这些被放入不同的文件夹，针对不同的变体，这样我的 Taylor LORA 可以调整灵活性。这是我如何为 LORA 设计全 AI 输入数据集的重要部分。希望避免模型崩溃。因此使用 GA 为 1 生成的图像可能会产生漂亮变体、经典/完美变体、工匠变体或 Skitter 变体的变化，通过使用组合动态提示扩展，这些变体可以被用来做各种不同的事情，穿不同的衣服，在不同的背景下，有不同的面部和身体表情。

缺点：如果您在提示词中引用了来自几张图像的标签，但使用 GA 为 1 训练的 LORA，您可能最终会得到像双头双胞胎这样的疯狂事物（据我所知，这是使用"翻转复制"数据多样化策略的不幸结果。我认为翻转复制是有用的，尤其是在双侧对称不重要的情况下）。它也可能使创建一个有凝聚力的"外观"变得困难，例如，完整的面部保真度有点难以实现。通过使用更高的 GA，您为每个输出引用几张图像，这可以帮助将面部保真度解析为更有凝聚力的整体。

### 使用 Prodigy 的 LoRA 训练建议 by Malessar
* 对 Lora 秩和 alpha 使用相同的值。8/8 对于一个人来说似乎不错，16/16 可能更好但灵活性较差，除非有非常好的图像描述。注意 alpha 需要等于或低于 rank。
* 使用 Prodigy 优化器，开启偏差校正，权重衰减为 0.01（默认是 0.1，也可以工作）。
* 调度器 Cosine
* 对 TE 和 Unet 使用 1 的学习率，注意：TE 是可选的，对于 SDXL 很难训练，由您决定是否使用它，您可以尝试 TE 1 或 2，因为它们的工作方式不同。
* 批量大小：您的 vram 能容纳多少，2 的倍数看起来更有效。
* 如果您的 VRAM 可以处理，将数据类型设置为 float 32（训练和模型选项卡）。但预设附带的默认值工作正常。

### Stable Cascade LORA 训练 by Drift Johnson
[Stable Cascade LORA 训练（Youtube）](https://www.youtube.com/watch?v=dmSZ5TWEWTQ)

[使用 Onetrainer 进行 Stable Cascade LORA 训练（Civitai）](https://civitai.com/articles/4253/stable-cascade-lora-training-with-onetrainer)

### ZLUDA 的奇怪问题 by Heasterian
* 如果您在使用 ZLUDA 时每隔 x 个 epoch 就会得到奇怪的有噪声的非 ema 样本，请检查这些 epoch 的损失是否不低。如果是这样，请关闭 Autocast Cache。看起来这是导致此问题的原因。

### 低 VRAM 微调视频教程 by SECourses
* [133 分钟完整视频教程](https://github.com/Nerogar/OneTrainer/wiki/Full-Stable-Diffusion-SD-&-XL-Fine-Tuning-Tutorial-With-OneTrainer-On-Windows-&-Cloud-%E2%80%90-Zero-To-Hero)

### ZLUDA 注意事项 by Calamdor
Zluda 正在开发中，目的是让 AMD 显卡能够与 CUDA 一起工作。目前 RoCm 仅在 Linux 上可用，这限制了 AMD 显卡在 Windows 上的使用。
ZLUDA 最好的分支在这里（因为原始开发者发布了这项工作，但不会继续开发）(https://github.com/lshqqytiger/ZLUDA)
没有必要使用这个 ZLUDA 包，OneTrainer 将允许在 install.bat 过程中安装 ZLUDA 作为选项，它将安装到 OneTrainer 的子文件夹中。
关于让它工作的最佳信息和注意事项目前在 SD.next wiki 上(https://github.com/vladmandic/automatic/wiki/ZLUDA)
关于 ZLUDA 的一些注意事项：
- 检查您的设备。(https://rocm.docs.amd.com/projects/install-on-windows/en/develop/reference/system-requirements.html) 如果您的卡在两列中都没有复选框，您将需要下载 SD.next wiki 上的 Rocmlibs 特殊库或自己构建它们。
- 确保您安装了 AMD 专业驱动程序（可选？）和 HIP 框架。链接在 SD.next wiki 上。
- 要有耐心。ZLUDA 在首次使用时需要编译。没有信息显示它正在这样做，这可能需要相当长的时间。这种编译可能针对每次出现的新 CUDA 函数（第一次）。
- XFormers 不工作，所以训练时使用默认或 SDP。
- ZLUDA 是一个 CUDA 包装器，所以使用 CUDA 作为设备。
- 请注意标准 ZLUDA 的限制，特别是关于集成 AMD 显卡的限制。

### 低 VRAM 配置 - by efhosci
使用正确的设置，在 OneTrainer 中几乎可以在使用 SD 1.5 训练时将 VRAM 使用量控制在 3 GB 以下，这对于较旧的笔记本 GPU、低端桌面 GPU 或 VRAM 有限的"挖矿"GPU 来说可能是可行的。在较旧的显卡上可能不会很快，但对于单个概念的 LoRA，您可能可以在一小时内完成，相比之下在 CPU 上运行可能需要几个小时。免责声明 - 我并不真正理解大多数这些设置的底层机制，我只是观察更改它们如何影响 VRAM 使用。系统运行 Linux Mint，GPU 是 P100，VRAM 使用量使用 nvidia-smi 监控。信息截至 2024 年 5 月是最新的。

以下是似乎有帮助的主要事项，或者我验证没有影响的事项。任何未列出的可能都没有影响 - 我没有调整每个设置，但任何乘以学习率或噪声强度或类似的东西都不太可能对内存使用产生影响。大致按选项卡顺序排列：
- 您是否使用"修剪"或"完整"模型无关紧要，至少在以下权重设置下是这样。修剪的模型文件大小应该在 2 GB 左右，而完整检查点大约是 5-6 GB。
- 如果可能，将"模型"中的所有权重设置为 float8，否则设置为 float16。最大的影响似乎是 UNet，将其设置为 float8/16 之间的差异约为 0.8 GB。文本编码器约为 100 MB，VAE 没有明显差异。将输出数据类型设置为 float8 会导致采样和保存错误，所以保持为 float16，请注意，所有阶段的低精度可能会导致输出质量问题。
- 开启潜变量缓存可节省约 100 MB。
- 使用 ADAMW_8BIT 而不是 ADAMW 可节省约 50 MB，无论模型权重设置为 float16 还是 float8。ADAFACTOR 大致相同。一些优化器特定的设置可能会影响 VRAM 使用，但默认值应该没问题。有关更多详细信息，请参阅 [这里](https://github.com/Nerogar/OneTrainer/wiki/Optimizers)。
- 批量大小需要设置为 1 - 增加到 2 会使使用的 VRAM 增加一倍以上（从 2.8 GB 增加到几乎 7 GB）。批量大小 3 和 4 也都在 7 GB 左右，增加到 8 大约是 8.3 GB，在 32 时似乎达到 13.5 的峰值，这表明批次中每增加一张图像大约需要 250 MB（在 512 分辨率下）。
    - 更新：在对 SDXL 进行了一些进一步测试后，我认为这里报告的 VRAM 使用量可能不准确 - 我不确定发生了什么，但似乎有些文件可能保留在内存中而没有清除，因此 nvidia-smi 报告的内存使用量比 OneTrainer 实际使用的要多。批量大小 2 或 3 可能能够装入 4 GB 的 VRAM。
- 累积步骤在增加到 1 以上时只有 20 MB 或更少的轻微影响。增加这应该在功能上类似于更高的批量大小，但速度要慢得多。比较批量大小 8 和梯度累积步骤 1 与反过来，前者完成速度快了两倍以上。
- 与"默认"注意力相比，xformers 和 SDP 都节省约 2.8 GB，大约是其他方式的一半，所以始终启用其中任何一个。
- 开启梯度检查点也节省了近 2 GB，但速度至少降低了 30%。
- 将训练数据类型设置为 float16 而不是 float32 节省约 80 MB。
- Autocast 缓存提到了速度和内存的差异，但我在开/关之间没有看到差异。
- 768 的图像分辨率（在"训练"和活动概念上）与两者都在 512 相比差异约为 0.7 GB，所以保持最大分辨率设置为低。
- AlignProp 使用大量 VRAM，EMA 几乎没有/没有影响。对于简单的 LoRA 或嵌入训练，都不需要启用。
- 启用掩码训练并没有增加太多 VRAM 使用，可能只有几 MB，但目前在启用潜变量缓存时它不起作用。
- 不同的损失权重函数只有几 MB 的差异。
- 在采样期间，对于 512x512 的图像，VRAM 峰值约为 2.7 GB。这比训练期间稳定下来的要少（使用上述所有优化时约为 2.8 GB），所以不用担心禁用采样来节省 VRAM。768x768 的样本图像似乎稳定在 2.8 GB 左右，但在切换到训练时可能会短暂飙升到略高于 3 GB，所以如果您接近极限，不要将分辨率提高太多。
- 备份或保存期间 VRAM 使用没有明显峰值。
- 我之前所有的测试都是在 LoRA 秩 16 下训练的 - 秩 32 高约 60 MB，秩 64 高约 200 MB，秩 8 低约 40 MB，所以大致是线性的。秩 16 对于大多数目的应该足够了。Alpha 和 dropout 对 VRAM 没有任何影响。
- 将 LoRA 权重数据类型从 float32 更改为 bfloat16 可能节省了 30 MB 的 VRAM，但是我使用的是不支持它的旧卡，所以如果使用 >3000 系列的卡，好处可能更高 - 但那样您就不太可能有严重的 VRAM 限制。
- 与 LoRA 一起训练额外的嵌入会增加约 80 MB 的 VRAM 使用量，更高的 token 数没有任何影响。

通过上述所有优化，程序在运行时最高达到约 2.8 GB。对我来说训练速度约为 1.1 it/s，总共有 1000 个步骤（加上一些采样时间），总训练时间约为 1100 秒，即 19 分钟。我使用的卡在 TechPowerup 上列出的 fp16 为 19 TFLOPS，fp32 为 9.5 FLOPS，您可以根据这一点估计其他 GPU 的训练时间。例如，使用 T1200 笔记本 GPU（7.3/3.6 fp16/fp32，4 GB VRAM），理论上应该需要大约 2.5 倍的时间，大约 50 分钟，尽管较新的 GPU 添加了张量核心，这意味着它们在实践中可能表现更快。由于内存速度、缓存和一些其他因素，也很难估计差异。如果卡列出的 fp16 低于 fp32，或者没有列出，您可以假设出于实际目的它等于 fp32。非常旧的 Nvidia GPU（超过 10 年）可能由于软件支持问题根本无法工作，AMD 可能类似。

[这是一个在 3 GB 以下训练的示例配置文件。](https://github.com/Nerogar/OneTrainer/files/15445637/lowvram-3GB.json) 与学习率和 epoch 相关的设置可能需要根据您的数据进行更改，但我能够使用它得到一个还算不错的单字符 LoRA。

如果您有 4 GB 的 VRAM 可用，最有益的更改可能是将模型权重更改为 fp16，训练数据类型更改为 fp32，使用非 8 位优化器，也许将训练分辨率提高到 640。对我来说这刚好低于 4 GB。有 6 GB，您可能可以关闭梯度检查点以提高速度，或者您可以尝试更高的分辨率和浮点精度。


更新（2024 年 8 月）：我也对 SDXL 做了一些快速测试 - 使用与上述相同的设置（权重为 fp8，潜变量缓存，批量 1，SDP 开启，梯度检查点开启等），但分辨率设置为 1024，VRAM 使用峰值约为 5.8 GB，运行速度约为 3.5 s/it。将分辨率降低到 768 甚至 512 似乎几乎不影响使用的 VRAM。批量大小为 2 时，VRAM 使用显示约为 15.1 GB，运行速度约为 5 s/it，然而，似乎报告的 VRAM 使用量中有很多是"剩余"文件，这些文件在内存几乎满之前不会被移除，真正的 VRAM 使用量可能低于 8 GB。我在 8 GB 的卡上测试了相同的配置，看起来 fp8 下的批量 2 刚好能够装入 VRAM，尽管速度慢得令人痛苦。

将所有权重增加到 fp16 在批量大小为 1 时达到约 8.6 GB，如果将文本编码器权重设置为 fp8 或只训练一个文本编码器，您应该能够控制在 8 GB 以下。在批量大小为 2 时，VRAM 稳定在约 10.4 GB - 我认为这是因为我上面提到的，在 fp16 下内存使用增加，它会更早清除内存，因此似乎在更低的内存下运行。理论上这可以装入 10/2080 Ti 奇怪的 11 GB 内存，但我无法确认。无论哪种方式，如果需要，您应该能够只用 6 GB 显存训练 SDXL 模型，尽管 8 GB 会更容易使用。


### 包含伪影或质量低于预期的图像 by Lim1tBreak

如果您已经用良好的数据集、提示词和训练参数训练了某个概念的 LoRA，但仍然得到质量不佳的结果，例如下图，请尝试对生成应用高分辨率修复。

![没有高分辨率修复](https://i.imgur.com/H4Iz5Ah.png)

在 A111 中，这就像启用高分辨率部分一样简单。

在 ComfyUI 中，从第一个 Ksampler 的输出中获取潜变量，将潜变量至少放大 1.25 倍，并将该潜变量用作相同 Ksampler 的输入，去噪强度为 0.5-0.7。将此技术应用于上图产生了以下结果：

![已应用高分辨率修复](https://i.imgur.com/cEmvo8F.png)


### 使用 PixArt Sigma 训练 by Ejektaflex

到目前为止，PixArt Sigma 在训练方面似乎相当有能力 - 然而，在某些情况下，如果用于训练 PixArt，Prodigy 可能会大大低估学习率。如果样本似乎没有显示学习的迹象，或者学习很慢，那么将优化器设置中的 `d_coef` 增加甚至**很大**的幅度可能是有益的。根据传闻，1.0 太小了，8.0 导致了模型崩溃，`d_coef=4.0` 达到了学习的最佳点，大致相当于使用余弦退火（只有一个周期的硬重启余弦）时 SDXL 的类似学习速度。

另一个选择是增加"Initial-D"来对抗较低的起始 LR。您设置得越高，Prodigy 需要补偿的就越少。然而，Prodigy 只会*增加* LR，永远不会减少它，所以太高的 Initial-D 值很可能对您的模型来说 LR 太高，而 Prodigy 永远不会降低自己来补偿！

此外，当用于训练嵌入时，Prodigy 对于猜测学习率几乎毫无用处（截至 2024-06-19）。选择的学习率（稳定在 1e-5）太小，甚至无法促进样本图像的变化。使用学习率为 **0.1** 的 ADAMW 优化器似乎给出了结果，尽管还没有进行足够的测试来确定最佳范围。

尽管 Prodigy 可能看起来很糟糕，**它仍然是一个有用的工具**来找到最佳 LR，只要您不介意进行一次次优的训练会话。我通常让 Prodigy 在一次训练中自己找到 LR，然后查看它找到的峰值 LR。使用该峰值 LR，我要么：
* 进行另一次 Prodigy 训练，d_coef=1.0，Initial-D 等于该峰值 LR
* 使用 ADAMW 进行训练，LR 等于该峰值 LR

这里最重要的要点是，PixArt、Prodigy 和可能其他自适应优化器可能会低估学习率，并且是学习缓慢的原因。这也可能存在于其他 DiT 模型中，例如 Stable Diffusion 3，不过时间会证明一切。


### 在 AMD/Linux 上让 OneTrainer 工作 by Thomas

我已经确认 OneTrainer 在 Arch Linux 上使用 ROCm 可以很好地用于 SDXL LoRA 训练。不过，在它顺利运行之前确实需要一些调整，所以我在这里记录了我的发现。希望这能为其他人省去头痛。

- 我的卡是 RX 6700 XT（12 GiB VRAM），但其他卡应该也一样好用。
  - 这张卡进行 1024x1024 SDXL LoRA 训练需要 3-4 秒/步，与我尝试过的所有其他训练软件相当。

#### 安装和设置

- 您可能需要特定版本的 Python 才能让安装顺利进行。我在安装 OneTrainer 之前使用 `pyenv` 将版本设置为 `3.10.9`。
- 如果您进行手动安装，您需要使用 `pip install -r requirements-rocm.txt` 而不是普通的 requirements.txt 文件。如果您只是使用 `install.sh` 脚本，它应该会自动解决问题。
- 在训练之前，确保您的用户在 `render` 和 `video` 组中，使用 `sudo usermod -a -G video,render $USER` 并重启。使用 `id` 命令确认您的组成员资格。
- 确保您使用的是 `amdgpu` 内核驱动程序（用 `lsmod | grep amdgpu` 检查）
- 如果您在 Xorg 上，请确保您使用的是 `xf86-video-amdgpu` 模块；您可以查看您的 `Xorg.0.log` 来确认这一点。

#### 环境变量

- 您可以将环境的更改（`export FOO=BAR`）放入 `start-ui.sh` 文件的开头，以便在每次启动时应用它们
- 如果您的卡技术上不支持 ROCm（比如 6700 XT），您可以用 `export HSA_OVERRIDE_GFX_VERSION=10.3.0` 假装它是另一张卡
- 如果您收到提到 `hipblaslt` 的错误，用 `export TORCH_BLAS_PREFER_HIPBLASLT=0` 来解决它
- 如果您因内存损坏而崩溃，例如"malloc(): corrupted top size"，您可以通过使用 `tcmalloc` 来解决这个问题。安装 `google-perftools` 并使用 `LD_PRELOAD=/usr/lib/libtcmalloc.so.4` 启动 OneTrainer。我使用 `jemalloc` 也有很好的经验，改为预加载 `/usr/lib/libjemalloc.so.2`
- 如果您在 `~/.bashrc` 中为其他训练软件设置了环境变量，它们可能会干扰 OneTrainer 并导致难以调试的问题。在这种情况下，尝试在启动 OneTrainer 之前取消设置环境变量，如 `HCC_AMDGPU_TARGET`、`PYTORCH_HIP_ALLOC_CONF` 和 `HIP_VISIBLE_DEVICES`
- 如果您因内存碎片而有 VRAM 问题，尝试设置 `export PYTORCH_HIP_ALLOC_CONF="max_split_size_mb:128"`。
  - `max_split_size_mb` 的不同值可能会有帮助，具体取决于您的设置；512 对我不起作用，但 128 起作用了。
  - 您也可以尝试 `garbage_collection_threshold` 设置。
  - 更多选项可以在 [pytorch 文档](https://pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf) 中找到


#### 初始训练设置

- 即使您使用的是 HIP/ROCm，您仍然需要输入"cuda:0"作为您的训练设备，在"通用"选项卡训练设置下输入"cpu"作为您的临时设备。
- 为了便于调试，尝试从最简单、最基本的训练设置开始
  - 一旦您的训练顺利运行，您就可以一次更改*一个*变量，并检查在您过渡到更复杂的训练设置时一切是否仍然有效。
- 为了更快地进行故障排除，从低训练分辨率（例如，512x512）和低 LoRA 秩（例如，8）开始
  - 这也节省了足够的 VRAM，您可能可以关闭梯度检查点，进一步简化设置
- 如果您在早期缓存期间（实际训练开始之前，您在控制台中看到 `step: 1/30`）出现内存不足错误，尝试将"通用"选项卡下的 `Dataloader Threads` 设置为 1。
- VAE 解码在新分辨率上第一次运行时总是很慢。这是正常的，所以要有耐心。
  - 这似乎是一个普遍的 AMD 硬件问题，因为它也发生在其他训练软件和不同的卡中。
  - 因此，如果您的第一次运行看起来像挂起了，尝试让它单独运行 5-10 分钟。之后事情*会*加速。
  - 考虑禁用 `训练前清除缓存`，这样您就不必每次都等待这个初始 VAE 解码。请注意，每当您更改数据集（"概念"）时，您都必须清除缓存。
- 您可以通过启用分块解码让 VAE 解码变得超级快
  - 分块使缓存变得非常快，并支持在 1024x1024 下采样而不会耗尽内存。
  - 要启用分块，向源代码添加一行。
  - 打开文件 `OneTrainer/modules/modelLoader/StableDiffusionXLLoRAModelLoader.py` 并找到显示 `def load(` 的行
  - 接下来的几行，直到显示 `return model` 的行，包含 `load` 函数的代码
  - 在 `return model` 行之前立即添加一行新代码，内容为 `model.vae.enable_tiling()`，这样您最终会得到类似 [这样](https://gist.github.com/tehybel/656a3f8fa8df20cf8665b1793fb1745a) 的东西

#### Linux 上训练期间的卡顿和延迟

- 如果您没有很多 RAM（<= 16 GiB），并且您的系统在训练期间变得无响应和卡顿，这可能是因为内存内容被交换到磁盘。
  - 您可以通过在训练时运行 `watch -d -n1 free -mh` 来检查是否发生这种情况
  - 如果您的系统正在交换，您可能想尝试调整 `vm.page-cluster`、`vm.swappiness` 和 `vm.vfs_cache_pressure` 以获得更好的性能。还可以考虑对 zram/zswap 开/关进行基准测试。
  - 我还发现 `sudo sysctl vm.compaction_proactiveness=35` 有助于随着时间的推移保持训练过程顺利进行。

#### 调试冻结和挂起
- 如果您在训练期间遇到完整的系统锁定/冻结，这可能是由于 amdgpu 驱动程序中的错误或硬件问题。
- 添加内核参数 `amdgpu.ppfeaturemask=0xfff7ffff` 允许更好地控制 GPU 电压和频率，这可能有助于稳定您的系统。
  - 如果您的系统冻结，考虑暂时增加一点电压（慢慢增加到 +50 mV 左右；更多可能不安全！）来检查这是否有助于稳定性。
  - 暂时降低最大内存时钟也值得一试，看看这是否是由于高速或电压过低导致的 VRAM 损坏问题
  - 您可以通过设置 `ppfeaturemask` 内核参数以允许超频，然后重启，然后使用例如 `lact` 或 `corectrl` 来设置这些值。
- 我通过设置 `amdgpu.gpu_recovery=1 amdgpu.noretry=0` 并测试 `amdgpu.reset_method` 的不同值取得了调试进展。非默认的 `reset_method=3` 意味着不是完整的系统冻结，只有 Xorg 崩溃。从那里我可以读取 `dmesg` 中的错误并谷歌搜索。
  - 您可以在 [内核文档](https://docs.kernel.org/gpu/amdgpu/module-parameters.html) 下找到更多可以尝试和调整的参数
- 当运行任何类型的基于 `ROCm` 的软件时，包括 SD 训练和推理，我的系统会完全冻结。dmesg 中的错误包括：
  - `amdgpu: Queue preemption failed for queue with doorbell_id: 80004008` 到 `amdgpu: GPU reset(1) succeeded`
  - `amdgpu: ring gfx_0.0.0 timeout, signaled seq=550221, emitted seq=550223` 到 ` VRAM is lost due to GPU reset`
  - `[drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125`
  - `amdgpu: Failed to evict queues of pasid 0x8006` / `amdgpu: Failed to evict process queues`
- 几个月后补充：我所有不稳定的根源都是 `GFXOFF, DS_GFXCLK, BACO` 功能。我通过使用 MorePowerTool 进行固件写入禁用了所有三个。从那以后我有了 100% 的稳定性。
- 冻结也可能是硬件问题。检查您的 PSU 是否足够强大，您的 GPU 是否没有过热，以及它是否正确地坐在 PCIe 插槽中。还要检查它的电源连接器。

 

#### 其他提示和技巧

- 您可以使用 `工具` -> `分析工具` -> `转储堆栈` 来查看程序挂在哪里或是什么导致了减速
- CAME 优化器对我来说似乎比其他优化器非常有效，我也听说其他人在 AMD 硬件上提到过这一点
- 我发现 `lact` 软件很方便，可以更改我卡上的电压和最大频率。
- 您还可以使用 `radeontop`、`amd-smi` / `rocm-smi` 和 `corectrl` 来控制和监控您的 GPU。
- 要在 AMD 卡上使用 8 位优化器，请按照 [AMD 说明](https://rocm.blogs.amd.com/artificial-intelligence/bnb-8bit/README.html) 从源代码构建 ROCm-bitsandbytes。具体来说：
  - 使用 `git clone --recurse https://github.com/ROCm/bitsandbytes && cd bitsandbytes && git checkout rocm_enabled` 获取源代码
  - 使用 ` pip install -r requirements-dev.txt && cmake -DCOMPUTE_BACKEND=hip -DBNB_ROCM_ARCH="gfx1030" -S .  && make` 构建它
  - 然后在激活您的 OneTrainer `venv` 后，使用 `pip install .` 从当前文件夹安装 bitsandbytes
