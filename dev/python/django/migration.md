## squash

使用 django 的 squashmigrations 操作不慎可能会出现一些问题，而且还会增加迁移的复杂性，文章介绍了一种方法，比较干脆，具体如下：

执行前需要确保环境已经应用了所有的迁移记录。

1. 删除所有迁移文件（先备份）
2. 使用 `python manage.py makemigrations` 重新生成迁移文件
3. 重新添加 data migrations 的内容
4. 如果部署流程中包含自动迁移的流程，需要临时关闭再部署
5. 部署后重置历史的迁移记录，参考脚本如下：

    ```python
    from django.core.management import call_command
    from django.db import connection

    with connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE django_migrations")

    # 该操作会将迁移记录标记为已完成，但是不会真正的应用他们
    call_command("migrate", fake=True)
    ```

6. 打开第 4 步中关闭的自动迁移流程

参考：
- [Stop Using Django's squashmigrations: There's a Better Way | Johnny Metz](https://johnnymetz.com/posts/squash-django-migrations/)


## 安全迁移

上线删除或重命名字段这类数据库变更时，一旦遇到错误，很难回退到之前的版本，这时可以使用更安全的做法，以减少此类错误。

- 对于删除字段：

    1. 先将字段设置为 nullable，上线运行
    2. 在运行没有异常后，可以在下个版本删除该字段

- 对于重命名字段

    1. 创建一个新字段用来作为过渡，除名称外其他属性与之前的字段保持一致
    2. 更新所有写入/更新操作中涉及新字段的逻辑，让其同步更新老字段的值
    3. 在运行没有异常后，可以在下个版本删除老字段

对于表级别的操作，同样也可以参考上述思路。

来自：[Loopwerk: Safe Django migrations without server errors](https://www.loopwerk.io/articles/2025/safe-django-db-migrations/?utm_campaign=Django%2BNewsletter&utm_medium=email&utm_source=Django_Newsletter_314)
