目录：
* [模型详情](https://github.com/Nerogar/OneTrainer/wiki/Flux#model-details)
* [限制](https://github.com/Nerogar/OneTrainer/wiki/Flux#limitations)
* [当前信息](https://github.com/Nerogar/OneTrainer/wiki/Flux#current-information)
* [Flux Krea](https://github.com/Nerogar/OneTrainer/wiki/Flux#flux-krea)


本页面正在建设中，随着对 Flux 的了解不断更新。

Flux 是一个 DiT Transformer 流匹配模型，具有很高的学习潜力，但它是一个非常大且处理速度很慢的模型。

### 模型详情：
* 与 SD3 一样，需要 huggingface 密钥或 diffusers 模型的本地副本。OneTrainer 现在有一个选项，让您可以在 GUI 中输入您的 HF token。
    * AIO（All in One）safetensor 模型可以工作。
        * 已测试 helheimFlux_v10FP8AIO.safetensors 和 helheimFlux_v10FP16AIO.safetensors
        * NF4 AIO 模型将无法工作（diffusers 不支持）
        * Turbo 模型 safetensors 可能无法工作，并且由于 Turbo 模型的制作方式，可能无论如何都无法用 OT 训练
    * 微调模型的 HuggingFace 链接可以工作，但仓库必须是 diffusers 格式。
        * 已测试：`AlekseyCalvin/Colossus_2.1_dedistilled_by_AfroMan4peace`
        * 网站链接：https://huggingface.co/AlekseyCalvin/Colossus_2.1_dedistilled_by_AfroMan4peace
* 完全去蒸馏的 Flux 将无法工作，因为 OneTrainer 工作流期望有引导变量。
* Black Forest Labs Hugging Face 仓库上的标准 Flux safetensors 文件只是 transformer 和 VAE，不包含文本编码器。
* BFL（Black Forest Labs）没有提供模型的所有细节，所以一些项目仍然是黑盒。然而，重要的是要注意，更高的分辨率需要时间偏移。OneTrainer 有一个选项，可以专门针对 Flux 根据训练分辨率自动偏移时间步长。

### Token 限制：

* Flux 现在支持最多 512 个 token 进行训练（最初是 77 个），但您必须自己决定要使用多少个 token。不幸的是，没有正确的值，但以下是我们所知道的：
* 模型可能是在 512 个 token 下训练的，但我们不确定。可能是混合的。
* 默认训练 token 仍然是 77，可能不是最佳选择。
* ComfyUI/Swarm 在 256 个 token 下采样 Flux。如果您为在 ComfyUI/Swarm 中使用而训练，256 可能是一个不错的选择。
* 在哪里设置 token 限制：

![TE2](https://github.com/user-attachments/assets/d3a82036-12c8-47af-83fb-45f5f939d7cf)




### 限制：
* ~~由于 T5 的性质，嵌入可能无法工作。~~
    * 更新，Nero 重构了嵌入，输出嵌入现在可以与 Flux 一起使用。
    * 然而，这些输出嵌入只能在 OneTrainer 中使用。在其他软件中使用可能需要先完成 OMI 格式。
* 某些 Lora 格式（Full Dora）在所有生成软件中都无法工作。众所周知，Forge 使用 full dora 会产生紫色输出。
* FLEX 目前不支持，因为它不完全是基于 Flux.1 dev 的模型。
* Flux Schnell 不支持，也没有任何支持计划。如果您想使用此模型，最好使用专用的 Flux 训练器（Flux Gym、AI Toolkit）

### 当前信息：
* Lora 是目前唯一推荐的训练方式。微调最终需要您通过模型的蒸馏进行训练。
* FP8 是推荐的最低精度，以避免出现伪影。
* NF4 精度允许 Flux 在较低 VRAM 的显卡上使用，但应注意，在此精度级别上网格图案可能非常明显。
* OneTrainer Lora 可以在 Comfy 的标准 Lora Loader 中使用。
* Flux 具有强大的架构。可以在 512 或 768 下训练 LoRa，然后在 1024 下生成，质量损失最小。
* 可以在具有 12GB VRAM 的 GPU 上训练 Flux Lora。
* 8GB 显卡可以通过添加 GGUF 支持来工作。由于基本的 Windows 功能可能会占用 1GB 或更多的 VRAM，如果使用 8GB 显卡，使用集成 GPU（iGPU）来运行 Windows 桌面可能会有益。
* Torch Compile（现已可用）等功能有助于加速 Lora 训练，对消费级 GPU 极其有益。

### Flux Krea：
* Black Forest Labs 发布了 Flux Krea 的模型权重
* 要使用此模型，请确保您有权访问 huggingface 仓库，因为模型是受控的。
* 在 OneTrainer 中，确保您的 hf token 在字段中，并使用 `black-forest-labs/FLUX.1-Krea-dev` 作为模型
* 原始 Flux Loras 在一定程度上可以与 Krea 一起使用，但它们会失去一些质量。
* 由于 Krea 被设计为 Flux.Dev 的直接替代品，您从原始 Flux 的训练设置应该适用。
