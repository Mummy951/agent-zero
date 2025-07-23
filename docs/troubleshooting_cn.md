# 故障排除和常见问题
本页解答了常见问题 (FAQ) 并提供了使用 Agent Zero 时遇到的常见问题的故障排除步骤。

## 常见问题
**1. 如何让 Agent Zero 直接处理我的文件或目录？**
- 将文件/目录放置在 `work_dir` 目录中。Agent Zero 将能够对其执行任务。`work_dir` 目录位于 Docker 容器的根目录中。

**2. 当我在聊天中输入内容时，没有任何反应。怎么回事？**
- 检查您是否在“设置”页面中设置了 API 密钥。如果未设置，应用程序将无法与运行 LLM 和执行任务所需的端点通信。

**3. 如何将开源模型与 Agent Zero 集成？**
请参阅文档的 [选择您的 LLM](installation.md#installing-and-using-ollama-local-models) 部分，了解配置不同 LLM 的详细说明和示例。本地模型可以使用 Ollama 或 LM Studio 运行。

> [!TIP]
> 某些 LLM 提供商提供免费使用其 API 的服务，例如 Groq、Mistral 或 SambaNova。

**6. 如何让 Agent Zero 在会话之间保留内存？**
请参阅文档的 [如何更新 Agent Zero](installation.md#how-to-update-agent-zero) 部分，了解如何在保留内存和数据的情况下更新 Agent Zero 的说明。

**7. 我在哪里可以找到更多文档或教程？**
- 加入 Agent Zero [Skool](https://www.skool.com/agent-zero) 或 [Discord](https://discord.gg/Z2tun2N3) 社区以获得支持和讨论。

**8. 如何调整 API 速率限制？**
修改 `initialize.py` 中 `AgentConfig` 类中的 `rate_limit_seconds` 和 `rate_limit_requests` 参数。

**9. 我的 `code_execution_tool` 无法工作，怎么回事？**
- 确保您已安装并正在运行 Docker。如果在 macOS 上使用 Docker Desktop，请在 Docker Desktop 的设置中授予其访问项目文件的权限。有关更多详细信息，请查看 [安装指南](installation.md#4-install-docker-docker-desktop-application)。
- 验证 Docker 镜像是否已更新。

**10. Agent Zero 可以与外部 API 或服务（例如 WhatsApp）交互吗？**
通过创建自定义工具或解决方案，Agent Zero 可以与外部 API 交互。请参阅有关创建它们的文档。

## 故障排除

**安装**
- **Docker 问题：** 如果 Docker 容器无法启动，请查阅 Docker 文档并验证您的 Docker 安装和配置。在 macOS 上，请确保您已按照 [安装指南](installation.md#4-install-docker-docker-desktop-application) 中所述，在 Docker Desktop 的设置中授予 Docker 访问项目文件的权限。验证 Docker 镜像是否已更新。

**使用**

- **终端命令未执行：** 确保 Docker 容器正在运行并已正确配置。如果适用，请检查 SSH 设置。通过从 Docker Desktop 应用程序中移除 Docker 镜像，然后重新拉取，检查 Docker 镜像是否已更新。

* **错误消息：** 密切关注 Web UI 或终端中显示的错误消息。它们通常为诊断问题提供有价值的线索。在在线搜索或社区论坛中查找特定错误消息以获取潜在解决方案。

* **性能问题：** 如果 Agent Zero 运行缓慢或无响应，可能是由于资源限制、网络延迟或您的提示和任务的复杂性造成的，尤其是在使用本地模型时。 