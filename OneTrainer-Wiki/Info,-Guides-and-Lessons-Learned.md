在这里您可以找到各种指南、信息和经验教训页面

# 杂项信息
* 对于 SD3 和 Flux（一般来说是门控模型）训练，您需要来自 HuggingFace 的读取令牌（在 HF 中进入您的 [设置](https://huggingface.co/settings/tokens) 并创建一个读取令牌）并将其设置为名为 "HF_TOKEN" 的环境变量。存在其他解决方案，如 [命令行指令（Discord 讨论）](https://discord.com/channels/1102003518203756564/1102013112124706827/1264266275639525376) 或使用 HF 文件夹的 [本地副本（Discord 讨论）](https://discord.com/channels/1102003518203756564/1188183242747158630/1259788529320595558)。
* 描述 token 限制：实际上，大多数都限制为 77 个 token（不包括开始和结束 token 为 75 个），因为 clip。唯一的例外是：
pixart（alpha/sigma）：120，sana：300。将来可能会改变。
* [从 Kohya 过来的常见错误](https://github.com/Nerogar/OneTrainer/wiki/Common-Mistakes-Coming-From-Kohya) 如果您无法获得在 Kohya 中可以获得的类似结果。
* [作者解释的验证](https://github.com/Nerogar/OneTrainer/wiki/How-Validation-works)

# 模型支持
* [概览](https://github.com/Nerogar/OneTrainer/wiki/Model-Support-Overview)
* [扩散模型](https://github.com/Nerogar/OneTrainer/wiki/Diffusion-Models-Overview)
* [Flux.1-Dev](https://github.com/Nerogar/OneTrainer/wiki/Flux)
* [Chroma](https://github.com/Nerogar/OneTrainer/wiki/Chroma)

# 指南
* [OneTrainer 2024 年 3 月指南](https://github.com/Nerogar/OneTrainer/wiki/OneTrainer-March-2024-Guide)
一个更详尽的 OneTrainer 指南，构建为清单。现在已经过时，但在某些方面仍然相关。
* [云训练](https://github.com/Nerogar/OneTrainer/wiki/Cloud-Training) OT 原生且支持的在 Runpod 或任何远程 Linux 服务器上运行训练的方式。
* [在 Runpod 中手动设置 OneTrainer](https://github.com/Nerogar/OneTrainer/wiki/Manually-setup-OneTrainer-in-Runpod) 自从我们现在在 UI 中原生支持它以来已经过时，但仍然是一个选项。

# 其他工具 - 有用的链接
[其他工具 - 有用的链接](https://github.com/Nerogar/OneTrainer/wiki/Other-Tools-%E2%80%90-Helpful-Links)

# 经验教训
* [常见问题](https://github.com/Nerogar/OneTrainer/wiki/F.A.Q.)
* [经验教训和教程](https://github.com/Nerogar/OneTrainer/wiki/Lessons-Learnt-and-Tutorials)
