> [!IMPORTANT]  
> 原生内置的 [云训练](https://github.com/Nerogar/OneTrainer/wiki/Cloud-Training) 于 2025 年 1 月发布，使用起来明显更容易、更集成（并且受支持），它还添加了有价值的选项。我们建议使用原生选项。

使用 Runpod，您可以在云端设置一个虚拟实例。一个优势是以合理的成本受益于大型 GPU，其次，由于它在云端运行，您可以在训练期间在本地机器上进行任何其他活动。

1. 部署一个 pod。
1. 安装 OneTrainer
1. 复制您的数据集、模型和配置。编辑配置。
1. 调用 `byobu` 终端（您可以使用任何您喜欢的 shell）并开始您的训练。


首先在 [runpod](https://www.runpod.io/) 上创建一个账户并用钱充值您的账户。这是训练所必需的，因为它是一项付费租赁服务。

然后部署一个 pod。
<img width="1083" alt="DEploy1" src="https://github.com/user-attachments/assets/76844e9a-f961-46b7-a5b5-0cfce6d8d5a4">

选择一个 GPU。它们在使用时按小时收费，最便宜的价格是 NVIDIA 上一代。
![GPU](https://github.com/user-attachments/assets/2dd22ef9-a8c2-4c21-a4bc-805d17004881)
![GPU2](https://github.com/user-attachments/assets/866612d3-e2a3-41ca-b4af-81118b7c860f)

选择一个模板。这里我使用的是 "RunPod VS Code Server"，但其他的也可以工作。注意有一个模板已经安装了 One Trainer，搜索 "dxqbyd/onetrainer-cli:0.7"，只要记得在使用时更新 OT，这个模板只针对主要的 OT 更新进行更新。

查看并编辑模板。
检查卷空间。OT 需要 10GB，然后您需要考虑您的数据集、缓存和工作区。如果您计划使用需要令牌的 Hugging Face 模型（SD3、Flux），您可以将您的 HF_TOKEN 设置为环境变量。

<img width="701" alt="hf" src="https://github.com/user-attachments/assets/51a0f6ff-6eeb-45ca-86c2-3b5b4eb5acc1">

选择一个定价计划并部署 pod。

![Plan](https://github.com/user-attachments/assets/5509b360-bb95-4b8c-852f-075797c4ba37)

使用右上角的蓝色箭头启动 pod。

![Capture d'écran 2024-09-07 102729](https://github.com/user-attachments/assets/ac8a6a02-60ac-443a-a88c-6c00cb82369c)

在连接到它之前，再次打开其参数（编辑 pod），您会找到 Jupyter Lab 的密码。

![Capture d'écran 2024-09-07 102857](https://github.com/user-attachments/assets/471a2a29-ccd6-471e-8fea-8035ef44fe4a)
<img width="698" alt="edittemplate" src="https://github.com/user-attachments/assets/6efa75fc-40ff-4764-ad11-9621fbbf7a28">

连接到 pod 并选择 "连接到 HTTP 服务（端口 8888）。

![Capture d'écran 2024-09-07 102934](https://github.com/user-attachments/assets/c93a2049-5f3b-4095-bbcd-fc7bbbd9c489)

系统会要求您输入 Jupyter 密码，Jupiter Lab 将打开。

![Capture d'écran 2024-09-07 103046](https://github.com/user-attachments/assets/00fb5dba-3845-41f3-85a7-5307454f399e)

打开终端并安装 OneTrainer 和 byobu：

`git clone https://github.com/Nerogar/OneTrainer.git`

`apt update`

`apt install ffmpeg byobu tmux aria2`

`cd OneTrainer/`

`./install.sh`

稍后您可以在 OneTrainer 目录中使用 `./update.sh` 更新 OT。

现在在您的本地计算机上打开 OneTrainer，从 UI 使用右下角的导出按钮导出您的训练配置。将其保存在本地。

回到 Jupyter，将您的配置、基础模型和数据集移动到根文件夹下。如果您从 HuggingFace 读取基础模型，则不需要上传它。
![Capture d'écran 2024-09-07 104359](https://github.com/user-attachments/assets/2e0e9e22-db22-4526-9af1-781838dca95d)

编辑您的配置以反映您的数据集（和模型）位置，保存它。

![Capture d'écran 2024-09-07 104447](https://github.com/user-attachments/assets/0b7a47fa-8eb8-4aa4-8067-12b8b02fea54)

确保从根文件夹 /workspace/ 开始，否则 OT 找不到它。

最后在 OneTrainer 目录中开始训练：

`byobu`

`source venv/bin/activate`

`python scripts/train.py --config-path "<path_to_config>"`

例如：`python scripts/train.py --config-path "/workspace/config.json"`

您可以在 byobu 中使用 `Ctrl C` 停止训练，它与从 UI 停止训练具有相同的效果：创建备份并保存模型。

就是这样！
