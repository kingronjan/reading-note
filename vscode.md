## 插件

- [IntelliJ IDEA Keybindings - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=k--kato.intellij-idea-keybindings) 这个插件可以将快捷键配置为 idea 的快捷键，这对于习惯了使用 pycharm 的快捷键的人很受用
- [Git Graph - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph) git 提交记录的图形化操作界面


## 主题

- [Linux Themes for VS Code - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SolarLiner.linux-themes)
- [Material Icon Theme - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)
- [GitHub Theme - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=GitHub.github-vscode-theme)


## vscode server 离线安装

1. 获取当前版本 vscode 的 commit_id：Help - > About -> Commit

2. 根据 commit_id 下载对应版本的 vscode-server：
   https://update.code.visualstudio.com/commit:${commit_id}/server-linux-x64/stable

3. 将下载好的 vscode-server-linux-x64.tar.gz 放在 ~/.vscode-server/bin/${commit_id} 目录下（没有则新建）

4. 将压缩包解压，得到 vscode-server-linux-x64 目录，将该目录下的所有内容移动到~/.vscode-server/bin/${commit_id} 下，并删除 vscode-server-linux-x64 目录和压缩包

5. 一键脚本：

   ```bash
   commit_id=XXX
   PATH_TO_YOUR_VSCODE_SERVER=XXX
   
   mkdir -p ~/.vscode-server/bin/${commit_id}
   cp ${PATH_TO_YOUR_VSCODE_SERVER}/vscode-server-linux-x64.tar.gz ~/.vscode-server/bin/${commit_id}
   
   cd ~/.vscode-server/bin/${commit_id}
   tar -xzf vscode-server-linux-x64.tar.gz && rm vscode-server-linux-x64.tar.gz
   mv vscode-server-linux-x64/* . && rm -r vscode-server-linux-x64
   
   mkdir -p ~/.vscode-server/extensions
   cp -r ${PATH_TO_YOUR_VSCODE_EXTENSIONS}/extensions/* ~/.vscode-server/extensions
   ```
