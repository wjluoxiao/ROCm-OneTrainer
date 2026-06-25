
本节介绍可用于训练目的的其他工具/程序。它们不是 One Trainer 解决方案的一部分，其中一些是在 [other-tools](https://discord.com/channels/1102003518203756564/1134202924495544541) Discord 线程中引入的。

欢迎在 Discord 上的 [Wiki](https://discord.com/channels/1102003518203756564/1144311654385983538) 讨论中建议任何其他工具。

# 数据集管理

## 描述 UI

### [TagGUI](https://github.com/jhc13/taggui)

用于图像数据集的标签管理器和描述工具。您也可以加入他们的 [Discord 线程](https://discord.com/channels/1102003518203756564/1194558844878209054)

功能：

* 键盘友好的界面，用于快速标记
* 基于您自己最常用标签的标签自动完成
* 集成的 Stable Diffusion token 计数器
* 用于重命名、删除和排序标签的批量标签操作
* 高级图像列表过滤
* 使用包括 CogVLM、LLaVA、moondream、Joy Caption 等模型的自动描述生成
* 选项以 4 位加载自动描述模型以减少 VRAM 使用

### [Dataset Helpers](https://github.com/Particle1904/DatasetHelpers)

功能：
* 与 taggui 相比，更专注于标签描述，缺点是模型更少：支持 SW-v3、JoyTag 和 WD1.4
* 图像裁剪、调整大小、排序和顺序重命名
* 仅使用 ONNX 模型，意味着您可以在 CPU 上运行
* 标签冗余去除和实验性合并
* 稍微更好的过滤

### [JoyCaption Alpha Two](https://github.com/fpgaminer/joycaption)

使用 Joy Caption 的描述工具。注意存在更新的版本（Beta 版本）。

* [D3voz 的非官方 GUI 修改版](https://github.com/D3voz/joy-caption-alpha-two-gui-mod)
* [Hugging Face Space](https://huggingface.co/spaces/fancyfeast/joy-caption-pre-alpha)
* [作者 Discord 线程](https://discord.com/channels/1010980909568245801/1268005663955484702)
* [OT Discord 线程](https://discord.com/channels/1102003518203756564/1291333024356630658)

功能：

* 4 位模型支持，用于更低的 VRAM（D3voz）。
* 批量处理

注意：
* 在（D3voz）版本中，提示选项可以在 gui_updated.py 中编辑（EXTRA_OPTIONS_LIST 部分），它会更新 UI 和发送给模型的命令，但由于 Alpha Two 不是通用指令跟随者，它不会很好地跟随其训练数据之外的提示。请谨慎使用此功能。
* 默认不支持 webp 格式（D3voz），但您可以在 gui_updated.py 中启用它（load_images 类，image_extensions 常量）。
* 我对它做了一些修改，以支持 webp 格式，从图像选择中排除掩码图像，并添加一个选项来生成描述作为新行。您可以在 [这里（discord）](https://discord.com/channels/1102003518203756564/1291333024356630658/1333717333549518930) 获取文件。
* 要求文件使用旧版本的 transformers（4.44），这会给出 bitsandbytes 错误。更新 transformers（确认 4.49 可以工作）。

### Joy Caption Beta One

* [Hugging Face Space](https://huggingface.co/spaces/fancyfeast/joy-caption-beta-one)
* Taggui 支持 4 位或完整版。
* Comfy 有完整、8 位或 4 位的节点。

## 图像处理

### [Birme.net](https://www.birme.net/?target_width=512&target_height=512)

将图像裁剪到特定分辨率的在线解决方案。

### 图像裁剪器

自动将图像裁剪到定义列表中最接近的宽高比，以适应主体（面部、主体）。

* [Github](https://github.com/dioxic/image-cropper)
* [Discord 线程](https://discord.com/channels/1102003518203756564/1277207050157293618)


### 分词器

使用这些工具来了解文本是如何被分词的。

* [扩散分词器 - Hugging Space 由 takarajordan 制作](https://huggingface.co/spaces/takarajordan/DiffusionTokenizer)
* [Novel.ai 的分词器](https://novelai.net/tokenizer) 

# 测试模型 - 提示助手

[TIPO](https://huggingface.co/KBlueLeaf/TIPO-500M)

接受输入提示并输出据称改进的提示的模型。适用于 Comfy、Forge 和 A111

### 主提示

基于 A1111 Unprompted 扩展。它可以为 SD1.5、SDXL 和 SDXL Turbo 生成强大且多样的提示。

* [Discord 链接](https://discord.com/channels/1102003518203756564/1196065267797721108)
* [Civitai](https://civitai.com/models/264781?modelVersionId=374396)

功能：

* 许多生成选项，如图像类型（写实、数字艺术）、分辨率、SFW 或不是、种族、年龄、性别...
* 可以包括一个或几个模型（嵌入、Lora）

注意：
* 由于它基于 A1111 扩展，并非所有解决方案都支持它。已宣布支持 comfyUI，但我没有测试它。




