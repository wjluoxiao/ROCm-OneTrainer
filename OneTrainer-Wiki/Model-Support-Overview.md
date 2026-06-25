此概览旨在列出 OT 中支持的模型、可用的训练类型和 token 限制。查看它们的页面以获取更详细的信息、训练分辨率和架构。几乎所有组合都有默认预设。

推理支持意味着对使用 OT 训练的模型的支持，考虑的推理是 Comfy/Swarm、Forge（见注释）和 OT 采样工具。

| 模型 | 微调 | Lora | 嵌入 | 最大 Token | 推理支持 |
| ----- | --------- | ---- | --------- | --------- | ----------------- |
| SD（1.5 到 3.5，SDXL） | X | X | X | 75 | 全部 |
| Flux.1-Dev | X | X | X | 512 | Lora 和 FT：全部，嵌入：仅 OT |
| Chroma | X | X | X |512 | Lora 和 FT：全部，嵌入：仅 OT |
| Qwen | X | X | - | 512 | 全部 |
| Hidream | X | X | X | 120 | 仅 OT |
| Hunyuan video | X | X | X | 75 | 仅 OT |
| Pixart alpha | X | X | X | 120 | 全部 |
| Pixart sigma | X | X | X | 120 | 全部 |
| Sana 1.6b | X | X | X | 300 | 全部 |
| Stable Cascade | X | X | X | 75 | 全部 |
| wuerstchen 2.0 | X | X | X | 75 | 全部 |

注释：

* Flux Token 限制：请参阅 [Token 限制](https://github.com/Nerogar/OneTrainer/wiki/Flux#token-limit)
* HiDream Token 限制根据代码对于所有四个文本编码器都是 120。由于 CLIP 不支持 120，这可能是一个错误。
* 旧模型可能有一些例外，如 Cascade
* Forge 是一个幸存的项目，被其作者放弃但由支持者维护，并有几个分支。其支持只是指示性的，取决于分支。
