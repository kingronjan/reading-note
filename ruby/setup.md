

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
