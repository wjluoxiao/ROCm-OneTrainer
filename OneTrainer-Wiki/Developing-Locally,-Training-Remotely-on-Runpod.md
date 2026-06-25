# 在云端开发

微调或更大的 LoRA 可能需要比您在消费级显卡上更多的 VRAM，需要您租用。另一方面，在租用的 GPU 上开发可能会变得昂贵，特别是当您在编辑 python 文件时让 GPU 闲置时。

## 设置 OneTrainer 的私有分支
在 github 上创建一个空仓库（不是 fork）。在本地运行：
```
git clone --bare https://github.com/Nerogar/OneTrainer
cd OneTrainer
git push --mirror https://github.com/your-username/OneTrainer-private
cd ..
git clone https://github.com/your-username/OneTrainer-private
cd OneTrainer-private
git remote add upstream https://github.com/Nerogar/OneTrainer
git remote set-url --push upstream DISABLE
```

## 设置云端
* 启动云服务器
* 使用 `apt-get update && apt-get install gh && gh auth login` 在云服务器上登录 github
* 在本地运行云 OneTrainer，更改设置：
  * OneTrainer 目录：/workspace/OneTrainer-private
  * 安装命令：git clone https://github.com/your-username/OneTrainer-private
* 开始训练
* 在 RunPod 上便宜地停止云端。当您在本地编辑 python 文件时，100 GB 只留下大约每小时 0.03 美元的磁盘成本。

## 开发
* 编辑文件后，在本地运行 `git commit -a -m "update" && git push` 以将更改推送到您的私有仓库
* 再次按"开始训练" - 远程云端获取更改并训练。"更新 OneTrainer"必须启用。
* 停止云端
* 完成后，删除云端以避免磁盘成本。下次，重复上面的 github 登录。
* 当您准备好将更改推送到公共分支时，避免由上述提交命令创建的长提交历史。一种方法是在您的私有仓库中使用 `git diff master > diff-file` 创建补丁，然后在您的公共仓库分支中 `git apply diff-file`。

## 限制
* 如果您需要 pdb `breakpoint()`，复制本地控制台中"开始训练"后显示的训练命令，并在云控制台上运行它
* 当您尝试恢复已停止的 RunPod 时，可能您存储所在机器上的所有 GPU 都被占用了。如果这经常发生，您可以通过使用网络存储卷来避免。请参阅 RunPod 网站。
