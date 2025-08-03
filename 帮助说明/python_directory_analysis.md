python/
├── __init__.py                                 # Python 包初始化文件
├── python目录结构说明.md                       # (可能包含项目Python目录的额外说明)
├── api/                                        # API 接口定义，处理前端请求
│   ├── backup_create.py                        # 创建备份
│   ├── backup_get_defaults.py                  # 获取默认备份设置
│   ├── backup_inspect.py                       # 检查备份内容
│   ├── backup_preview_grouped.py               # 预览分组备份
│   ├── backup_restore_preview.py               # 预览备份恢复
│   ├── backup_restore.py                       # 恢复备份
│   ├── backup_test.py                          # 备份测试相关接口
│   ├── chat_export.py                          # 导出聊天记录
│   ├── chat_load.py                            # 加载聊天记录
│   ├── chat_remove.py                          # 删除聊天记录
│   ├── chat_reset.py                           # 重置聊天
│   ├── csrf_token.py                           # CSRF Token 相关接口
│   ├── ctx_window_get.py                       # 获取上下文窗口信息
│   ├── delete_work_dir_file.py                 # 删除工作目录文件
│   ├── download_work_dir_file.py               # 下载工作目录文件
│   ├── file_info.py                            # 获取文件信息
│   ├── get_work_dir_files.py                   # 获取工作目录文件列表
│   ├── health.py                               # 健康检查接口
│   ├── history_get.py                          # 获取历史记录
│   ├── image_get.py                            # 获取图像
│   ├── import_knowledge.py                     # 导入知识
│   ├── mcp_server_get_detail.py                # 获取 MCP 服务器详情
│   ├── mcp_server_get_log.py                   # 获取 MCP 服务器日志
│   ├── mcp_servers_apply.py                    # 应用 MCP 服务器配置
│   ├── mcp_servers_status.py                   # 获取 MCP 服务器状态
│   ├── message_async.py                        # 异步消息处理
│   ├── message.py                              # 核心消息处理接口，接收用户消息（包括附件）
│   ├── nudge.py                                # 推动/触发 Agent 行为
│   ├── pause.py                                # 暂停 Agent
│   ├── poll.py                                 # 轮询接口
│   ├── restart.py                              # 重启 Agent
│   ├── rfc.py                                  # RFC（Remote Function Call）相关接口
│   ├── scheduler_task_create.py                # 创建调度任务
│   ├── scheduler_task_delete.py                # 删除调度任务
│   ├── scheduler_task_run.py                   # 运行调度任务
│   ├── scheduler_task_update.py                # 更新调度任务
│   ├── scheduler_tasks_list.py                 # 列出所有调度任务
│   ├── scheduler_tick.py                       # 调度器计时
│   ├── settings_get.py                         # 获取设置
│   ├── settings_set.py                         # 设置参数
│   ├── synthesize.py                           # 语音合成接口
│   ├── transcribe.py                           # 语音转文本接口
│   ├── tunnel_proxy.py                         # 隧道代理
│   ├── tunnel.py                               # 隧道管理接口
│   ├── upload_work_dir_files.py                # 上传工作目录文件
│   └── upload.py                               # 文件上传通用接口
├── extensions/                                 # Agent 消息循环的扩展点
│   ├── before_main_llm_call/                   # 在主 LLM 调用前执行的扩展
│   │   ├── _10_log_for_stream.py               # 记录流式日志
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── message_loop_end/                       # 消息循环结束时执行的扩展
│   │   ├── _10_organize_history.py             # 组织/压缩历史记录
│   │   ├── _90_save_chat.py                    # 保存聊天记录
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── message_loop_prompts_after/             # 消息循环提示词后执行的扩展
│   │   ├── _50_recall_memories.py              # 召回记忆
│   │   ├── _51_recall_solutions.py             # 召回解决方案
│   │   ├── _60_include_current_datetime.py     # 包含当前日期时间到提示词
│   │   ├── _91_recall_wait.py                  # 等待记忆/解决方案召回完成
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── message_loop_prompts_before/            # 消息循环提示词前执行的扩展
│   │   ├── _90_organize_history_wait.py        # 等待历史记录组织完成
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── message_loop_start/                     # 消息循环开始时执行的扩展
│   │   ├── _10_iteration_no.py                 # 增加迭代次数
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── monologue_end/                          # Agent 自言自语结束时执行的扩展
│   │   ├── _50_memorize_fragments.py           # 记忆碎片
│   │   ├── _51_memorize_solutions.py           # 记忆解决方案
│   │   ├── _90_waiting_for_input_msg.py        # 等待用户输入消息
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── monologue_start/                        # Agent 自言自语开始时执行的扩展
│   │   ├── _60_rename_chat.py                  # 重命名聊天
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── reasoning_stream/                       # 推理流处理的扩展
│   │   ├── _10_log_from_stream.py              # 从流中记录日志
│   │   └── .gitkeep                            # (Git 占位符)
│   ├── response_stream/                        # 响应流处理的扩展
│   │   ├── _10_log_from_stream.py              # 从流中记录日志
│   │   ├── _20_live_response.py                # 处理实时响应
│   │   └── .gitkeep                            # (Git 占位符)
│   └── system_prompt/                          # 系统提示词处理的扩展
│       ├── _10_system_prompt.py                # 核心系统提示词生成逻辑
│       ├── _20_behaviour_prompt.py             # 处理 Agent 行为提示词
│       └── .gitkeep                            # (Git 占位符)
├── helpers/                                    # 辅助函数和模块，提供通用功能
│   ├── api.py                                  # API 处理基类和通用工具
│   ├── attachment_manager.py                   # 附件管理
│   ├── backup.py                               # 备份和恢复服务核心逻辑
│   ├── browser_use.py                          # 浏览器使用辅助
│   ├── browser.py                              # 浏览器相关实用函数
│   ├── call_llm.py                             # 调用 LLM 模型
│   ├── cloudflare_tunnel._py                   # Cloudflare Tunnel 相关辅助
│   ├── crypto.py                               # 加密相关辅助
│   ├── defer.py                                # 延迟任务处理
│   ├── dirty_json.py                           # 处理不规范的 JSON
│   ├── docker.py                               # Docker 容器管理辅助
│   ├── document_query.py                       # 文档查询辅助
│   ├── dotenv.py                               # .env 文件处理
│   ├── duckduckgo_search.py                    # DuckDuckGo 搜索集成
│   ├── errors.py                               # 错误处理
│   ├── extension.py                            # 扩展机制基类
│   ├── extract_tools.py                        # 工具提取
│   ├── faiss_monkey_patch.py                   # Faiss 库的猴子补丁
│   ├── file_browser.py                         # 文件浏览器功能
│   ├── files.py                                # 核心文件系统操作工具集
│   ├── git.py                                  # Git 相关辅助
│   ├── history.py                              # 历史记录管理
│   ├── images.py                               # 图像处理辅助
│   ├── job_loop.py                             # 作业循环
│   ├── knowledge_import.py                     # 知识导入工具
│   ├── kokoro_tts.py                           # Kokoro 文本转语音 (TTS)
│   ├── localization.py                         # 本地化支持
│   ├── log.py                                  # 日志记录
│   ├── mcp_handler.py                          # MCP (Multi-Agent Collaboration Protocol) 处理
│   ├── mcp_server.py                           # MCP 服务器相关
│   ├── memory.py                               # 记忆管理
│   ├── messages.py                             # 消息处理
│   ├── perplexity_search.py                    # Perplexity 搜索集成
│   ├── persist_chat.py                         # 聊天持久化
│   ├── playwright.py                           # Playwright 浏览器自动化
│   ├── print_catch.py                          # 打印捕获
│   ├── print_style.py                          # 格式化输出到控制台
│   ├── process.py                              # 进程管理
│   ├── rate_limiter.py                         # 速率限制
│   ├── rfc_exchange.py                         # RFC (Remote Function Call) 交换
│   ├── rfc_files.py                            # RFC 文件操作
│   ├── rfc.py                                  # RFC 框架核心
│   ├── runtime.py                              # 运行时信息和函数
│   ├── searxng.py                              # SearXNG 搜索集成
│   ├── settings.py                             # 设置管理
│   ├── shell_local.py                          # 本地 shell 交互
│   ├── shell_ssh.py                            # SSH shell 交互
│   ├── strings.py                              # 字符串处理
│   ├── task_scheduler.py                       # 任务调度器核心逻辑
│   ├── timed_input.py                          # 定时输入
│   ├── tokens.py                               # 令牌计数和管理
│   ├── tool.py                                 # 工具基类
│   ├── tunnel_manager.py                       # 隧道管理器
│   ├── vector_db.py                            # 向量数据库操作
│   └── whisper.py                              # Whisper 语音识别集成
└── tools/                                      # Agent 可调用的工具定义
    ├── behaviour_adjustment.py                 # 调整 Agent 行为
    ├── browser_agent.py                        # 浏览器自动化工具
    ├── browser_do._py                          # 浏览器操作（执行JS）
    ├── browser_open._py                        # 浏览器操作（打开网页）
    ├── browser._py                             # 浏览器通用接口
    ├── call_subordinate.py                     # 调用子 Agent
    ├── code_execution_tool.py                  # 代码执行和终端命令工具
    ├── document_query.py                       # 文档查询工具
    ├── input.py                                # 用户输入工具
    ├── knowledge_tool._py                      # 知识管理工具
    ├── memory_delete.py                        # 删除记忆
    ├── memory_forget.py                        # 遗忘记忆
    ├── memory_load.py                          # 加载记忆
    ├── memory_save.py                          # 保存记忆
    ├── response.py                             # Agent 响应工具
    ├── scheduler.py                            # 任务调度工具
    ├── search_engine.py                        # 搜索引擎工具
    ├── unknown.py                              # 处理未知工具调用
    └── vision_load.py                          # 视觉（图像）加载工具