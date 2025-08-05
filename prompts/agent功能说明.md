# agent 功能说明

## 提示词文件列表及功能

- [`_context.md`](prompts/default/_context.md): Agent0 角色的英文上下文信息。
- [`agent.system.main.role.md`](prompts/default/agent.system.main.role.md): Agent0 角色的主要系统提示词（英文）。
- [`agent.system.tool.response.md`](prompts/default/agent.system.tool.response.md): Agent0 工具响应相关的英文提示词。
- [`agent.context.extras.md`](prompts/default/agent.context.extras.md): 代理额外上下文（英文）。
- [`agent.system.behaviour.md`](prompts/default/agent.system.behaviour.md): 代理行为相关的英文系统提示。
- [`agent.system.behaviour_default.md`](prompts/default/agent.system.behaviour_default.md): 代理默认行为相关的英文系统提示。
- [`agent.system.datetime.md`](prompts/default/agent.system.datetime.md): 代理日期时间相关的英文系统提示。
- [`agent.system.instruments.md`](prompts/default/agent.system.instruments.md): 代理工具相关的英文系统提示。
- [`agent.system.main.md`](prompts/default/agent.system.main.md): 代理主要系统提示（英文）。
- [`agent.system.main.communication.md`](prompts/default/agent.system.main.communication.md): 代理主要系统通信相关的英文提示。
- [`agent.system.main.environment.md`](prompts/default/agent.system.main.environment.md): 代理主要系统环境相关的英文提示。
- [`agent.system.main.role.md`](prompts/default/agent.system.main.role.md): 代理主要系统角色相关的英文提示。
- [`agent.system.main.solving.md`](prompts/default/agent.system.main.solving.md): 代理主要系统解决问题相关的英文提示。
- [`agent.system.main.tips.md`](prompts/default/agent.system.main.tips.md): 代理主要系统提示和技巧相关的英文提示。
- [`agent.system.mcp_tools.md`](prompts/default/agent.system.mcp_tools.md): 代理 MCP 工具相关的英文系统提示。
- [`agent.system.memories.md`](prompts/default/agent.system.memories.md): 代理记忆相关的英文系统提示。
- [`agent.system.solutions.md`](prompts/default/agent.system.solutions.md): 代理解决方案相关的英文系统提示。
- [`agent.system.tool.behaviour.md`](prompts/default/agent.system.tool.behaviour.md): 代理工具行为相关的英文系统提示。
- [`agent.system.tool.browser._md`](prompts/default/agent.system.tool.browser._md): 代理浏览器工具（旧版或特殊）相关的英文系统提示。
- [`agent.system.tool.browser.md`](prompts/default/agent.system.tool.browser.md): 代理浏览器工具相关的英文系统提示。
- [`agent.system.tool.call_sub.md`](prompts/default/agent.system.tool.call_sub.md): 代理调用子工具相关的英文系统提示。
- [`agent.system.tool.call_sub.py`](prompts/default/agent.system.tool.call_sub.py): 代理调用子工具相关的 Python 脚本。
- [`agent.system.tool.code_exe.md`](prompts/default/agent.system.tool.code_exe.md): 代理代码执行工具相关的英文系统提示。
- [`agent.system.tool.document_query.md`](prompts/default/agent.system.tool.document_query.md): 代理文档查询工具相关的英文系统提示。
- [`agent.system.tool.input.md`](prompts/default/agent.system.tool.input.md): 代理输入工具相关的英文系统提示。
- [`agent.system.tool.knowledge.md`](prompts/default/agent.system.tool.knowledge.md): 代理知识库工具相关的英文系统提示。
- [`agent.system.tool.memory.md`](prompts/default/agent.system.tool.memory.md): 代理记忆工具相关的英文系统提示。
- [`agent.system.tool.response.md`](prompts/default/agent.system.tool.response.md): 代理工具响应相关的英文系统提示。
- [`agent.system.tool.scheduler.md`](prompts/default/agent.system.tool.scheduler.md): 代理调度工具相关的英文系统提示。
- [`agent.system.tool.search_engine.md`](prompts/default/agent.system.tool.search_engine.md): 代理搜索引擎工具相关的英文系统提示。
- [`agent.system.tool.web.md`](prompts/default/agent.system.tool.web.md): 代理 Web 工具相关的英文系统提示。
- [`agent.system.tools_vision.md`](prompts/default/agent.system.tools_vision.md): 代理视觉工具相关的英文系统提示。
- [`agent.system.tools.md`](prompts/default/agent.system.tools.md): 代理通用工具相关的英文系统提示。

## 功能总结

这类提示词主要围绕代理（Agent）的系统行为、通信、工具使用、角色定义、问题解决、记忆管理等方面。它们是构建 Agent0 框架中代理核心功能和交互逻辑的基础，涵盖了代理在不同场景下的多种操作和响应。