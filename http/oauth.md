OAuth的核心是访问令牌，它类似于特定用户的API密钥。应用程序获取访问令牌后，就可以使用该令牌代表用户执行操作或访问用户的数据。


首先，我在使用 YNAB，我想将 Chase 银行添加为数据源。OAuth 流程如下所示：

1. YNAB 将我重定向到 Chase 银行。
2. 在 Chase 银行，我使用用户名和密码登录。
3. Chase 屏幕上显示“YNAB 想要连接到 Chase 银行。请选择要授予 YNAB 访问权限的账户”。它会显示我的所有账户列表。假设我只选择我的支票账户，授予 YNAB 读取该账户的权限，然后点击“确定”。
4. 从 Chase 银行，我被重定向回 YNAB，现在，神奇的是，YNAB 已经连接到 Chase 银行了。

## reference
- [OAuth 图解指南 - 作者：Aditya Bhargava](https://www.ducktyped.org/p/an-illustrated-guide-to-oauth)
