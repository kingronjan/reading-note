# debain setup


## apt
  
设置 apt 源：

```shelldebain setup
bash <(curl -sSL https://linuxmirrors.cn/main.sh)
```

## 输入法
       
安装中文输入法 参考： [Debian Linux安装配置ibus rime中文输入法_debian ibus-CSDN博客](https://blog.csdn.net/izwmain/article/details/134796292)：

配置输入法，选择 ibus，安装 rime：

```shell
sudo apt install ibus-rime
```

重启后在系统输入法中增加汉语（中文）的输入法即可。

设置首选简体中文配置 参考： [rime设置为默认简体 - 喵星人聚居地](https://miaostay.com/2018/11/rime%E8%AE%BE%E7%BD%AE%E4%B8%BA%E9%BB%98%E8%AE%A4%E7%AE%80%E4%BD%93/)：

```bash
echo '
# encoding: utf-8
patch:
  switches:
    - name: ascii_mode
      reset: 0
      states: ["中文", "西文"]
    - name: full_shape
      states: ["半角", "全角"]
    - name: simplification
      reset: 1
      states: ["漢字", "汉字"]
    - name: ascii_punct
      states: ["。，", "．，"]
' > ~/.config/ibus/rime/build/luna_pinyin.schema.custom.yaml
```
主要是设置 `reset: 1`

设置中文输入状态下，输入英文时按 `shift` 直接将英文上屏，然后切换到英文状态输入：

修改 `~/.config/ibus/rime/build/default.yaml` 中的 `ascii_composer.switch_key.Shift_L` 为 `commit_code`：

```yaml
ascii_composer:
  good_old_caps_lock: true
  switch_key:
    Caps_Lock: clear
    Control_L: noop
    Control_R: noop
    Eisu_toggle: clear
    Shift_L: commit_code
    Shift_R: commit_text
```

该配置的可选项参考：[使用 Control 鍵切換中西文，上屏已輸入的編碼；令 Caps Lock 改變字母的大小寫](https://gist.github.com/lotem/2981316)

- inline_ascii 在輸入法的臨時西文編輯區內輸入字母、數字、符號、空格等，回車上屏後自動復位到中文
- commit_text 已輸入的候選文字上屏並切換至西文輸入模式
- commit_code 已輸入的編碼字符上屏並切換至西文輸入模式
- noop，屏蔽該切換鍵


## gnome 终端配置

**使用鼠标中键粘贴**

安装 consolas 字体 参考：[将 Linux 上的 VSCode 改为 Consolas 字体 | 海岚的个人空间](https://cvftgfjgbfknfbf.ac.cn/index.php/2024/09/01/%E5%B0%86-linux-%E4%B8%8A%E7%9A%84-vscode-%E6%94%B9%E4%B8%BA-consolas-%E5%AD%97%E4%BD%93/):

```shell
wget https://down.gloriousdays.pw/Fonts/Consolas.zip
unzip Consolas.zip
sudo mkdir -p /usr/share/fonts/consolas
sudo cp consola*.ttf /usr/share/fonts/consolas/
sudo chmod 644 /usr/share/fonts/consolas/consola*.ttf
cd /usr/share/fonts/consolas
sudo mkfontscale && sudo mkfontdir && sudo fc-cache -fv
```

确保安装成功 :

```shell
fc-list | grep -i consolas
```

配置字体：在首选项 -> 配置文件 -> 未命名 -> 文本 中输入 `Consolas`


### nvim 退出后光标形状被改为块状

使用如下方法：

```shell
# 函数名可以自定义，这里我命名为 nvim_fix_cursor
function nvim_fix_cursor() {
    # ----------------------------------------------------
    # 1. 启动 Neovim，并将所有参数 ($@) 传递给它
    # ----------------------------------------------------
    nvim "$@"

    # ----------------------------------------------------
    # 2. Neovim 退出后，强制设置光标为竖线 (I-beam)
    #    \033 是 ESC 的八进制表示，[5 q 是设置竖线（不闪烁）的序列
    # ----------------------------------------------------
    echo -ne "\033[5 q"
}

# ----------------------------------------------------
# (可选) 设置一个别名，让你依然可以使用 nvim 命令来调用这个函数
# ----------------------------------------------------
alias nvim='nvim_fix_cursor'
```

## proxy

参考：

- [树莓派使用 V2Ray 魔法上网 | Jacob's Thoughts](https://weixiang.github.io/posts/raspberry-pi-uses-v2ray-magic-to-surf-the-internet/)
- [zfl9/gfwlist2privoxy: 将 gfwlist.txt（Adblock Plus 规则）转换为 privoxy.action](https://github.com/zfl9/gfwlist2privoxy)

下载 v2ray-core [Releases · v2ray/v2ray-core](https://github.com/v2ray/v2ray-core/releases)

下载后解压到 `~/app/v2ray-linux-64`，在下面创建配置文件 `myconfig.json`，格式参考目录下的 config.json 文件（可以直接从现有的配置中拷贝完整的配置内容复制即可）：

建立 systemd 服务：

```shell
echo '
[Unit]
Description=V2Ray Service
Documentation=https://www.v2fly.org/
After=network.target nss-lookup.target

[Service]
User=kingron
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/home/kingron/app/v2ray-linux-64/v2ray -config=/home/kingron/app/v2ray-linux-64/myconfig.json
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
' > /etc/systemd/system/v2ray.service 

systemctl daemon-reload
systemctl enable v2ray
systemctl start v2ray
```

生成 gfwlist.action:

```shell
curl -4sSkLO https://raw.github.com/zfl9/gfwlist2privoxy/master/gfwlist2privoxy
bash gfwlist2privoxy 127.0.0.1:10808
mv -f gfwlist.action /etc/privoxy/
```

配置 privoxy:

```shell
apt install -y privoxy
sudo cp /etc/privoxy/config /etc/privoxy/config.bak
sudo cat /etc/privoxy/config | grep -v '^#' | grep -v '::1' > /etc/privoxy/config 
sudo echo 'actionsfile gfwlist.action' >> /etc/privoxy/config 
```

重启 privoxy:

```shell
systemctl restart privoxy.service
```

在 Chrome 中：

1. 打开“ Settings”菜单，或在地址栏中输入chrome://settings
2. 向下滚动到底部
3. 点击“ 高级 ”打开高级设置
4. 向下滚动，直到看到“ 系统 ”选项
5. 点击 打开您计算机的代理设置

配置手动代理，将 HTTP 和 HTTPS 类型的地址都填写为 `127.0.0.1:8118`

## 剪贴板

安装 gpaste:

```shell
sudo apt install gpaste-2
```

启动 ui 界面：

```shell
gpaste-client ui
```

像 windows 一样使用 (`windows` + `v`)，参考：[Gpaste - wsttask - 博客园](https://www.cnblogs.com/wsttask/p/18647329)

1. 配置快捷键 设置->键盘->查看和自定义快捷键 
2. 添加快捷键 命令为 `/usr/bin/gpaste-client ui`，按键为 `windows + v`

## flatpak

参考：[Linux捣鼓记录：安装flatpak软件仓库，更换国内镜像 - lwlnice - 博客园](https://www.cnblogs.com/lwlnice/p/18263967)

vinarios 默认有安装 flatpak，可以在命令行输入 `flatpak` 验证。

更换为国内源：

```shell
# 中科大镜像
flatpak remote-modify flathub --url=https://mirrors.ustc.edu.cn/flathub

# 上海交大 see: https://mirror.sjtu.edu.cn/docs/flathub
# flatpak remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub

# 恢复官方源
# flatpak remote-modify flathub --url=https://dl.flathub.org/repo
```

安装 Extension Manager：

```shell
# 先搜索
$ flatpak search "extension manager"
名称                      描述                             应用程序 ID                              版本          分支           远程仓库
Extension Manager         Install GNOME Extensions         com.mattjakeman.ExtensionManager         0.6.5         stable         flathub

# 安装时使用应用程序 ID
$ flatpak install com.mattjakeman.ExtensionManager
```


## docker

参考:

- [Debian / Ubuntu 安装 Docker 以及 Docker Compose 教程 - 烧饼博客](https://u.sb/debian-install-docker/)
- [Debian 12 Linux(bookworm) 容器镜像使用国内镜像源](https://www.zzxworld.com/posts/cn-mirrors-for-debian-12-linux)
- [镜像加速器 · Docker -- 从入门到实践](https://docker-practice.github.io/zh-cn/install/mirror.html)

安装（切换到 root 执行）：

```shell
apt update
apt upgrade -y

# 安装依赖应用
apt install curl vim wget gnupg dpkg apt-transport-https lsb-release ca-certificates

# 添加镜像源（清华源）
curl -sSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list


# 安装 docker
apt update
apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

如果遇到源不可用也可以替换为其他源：

- 华为: mirrors.huaweicloud.com
- 163: mirrors.163.com
- 中科大：mirrors.ustc.edu.cn
- 交大：mirror.bjtu.edu.cn
- 兰州大学：mirror.lzu.edu.cn
- 教育网：mirror.nju.edu.cn
- 北外: mirrors.bfsu.edu.cn

只需要将上面的 `mirrors.tuna.tsinghua.edu.cn` 改为要用的域名即可，比如使用华为源：

```shell
curl -sSL https://mirrors.huaweicloud.com/docker-ce/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://mirrors.huaweicloud.com/docker-ce/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list
```

让非 root 用户以 rootless 运行，切换到非 root 用户下执行:

```shell
# 先停止使用 root 启动的 dockerd
sudo systemctl stop docker

# 安装 rootless
sudo apt install docker-ce-rootless-extras

# 加入组
sudo usermod -aG docker $(whoami)

# 检查环境依赖
dockerd-rootless-setuptool.sh check

# 根据检查结果执行提示的命令

# 安装到当前用户
dockerd-rootless-setuptool.sh install
```

以下配置会增加一段自定义内网 IPv6 地址，开启容器的 IPv6 功能，以及限制日志文件大小，防止 Docker 日志塞满硬盘：

```shell
cat > /etc/docker/daemon.json << EOF
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "20m",
        "max-file": "3"
    },
    "userland-proxy": false,
    "ipv6": true,
    "fixed-cidr-v6": "fdb::/64",
    "experimental":true,
    "ip6tables":true
}
EOF
```

## ondriver

参考：

- [jstaf/onedriver: A native Linux filesystem for Microsoft OneDrive](https://github.com/jstaf/onedriver)
- [安装软件包 home:jstaf / onedriver](https://software.opensuse.org/download.html?project=home%3Ajstaf&package=onedriver)

```shell
echo 'deb http://download.opensuse.org/repositories/home:/jstaf/Debian_12/ /' | sudo tee /etc/apt/sources.list.d/home:jstaf.list
curl -fsSL https://download.opensuse.org/repositories/home:jstaf/Debian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_jstaf.gpg > /dev/null
sudo apt update
sudo apt install onedriver
```

安装后打开，选择挂载的文件夹，登录即可开始同步。

## gnome 插件

- [G-dH/custom-hot-corners-extended](https://github.com/G-dH/custom-hot-corners-extended)  扩展屏幕四个角的热点功能 
- [Blur my Shell - GNOME Shell Extensions](https://extensions.gnome.org/extension/3193/blur-my-shell/) 让状态栏，dock 栏，以及 gnome shell 等应用高斯模糊
- [Lock Keys - GNOME Shell Extensions](https://extensions.gnome.org/extension/36/lock-keys/) 在状态栏显示大写锁定和数字键盘锁定的状态

## 禁用切换桌面快捷键

See: [11.10 - How do I disable Ctrl+Alt+Left/Right? - Ask Ubuntu](https://askubuntu.com/questions/82007/how-do-i-disable-ctrlaltleft-right)

`ctrl` + `alt` + `left`/`right` 默认会切换桌面，个人很少用到，不过在代码编辑器中比较习惯使用该快捷键作为前进后退的快捷键，使用下面的命令禁用默认的切换桌面快捷键：

```shell
 gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left "['']"
 gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right "['']"
```

## 将 home 目录下的文件夹设置为英文

参考：[如何将 Home 目录下的文件夹设置为英文 – Mogeko's Blog](https://mogeko.me/zh-cn/posts/zh-cn/060/)


修改 `~/.config/user-dirs.dirs` 文件内容为：

```shell
# This file is written by xdg-user-dirs-update
# If you want to change or add directories, just edit the line you're
# interested in. All local changes will be retained on the next run.
# Format is XDG_xxx_DIR="$HOME/yyy", where yyy is a shell-escaped
# homedir-relative path, or XDG_xxx_DIR="/yyy", where /yyy is an
# absolute path. No other format is supported.
# 
XDG_DESKTOP_DIR="$HOME/Desktop"
XDG_DOWNLOAD_DIR="$HOME/Downloads"
XDG_TEMPLATES_DIR="$HOME/Templates"
XDG_PUBLICSHARE_DIR="$HOME/Public"
XDG_DOCUMENTS_DIR="$HOME/Documents"
XDG_MUSIC_DIR="$HOME/Music"
XDG_PICTURES_DIR="$HOME/Pictures"
XDG_VIDEOS_DIR="$HOME/Videos"
```

重命名原来的文件夹：

```shell
mv $HOME/桌面 $HOME/Desktop
mv $HOME/下载 $HOME/Downloads
mv $HOME/模板 $HOME/Templates
mv $HOME/公共 $HOME/Public
mv $HOME/文档 $HOME/Documents
mv $HOME/音乐 $HOME/Music
mv $HOME/图片 $HOME/Pictures
mv $HOME/视频 $HOME/Videos
```
