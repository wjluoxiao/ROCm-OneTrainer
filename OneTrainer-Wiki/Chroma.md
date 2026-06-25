[Chroma](https://huggingface.co/lodestones/Chroma1-HD) 现在在主分支上可用。Chroma1-HD 是一个基于 Flux 的 8.9B 参数文本到图像基础模型，但它完全采用 Apache 2.0 许可证，确保任何人都可以使用、修改和构建它。

此页面正在进行中，因为 Chroma 分支正在测试，Chroma 继续开发。


OneTrainer 中 Flux 的详细信息：
* Huggingface 链接：lodestones/Chroma1-HD
* PR：https://github.com/Nerogar/OneTrainer/pull/945
* 不要使用 FULL 层，因为这将包括 distilled_guidance_layer，不建议训练。需要 lora 层更新。硬编码为微调不包括。
* Lora 在 Comfy/Swarm 中工作（与 Flux 相同的键结构）
* OneTrainer 的样本设置 - CFG 3，步骤 40（采样器始终是 Euler，无论您选择什么）
* Chroma 的 Token 限制：512
* 以 1024px 训练很慢，甚至与 Flux 相比也是如此。注意：Chroma 的大多数基础训练都是 512px，然后在 1024px 完成。
* 不建议使用动态时间步偏移（Chroma 没有使用它训练）


当前测试：
* Lora 在 ComfyUI（Swarm）中工作
* Dora 在 ComfyUI（Swarm）中工作
* Lora 在 SD.Next 中工作 
* Lora 在 Forge 中不工作（取决于分支？）


VRAM 使用：
* 请参阅预设的 VRAM 设置，正在为微调和 Lora 创建 8GB、16GB 和 24GB 预设

其他注意事项：
* ~~FP8 微调"有效"，但可能需要更多研究，并使用各种版本的 fp8 进行前向传播与反向传播。任何使用此功能都被视为严格的研究。~~ 推荐使用带有 BF16 的 8GB 或 16GB 模板
