<div align="center">

# `Agent Zero`


[![Agent Zero Website](https://img.shields.io/badge/Website-agent--zero.ai-0A192F?style=for-the-badge&logo=vercel&logoColor=white)](https://agent-zero.ai) [![Thanks to Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Thanks%20to%20Sponsors-FF69B4?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/agent0ai) [![Follow on X](https://img.shields.io/badge/X-Follow-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/Agent0ai) [![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/B8KZKNsPpj) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@AgentZeroFW) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jan-tomasek/) [![Follow on Warpcast](https://img.shields.io/badge/Warpcast-Follow-5A32F3?style=for-the-badge)](https://warpcast.com/agent-zero)

[简介](#a-personal-organic-agentic-framework-that-grows-and-learns-with-you) •
[安装](./docs/installation.md) •
[如何更新](./docs/installation.md#how-to-update-agent-zero) •
[文档](./docs/README.md) •
[使用](./docs/usage.md)

</div>


<div align="center">

> ### 🚨 **重要公告** 🚨

Agent Zero 的原始 GitHub 和 DockerHub 仓库已转移到新的命名空间：

- **GitHub & DockerHub:** `agent0ai/agent-zero`

从现在开始，`git clone` 和 `docker pull` 命令都请使用此名称。

</div>



[![展示](/docs/res/showcase-thumb.png)](https://youtu.be/lazLNcEYsiQ)



## 一个与您共同成长和学习的个性化、有机智能体框架



- Agent Zero 不是一个预定义的智能体框架。它旨在动态地、有机地成长，并随着您的使用而学习。
- Agent Zero 完全透明、可读、可理解、可定制且交互性强。
- Agent Zero 使用计算机作为工具来完成其（您的）任务。

# 💡 主要功能

1. **通用助手**

- Agent Zero 未针对特定任务进行预编程（但可以）。它旨在成为一个通用个人助手。给它一个任务，它将收集信息、执行命令和代码、与其他代理实例协作，并尽力完成任务。
- 它具有持久内存，允许它记住以前的解决方案、代码、事实、指令等，以便将来更快、更可靠地解决任务。

![Agent 0 工作](/docs/res/ui-screen-2.png)

2. **计算机即工具**

- Agent Zero 使用操作系统作为工具来完成任务。它没有预编程的单一用途工具。相反，它可以编写自己的代码并使用终端根据需要创建和使用自己的工具。
- 其工具库中唯一的默认工具是在线搜索、内存功能、通信（与用户和其他代理）以及代码/终端执行。其他所有功能均由代理本身创建或可由用户扩展。
- 工具使用功能已从头开发，以实现最佳兼容性和可靠性，即使使用非常小的模型也是如此。
- **默认工具：** Agent Zero 包括知识、网页内容、代码执行和通信等工具。
- **创建自定义工具：** 通过创建自己的自定义工具来扩展 Agent Zero 的功能。
- **仪器：** 仪器是一种新型工具，允许您创建可由 Agent Zero 调用的自定义函数和过程。

3. **多代理协作**

- 每个代理都有一个上级代理为其分配任务和指令。每个代理都会向上级报告。
- 对于链中的第一个代理（Agent 0），上级是人类用户；代理没有区别。
- 每个代理都可以创建其下级代理，以帮助分解和解决子任务。这有助于所有代理保持其上下文清晰和专注。

![多代理](docs/res/physics.png)
![多代理 2](docs/res/physics-2.png)

4. **完全可定制和可扩展**

- 该框架中几乎没有任何硬编码。没有任何东西是隐藏的。一切都可以由用户扩展或更改。
- 整个行为由 `prompts/default/agent.system.md` 文件中的系统提示定义。更改此提示将极大地改变框架。
- 框架不以任何方式指导或限制代理。代理没有必须遵循的硬编码规则。
- 发送给代理的通信循环中的每个提示、每个小消息模板都可以在 `prompts/` 文件夹中找到并更改。
- 每个默认工具都可以在 `python/tools/` 文件夹中找到，并可以更改或复制以创建新的预定义工具。

![提示](/docs/res/prompts.png)

5. **沟通是关键**

- 给您的代理一个适当的系统提示和指令，它就能创造奇迹。
- 代理可以与上级和下级沟通，提问、给出指令并提供指导。在系统提示中指导您的代理如何有效沟通。
- 终端界面是实时流式传输和交互式的。您可以随时停止并介入。如果您发现代理方向错误，只需立即停止并告诉它。
- 该框架有很多自由度。您可以指示您的代理定期向上级报告，请求继续的许可。您可以指示它们在使用积分系统决定何时委派子任务。上级可以复核下级的成果并提出异议。可能性是无限的。

## 🚀 您可以用 Agent Zero 构建的东西

- **开发项目** - `“创建一个具有实时数据可视化的 React 仪表盘”`

- **数据分析** - `“分析上季度 NVIDIA 销售数据并创建趋势报告”`

- **内容创作** - `“撰写一篇关于微服务的技术博客文章”`

- **系统管理** - `“为我们的 Web 服务器设置监控系统”`

- **研究** - `“收集并总结五篇关于 CoT 提示的最新 AI 论文”`



# ⚙️ 安装

点击观看视频，了解如何安装 Agent Zero：

[![简易安装指南](/docs/res/easy_ins_vid.png)](https://www.youtube.com/watch?v=w5v5Kjx51hs)

包含视频的 Windows、macOS 和 Linux 详细设置指南可在 Agent Zero 文档的[此页面](./docs/installation.md)找到。

### ⚡ 快速开始

```bash
# 拉取并运行 Docker 镜像

docker pull agent0ai/agent-zero
docker run -p 50001:80 agent0ai/agent-zero

# 访问 http://localhost:50001 开始使用
```

## 🐳 完全 Docker 化，支持语音转文本和文本转语音

![设置](docs/res/settings-page-ui.png)

- 可定制的设置允许用户根据自己的需求调整代理的行为和响应。
- Web UI 输出非常清晰、流畅、色彩丰富、可读且交互性强；没有任何隐藏。
- 您可以直接在 Web UI 中加载或保存聊天记录。
- 您在终端中看到的相同输出会自动保存到每个会话的 `logs/` 文件夹中的 HTML 文件中。

![时间示例](/docs/res/time_example.jpg)

- 代理输出实时流式传输，允许用户随时阅读和干预。
- 无需编码；只需提示和沟通技巧即可。
- 凭借可靠的系统提示，即使是小型模型，框架也能可靠运行，包括精确的工具使用。

## 👀 请记住

1. **Agent Zero 可能很危险！**

- 经过适当的指导，Agent Zero 能够完成许多事情，甚至可能对您的计算机、数据或帐户造成潜在危险操作。始终在隔离环境（如 Docker）中运行 Agent Zero，并谨慎对待您的愿望。

2. **Agent Zero 基于提示。**

- 整个框架由 `prompts/` 文件夹指导。代理指南、工具说明、消息、实用 AI 功能，都在那里。


## 📚 阅读文档

| 页面 | 描述 |
|-------|-------------|
| [安装](./docs/installation.md) | 安装、设置和配置 |
| [使用](./docs/usage.md) | 基本和高级使用 |
| [架构](./docs/architecture.md) | 系统设计和组件 |
| [贡献](./docs/contribution.md) | 如何贡献 |
| [故障排除](./docs/troubleshooting.md) | 常见问题及其解决方案 |


## 🎯 更新日志


### v0.9.2 - Kokoro TTS，附件
[发布视频](https://www.youtube.com/watch?v=sPot_CAX62I)

- Kokoro 文本转语音集成
- 新的消息附件系统
- 次要更新：日志截断、超链接目标、组件示例、API 清理



### v0.9.1 - LiteLLM，UI 改进
[发布视频](https://youtu.be/crwr0M4Spcg)
- Langchain 已替换为 LiteLLM
    - 支持推理模型流式传输
    - 支持更多提供商
    - Openrouter 设置为默认，而不是 OpenAI
- UI 改进
    - 新的消息分组系统
    - 通信更流畅、更高效
    - 可折叠的消息类型
    - 代码执行工具输出改进
    - 表格和代码块可滚动
    - 在移动设备上更省空间
- 支持可流式 HTTP MCP 服务器
- LLM API URL 已添加到 Azure、本地和自定义提供商的模型配置中
    

### v0.9.0 - 代理角色，备份/恢复
[发布视频](https://www.youtube.com/watch?v=rMIe-TC6H-k)
- 下级代理可以使用提示配置文件来扮演不同角色
- 备份/恢复功能，方便升级
- 安全和错误修复

### v0.8.7 - 格式化，文档 RAG 最新
[发布视频](https://youtu.be/OQJkfofYbus)
- 响应中的 markdown 渲染
- 实时响应渲染
- 文档问答工具

### v0.8.6 - 合并和更新
[发布视频](https://youtu.be/l0qpK3Wt65A)
- 与 Hacking Edition 合并
- 浏览器使用升级和集成重做
- 隧道提供商切换

### v0.8.5 - **MCP 服务器 + 客户端**
[发布视频](https://youtu.be/pM5f4Vz3_IQ)

- Agent Zero 现在可以充当 MCP 服务器
- Agent Zero 可以使用外部 MCP 服务器作为工具

### v0.8.4.1 - 2
默认模型设置为 gpt-4.1
- 代码执行工具改进
- 浏览器代理改进
- 内存改进
- 与上下文管理相关的各种错误修复
- 消息格式改进
- 调度程序改进
- 新的模型提供商
- 输入工具修复
- 兼容性和稳定性改进

### v0.8.4
[发布视频](https://youtu.be/QBh_h_D_E24)

- **远程访问（移动）**

### v0.8.3.1
[发布视频](https://youtu.be/AGNpQ3_GxFQ)

- **自动嵌入**


### v0.8.3
[发布视频](https://youtu.be/bPIZo0poalY)

- ***规划和调度***

### v0.8.2
[发布视频](https://youtu.be/xMUNynQ9x6Y)

- **终端多任务处理**
- **聊天名称**

### v0.8.1
[发布视频](https://youtu.be/quv145buW74)

- **浏览器代理**
- **UX 改进**

### v0.8
[发布视频](https://youtu.be/cHDCCSr1YRI)

- **Docker 运行时**
- **新的消息历史和摘要系统**
- **代理行为更改和管理**
- **文本转语音 (TTS) 和语音转文本 (STT)**
- **Web UI 中的设置页面**
- **SearXNG 集成取代 Perplexity + DuckDuckGo**
- **文件浏览器功能**
- **KaTeX 数学可视化支持**
- **聊天中文件附件**

### v0.7
[发布视频](https://youtu.be/U_Gl0NPalKA)

- **自动内存**
- **UI 改进**
- **工具**
- **扩展框架**
- **反射提示**
- **错误修复**

## 🤝 社区与支持

- [加入我们的 Discord](https://discord.gg/B8KZKNsPpj) 进行实时讨论或[访问我们的 Skool 社区](https://www.skool.com/agent-zero)。
- [关注我们的 YouTube 频道](https://www.youtube.com/@AgentZeroFW) 获取动手解释和教程
- [报告问题](https://github.com/agent0ai/agent-zero/issues) 获取错误修复和功能 