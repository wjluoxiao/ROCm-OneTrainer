
在这里，您定义用于训练的基础模型、数据类型和所需的输出模型名称（这适用于 LoRA 和微调）

<img width="799" alt="model" src="https://github.com/user-attachments/assets/298cac92-772f-4ef3-ac1c-e3024b0873b4" />


* `Hugging Face Token`：您可以在此处指定您的 HF token，这是从 Hugging Face 下载受控模型（SD3、Flux）所必需的。它将本地保存在 secrets.json 中，并在加载任何预设时重用。
* `基础模型`（默认：Hugging Face 仓库）：要么保持默认，要么提供保存模型的路径（safetensor 格式或扩散模型的目录）。如果您进行了大规模微调，然后想要继续训练，这就是您放置它的地方。
* `覆盖 transformer / GGUF` Lora 的 GGUF 支持，此字段在选择 Flux/Chroma/Qwen 预设时出现，请参阅下面的说明了解其用法和用途。
* `Vae 覆盖`（默认：空白）：如果您想使用自定义 VAE，请提供 Hugging Face 链接或本地文件的路径。
* `模型输出目标`：输出模型保存的文件名或目录。如果是目录，OT 使用备份选项卡中设置的保存前缀和时间戳来命名文件。
* `输出格式`（默认：safetensors）：在这里您可以在默认的 safetensors 和可选的 checkpoint 格式之间进行选择。
* 数据类型：有几个选项可用。默认预设（#SD1.5 LoRA、#SD1.5 Embedding、...）会设置默认值，您可以坚持使用，它们工作正常。除非您有理由，否则不要碰。

注意：要恢复特定的备份（而不是最新的），请选择您关心的特定备份 epoch **文件夹**作为基础模型路径。

关于 Lora 的 GGUF 支持的注意事项（仅 Flux/Chroma/Qwen）：
* 如果您在推理期间使用 GGUF，您可以通过在训练期间使用相同的模型来更准确地训练到该检查点。
* 通过使用高质量的 GGUF，如 Q8：比使用 float8 更高质量地训练。
* 通过使用中等质量的 GGUF，如 Q4_K_S：比 nfloat4 更高质量地训练。nfloat4 在几个模型上显示出问题。类似大小的 GGUF 模型可能更好。
* 通过使用低质量的 GGUF，如 Q2 或 Q3：极低 VRAM 训练。建议在推理期间使用与训练期间相同的 GGUF。

用法：
* 选择一个 GGUF 文件（[Flux.-dev-GGUF](https://huggingface.co/city96/FLUX.1-dev-gguf)、[Chroma1-HD-GGUF](https://huggingface.co/silveroxides/Chroma1-HD-GGUF)、[Qwen-image-GGUF](https://huggingface.co/city96/Qwen-Image-gguf)）并将其放在 `覆盖 transformer / GGUF` 中，可以是链接或本地文件。
<img width="617" height="73" alt="gguf" src="https://github.com/user-attachments/assets/da08c559-de48-4033-973f-59604920252b" />





