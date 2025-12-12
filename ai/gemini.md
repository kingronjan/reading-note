# Gemini CLI 使用技巧

本文总结了 [addyosmani/gemini-cli-tips](https://github.com/addyosmani/gemini-cli-tips) 中介绍的 Gemini CLI 高效使用技巧。

---

### Tip 1: 使用 `GEMINI.md` 进行持久上下文

*   **关键思路**: 通过在项目中创建 `GEMINI.md` 文件，为 AI 提供项目特定的持久上下文（如编码风格、项目架构），避免在每次提示中重复说明。
*   **命令**:
    *   `/init`: 快速生成一个包含项目信息的 `GEMINI.md` 模板。
    *   `/memory show`: 显示 AI 当前加载的完整上下文。
    *   `/memory refresh`: 重新加载磁盘上的上下文（在手动编辑 `GEMINI.md` 后）。
*   **示例**:
    *   `GEMINI.md` 文件内容:
        ```markdown
        # Project Phoenix - AI Assistant
        - All Python code must follow PEP 8 style.
        - Use 4 spaces for indentation.
        - The user is building a data pipeline; prefer functional programming paradigms.
        ```

---

### Tip 2: 创建自定义斜杠命令

*   **关键思路**: 定义自己的斜杠命令来加速重复性任务，本质上是预定义的提示模板。
*   **示例**:
    *   创建文件 `~/.gemini/commands/test/gen.toml`:
        ```toml
        # Invoked as: /test:gen "Description of the test"
        description = "Generates a unit test based on a requirement."
        prompt = """
        You are an expert test engineer. Based on the following requirement, please write a comprehensive unit test using the Jest framework.
        Requirement: {{args}}
        """
        ```
    *   使用: `/test:gen "Ensure the login button redirects to the dashboard upon success"`

---

### Tip 3: 使用自己的 MCP 服务器扩展 Gemini

*   **关键思路**: 通过运行自定义模型上下文协议 (MCP) 服务器，将 Gemini CLI 与外部系统或自定义工具（如专有数据库、Figma 设计）集成。
*   **命令**:
    *   `gemini mcp add myserver --command "python3 my_mcp_server.py" --port 8080`: 注册一个 MCP 服务器。
    *   `/mcp`: 列出所有已注册的 MCP 服务器及其工具。

---

### Tip 4: 利用记忆添加与召回

*   **关键思路**: 将重要事实添加到 AI 的长期记忆中，以便 AI 始终能访问这些信息。
*   **命令**:
    *   `/memory add "<text>"`: 将事实或笔记添加到记忆中。
*   **示例**:
    *   `/memory add "Our staging RabbitMQ is on port 5673"`

---

### Tip 5: 使用检查点和 `/restore` 作为撤销按钮

*   **关键思路**: 启用检查点功能，在 Gemini CLI 修改文件前创建快照，方便回滚。
*   **命令**:
    *   `gemini --checkpointing`: 启动时启用。
    *   `/restore list`: 查看最近的检查点列表。
    *   `/restore <id>`: 回滚到特定的检查点。

---

### Tip 6: 阅读 Google Docs、Sheets 等

*   **关键思路**: 配置 Workspace MCP 服务器后，可以直接粘贴 Google Docs/Sheets 链接，让 Gemini CLI 获取并阅读其内容。
*   **示例**:
    *   `Summarize the requirements from this design doc: https://docs.google.com/document/d/<id>`

---

### Tip 7: 使用 `@` 引用文件和图像以获取明确上下文

*   **关键思路**: 使用 `@` 语法直接将文件、目录或图像附加到提示中，确保 AI 准确地看到这些内容作为上下文。
*   **示例**:
    *   `Explain this code to me: @./src/main.js`
    *   `Refactor the code in @./utils/ to use async/await.`
    *   `Describe what you see in this screenshot: @./design/mockup.png`

---

### Tip 8: 即时工具创建

*   **关键思路**: 让 Gemini CLI 在会话中根据需要创建小型脚本或实用工具。
*   **示例**:
    *   `Generate a Node.js script that reads all '.log' files in the current directory and reports the number of lines in each.`

---

### Tip 9: 使用 Gemini CLI 进行系统故障排除和配置

*   **关键思路**: 将 Gemini CLI 用作操作系统的智能助手，处理通用系统任务。
*   **示例**:
    *   `Fix my .bashrc file, it has an error.`
    *   `When I run npm install, I get an EACCES permission error - how do I fix this?`

---

### Tip 10: YOLO 模式 (谨慎使用)

*   **关键思路**: 启用 YOLO 模式，让 Gemini CLI 自动执行工具操作，无需用户确认。
*   **命令**:
    *   `gemini --yolo` 或 `gemini -y`: 启动时启用。
    *   `Ctrl+Y`: 在交互式会话中切换。

---

### Tip 11: 无头和脚本模式

*   **关键思路**: 在脚本或自动化中使用 Gemini CLI，通过命令行参数或环境变量提供提示。
*   **命令**:
    *   `gemini -p "...prompt..."`: 单次调用。
    *   `some_command | gemini -p "Given the above output, what went wrong?"`: 通过管道输入命令输出。

---

### Tip 12: 保存和恢复聊天会话

*   **关键思路**: 保存和恢复会话，实现长时间对话的无缝暂停和继续。
*   **命令**:
    *   `/chat save <tag>`: 保存当前会话状态。
    *   `/chat resume <tag>`: 恢复指定标签的会话。

---

### Tip 13: 多目录工作区

*   **关键思路**: Gemini CLI 可以为不同项目目录加载独立的上下文 (`./.gemini/GEMINI.md`)，或使用全局上下文 (`~/.gemini/GEMINI.md`)。
*   **示例**: 在不同项目目录中运行 `gemini` 会自动切换上下文。

---

### Tip 14: AI 协助文件整理

*   **关键思路**: 利用 AI 理解文件内容和目的的能力来帮助组织和清理文件。
*   **示例**:
    *   `"Organize these files into appropriate subdirectories: @./"`
    *   `"Delete all temporary build files in this directory."`

---

### Tip 15: 压缩长对话

*   **关键思路**: 通过提示 AI 总结或压缩过去的交互，来管理长对话中的 token 限制。
*   **示例**: `"Summarize our conversation so far."`

---

### Tip 16: 使用 `!` 传递 Shell 命令

*   **关键思路**: 使用 `!` 前缀直接在 Gemini CLI 会话中执行 shell 命令，无需退出。
*   **示例**:
    *   `!ls -l`
    *   `!git status`

---

### Tip 17: 将每个 CLI 工具视为 Gemini 工具

*   **关键思路**: Gemini CLI 可以调用任何现有的命令行工具，从而扩展其能力。
*   **示例**: `"Use 'grep' to find all occurrences of 'TODO' in the current project."`

---

### Tip 18: 利用多模态 AI 查看图像

*   **关键思路**: 使用 `@` 语法引用图像，让 Gemini 理解和处理图像内容。
*   **示例**: `"Describe what you see in this screenshot: @./design/mockup.png"`

---

### Tip 19: 自定义 `$PATH` 提高稳定性

*   **关键思路**: 通过在 `settings.json` 中配置 `$PATH`，可以控制 AI 能访问的 shell 命令，确保稳定性和安全性。
*   **示例**: 在 `settings.json` 中限制 `shell.path`。

---

### Tip 20: 跟踪和减少 Token 消耗

*   **关键思路**: 通过内部的缓存和统计机制来监控和优化 token 使用。
*   **命令**: (具体命令未在文章中明确，但暗示有相关功能)
    *   可能通过 `/token stats` 或类似命令查看。

---

### Tip 21: 使用 `/copy` 快速复制

*   **关键思路**: 使用 `/copy` 命令将 Gemini 的输出快速复制到系统剪贴板。
*   **命令**:
    *   `/copy`: 复制上一个 AI 响应。
    *   `/copy @./file.txt`: 复制文件内容。

---

### Tip 22: 掌握 `Ctrl+C`

*   **关键思路**: `Ctrl+C` 有特殊功能：单按可切换到 shell 模式，双按可退出 CLI。

---

### Tip 23: 使用 `settings.json` 自定义

*   **关键思路**: 通过编辑 `~/.gemini/settings.json` (全局) 或 `./.gemini/settings.json` (项目) 文件来配置 Gemini 的行为。
*   **示例**: `{"checkpointing": { "enabled": true }}`

---

### Tip 24: IDE 集成 (VS Code)

*   **关键思路**: 通过 VS Code 扩展与 Gemini CLI 集成，可以在 IDE 内提供上下文并直观地显示文件差异。

---

### Tip 25: GitHub Action 自动化

*   **关键思路**: 将 Gemini CLI 集成到 GitHub Actions 工作流中，以自动化代码审查、文档生成等任务。

---

### Tip 26: 启用遥测

*   **关键思路**: 启用遥测可以向 Google 发送匿名使用数据，帮助改进 Gemini CLI，并提供使用模式的洞察。
*   **示例**: 通过 `settings.json` 或启动标志 `--telemetry-enable` (假设) 启用。

---

### Tip 27: 关注路线图

*   **关键思路**: 关注项目的官方路线图，了解如后台代理等即将推出的新功能。

---

### Tip 28: 使用扩展

*   **关键思路**: Gemini CLI 支持通过扩展（如 MCP 服务器）来增加新功能和集成。

---

### Tip 29: Corgi 模式彩蛋 🐕

*   **关键思路**: 一个有趣的隐藏彩蛋功能。
*   **示例**: 尝试输入 `/corgi` 或 `corgi mode`。

---

**文章来源**: [https://github.com/addyosmani/gemini-cli-tips](https://github.com/addyosmani/gemini-cli-tips)