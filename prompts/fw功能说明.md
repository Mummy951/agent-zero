# fw 功能说明

## 提示词文件列表及功能

- [`fw.ai_response.md`](prompts/default/fw.ai_response.md): 框架 AI 响应相关的英文提示。
- [`fw.bulk_summary.msg.md`](prompts/default/fw.bulk_summary.msg.md): 框架批量摘要消息相关的英文提示。
- [`fw.bulk_summary.sys.md`](prompts/default/fw.bulk_summary.sys.md): 框架批量摘要系统相关的英文提示。
- [`fw.code.info.md`](prompts/default/fw.code.info.md): 框架代码信息相关的英文提示。
- [`fw.code.max_time.md`](prompts/default/fw.code.max_time.md): 框架代码执行最大时间相关的英文提示。
- [`fw.code.no_out_time.md`](prompts/default/fw.code.no_out_time.md): 框架代码无输出时间相关的英文提示。
- [`fw.code.no_output.md`](prompts/default/fw.code.no_output.md): 框架代码无输出相关的英文提示。
- [`fw.code.pause_dialog.md`](prompts/default/fw.code.pause_dialog.md): 框架代码暂停对话框相关的英文提示。
- [`fw.code.pause_time.md`](prompts/default/fw.code.pause_time.md): 框架代码暂停时间相关的英文提示。
- [`fw.code.reset.md`](prompts/default/fw.code.reset.md): 框架代码重置相关的英文提示。
- [`fw.code.runtime_wrong.md`](prompts/default/fw.code.runtime_wrong.md): 框架代码运行时错误相关的英文提示。
- [`fw.document_query.optmimize_query.md`](prompts/default/fw.document_query.optmimize_query.md): 框架文档查询优化查询相关的英文提示。
- [`fw.document_query.system_prompt.md`](prompts/default/fw.document_query.system_prompt.md): 框架文档查询系统提示相关的英文提示。
- [`fw.error.md`](prompts/default/fw.error.md): 框架错误相关的英文提示。
- [`fw.intervention.md`](prompts/default/fw.intervention.md): 框架干预相关的英文提示。
- [`fw.knowledge_tool.response.md`](prompts/default/fw.knowledge_tool.response.md): 框架知识工具响应相关的英文提示。
- [`fw.memories_deleted.md`](prompts/default/fw.memories_deleted.md): 框架记忆删除相关的英文提示。
- [`fw.memories_not_found.md`](prompts/default/fw.memories_not_found.md): 框架记忆未找到相关的英文提示。
- [`fw.memory_saved.md`](prompts/default/fw.memory_saved.md): 框架记忆保存相关的英文提示。
- [`fw.memory.hist_suc.sys.md`](prompts/default/fw.memory.hist_suc.sys.md): 框架记忆历史成功系统相关的英文提示。
- [`fw.memory.hist_sum.sys.md`](prompts/default/fw.memory.hist_sum.sys.md): 框架记忆历史总结系统相关的英文提示。
- [`fw.msg_cleanup.md`](prompts/default/fw.msg_cleanup.md): 框架消息清理相关的英文提示。
- [`fw.msg_from_subordinate.md`](prompts/default/fw.msg_from_subordinate.md): 框架来自下属消息相关的英文提示。
- [`fw.msg_misformat.md`](prompts/default/fw.msg_misformat.md): 框架消息格式错误相关的英文提示。
- [`fw.msg_repeat.md`](prompts/default/fw.msg_repeat.md): 框架消息重复相关的英文提示。
- [`fw.msg_summary.md`](prompts/default/fw.msg_summary.md): 框架消息摘要相关的英文提示。
- [`fw.msg_timeout.md`](prompts/default/fw.msg_timeout.md): 框架消息超时相关的英文提示。
- [`fw.msg_truncated.md`](prompts/default/fw.msg_truncated.md): 框架消息截断相关的英文提示。
- [`fw.rename_chat.msg.md`](prompts/default/fw.rename_chat.msg.md): 框架聊天重命名消息相关的英文提示。
- [`fw.rename_chat.sys.md`](prompts/default/fw.rename_chat.sys.md): 框架聊天重命名系统相关的英文提示。
- [`fw.tool_not_found.md`](prompts/default/fw.tool_not_found.md): 框架工具未找到相关的英文提示。
- [`fw.tool_result.md`](prompts/default/fw.tool_result.md): 框架工具结果相关的英文提示。
- [`fw.topic_summary.msg.md`](prompts/default/fw.topic_summary.msg.md): 框架主题摘要消息相关的英文提示。
- [`fw.topic_summary.sys.md`](prompts/default/fw.topic_summary.sys.md): 框架主题摘要系统相关的英文提示。
- [`fw.user_message.md`](prompts/default/fw.user_message.md): 框架用户消息相关的英文提示。
- [`fw.warning.md`](prompts/default/fw.warning.md): 框架警告相关的英文提示。

## 功能总结

这类提示词主要关注框架（Framework）级别的通用功能和交互，包括 AI 响应、批量摘要、代码执行、错误处理、干预、知识工具、记忆管理、消息处理（清理、格式、重复、超时等）、聊天重命名以及工具结果和警告等。它们是整个 Agent0 框架运行和维护的关键组成部分。