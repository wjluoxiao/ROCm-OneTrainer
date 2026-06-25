欢迎来到 OneTrainer！

OneTrainer（OT）是您训练[扩散模型](https://en.wikipedia.org/wiki/Diffusion_model)的一体化解决方案。

这是针对新用户的针对性介绍。这**不是**一个逐步教程。您仍然需要阅读选项卡说明和 GUI 中的标签工具提示。

## 1. 我在看什么？

在左上角，"OneTrainer" 标志旁边，您会发现一个空白的下拉列表，用于 'configs'（预设）。预设充当您所有训练预设的保存文件。它们**不是**您的模型名称。作为初学者，为您想要训练的模型选择一个默认值。

![image](https://github.com/Nerogar/OneTrainer/assets/18110006/cb7e81a4-2316-492a-bd79-a3a9c957694a)

在其下方，有一个选项卡栏，活动选项卡以蓝色高亮显示。点击 `general` 选项卡。

![image](https://github.com/Nerogar/OneTrainer/assets/18110006/816303ac-b6ed-42e2-b941-3f0699b18ea7)

工作区目录是您的备份、中间保存和其他内容存放的地方，最终输出进入 `models` 

如果您有 RTX 4090，考虑将数据加载器线程增加到 8（请谨慎，因为设置过高可能会导致 VRAM 问题）。

## 2. 模型选项卡

导航到 `model` 选项卡并观察其中的内容，目前我们将保持默认。如果您想使用自定义模型，请设置 `Base model` 及其指向 HF 链接或本地目录的路径。

在训练之前，您可能想要设置 `Model Output Destination`。这将是您训练输出的文件名，例如：`models/ModelMyTry1.safetensors`

## 3. 数据选项卡

导航到 `data` 选项卡，并确保所有内容都已打开（这些默认情况下应该是打开的）。作为初学者，您希望所有这些选项都启用。

<img width="289" height="190" alt="image" src="https://github.com/user-attachments/assets/8ef6a300-a7f8-4b8a-ae18-0605d92883a9" />

## 4. 概念选项卡（又名数据集）

导航到 `concept` 选项卡。这是您配置数据集的地方，可以作为单独的文本文件或在图像名称中。虽然描述是可选的，但建议使用。90% 的工作是收集高质量、多样化的图像并创建高质量（且多样化）的描述。

您也可以使用工具选项卡打开您的数据集并使用自动描述器/标签生成器生成描述，但这超出了本指南的范围。

点击 `add concept`，然后点击新添加的项目。这将打开一个新的模态框（窗口）。

![image](https://github.com/Nerogar/OneTrainer/assets/18110006/90e1bfec-2683-4f57-8bd3-129d8224790c)

在 `Path` 中提供您的数据集路径。在 `Prompt Source` 中，说明您如何为图像添加描述。作为初学者，您应该使用 img-txt 文件对，通过设置 "From text file per sample" 并创建文件对来实现，例如 `001.jpeg` & `001.txt`

有关概念选项的更多信息，请查看专门的 [Concept](https://github.com/Nerogar/OneTrainer/wiki/Concepts) 页面。

有关宽高比和分桶的详细信息，请查看 [AR Buckets](https://github.com/Nerogar/OneTrainer/wiki/Aspect-Ratio-Bucketing) 页面。

## 5. 训练

训练选项卡是您调整训练设置的地方。稍后当您定义好数据集后，我们建议您在首次运行时坚持使用默认值。查看此 [页面](https://github.com/Nerogar/OneTrainer/wiki/Training) 了解更多信息

## 6. 采样选项卡

采样使用您当前正在训练的模型生成图像，使您能够直观地观察其进度。作为初学者，您可能还不知道要寻找什么，但利用它很重要。

请参阅 [Sampling](https://github.com/Nerogar/OneTrainer/wiki/Sampling) 了解更多信息

## 7. LoRA 选项卡

接下来转到 `LoRA` 选项卡

`LoRA rank`：对于 SD1.5，保持默认值 16，对于 SDXL，尝试 8 或 16，**更大并不等于更好**，更大的秩更容易过拟合。

将 `LoRA alpha` 保持在默认值 1.0，它只会乘以模型的权重。每当您修改它时，您也必须修改学习率。

## 8. 训练

在 UI 的右下角有一个大的 `Start Training` 

<img width="153" height="48" alt="image" src="https://github.com/user-attachments/assets/ed036ab7-8ef3-459b-8236-3401218bbbef" />

当您定义好概念并准备开始训练时，您首先点击它，然后通过 UI 左下角的训练进度条、CLI 或点击 `Tensorboard` 按钮来监控训练。

## 9. 在推理软件中测试 LoRA

最后，假设您有一个训练好的 LoRA，您会想要测试它。它是否按预期执行？恭喜！如果没有，欢迎来到机器学习的世界。这是一个迭代过程。虽然广泛的测试超出了本指南的范围，但这里有一个关键词可以搜索：

XYZ 网格扩展（生成用于评估的图像网格）[A111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 或 [SwarmUI](https://github.com/mcmonkeyprojects/SwarmUI)

这就结束了 OneTrainer 的非常高层次的概述。现在您应该阅读各个选项卡的 Wiki 页面来了解更多。
