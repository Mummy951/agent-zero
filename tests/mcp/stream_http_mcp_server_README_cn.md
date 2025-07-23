# 带有流式 HTTP 的 FastMCP Hello World 服务器

这是一个全面的 hello world 示例，演示了如何使用 FastMCP 框架和流式 HTTP 传输构建 MCP（模型上下文协议）服务器。

## 🚀 功能

此服务器演示了所有三个核心 MCP 原语：

### 🔧 工具（LLM 可调用函数）
- **hello_world** - 带有时间戳的个性化问候语
- **add_numbers** - 简单的数学运算
- **get_server_status** - 带有上下文日志记录的服务器状态和信息

### 📚 资源（数据源）
- **info://server** - 静态服务器信息
- **greeting://{user_name}** - 动态个性化问候模板

### 💡 提示（可重用模板）
- **introduction_prompt** - 服务器功能介绍
- **math_prompt** - 数学辅助模板

## 📋 先决条件

- Python 3.10+
- pip 或 uv 包管理器

## 🛠️ 安装

### 选项 1：使用 pip
```bash
# 安装依赖项
pip install -r stream_http_mcp_server_requirements.txt

# 或者直接安装 FastMCP
pip install fastmcp
```

### 选项 2：使用 uv（推荐）
```bash
# 使用 uv 安装 FastMCP
uv pip install fastmcp
```

## ▶️ 运行服务器

### 基本用法
```bash
# 使用默认设置运行 (localhost:8000/mcp)
python stream_http_mcp_server.py
```

### 通过环境变量进行自定义配置
```bash
# 设置自定义主机、端口和路径
export MCP_HOST=0.0.0.0
export MCP_PORT=3000
export MCP_PATH=/hello-mcp

python stream_http_mcp_server.py
```

### 预期输出
```
🚀 正在启动带有流式 HTTP 的 Hello World MCP 服务器...
📡 传输：streamable-http
🌐 框架：FastMCP 2.0
🔗 协议：模型上下文协议 (MCP)

🏠 主机：127.0.0.1
🚪 端口：8000
🛤️  路径：/mcp
📍 完整 URL：http://127.0.0.1:8000/mcp

✅ 服务器已准备好接受 MCP 连接！
💡 将此服务器与支持流式 HTTP 传输的 MCP 客户端一起使用
```

## 🧪 测试服务器

### 方法 1：使用 MCP Inspector（推荐）

1. **安装 MCP Inspector**：
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **运行 Inspector**：
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **连接到服务器**：
   - 选择“Streamable HTTP”传输
   - 输入 URL：`http://localhost:8000/mcp`
   - 单击“连接”

4. **测试工具**：
   - 转到“工具”选项卡
   - 尝试 `hello_world` 和 `{"name": "Alice"}`
   - 尝试 `add_numbers` 和 `{"a": 5, "b": 3}`
   - 尝试 `get_server_status`（不需要参数）

5. **测试资源**：
   - 转到“资源”选项卡
   - 查看 `info://server`
   - 尝试 `greeting://YourName`

6. **测试提示**：
   - 转到“提示”选项卡
   - 尝试 `introduction_prompt` 和 `{"user_name": "Developer"}`
   - 尝试 `math_prompt` 和 `{"operation": "multiplication"}`

### 方法 2：Agent Zero 集成

通过添加到您的 MCP 服务器配置来配置 Agent Zero 以使用此服务器：

```json
[
  {
    "name": "hello_world_server",
    "type": "streamable-http",
    "url": "http://localhost:8000/mcp",
    "description": "带有流式 HTTP 的 Hello World FastMCP 服务器"
  }
]
```

### 方法 3：自定义 MCP 客户端

使用 MCP Python SDK 的示例：

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def test_server():
    async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test tool
            result = await session.call_tool("hello_world", {"name": "Test"})
            print(f"Tool result: {result}")

            # Test resource
            resource = await session.read_resource("info://server")
            print(f"Resource: {resource}")

# Run with: asyncio.run(test_server())
```

## 🔧 配置选项

### 环境变量
- `MCP_HOST` - 服务器主机（默认值：127.0.0.1）
- `MCP_PORT` - 服务器端口（默认值：8000）
- `MCP_PATH` - 服务器路径（默认值：/mcp）

### 服务器功能
此服务器支持所有 MCP 功能：
- ✅ 工具（支持异步和上下文日志记录）
- ✅ 资源（静态和动态模板）
- ✅ 提示（字符串和基于消息的）
- ✅ 流式 HTTP 传输
- ✅ 会话管理

## 🎯 演示的关键概念

1. **FastMCP 框架**：现代、生产就绪的 MCP 服务器开发
2. **流式 HTTP 传输**：适用于 Web 部署的可扩展传输
3. **类型安全**：完整的 Python 类型提示和文档字符串
4. **异步支持**：带有上下文的正确异步/等待模式
5. **动态资源**：基于模板的带参数资源
6. **上下文日志记录**：使用 MCP 上下文进行客户端通信
7. **错误处理**：优雅的启动和关闭

## 📚 下一步

- **扩展**：使用 FastMCP 的服务器组合来挂载多个应用程序
- **添加身份验证**：为生产实现 OAuth 身份验证
- **部署**：使用 Docker 或云平台进行生产部署
- **集成**：与 Claude Desktop、Agent Zero 或自定义客户端连接
- **扩展**：添加更复杂的工具、资源和提示

## 🐛 故障排除

### 服务器无法启动
- 检查端口 8000 是否可用：`lsof -i :8000`
- 尝试不同的端口：`MCP_PORT=8001 python stream_http_mcp_server.py`

### 连接问题
- 验证客户端中的 URL 与服务器输出匹配
- 检查端口的防火墙设置
- 确保您正在使用“streamable-http”传输类型

### 导入错误
- 安装 FastMCP：`pip install fastmcp`
- 检查 Python 版本：`python --version`（需要 3.10+）

## 📖 文档链接

- [FastMCP 文档](https://gofastmcp.com/)
- [MCP 规范](https://spec.modelcontextprotocol.io/)
- [Agent Zero MCP 集成](../../docs/mcp_setup.md)

---

使用 ❤️ 和 FastMCP 2.0 以及模型上下文协议构建 