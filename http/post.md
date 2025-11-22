## 各种 content-type 类型

see: [Understanding the Different POST Content Types - DjangoTricks](https://www.djangotricks.com/blog/2025/11/understanding-the-different-post-content-types/?utm_campaign=Django%2BNewsletter&utm_medium=email&utm_source=Django_Newsletter_312)

- application/x-www-form-urlencoded 内容为 url 编码后的文本，类似于 get 请求中的查询参数，如 `username=john_doe&password=pass123`
- multipart/form-data 包含文件的 form 表单内容，如：`{"name": "...", "file": file}`，在 djnago 中，可以通过 `request.FILES['file']` 获取到 `file` 的内容
- application/json json 字符串
- application/x-ndjson 全称 Newline-Delimited JSON，包含多行的 json 字符串，每一行都可以被解析为 json 对象
- text/plain 纯文本
- text/html html 格式
- application/xml xml 格式
- image/svg+xml xml 格式的 svg 文件内容
- application/octet-stream 二进制内容
