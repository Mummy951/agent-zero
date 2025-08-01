Agent Zero 的代码库结构大致如下：

*   **根目录：** 包含主要的运行脚本 (`run_cli.py`, `run_ui.py`), README 文件, `requirements.txt`。
*   **`docker/`：** 包含 Docker 相关的文件，用于构建和运行容器。
*   **`docs/`：** 存放项目文档，包括安装、使用、架构等。
*   **`instruments/`：** 可能包含 Agent Zero 可以使用的自定义工具或功能的定义。
*   **`knowledge/`：** 可能用于存储 Agent Zero 的知识库或预加载信息。
*   **`lib/`：** 通用库，例如 `lib/browser/`。
*   **`logs/`：** 存放运行日志。
*   **`memory/`：** 存放 Agent Zero 的持久化记忆，例如向量数据库和嵌入文件。
*   **`prompts/`：** 核心目录，包含定义代理行为、工具说明和消息的提示文件。例如 `prompts/default/agent.system.md` 定义了系统行为。
*   **`python/`：** 主要的 Python 源代码，细分为：
    *   `python/api/`：定义 Flask API 端点处理器。
    *   `python/extensions/`：包含 Agent Zero 扩展机制的代码，例如在 LLM 调用前后、消息循环结束时等插入自定义逻辑。
    *   `python/helpers/`：提供各种辅助函数和模块，如文件操作、日志、Git、Docker、MCP 交互、运行时管理等。
    *   `python/tools/`：包含 Agent Zero 可以使用的内置工具的实现。
*   **`tests/`：** 包含项目的测试文件。
*   **`webui/`：** 包含 Web 用户界面的前端文件（HTML, CSS, JavaScript）。