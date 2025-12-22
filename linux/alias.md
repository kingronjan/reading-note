## 给通过 `alias` 定义的命令加上参数的支持。

如果只是想将参数用作命令的后面部分，比如 `ll` 命令，那么无需任何额外的操作：
```shell
alias ll='ls -al'
ll ~
```
如果想将参数用作拼成命令的一部分，则可以将命令转为自定义函数来实现，比如，想要给 `django` 项目生成迁移文件，而且自定义迁移文件名称，但是每次都需要先 `cd` 到项目目录，然后运行 `makemigrate` 命令，比较麻烦，可以转为使用 `alias` 将这些操作改为一个命令：
```shell
# 原来的操作
cd djangoproject
python manage.py makemigrations model --empty --name data_xxx


# 使用 alias 的操作
alias migratedata='migrate(){ cd djangoproject;python manage.py makemigrations model --empty --name data_$1;};migrate'
migratedata xxx
```
因为 `alias` 本身并不支持直接传参，因此这里使用了将命令封装到一个函数 `migrate`，然后通过执行函数以接收参数。



### 扩展
如果不通过函数接收参数 `$1`， `$1` 会使用 `shell` 的参数（就像引入其他环境变量一样，但是 `$1` 通常没有指定任何值）


### 参考
1. [bash - Can I pass arguments to an alias command? - Ask Ubuntu](https://askubuntu.com/questions/626458/can-i-pass-arguments-to-an-alias-command)


## 在 alias 定义中使用单引号

在 Linux 中，`alias` 可以用来给需要输入很长一串字符的命令创建一个快捷方式，比如我们常见的 `ll` 命令实际上就等于 `ls -l`：

```bash
alias ll='ls -l'
```

定义时，需要用单引号将命令包裹起来，如果命令本身就包含单引号，该怎么处理才能让系统正确识别呢？比如下面的命令：

```bash
alias rxvt='urxvt -fg '#111111' -bg '#111111''
```

你可能会想，换成双引号来包裹。但是如果用双引号，其中的内容会被转义解释成具体获得的值。而不是命令本身。而且，如果命令即包含双引号，也包含单引号，那么这种方式就行不通了。


### 解决方案

如果确实想在外层使用单引号，那么可以粘贴两种引号，比如：

```bash
 alias rxvt='urxvt -fg '"'"'#111111'"'"' -bg '"'"'#111111'"'"
 #                     ^^^^^       ^^^^^     ^^^^^       ^^^^
 #                     12345       12345     12345       1234
```

为什么 `'"'"'` 会被解释为 `'`?

首先看一下系统解释这段命令的过程：

1. `'` 结束命令开始的单引号到当前单引号的内容

2. `"` 开始新的引用，并使用双引号，以保证接下来的引用会被直接解释成具体的值

3. `'` 代表被引用的值，也就是我们期望的单引号

4. `"` 结束第 2 步的引用
5. `'` 开始新的引用，使用单引号

在这里，如果有两个连着的单引号引用，会被视为一个命令，比如：

```bash
$ echo 'abc''123'  
abc123
```

而使用了 `'"'"'` 的方式，则中间的单引号会被视为一个字符而不是起始的位置：

```bash
$ echo 'abc'"'"'123'
abc'123
```

### 参考

1. [bash - How to escape single quotes within single quoted strings - Stack Overflow](https://stackoverflow.com/questions/1250079/how-to-escape-single-quotes-within-single-quoted-strings)

