

## 换源

参考：[RubyGems Mirror - Ruby China](https://index.ruby-china.com/)

```shell
gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/
gem sources -l
# 确保结果只有 gems.ruby-china.com
# https://gems.ruby-china.com
```

修改 bundler 的 gem 源

```shell
bundle config mirror.https://rubygems.org https://gems.ruby-china.com
```


## 安装 Jekyll

参考：[Jekyll on Ubuntu | Jekyll • Simple, blog-aware, static sites](https://jekyllrb.com/docs/installation/ubuntu/)

对于 debain 需要先安装 ruby-dev:

```shell
sudo apt install ruby-dev
```

安装 jekyll:

```shell
gem install jekyll bundler
```

安装后可以根据提示将 gem 可执行文件路径加入到 `PATH` 中：

```shell
echo "export PATH=\$PATH:~/.local/share/gem/ruby/3.3.0/bin/" >> ~/.bash_profile
```

在项目中使用 bundle 命令时报错：
```
Bundler::PermissionError: There was an error while trying to write to `/var/lib/gems/3.3.0/cache`. It is likely that you need to grant write
permissions for that path.
```

参考 [ruby - How to fix permission error while install bundle for rails project on ubuntu? - Stack Overflow](https://stackoverflow.com/questions/77770696/how-to-fix-permission-error-while-install-bundle-for-rails-project-on-ubuntu) 配置 bundle 安装时使用的路径，配置为有权限写入的路径：

```shell
bundle config path ~/data/ruby-bundle
```
