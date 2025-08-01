# Python 目录结构说明

这是一个 Python 应用程序的目录结构及其功能的详细说明。

## 顶层目录

*   **python/**: Python 应用程序的根目录。
    *   `__init__.py`: Python 包的初始化文件，通常为空。

## 子目录

### `python/api/`

定义了与前端交互的 API 接口。

*   `backup_create.py`: 创建系统备份。
*   `backup_get_defaults.py`: 获取默认备份配置。
*   `backup_inspect.py`: 检查备份文件的内容和元数据。
*   `backup_preview_grouped.py`: 预览按组分类的备份文件，支持过滤和深度限制。
*   `backup_restore.py`: 恢复系统备份。
*   `backup_test.py`: 测试备份配置的模式匹配。
*   `chat_export.py`: 导出聊天记录。
*   `chat_load.py`: 导入聊天记录。
*   `chat_remove.py`: 移除聊天上下文和相关的任务。
*   `chat_reset.py`: 重置聊天上下文。
*   `csrf_token.py`: 获取 CSRF token，用于安全验证。
*   `ctx_window_get.py`: 获取代理上下文窗口的内容。
*   `delete_work_dir_file.py`: 删除工作目录中的文件。
*   `download_work_dir_file.py`: 下载工作目录中的文件。
*   `file_info.py`: 获取文件或目录的详细信息。
*   `get_work_dir_files.py`: 获取工作目录中的文件列表。
*   `health.py`: 执行健康检查并返回 Git 信息。
*   `history_get.py`: 获取代理的聊天历史。
*   `image_get.py`: 获取图像文件或文件类型图标。
*   `import_knowledge.py`: 导入知识文件到代理的记忆中。
*   `mcp_server_get_detail.py`: 获取 MCP 服务器的详细信息。
*   `mcp_server_get_log.py`: 获取 MCP 服务器的日志。
*   `mcp_servers_apply.py`: 应用 MCP 服务器配置。
*   `mcp_servers_status.py`: 获取 MCP 服务器的状态。
*   `message_async.py`: 处理异步消息，用于代理的响应。
*   `message.py`: 处理用户消息，包括文本和附件。
*   `nudge.py`: “推动”代理，重置其进程。
*   `pause.py`: 暂停或恢复代理的运行。
*   `poll.py`: 定期轮询代理状态、日志和任务列表。
*   `restart.py`: 重启应用程序。
*   `rfc.py`: 处理 RFC (Request For Comments) 请求。
*   `scheduler_task_create.py`: 创建新的调度任务（定时、即席、计划）。
*   `scheduler_task_delete.py`: 删除调度任务。
*   `scheduler_task_run.py`: 手动运行调度任务。
*   `scheduler_task_update.py`: 更新调度任务。
*   `scheduler_tasks_list.py`: 列出所有调度任务。
*   `scheduler_tick.py`: 触发调度器执行检查和运行任务。
*   `settings_get.py`: 获取应用程序设置。
*   `settings_set.py`: 设置应用程序设置。
*   `synthesize.py`: 通过 TTS (Text-to-Speech) 合成语音。
*   `transcribe.py`: 通过 STT (Speech-to-Text) 转录音频。
*   `tunnel.py`: 管理网络隧道，例如创建、停止、获取隧道 URL。
*   `tunnel_proxy.py`: 代理隧道服务的请求。
*   `upload.py`: 上传文件。
*   `upload_work_dir_files.py`: 上传文件到工作目录。

### `python/extensions/`

包含了代理行为的扩展点，通常在代理的消息循环或独白的不同阶段执行。

*   **`before_main_llm_call/`**: 在主 LLM 调用之前执行的扩展。
    *   `_10_log_for_stream.py`: 为 LLM 流式响应创建日志条目，用于显示“生成中...”等状态。
    *   `.gitkeep`: 占位文件。
*   **`message_loop_end/`**: 消息循环结束时执行的扩展。
    *   `_10_organize_history.py`: 异步压缩代理的历史记录，以节省上下文空间。
    *   `_90_save_chat.py`: 保存当前聊天上下文到文件。
    *   `.gitkeep`: 占位文件。
*   **`message_loop_prompts_after/`**: 在消息循环中，在生成提示后执行的扩展。
    *   `_50_recall_memories.py`: 根据当前对话内容搜索并召回记忆。
    *   `_51_recall_solutions.py`: 根据当前对话内容搜索并召回解决方案和工具。
    *   `_60_include_current_datetime.py`: 在提示中包含当前日期和时间。
    *   `_91_recall_wait.py`: 等待记忆和解决方案召回任务完成。
    *   `.gitkeep`: 占位文件。
*   **`message_loop_prompts_before/`**: 在消息循环中，在生成提示之前执行的扩展。
    *   `_90_organize_history_wait.py`: 等待历史记录压缩任务完成，如果历史记录过大则同步执行。
    *   `.gitkeep`: 占位文件。
*   **`message_loop_start/`**: 消息循环开始时执行的扩展。
    *   `_10_iteration_no.py`: 记录消息循环的迭代次数。
    *   `.gitkeep`: 占位文件。
*   **`monologue_end/`**: 代理独白结束时执行的扩展。
    *   `_50_memorize_fragments.py`: 记忆对话中的新信息片段。
    *   `_51_memorize_solutions.py`: 记忆成功解决的问题和方案。
    *   `_90_waiting_for_input_msg.py`: 显示等待用户输入的消息。
    *   `.gitkeep`: 占位文件。
*   **`monologue_start/`**: 代理独白开始时执行的扩展。
    *   `_60_rename_chat.py`: 根据聊天内容异步重命名聊天会话。
    *   `.gitkeep`: 占位文件。
*   **`reasoning_stream/`**: 处理推理流的扩展。
    *   `_10_log_from_stream.py`: 从推理流中记录日志，用于显示代理的思考过程。
    *   `.gitkeep`: 占位文件。
*   **`response_stream/`**: 处理响应流的扩展。
    *   `_10_log_from_stream.py`: 从响应流中记录日志，用于显示代理的响应。
    *   `_20_live_response.py`: 处理实时响应，例如将工具输出显示给用户。
    *   `.gitkeep`: 占位文件。
*   **`system_prompt/`**: 构建系统提示的扩展。
    *   `_10_system_prompt.py`: 构建主要系统提示，包括工具和 MCP 工具的描述。
    *   `_20_behaviour_prompt.py`: 添加行为提示（规则）到系统提示中。
    *   `.gitkeep`: 占位文件。

### `python/helpers/`

包含各种辅助函数和类，为 Agent Zero 提供核心功能。

*   `api.py`: 提供 `ApiHandler` 类，用于处理 API 请求和响应，以及管理代理上下文。
*   `attachment_manager.py`: 管理文件附件的上传、保存和图像预览生成。
*   `backup.py`: 提供备份和恢复功能，包括文件模式匹配、系统信息收集和 zip 文件操作。
*   `browser.py`: (已注释掉大部分代码) 曾用于基于 Playwright 的浏览器自动化，可能已废弃或被 `browser_use` 替代。
*   `browser_use.py`: 可能用于初始化或配置 `browser-use` 框架，该框架用于代理驱动的 Web 交互。
*   `call_llm.py`: 封装了调用 LLM 的逻辑，支持系统提示、消息、示例和回调，用于与 LLM 模型进行通信。
*   `cloudflare_tunnel._py`: 处理 Cloudflare Tunnel 的下载、启动和停止，用于创建公共可访问的 URL。
*   `crypto.py`: 提供数据哈希、验证、加密和解密功能，用于安全相关操作。
*   `defer.py`: 实现了异步任务的延迟执行和管理，包括 `DeferredTask` 和 `EventLoopThread`，用于后台任务处理。
*   `dirty_json.py`: 用于解析“不规范”的 JSON 字符串，例如包含注释或缺少引号的 JSON，增强 JSON 解析的鲁棒性。
*   `docker.py`: 管理 Docker 容器的生命周期，包括启动、停止和清理，用于提供隔离的执行环境。
*   `document_query.py`: 提供文档查询功能，包括文档添加、检索、搜索和不同文档类型的处理（HTML、PDF、图像等），用于知识库查询。
*   `dotenv.py`: 管理 `.env` 文件中的环境变量，用于应用程序配置。
*   `duckduckgo_search.py`: 集成了 DuckDuckGo 搜索功能。
*   `errors.py`: 提供错误处理和格式化功能，用于统一错误输出。
*   `extension.py`: 定义了 `Extension` 抽象基类，用于构建代理的扩展，提供通用的扩展点。
*   `extract_tools.py`: 从模块中提取工具类，并处理 JSON 字符串的解析，用于动态加载工具。
*   `faiss_monkey_patch.py`: 为 FAISS 库打补丁，以解决特定环境下的兼容性问题。
*   `file_browser.py`: 提供文件浏览器功能，包括文件上传、删除、列出目录内容等，用于文件管理。
*   `files.py`: 提供各种文件操作函数，如读取、写入、移动、删除文件和目录，以及路径处理。
*   `git.py`: 获取 Git 仓库信息，如分支、提交哈希和标签，用于版本控制信息。
*   `history.py`: 管理代理的聊天历史，包括消息、主题和批量压缩，用于上下文管理。
*   `images.py`: 提供图像处理功能，如图像压缩，用于图像优化。
*   `job_loop.py`: 实现一个后台作业循环，用于定期执行调度任务，确保任务按时执行。
*   `knowledge_import.py`: 导入知识文件，支持多种文件类型，并计算文件校验和，用于构建知识库。
*   `kokoro_tts.py`: 集成 Kokoro TTS 语音合成功能。
*   `localization.py`: 处理时间区域转换和本地化设置。
*   `log.py`: 提供日志记录功能，包括不同类型的日志条目、进度更新和日志截断。
*   `mcp_handler.py`: 处理 MCP (Model Context Protocol) 客户端连接、工具发现和工具调用。
*   `mcp_server.py`: 提供 Agent Zero 作为 MCP 服务器的功能，暴露 `send_message` 和 `finish_chat` 等工具。
*   `memory.py`: 管理代理的记忆存储，使用 FAISS 进行向量搜索，支持不同记忆区域。
*   `messages.py`: 处理消息截断和格式化。
*   `perplexity_search.py`: 集成了 Perplexity AI 搜索功能。
*   `persist_chat.py`: 持久化聊天上下文和日志。
*   `playwright.py`: 确保 Playwright 浏览器二进制文件的安装。
*   `print_catch.py`: 捕获异步函数的打印输出。
*   `print_style.py`: 提供带颜色和样式的打印输出，并记录到 HTML 日志文件。
*   `process.py`: 管理进程的生命周期，包括重启和退出。
*   `rate_limiter.py`: 实现请求和令牌的速率限制。
*   `rfc.py`: 实现了远程函数调用 (RFC) 的客户端和服务器端逻辑。
*   `rfc_exchange.py`: 处理 RFC 相关的密钥交换和根密码获取。
*   `rfc_files.py`: 提供了通过 RFC 机制进行文件操作的接口。
*   `runtime.py`: 提供运行时环境信息，如是否在 Docker 中运行，以及处理开发模式下的 RFC 调用。
*   `searxng.py`: 集成了 SearXNG 搜索功能。
*   `settings.py`: 管理应用程序的设置，包括模型配置、API 密钥、认证和 MCP 设置。
*   `shell_local.py`: 提供本地交互式 shell 会话。
*   `shell_ssh.py`: 提供 SSH 交互式 shell 会话。
*   `strings.py`: 提供字符串处理函数，如清理、格式化和截断。
*   `task_scheduler.py`: 实现了任务调度器，支持定时任务、即席任务和计划任务。
*   `timed_input.py`: 提供带超时功能的输入函数。
*   `tokens.py`: 处理文本令牌的计数和截断。
*   `tool.py`: 定义了 `Tool` 抽象基类，用于构建 Agent Zero 的工具。
*   `tunnel_manager.py`: 管理各种网络隧道服务，如 Cloudflare Tunnel 和 Serveo。
*   `vector_db.py`: 提供向量数据库功能，使用 FAISS 进行相似性搜索和文档存储。
*   `whisper.py`: 集成 OpenAI Whisper 语音转文本功能。

### `python/tools/`

定义了 Agent Zero 可以使用的各种工具。

*   `behaviour_adjustment.py`: 允许代理调整其行为规则。
*   `browser_agent.py`: 允许代理使用 `browser-use` 框架进行 Web 交互。
*   `browser_do._py`: (已注释掉大部分代码) 用于浏览器执行操作（点击、填写、按键等），可能已废弃或被 `browser_agent` 替代。
*   `browser_open._py`: (已注释掉大部分代码) 用于浏览器打开 URL，可能已废弃或被 `browser_agent` 替代。
*   `browser._py`: (已注释掉大部分代码) 浏览器工具的基类，包含截图和历史清理等功能，可能已废弃或被 `browser_agent` 替代。
*   `call_subordinate.py`: 允许代理调用子代理来处理特定任务。
*   `code_execution_tool.py`: 允许代理执行 Python、Node.js 代码或终端命令。
*   `document_query.py`: 允许代理查询文档内容，并进行问答。
*   `input.py`: 允许代理模拟键盘输入到终端会话。
*   `knowledge_tool._py`: 允许代理执行知识搜索，包括在线搜索和记忆库搜索。
*   `memory_delete.py`: 允许代理从记忆中删除指定 ID 的文档。
*   `memory_forget.py`: 允许代理根据查询条件从记忆中删除相关文档。
*   `memory_load.py`: 允许代理根据查询条件从记忆中加载相关文档。
*   `memory_save.py`: 允许代理保存文本到记忆中。
*   `response.py`: 一个特殊的工具，用于代理向用户返回最终响应并结束对话循环。
*   `scheduler.py`: 允许代理管理调度任务（创建、列出、查找、运行、删除）。
*   `search_engine.py`: 允许代理执行在线搜索，主要是通过 SearXNG。
*   `unknown.py`: 当代理尝试使用一个不存在的工具时，此工具会提供一个错误响应。
*   `vision_load.py`: 允许代理加载图像并将其转换为适合 LLM 视觉模型的格式。