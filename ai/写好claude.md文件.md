
### 渐进式披露

来自：[写好 CLAUDE.md | HumanLayer 博客](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

编写一份简洁明了的 CLAUDE.md 文件，涵盖你想让 claude 知道的所有内容，可能是一项挑战，尤其是在大型项目中。

为了解决这个问题，我们可以利用渐进式披露原则，确保 Claude 只在需要时才看到特定于任务或项目的指令。

我们建议不要将所有关于构建项目、运行测试、代码约定或其他重要上下文的不同说明都放在同一个 CLAUDE.md 文件中，而是将特定于任务的说明保存在项目某个位置的、具有自描述性名称的单独 Markdown 文件中。

例如：

```
agent_docs/
  |- building_the_project.md
  |- running_tests.md 
  |- code_conventions.md
  |- service_architecture.md
  |- database_schema.md
  |- service_communication_patterns.md
```

然后，可以在 CLAUDE.md 文件中列出这些文件，并简要描述每个文件，然后指示 Claude 判断哪些文件（如果有）是相关的，并在开始工作前阅读这些文件。或者，您可以要求 Claude 在阅读文件之前先向您展示它需要阅读的文件，以获得您的批准。

尽量使用指向原始文件的指针，而不是直接复制粘贴。如果可能，不要在这些文件中包含代码片段——它们很快就会过时。相反，应该提供 file:line 指向权威上下文的引用。

从概念上讲，这与 Claude Skills 的运作方式非常相似，尽管 Claude Skills 更侧重于工具的使用，而不是操作说明。
