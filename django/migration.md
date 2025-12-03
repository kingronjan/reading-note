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

