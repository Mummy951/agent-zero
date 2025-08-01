以下是 Agent Zero 项目中常用的命令：

**项目运行命令：**
*   **Docker 运行：**
    *   拉取镜像：`docker pull agent0ai/agent-zero`
    *   运行容器：`docker run -p 50001:80 agent0ai/agent-zero`
*   **Python 运行（Web UI 和 API）：** `python run_ui.py`

**代码质量命令（推断）：**
*   **测试：** `pytest`
*   **格式化：** `black .` 或 `autopep8 .`
*   **Linting：** `flake8 .`

**通用系统命令（Windows 环境）：**
*   **列出目录内容：** `dir`
*   **改变目录：** `cd <目录路径>`
*   **显示文件内容：** `type <文件名>`
*   **在文件中查找字符串：** `findstr <字符串> <文件名>`
*   **复制文件：** `copy <源文件> <目标文件>`
*   **移动文件：** `move <源文件> <目标文件>`
*   **删除文件：** `del <文件名>`