本文记录了我使用 ai 编码工具的一些心得体会，仍在完善中，希望对你也有帮助，如果你看完有任何想法，也欢迎和我沟通。

# ai 工具

我目前在用的有三款：

- [gemini cli](https://github.com/google-gemini/gemini-cli)
- [iflow cli](https://github.com/iflow-ai/iflow-cli)
- [claude code](https://github.com/anthropics/claude-code) 国内使用[参考教程](https://www.cnblogs.com/javastack/p/19217578)，使用的是 doubao-seed-code 模型

我偏向使用 cli-like 的 ai 工具，在终端看着它自己运行并解决问题体验挺好的。对于一些简单的问题，比如：pgrep 的用法？我会倾向于使用网页版，毕竟网页版的页面进入很快。

各个工具的官方文档其实也详细介绍了各种使用技巧，值得学习，比如：

- [claude code 常用工作流程](https://code.claude.com/docs/en/common-workflows)

# 用 git worktree 让工具并行

这里引用 claude code 官方文档上的描述：

- 每个工作树都有其独立的文件状态，这使其非常适合并行 Claude Code 会话
- 在一个工作树中所做的更改不会影响其他工作树，从而防止 Claude 实例之间相互干扰
- 所有工作树共享相同的 Git 历史记录和远程连接
- 对于长时间运行的任务，您可以让 Claude 在一个工作树中工作，而您则在另一个工作树中继续开发
- 使用描述性的目录名称，以便轻松识别每个工作树所对应的任务
- 请记住，在每个新的工作树中，都要根据项目配置初始化开发环境

# 重视测试

测试可以让 ai 快速的验证自己写的代码有无问题，如果你在写开始项目之前已经有非常完善的测试，那么完全可以放心的让 ai 遵循测试驱动开发的流程来工作，只要让 ai 别修改测试文件就行，如果它认为确实有必要修改，那么也要先征得你的同意。

# 氛围编程

对于一些小工具，比较偏向于使用这种方式，把 ai 写的代码当作一个黑盒，从不打开看，让 ai 自己去编写、验证、修改，我看着哪里不好，就给出修改意见，哪怕这个意见比较模糊，比如，把边栏再调宽一点。最后直到我满意为止，我不会去看甚至理解具体的实现细节，一方面也是怕我自己强迫症犯了忍不住去改。

# 规范驱动开发

大型应用开发时我比较偏向使用这种方式，可以减少 ai 的理解偏差，也可以减少团队成员的理解偏差。

据我所知目前的几种规范落地工具：

- [openspec](https://github.com/Fission-AI/OpenSpec)
- [github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development](https://github.com/github/spec-kit)

我目前仅仅使用过 openspec，用下来发现这仍然时比较考验模型本身能力的，此外，虽然 openspec 本身的命令有标准的提示词，但我们仍然可以对其修改，以符合自己的项目实际情况，比如在生成提案时，需要明确的给出表结构语句、涉及的 sql 等，可以减少应用提案时的歧义。

在第一次生成提案时，可能会反复的和 ai 沟通，确保生成的结果是准确且符合预期的，那么在这之后，可以将沟通的内容总结出来，改进生成提案命令所使用的提示词。

另外最近看到一个只包含规范的开源项目：[whenwords](https://github.com/dbreunig/whenwords)，作者本质上仅仅开源了规范，而我们可以根据这份规范使用任意 ai 模型生成想要的代码语言。背景和相关思考可以参见：[一个无需代码的软件库](https://www.dbreunig.com/2026/01/08/a-software-library-with-no-code.html)

# 提示词依然很重要

值得参考的提示词：

- [分享个人在用的 IFLOW 编程全局提示词 - iFlow CLI / 实践探索 - 心流 AI 交流社区](https://vibex.iflow.cn/t/topic/257)