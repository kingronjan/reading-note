## 使用 -f 参数后部分 logger 没有输出到文件中

worker 使用了 -f 参数后，celery [默认会把 stdout 和 stderr 重定向到文件](https://docs.celeryq.dev/en/main/userguide/configuration.html#worker-redirect-stdouts)，但是有时候没有生效，场景如下：

django 项目中的 logging 配置：

```python
# settings.py

LOGGING = {
    ...
    handlers: {
        'console': {
            'class': 'logging.StreamHandler'
        },
        ...
    },
    'loggers': {
        'custom': {
            'handlers': ['console', ...]
        }
    }
}
```

使用示例：

```python
import logging

# 出现在日志文件中
default_logger = logging.getLogger(__name__)
default_logger.info('from custom logger')

# 出现在终端屏幕，但没有出现在日志文件
custom_logger = logging.getLogger('custom')
custom_logger.info('from custom logger')
```

启动 worker 后发现，`default_logger` 记录的信息写到了日志文件中，`custom_logger` 记录的信息却只打印到了终端屏幕上，没有出现在文件中。

查阅 [`logging.StreamHandler` 的源码](https://github.com/python/cpython/blob/8801c6dec79275e9b588ae03e356d8e7656fa3f0/Lib/logging/__init__.py#L1109) 发现它是将信息写入到 `sys.stderr`，但如果是使用 `print` 将信息输出到 `sys.stderr` 该信息仍然会写入到文件中，偏偏 `custom_logger` 不会。

```python
import sys

# 出现在日志文件中
print('from print', file=sys.stderr)
```

在查阅 [celery 对 `worker_redirect_stdouts` 参数的处理逻辑](https://github.com/celery/celery/blob/cca11164860a1bee6ad8626c27a683b482f741eb/celery/app/log.py#L183)后发现，celery 是对 `sys.stdout` 和 `sys.stderr` 重新赋值实现的重定向，因此可以判断出在 celery 重定向之前，`custom_logger` 的 `console` handler 已经拿到了原始的 `sys.stderr`，所以即便 celery 做了重定向，也无法影响到 `custom_logger` 的输出目的地。

可选的处理思路为：在 celery 处理完 logger 的配置后，再将 `custom_logger` 的 `console` handler 重新配置。

具体代码如下：

```python
import sys
import logging

import celery

@celery.signals.after_setup_logger.connect
def on_after_setup_logger(**kwargs):
    logger = logging.getLogger('custom')

    for handler in logger.handlers:
        if handler.name == 'console':
            handler.setStream(sys.stderr)
```

