# 概览
欢迎来到 OneTrainer 维基！OneTrainer 是一个基于 customtkinter 的 GUI 工具，用于训练和处理各种扩散模型，主要构建在 [Diffusers](https://github.com/huggingface/diffusers) 库之上。

![OneTrainerGUIResize](https://github.com/Nerogar/OneTrainer/assets/132208482/f9d1ea09-c247-405a-abb3-72da3dcfc9b3)

# 学习
* [快速入门](https://github.com/Nerogar/OneTrainer/wiki/Getting-Started)
* [程序介绍 - OT 的各个选项卡](https://github.com/Nerogar/OneTrainer/wiki/The-Program)
* [信息、指南与经验总结](https://github.com/Nerogar/OneTrainer/wiki/Info,-Guides-and-Lessons-Learned)
* [开发者角落](https://github.com/Nerogar/OneTrainer/wiki/Dev-Corner)

# OneTrainer 系统要求
* 需要支持 `PyTorch 2.7.1` 或更高版本的系统，Python 版本 >= `3.10` 且 < `3.13`。对于 CUDA，这意味着需要 11.8 或更高版本的 CUDA；对于 ROCM，则需要 6.2.4 或更高版本。
* 大约需要 7GB 可用空间进行安装。训练过程中会占用更多空间，因为会保存模型文件和备份。
* 对于需要进行 CPU 卸载的用户，我们强烈建议使用 `64GB` 内存，`32GB` 也可以运行，但可能会因为垃圾回收导致内存不足（OOM）。

# 进一步帮助
* 如果您需要帮助，最佳去处是 [Discord](https://discord.gg/KwgcQd5scF)
* 如果您发现了 bug、问题或有功能请求，请先搜索现有 issue，然后再创建新 issue：https://github.com/Nerogar/OneTrainer/issues
