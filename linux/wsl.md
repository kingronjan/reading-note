

## alias

```shell
alias ll='ls -al'

# wsl 的 ip
alias hostip="$(wsl.exe hostname -I | sed 's/\s*//g')"

# windows 的 ip
alias winhostip="$(ipconfig.exe | grep -i ipv4 | tail -1 | cut -d':' -f2 | sed 's/\s*//g')"

# 代理设置
alias setproxy='export HTTP_PROXY=http://$(winhostip):10809 && export HTTPS_PROXY=http://$(winhostip)s:10809'

# gemini
alias gemini='setproxy && GOOGLE_CLOUD_PROJECT_ID="<GOOGLE_CLOUD_PROJECT_ID>" gemini'
```

## 安装参考

- [在 windows11上使用 WSL2 安装 centOS9 系统（支持 systemd） - web 服务器配置](https://www.lanmper.cn/redis/t9367)
- [reading/linux/centos9配置阿里云源.md at main · kingronjan/reading](https://github.com/kingronjan/reading/blob/main/linux/centos9%E9%85%8D%E7%BD%AE%E9%98%BF%E9%87%8C%E4%BA%91%E6%BA%90.md)
- [Get the IP address of the desktop / windows host in WSL2 - Philipp Scheit - Medium](https://pscheit.medium.com/get-the-ip-address-of-the-desktop-windows-host-in-wsl2-7dc61653ad51)

