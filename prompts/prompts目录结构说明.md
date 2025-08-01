# Prompts 目录结构说明

此文档旨在说明 `prompts` 目录下各子目录的用途和功能，并提供完整的目录树结构。

```
prompts/
├── agent0/                                 # 针对 Agent0 框架或特定 Agent0 行为相关的提示词。
│   ├── _context.md                         # Agent0 角色的英文上下文信息。
│   ├── agent.system.main.role.md           # Agent0 角色的主要系统提示词（英文）。
│   └── agent.system.tool.response.md       # Agent0 工具响应相关的英文提示词。
├── default/                                # 默认的、通用的或不属于任何特定角色的提示词，例如通用的系统角色定义。
│   ├── _context.md                         # 默认角色的英文上下文信息。
│   ├── agent.context.extras.md             # 代理额外上下文（英文）。
│   ├── agent.system.behaviour.md           # 代理行为相关的英文系统提示。
│   ├── agent.system.behaviour_default.md   # 代理默认行为相关的英文系统提示。
│   ├── agent.system.datetime.md            # 代理日期时间相关的英文系统提示。
│   ├── agent.system.instruments.md         # 代理工具相关的英文系统提示。
│   ├── agent.system.main.md                # 代理主要系统提示（英文）。
│   ├── agent.system.main.communication.md  # 代理主要系统通信相关的英文提示。
│   ├── agent.system.main.environment.md    # 代理主要系统环境相关的英文提示。
│   ├── agent.system.main.role.md           # 代理主要系统角色相关的英文提示。
│   ├── agent.system.main.solving.md        # 代理主要系统解决问题相关的英文提示。
│   ├── agent.system.main.tips.md           # 代理主要系统提示和技巧相关的英文提示。
│   ├── agent.system.mcp_tools.md           # 代理 MCP 工具相关的英文系统提示。
│   ├── agent.system.memories.md            # 代理记忆相关的英文系统提示。
│   ├── agent.system.solutions.md           # 代理解决方案相关的英文系统提示。
│   ├── agent.system.tool.behaviour.md      # 代理工具行为相关的英文系统提示。
│   ├── agent.system.tool.browser._md       # 代理浏览器工具（旧版或特殊）相关的英文系统提示。
│   ├── agent.system.tool.browser.md        # 代理浏览器工具相关的英文系统提示。
│   ├── agent.system.tool.call_sub.md       # 代理调用子工具相关的英文系统提示。
│   ├── agent.system.tool.call_sub.py       # 代理调用子工具相关的 Python 脚本。
│   ├── agent.system.tool.code_exe.md       # 代理代码执行工具相关的英文系统提示。
│   ├── agent.system.tool.document_query.md # 代理文档查询工具相关的英文系统提示。
│   ├── agent.system.tool.input.md          # 代理输入工具相关的英文系统提示。
│   ├── agent.system.tool.knowledge.md      # 代理知识库工具相关的英文系统提示。
│   ├── agent.system.tool.memory.md         # 代理记忆工具相关的英文系统提示。
│   ├── agent.system.tool.response.md       # 代理工具响应相关的英文系统提示。
│   ├── agent.system.tool.scheduler.md      # 代理调度工具相关的英文系统提示。
│   ├── agent.system.tool.search_engine.md  # 代理搜索引擎工具相关的英文系统提示。
│   ├── agent.system.tool.web.md            # 代理 Web 工具相关的英文系统提示。
│   ├── agent.system.tools_vision.md        # 代理视觉工具相关的英文系统提示。
│   ├── agent.system.tools.md               # 代理通用工具相关的英文系统提示。
│   ├── behaviour.merge.msg.md              # 行为合并消息相关的英文提示。
│   ├── behaviour.merge.sys.md              # 行为合并系统相关的英文提示。
│   ├── behaviour.search.sys.md             # 行为搜索系统相关的英文提示。
│   ├── behaviour.updated.md                # 行为更新相关的英文提示。
│   ├── browser_agent.system.md             # 浏览器代理系统相关的英文提示。
│   ├── fw.ai_response.md                   # 框架 AI 响应相关的英文提示。
│   ├── fw.bulk_summary.msg.md              # 框架批量摘要消息相关的英文提示。
│   ├── fw.bulk_summary.sys.md              # 框架批量摘要系统相关的英文提示。
│   ├── fw.code.info.md                     # 框架代码信息相关的英文提示。
│   ├── fw.code.max_time.md                 # 框架代码执行最大时间相关的英文提示。
│   ├── fw.code.no_out_time.md              # 框架代码无输出时间相关的英文提示。
│   ├── fw.code.no_output.md                # 框架代码无输出相关的英文提示。
│   ├── fw.code.pause_dialog.md             # 框架代码暂停对话框相关的英文提示。
│   ├── fw.code.pause_time.md               # 框架代码暂停时间相关的英文提示。
│   ├── fw.code.reset.md                    # 框架代码重置相关的英文提示。
│   ├── fw.code.runtime_wrong.md            # 框架代码运行时错误相关的英文提示。
│   ├── fw.document_query.optmimize_query.md # 框架文档查询优化查询相关的英文提示。
│   ├── fw.document_query.system_prompt.md  # 框架文档查询系统提示相关的英文提示。
│   ├── fw.error.md                         # 框架错误相关的英文提示。
│   ├── fw.intervention.md                  # 框架干预相关的英文提示。
│   ├── fw.knowledge_tool.response.md       # 框架知识工具响应相关的英文提示。
│   ├── fw.memories_deleted.md              # 框架记忆删除相关的英文提示。
│   ├── fw.memories_not_found.md            # 框架记忆未找到相关的英文提示。
│   ├── fw.memory_saved.md                  # 框架记忆保存相关的英文提示。
│   ├── fw.memory.hist_suc.sys.md           # 框架记忆历史成功系统相关的英文提示。
│   ├── fw.memory.hist_sum.sys.md           # 框架记忆历史总结系统相关的英文提示。
│   ├── fw.msg_cleanup.md                   # 框架消息清理相关的英文提示。
│   ├── fw.msg_from_subordinate.md          # 框架来自下属消息相关的英文提示。
│   ├── fw.msg_misformat.md                 # 框架消息格式错误相关的英文提示。
│   ├── fw.msg_repeat.md                    # 框架消息重复相关的英文提示。
│   ├── fw.msg_summary.md                   # 框架消息摘要相关的英文提示。
│   ├── fw.msg_timeout.md                   # 框架消息超时相关的英文提示。
│   ├── fw.msg_truncated.md                 # 框架消息截断相关的英文提示。
│   ├── fw.rename_chat.msg.md               # 框架聊天重命名消息相关的英文提示。
│   ├── fw.rename_chat.sys.md               # 框架聊天重命名系统相关的英文提示。
│   ├── fw.tool_not_found.md                # 框架工具未找到相关的英文提示。
│   ├── fw.tool_result.md                   # 框架工具结果相关的英文提示。
│   ├── fw.topic_summary.msg.md             # 框架主题摘要消息相关的英文提示。
│   ├── fw.topic_summary.sys.md             # 框架主题摘要系统相关的英文提示。
│   ├── fw.user_message.md                  # 框架用户消息相关的英文提示。
│   ├── fw.warning.md                       # 框架警告相关的英文提示。
│   ├── memory.memories_query.sys.md        # 记忆查询系统相关的英文提示。
│   ├── memory.memories_sum.sys.md          # 记忆总结系统相关的英文提示。
│   ├── memory.solutions_query.sys.md       # 解决方案查询系统相关的英文提示。
│   ├── memory.solutions_sum.sys.md         # 解决方案总结系统相关的英文提示。
│   └── msg.memory_cleanup.md               # 消息记忆清理相关的英文提示。
├── developer/                              # 为“开发者”角色设计的提示词，例如代码生成、调试、API 使用、软件开发流程等。
│   ├── _context.md                         # 开发者角色的英文上下文信息。
│   ├── agent.system.main.communication.md  # 开发者角色主要系统通信相关的英文提示。
│   └── agent.system.main.role.md           # 开发者角色主要系统提示词（英文）。
├── hacker/                                 # 与“黑客”或安全相关任务的提示词，例如漏洞分析、渗透测试场景、逆向工程等。
│   ├── _context.md                         # 黑客角色的英文上下文信息。
│   ├── agent.system.main.environment.md    # 黑客角色主要系统环境相关的英文提示。
│   └── agent.system.main.role.md           # 黑客角色主要系统提示词（英文）。
└── researcher/                             # 为“研究员”角色设计的提示词，例如信息检索、数据分析、论文写作、文献综述等。
    ├── _context.md                         # 研究员角色的英文上下文信息。
    ├── agent.system.main.communication.md  # 研究员角色主要系统通信相关的英文提示。
    └── agent.system.main.role.md           # 研究员角色主要系统提示词（英文）。