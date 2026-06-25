在 RunPod 中设置 OneTrainer 后，我们建议在阅读并确定它是否适合您之后运行以下命令：

```shell
python -m pip install --upgrade pip; apt-get update; apt-get install mc nvtop ncdu --yes; pip install gdown
```

该命令更新 pip 并安装一些软件，详细如下：

### MC
Midnight Commander<br>
https://midnight-commander.org/<br>
如果您不是真正的命令行高手，可能会有帮助。

### nvtop
Neat Videocard TOP<br>
https://github.com/Syllo/nvtop<br>
当您调整"批量大小"和其他选项以将任务放入 VRAM 时，它非常有用

### ncdu
NCurses Disk Usage<br>
https://dev.yorhel.nl/ncdu<br>
显示有关可用和已用空间分布的详细信息

### gdown
当 Curl/Wget 失败时的 Google Drive 公共文件下载器<br>
https://github.com/wkentaro/gdown

### Bitvise SSH Client
https://bitvise.com/ssh-client<br>
如果您需要远程文件操作，例如上传到 POD/从 POD 下载、查看/编辑文件，您应该在工作场所手动安装它。
它支持公钥认证
