## mysql 数据库相关

### 提取 MySQL 中使用文本类型保存的 json 内容，并转为特定类型

from: [How to display a JSON value in Django admin (when using MySQL) // Enrique Soria](https://blog.enriquesoria.com/display-json-value-django-admin-list/?utm_campaign=Django%2BNewsletter&utm_medium=email&utm_source=Django_Newsletter_312)

```python
from django.db.models import CharField
from django.db.models import Func
from django.db.models import Value
from django.db.models.functions import Cast


class JSONExtractAndCast(Cast):
    def __init__(self, expression, *paths, output_field):
        # borrowed from django_mysql.models.functions.JSONExtract
        exprs = [expression]
        for path in paths:
            if not hasattr(path, "resolve_expression"):
                path = Value(path)
            exprs.append(path)

        extracted_value = Func(
            *exprs,
            function="JSON_EXTRACT",
            output_field=CharField(),
        )
        unquoted_value = Func(
            extracted_value,
            function="JSON_UNQUOTE",
            output_field=output_field,
        )
        super().__init__(unquoted_value, output_field=output_field)
```

usage:

```python
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _payload_timestamp=JSONExtractAndCast(
                "payload",
                "$.timestamp",
                output_field=DateTimeField(),
            )
        )
```
