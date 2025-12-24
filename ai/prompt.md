# from
- [如何用AI Coding和Claude Code提升开发效率？看我的全流程复盘](https://mp.weixin.qq.com/s/6j-MqSrJz5YlKAe2LZW6pg?poc_token=HPpBS2mj7Oz8oUBYV7OcM_BanJQbH40L81Q2pfVU)


# references
- [awesome-cursor-rules-mdc/rules-mdc/python.mdc at main · sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc/blob/main/rules-mdc/python.mdc)


# 摘录

在开始使用 AI Coding 之前，是有必要系统学习一下 Prompt 技巧，对后续使用效果影响是很大。

## 经验

### 1. 清晰的需求描述

如果一个需求不能描述出来，那么谨慎将任务交给 AI，因为你可能获取到的是惊喜，也可能是失望。举个例子，作为服务端同学，如果没法用语言描述前端这个输入框的视觉效果，那就没办法让 AI 实现前端代码

另外，在中文表达的时候可能存在二义性，可以中英文混合描述来表达需求。

### 2. 使用结构化的方式表示 Prompt

COSTAR 框架是 2023 年新加坡 prompt 大赛冠军总结出来的一个提示词编写框架，他将 Prompt 分成了 Context、Objective、Style、Tone、Audience、Response 这几个部分，分别表示任务的背景、agent 的目标、风格、回复预期、受众以及响应格式要求。我经常会将 style、tone、audience 做一些修改，加入一些对 agent 的要求。


### 3. 让 AI 协助将需求明确清楚，然后再做 prompt engineering

在高效写 prompt，或者明确需求这块，可以借助一些 AI 的工具，提升写 prompt 的效率。比如 openai 的 prompt 工具，也可以自己写一个 prompt 优化的 agent。Claude 在写 prompt template 这方面的效果比较不错。


## 合理划分 AI 任务边界

1. 能力范围内的任务：让 AI 处理逻辑清晰但实现耗时的任务，可以显著提升效率。
2. 略超出能力范围的任务：通过调研、短期学习，就可以解决的，那也可以把这部分任务交给 AI 去解决。
3. 远超能力范围的任务：对于自己完全不熟悉的技术领域，不建议完全依赖 AI，除非这个代码仅仅只是用于 demo 用途，否则容易积累技术债。

## 小步快跑，每一步需要可验证

不要等代码全生成了，然后一次性调试，好的代码应该像细菌🦠一样（by Karpathy），精炼，模块化，闭包 (copy paste-able)。

## AI 生成的方案和代码必须要 Review

除非需求极其清晰，否则不要期望一次命令就能完成一个完整需求，AI 认为的完成，有可能并不是实际的完成。一方面可能会因为上下文长度的原因，遗忘，或者产生幻觉。 另外一方面对于项目的了解程度的片面性，生产出来的代码质量或技术方案不够好。

## 频繁提交到 git 仓库
1. git history 就是项目的另外一份 README.md
2. 频繁提交有助于在问题出现时方便回滚。

## 有效管理上下文

1. 提供精确信息

    - 当已确定修改范围时，应提供准确的文件路径和相关细节。
    - 先通过与 AI 逐步沟通，获取并明确关键信息，形成清晰上下文后，再让 AI 执行。

2. 信息压缩策略

    手动筛选重要信息，只保留有价值的部分。

3. 控制任务粒度

    不要一次完成太复杂的任务，增加 review 难度

4. 利用外部记忆

    将失败的任务手动编辑出来，并存储在一个外部文档中，然后告诉 AI 去逐个修复。

5. 知识库很重要

    对于一个已经存在的工程项目，建议先让 AI 针对代码写说明文档 (README.md)，然后再让他参与到写代码 。
