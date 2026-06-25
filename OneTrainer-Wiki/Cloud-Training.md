
此功能允许在 Runpod 或任何远程 Linux 服务器上进行云端训练。在使用之前，请务必阅读限制和最佳用法，这将为您节省时间。

<img width="1276" alt="cloud" src="https://github.com/user-attachments/assets/5f0b3280-efa5-4430-93ba-2ff4477335f4" />


# 描述
已经可以使用命令行界面在远程服务器或 Runpod 上训练。有了这个新选项卡，您可以通过在自己的 PC 上使用 OneTrainer UI 进行远程训练。这是用户友好的选项，并提供一些额外的优势，如保存模型和您需要的任何本地内容，在结束时停止或删除 pod，这样如果您外出或睡觉就不必担心额外费用。

您像往常一样设置训练配置。定义远程服务器和选项，点击"开始训练"时，它将上传概念和训练配置到远程服务器。在训练期间，它将下载远程工作区到本地，这样您就可以查看样本、调用 Tensorboard、访问备份和保存，就像您进行本地训练一样。

在训练期间，您将看到其进度（epochs/步骤）。您可以停止本地 OneTrainer 实例，关闭计算机，训练将在云端继续。当您再次启动本地 OneTrainer 时，它将同步远程工作区，这样您不会丢失任何信息。

训练结束后，它将停止或删除 pod（使用 Runpod 时）。

此选项卡上的每个字段都有非常详细的工具提示。此页面旨在使其使用更加简单。

# 用法

使用启用开关启用云训练（默认关闭）。

## 在 Runpod 上训练

选择类型：RUNPOD。

首先在您的 [Runpod 用户设置](https://www.runpod.io/console/user/settings) 中创建一个具有读写权限的 API 密钥。

创建您的 SSH 公钥和私钥 (*) 并在 [Runpod 用户设置](https://www.runpod.io/console/user/settings) 中上传公钥。

(*) 在 Windows 上，您可以在命令提示符或 Powershell 中使用命令 `ssh-Keygen` 创建这些密钥。它们将被放置在 "C:\Users\username\ .ssh" 中，在文本编辑器中打开公钥 `id_ed25519.pub`（ed25519 是默认协议，无论您使用另一个）以获取其值，这是一个以 ssh-protocol 开头以某种邮件地址结尾的长文本链。

注意：部署新 pod 时，它将使用一个 [docker 镜像](https://www.runpod.io/console/explore/1a33vbssq9)，其中已安装 OneTrainer，以节省 OneTrainer 安装时间。

注意：作为当前开发状态：不要更改 SSH 密钥的名称，也不要设置密码（提示时只需按回车）。这可能会在未来的 PR 中更改。

如果您在控制台中收到消息"警告：远程主机标识已更改！请联系您的系统管理员。在 C:\\Users\\username/.ssh/known_host 中添加正确的主机密钥"，只需删除 known_host 文件，这不会损害训练，可以在运行时完成，无需担心，_随机的_ Runpod/SSH 问题。

<img width="692" alt="ssh public" src="https://github.com/user-attachments/assets/c024511d-d136-4966-afd9-20c3ad188372" />


 
现在，您可以选择使用现有 pod 或创建新 pod。

### 使用现有 pod。

在 Cloud ID 下输入您的 pod id。

将主机名和端口留空，保持用户为默认值（root）。

目录：部署 pod 时，工作区目录默认为 /workspace（卷挂载路径），所以只有在您在 pod 中更改了此值时才更改它。

安装 OneTrainer：如果 /workspace/OneTrainer 目录为空，它将安装 OneTrainer。

创建云：未使用。

云名称 / 类型：对于现有 pod 未使用。

GPU：未使用。

### 创建新 pod。

将主机名、端口和 pod id 留空，保持用户为默认值（root）。

创建云：开启。

云名称（默认 OneTrainer）：pod 的名称。

类型：社区或安全，请参阅 Runpod [常见问题](https://docs.runpod.io/references/faq#secure-cloud-vs-community-cloud ) 了解更多信息。

目录：保持默认。

安装 OneTrainer：开启。

GPU：首先点击旁边的三个点以更新列表。导航到 Runpod 中的 pod 并选择部署 pod 以查看每个 GPU 的特性、成本和可用性。选择一个至少满足您训练需求的 GPU，在 RAM 和 VRAM 方面。

## 在 Linux 远程服务器上训练

与 Runpod 相同，但如果您这样做，我们猜测需要什么连接参数。

请查看此页面了解更多信息（Debian/Ubuntu 发行版）：[在远程 Linux 服务器上训练](https://github.com/Nerogar/OneTrainer/wiki/Training-on-a-remote-Linux-Server)

## 常用选项

安装 / 更新 OneTrainer（开启）和 OneTrainer 目录（/workspace/OneTrainer）：保持一切默认。

文件同步方法：NATIVE_SCP 或 FABRIC_SFTP。如有疑问，请选择 NATIVE_SCP，在 Windows 上快得多，FABRIC_SFTP 是基于 Paramiko/fabrik 的经典方法，在 Windows 上较慢。

最小下载（默认 0）：定义选择 GPU 时的最小下载速度（Mbps），对于社区云更相关。将其从 600 更改为 3000 以防止下载超时异常。对于社区云更相关，我从未在安全云中遇到过这个问题，无论 GPU 是什么（所以默认 0 就可以）。

Jupyter 密码：Jupyter 访问的密码。如果您将其留空，Jupyter 根本不会启动。

完成/错误时的操作：要么什么都不做，停止或删除 pod。不言自明。

下载样本/输出模型/保存的检查点...：同步选项。不建议下载备份，但作为选项提供。

删除远程工作区：节省远程服务器空间的选项。

Tensorboard 访问：要么激活 Tensorboard TCP 通道，您不需要下载 Tensorboards 日志，要么停用 TCP 隧道，您必须下载 Tensorboard 日志。注意，不使用 TCP 隧道时，建议不要将样本暴露给 Tensorboard 以避免下载时间。

**分离远程训练器**（默认关闭）：
* 如果选中，如果您失去连接或关闭本地 One Trainer 实例，训练将继续在云端运行。训练结束时，它的行为将像您在"分离完成时的操作"选项中设置的那样。您可以使用"立即重新连接"按钮同步回来，它将下载最新的日志和模型（如果完成）。

注意：如果您因为没有可用的 GPU 而无法启动 pod（控制台中的消息），您可以在 Runpod 上手动启动没有 GPU 的 pod，您将能够连接到它并下载模型。

* 如果未选中，它的行为就像本地 One Trainer 实例一样，如果关闭本地 One Trainer 实例，训练将停止，pod 将继续运行。

# 限制和最佳用法

完成/错误/分离或不完成时的操作：停止（最安全的选项），如果您计划在接下来的几天继续训练，可以节省成本，因为一切都保存在 pod 中（OT 安装、模型、数据集和工作区）。

**重要注意**：如果您手动停止训练，pod 将继续运行。这是有意的：通过设置新训练，您在几步后意识到忘记更改采样、训练等的一些选项。停止训练，调整您的设置并重新开始。Pod 在等您，不需要再次上传数据集，如果没有 GPU 可用也不需要下载模型。

分离远程训练器：如果您计划关闭 PC 或本地 One trainer，有不稳定的连接，Windows 自动更新或其他任何情况，请开启。如果您有信心，请关闭。

实际上，解决方案只能在远程服务器上执行操作。例如：停止、立即备份、立即采样都在工作。但编辑样本和一些训练参数在飞行中不起作用。这可能会在未来版本中实现。

所以如果您意识到需要更改设置（例如，样本分辨率、训练设置），最好停止训练，编辑设置并重新开始。

对于专家用户：

您现在可以使用截图中的路径来引用您本地没有但只在云端的文件和目录。当您训练了一个 LoRA，现在想要继续它时，这可能很有用。或者您想从第三方云存储下载到 RunPod 并使用的大型数据集，但本地没有。

![cloud path](https://github.com/user-attachments/assets/d283c8de-53f9-46db-ae57-9bf401d0014c)

