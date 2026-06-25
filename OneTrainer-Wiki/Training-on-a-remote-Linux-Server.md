这假设您已经在服务器的主目录中安装了 OneTrainer。如果没有，请相应地调整路径。不要在服务器上启动应用程序。如果您做得正确，当您在客户端应用程序中单击"开始训练"时，它会自动启动。如果您收到连接错误，请检查您的 SSH 服务器的端口，并确保它在客户端应用程序中相同。
服务器说明适用于基于 Debian/Ubuntu 的发行版。调整命令以匹配您的服务器。


客户端
1. ssh-keygen（无密码短语）
2. 将 <您的主目录>/.ssh/<文件名>.pub 复制到磁盘


服务器
1. 将文件复制到 /home/<用户名>/.ssh/
2. 将文件重命名为 "authorized_keys"（无扩展名）
3. chmod 700 /home/<用户名>/.ssh && chmod 600 /home/<用户名>/.ssh/authorized_keys
4. chown -R <用户名>:<用户名> /home/<用户名>/.ssh
5. sudo apt update
6. sudo apt install openssh-server
7. sudo systemctl start ssh
8. sudo systemctl enable ssh


OneTrainer 设置

<img width="808" height="465" alt="OTSettings" src="https://github.com/user-attachments/assets/0400b43d-f6f5-44a8-847b-ac11b301e506" />
