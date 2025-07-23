# Windows、macOS 和 Linux 用户安装指南

点击观看视频，了解如何安装 Agent Zero：

[![简易安装指南](/docs/res/easy_ins_vid.png)](https://www.youtube.com/watch?v=w5v5Kjx51hs)

以下用户指南提供了使用 Docker 安装和运行 Agent Zero 的说明，Docker 是框架的主要运行时环境。对于开发人员和贡献者，我们还提供了设置[完整开发环境](#in-depth-guide-for-full-binaries-installation)的说明。


## Windows、macOS 和 Linux 设置指南


1. **安装 Docker Desktop：**
- Docker Desktop 提供了 Agent Zero 的运行时环境，确保跨平台的一致行为和安全性
- 整个框架在 Docker 容器中运行，提供隔离和易于部署
- 可作为适用于所有主要操作系统的用户友好 GUI 应用程序使用

1.1. 前往 Docker Desktop 的下载页面[此处](https://www.docker.com/products/docker-desktop/)。如果链接不起作用，只需在网上搜索“docker desktop download”。

1.2. 下载适用于您操作系统的版本。对于 Windows 用户，Intel/AMD 版本是主要的下载按钮。

<img src="res/setup/image-8.png" alt="docker download" width="200"/>
<br><br>

> [!NOTE]
> **Linux 用户：** 您可以安装 Docker Desktop 或 docker-ce（社区版）。
> 对于 Docker Desktop，请按照您特定 Linux 发行版的说明[此处](https://docs.docker.com/desktop/install/linux-install/)。
> 对于 docker-ce，请按照说明[此处](https://docs.docker.com/engine/install/)。
>
> 如果您正在使用 docker-ce，则需要将您的用户添加到 `docker` 组：
> ```bash
> sudo usermod -aG docker $USER
> ```
> 退出并重新登录，然后运行：
> ```bash
> docker login
> ```

1.3. 使用默认设置运行安装程序。在 macOS 上，将应用程序拖放到您的应用程序文件夹中。

<img src="res/setup/image-9.png" alt="docker install" width="300"/>
<img src="res/setup/image-10.png" alt="docker install" width="300"/>

<img src="res/setup/image-12.png" alt="docker install" width="300"/>
<br><br>

1.4. 安装完成后，启动 Docker Desktop：

<img src="res/setup/image-11.png" alt="docker installed" height="100"/>
<img src="res/setup/image-13.png" alt="docker installed" height="100"/>
<br><br>

> [!IMPORTANT]
> **macOS 配置：** 在 Docker Desktop 的偏好设置（Docker 菜单）→ 设置 →
> 高级，启用“允许使用默认 Docker 套接字（需要密码）”。

![docker socket macOS](res/setup/macsocket.png)

2. **运行 Agent Zero：**

- 注意：Agent Zero 还提供了一个基于 Kali Linux 的 Hacking Edition，带有用于网络安全任务的修改提示。设置与常规版本相同，只需使用 agent0ai/agent-zero:hacking 镜像而不是 agent0ai/agent-zero。

2.1. 拉取 Agent Zero Docker 镜像：
- 在 Docker Desktop 中搜索 `agent0ai/agent-zero`
- 点击 `Pull` 按钮
- 镜像将在几分钟内下载到您的机器上

![docker pull](res/setup/1-docker-image-search.png)

> [!TIP]
> 或者，在您的终端中运行以下命令：
>
> ```bash
> docker pull agent0ai/agent-zero
> ```

2.2. 创建数据目录以进行持久化：
- 在您的机器上选择或创建一个目录，您希望在其中存储 Agent Zero 的数据
- 这可以是您喜欢的任何位置（例如，`C:/agent-zero-data` 或 `/home/user/agent-zero-data`）
- 此目录将包含您的所有 Agent Zero 文件，就像传统的根文件夹结构一样：
  - `/memory` - 代理的内存和学习信息
  - `/knowledge` - 知识库
  - `/instruments` - 工具和功能
  - `/prompts` - 提示文件
  - `/work_dir` - 工作目录
  - `.env` - 您的 API 密钥
  - `settings.json` - 您的 Agent Zero 设置

> [!TIP]
> 选择一个易于访问和备份的位置。您的所有 Agent Zero 数据
> 将在此目录中直接访问。

2.3. 运行容器：
- 在 Docker Desktop 中，返回到“镜像”选项卡
- 点击 `agent0ai/agent-zero` 镜像旁边的 `Run` 按钮
- 打开“可选设置”菜单
- 在第二个“主机端口”字段中将端口设置为 `0`（用于自动端口分配）

您可以选择性地映射本地文件夹以进行文件持久化：
- 在“卷”下，配置：
  - 主机路径：您选择的目录（例如，`C:\agent-zero-data`）
  - 容器路径：`/a0`

![docker port mapping](res/setup/3-docker-port-mapping.png)

- 点击“镜像”选项卡中的 `Run` 按钮。
- 容器将启动并显示在“容器”选项卡中

![docker containers](res/setup/4-docker-container-started.png)

> [!TIP]
> 或者，在您的终端中运行以下命令：
> ```bash
> docker run -p $PORT:80 -v /path/to/your/data:/a0 agent0ai/agent-zero
> ```
> - 将 `$PORT` 替换为您要使用的端口（例如，`50080`）
> - 将 `/path/to/your/data` 替换为您选择的目录路径

2.4. 访问 Web UI：
- 框架将需要几秒钟来初始化，Docker 日志将如下图所示。
- 在 Docker Desktop 中找到映射的端口（显示为 `<PORT>:80`）或点击容器 ID 正下方的端口，如下图所示

![docker logs](res/setup/5-docker-click-to-open.png)

- 在浏览器中打开 `http://localhost:<PORT>`
- Web UI 将打开。Agent Zero 已准备好进行配置！

![docker ui](res/setup/6-docker-a0-running.png)

> [!TIP]
> 您还可以通过点击 Docker Desktop 中容器 ID 正下方的端口来访问 Web UI。

> [!NOTE]
> 启动容器后，您将在您选择的目录中找到所有 Agent Zero 文件。
> 您可以直接在您的机器上访问和编辑这些文件，并且更改将立即反映在正在运行的容器中。

3. 配置 Agent Zero
- 有关如何配置 Agent Zero 的完整指南，请参阅以下部分。

## 设置配置
Agent Zero 提供了一个全面的设置界面，用于自定义其功能的各个方面。通过单击侧边栏中带有齿轮图标的“设置”按钮来访问设置。

### 代理配置
- **提示子目录：** 选择 `/prompts` 中用于代理行为自定义的子目录。“default”目录包含标准提示。
- **内存子目录：** 选择用于代理内存存储的子目录，允许在不同实例之间进行分离。
- **知识子目录：** 指定自定义知识文件的位置以增强代理的理解能力。

![settings](res/setup/settings/1-agentConfig.png)

### 聊天模型设置
- **提供商：** 选择聊天模型提供商（例如，Ollama）
- **模型名称：** 选择特定模型（例如，llama3.2）
- **温度：** 调整响应随机性（0 表示确定性，更高的值表示更有创意的响应）
- **上下文长度：** 设置上下文窗口的最大令牌限制
- **上下文窗口空间：** 配置上下文窗口中有多少用于聊天历史

![chat model settings](res/setup/settings/2-chat-model.png)

### 实用模型配置
- **提供商和模型：** 选择一个更小、更快的模型用于实用任务，例如内存组织和摘要
- **温度：** 调整实用响应的确定性

### 嵌入模型设置
- **提供商：** 选择嵌入模型提供商（例如，OpenAI）
- **模型名称：** 选择特定的嵌入模型（例如，text-embedding-3-small）

### 语音转文本选项
- **模型大小：** 选择语音识别模型大小
- **语言代码：** 设置语音识别的主要语言
- **静音设置：** 配置语音输入的静音阈值、持续时间和超时参数

### API 密钥
- 直接在 Web UI 中配置各种服务提供商的 API 密钥
- 点击 `Save` 以确认您的设置

### 身份验证
- **UI 登录：** 设置 Web 界面访问的用户名
- **UI 密码：** 配置 Web 界面安全的密码
- **Root 密码：** 管理 Docker 容器 root 密码以进行 SSH 访问

![settings](res/setup/settings/3-auth.png)

### 开发设置
- **RFC 参数（仅限本地实例）：** 配置实例之间远程函数调用的 URL 和端口
- **RFC 密码：** 配置远程函数调用的密码
在此处了解有关远程函数调用及其用途的更多信息[此处](#7-configure-agent-zero-rfc)。

> [!IMPORTANT]
> 始终确保您的 API 密钥和密码安全。

# 选择您的 LLM
“设置”页面是选择为 Agent Zero 提供支持的大型语言模型 (LLM) 的控制中心。您可以为不同的角色选择不同的 LLM：

| LLM 角色 | 描述 |
| --- | --- |
| `chat_llm` | 这是用于对话和生成响应的主要 LLM。 |
| `utility_llm` | 此 LLM 处理内部任务，例如总结消息、管理内存和处理内部提示。在此处使用更小、更便宜的模型可以提高效率。 |
| `embedding_llm` | 此 LLM 负责生成用于内存检索和知识库查找的嵌入。更改 `embedding_llm` 将重新索引 A0 的所有内存。 |

**如何更改：**
1. 打开 Web UI 中的“设置”页面。
2. 为每个角色（聊天模型、实用模型、嵌入模型）选择 LLM 的提供商并写入模型名称。
3. 点击“保存”以应用更改。

## 重要注意事项

> [!CAUTION]
> 更改 `embedding_llm` 将重新索引所有内存和知识，并且
> 需要清除 `memory` 文件夹以避免错误，因为嵌入不能
> 在向量数据库中混合。请注意，这将删除 Agent Zero 的所有内存。

## 安装和使用 Ollama（本地模型）
如果您对 Ollama 感兴趣，它是一个功能强大的工具，允许您在本地运行各种大型语言模型，以下是安装和使用它的方法：

#### 第一步：安装
**在 Windows 上：**

从官方网站下载 Ollama 并将其安装到您的机器上。

<button>[下载 Ollama 安装程序](https://ollama.com/download/OllamaSetup.exe)</button>

**在 macOS 上：**
```
brew install ollama
```
否则从[官方网站](https://ollama.com/)选择 macOS 安装程序。

**在 Linux 上：**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**查找模型名称：**
访问 [Ollama 模型库](https://ollama.com/library)以获取可用模型及其相应名称的列表。格式通常是 `provider/model-name`（或在某些情况下仅为 `model-name`）。

#### 第二步：拉取模型
**在 Windows、macOS 和 Linux 上：**
```
ollama pull <model-name>
```

1. 将 `<model-name>` 替换为您要使用的模型的名称。例如，要拉取 Mistral Large 模型，您可以使用命令 `ollama pull mistral-large`。

2. CLI 消息应确认模型已下载到您的系统上

#### 在 Agent Zero 中选择您的模型
1. 下载模型后，您必须在 GUI 的“设置”页面中选择它。

2. 在聊天模型、实用模型或嵌入模型部分中，选择 Ollama 作为提供商。

3. 按照 Ollama 预期的格式写入您的模型代码，例如 `llama3.2` 或 `qwen2.5:7b`

4. 点击 `Save` 以确认您的设置。

![ollama](res/setup/settings/4-local-models.png)

#### 管理您下载的模型
下载了一些模型后，您可能需要检查哪些可用或删除不再需要的模型。

- **列出下载的模型：**
  要查看所有已下载模型的列表，请使用以下命令：
  ```
  ollama list
  ```
- **删除模型：**
  如果您需要删除已下载的模型，可以使用 `ollama rm` 命令，后跟模型名称：
  ```
  ollama rm <model-name>
  ```


- 尝试不同的模型组合，以找到最适合您需求的性能和成本平衡。例如，更快、延迟更低的 LLM 会有所帮助，您还可以使用 `faiss_gpu` 而不是 `faiss_cpu` 作为内存。

## 在您的移动设备上使用 Agent Zero
Agent Zero 的 Web UI 可以通过 Docker 容器从您网络上的任何设备访问：

1. Docker 容器自动将 Web UI 暴露给所有网络接口
2. 在 Docker Desktop 中查找映射的端口：
   - 查看容器名称下方（通常格式为 `<PORT>:80`）
   - 例如，如果您看到 `32771:80`，则您的端口是 `32771`
3. 从任何设备访问 Web UI，使用：
   - 本地访问：`http://localhost:<PORT>`
   - 网络访问：`http://<YOUR_COMPUTER_IP>:<PORT>`

> [!TIP]
> - 您计算机的 IP 地址通常为 `192.168.x.x` 或 `10.0.x.x` 格式
> - 您可以通过运行 `ipconfig` (Windows) 或 `ifconfig` (Linux/Mac) 查找您的外部 IP 地址
> - 除非您指定，否则端口由 Docker 自动分配

> [!NOTE]
> 如果您直接在系统上运行 Agent Zero（传统方法）而不是
> 使用 Docker，您需要手动在 `run_ui.py` 中配置主机，以使用 `host="0.0.0.0"` 在所有接口上运行。

对于需要直接在系统上运行 Agent Zero 的开发人员或用户，请参阅[完整二进制安装深入指南](#in-depth-guide-for-full-binaries-installation)。

# 如何更新 Agent Zero

1. **如果您来自 Agent Zero 的先前版本：**
- 您的数据安全地存储在 Agent Zero 文件夹中的各个目录和文件中。
- 要更新到新的 Docker 运行时版本，您可能需要备份以下文件和目录：
  - `/memory` - 代理的内存
  - `/knowledge` - 自定义知识库（如果您导入了任何自定义知识文件）
  - `/instruments` - 自定义工具和功能（如果您创建了任何自定义）
  - `/tmp/settings.json` - 您的 Agent Zero 设置
  - `/tmp/chats/` - 您的聊天历史记录
- 保存这些文件和目录后，您可以继续执行 Docker 运行时[上述安装说明](#windows-macos-and-linux-setup-guide)设置指南。
- 找到您保存数据的文件夹，并将其复制到安装过程中设置的新 Agent Zero 文件夹中。
- Agent Zero 将自动检测您保存的数据，并将其用于内存、知识、工具、提示和设置。

> [!IMPORTANT]
> 如果您在加载设置时遇到问题，可以尝试删除 `/tmp/settings.json` 文件，让 Agent Zero 生成一个新的。
> 对于 `/tmp/chats/` 中的聊天记录也是如此，它们可能与新版本不兼容

2. **更新过程（Docker Desktop）**
- 转到 Docker Desktop，并在“容器”选项卡中停止容器
- 右键单击并选择“移除”以移除容器
- 转到“镜像”选项卡，移除 `agent0ai/agent-zero` 镜像，或单击三个点以拉取差异并更新 Docker 镜像。

![docker delete image](res/setup/docker-delete-image-1.png)

- 如果您选择移除新镜像，则搜索并拉取新镜像
- 使用与旧容器相同的卷设置运行新容器

> [!IMPORTANT]
> 确保在新容器运行时使用相同的卷挂载路径
> 以保留您的数据。确切路径取决于您存储
> Agent Zero 数据目录的位置（您机器上选择的目录）。

> [!TIP]
> 或者，在您的终端中运行以下命令：
>
> ```bash
> # 停止当前容器
> docker stop agent-zero
>
> # 移除容器（数据在文件夹中是安全的）
> docker rm agent-zero
>
> # 移除旧镜像
> docker rmi agent0ai/agent-zero
>
> # 拉取最新镜像
> docker pull agent0ai/agent-zero
>
> # 使用相同的卷挂载运行新容器
> docker run -p $PORT:80 -v /path/to/your/data:/a0 agent0ai/agent-zero
> ```

3. **完整二进制文件**
- 使用 Git/GitHub：拉取 Agent Zero 存储库的最新版本。
- 自定义知识、解决方案、内存和其他数据将被忽略，因此您无需担心丢失任何自定义数据。您的 .env 文件（包含所有 API 密钥）和 settings.json 也是如此。

> [!WARNING]
> - 如果您手动更新，请注意：保存您的 .env 文件（包含 API 密钥），并查找 requirements.txt 中的新依赖项。
> - 如果更新版本的要求有任何更改，您必须在激活 a0 conda 环境后在其中执行此命令：
> ```bash
> pip install -r requirements.txt

# 完整二进制安装深入指南
- Agent Zero 是一个框架。它旨在进行定制、编辑和增强。因此，当您下载其完整二进制文件时，需要安装必要的组件才能运行它。本指南将帮助您完成此操作。
- 以下分步说明可以与本教程的视频一起进行，了解如何使 Agent Zero 与其完整的开发环境一起工作。

[![Video](res/setup/thumb_play.png)](https://youtu.be/8H7mFsvxKYQ)

## 提醒：
1. 无需安装 Python，Conda 会为您管理。
2. 您不一定需要 API 密钥：Agent Zero 可以与本地模型一起运行。不过，在本教程中，我们将保留默认的 OpenAI API。有关下载 Ollama 和本地模型的指南可在此处获取[此处](#installing-and-using-ollama-local-models)。
3. Visual Studio Code 或任何其他代码编辑器不是强制性的，但它使导航和编辑文件变得更容易。
4. Git/GitHub 不是强制性的，您可以通过浏览器下载框架文件。本教程将不演示如何使用 Git。
5. 对于完整二进制安装，Docker 不是强制性的，因为框架将在您的机器上通过 Web UI RFC 功能连接到 Docker 容器。
6. 在没有 Docker 的情况下运行 Agent Zero 会使过程更复杂，这适用于开发人员和贡献者。

> [!IMPORTANT]
> Linux 说明作为任何 Linux 发行版的通用说明提供。如果您使用的发行版不是 Debian/Ubuntu，您可能需要相应地调整说明。
>
> 对于 Debian/Ubuntu，只需遵循 macOS 说明，因为它们是相同的。

## 1. 安装 Conda (miniconda)
- Conda 是一个 Python 环境管理器，它将帮助您保持项目和安装的分离。
- 它是 Anaconda 的轻量级版本，仅包含 conda、Python、它们所依赖的包以及少量其他有用的包，包括 pip、zlib 等。

1. 前往 miniconda 的下载页面[此处](https://docs.anaconda.com/miniconda/#miniconda-latest-installer-links)。如果链接不起作用，只需在网上搜索“miniconda download”。
2. 根据您的操作系统，下载正确的 miniconda 安装程序。对于 macOS，选择以“pkg”结尾的版本。

<img src="res/setup/image-1.png" alt="miniconda download win" width="500"/>
<img src="res/setup/image-5.png" alt="miniconda download macos" width="500"/>
<br><br>

3. 运行安装程序并完成安装过程，此处您可以保留所有默认设置并单击“下一步”、“下一步”... macOS 上的“pkg”图形安装程序也是如此。

<img src="res/setup/image.png" alt="miniconda install" width="200"/>
<img src="res/setup/image-2.png" alt="miniconda install" width="200"/>
<img src="res/setup/image-3.png" alt="miniconda install" width="200"/>
<img src="res/setup/image-4.png" alt="miniconda install" width="200"/>
<br><br>

4. 安装完成后，您的 Windows 机器上应该安装了“Anaconda Powershell Prompt”。在 macOS 上，当您在“应用程序”文件夹中打开“终端”应用程序并键入“conda --version”时，您应该会看到安装的版本。

<img src="res/setup/image-6.png" alt="miniconda installed" height="100"/>
<img src="res/setup/image-7.png" alt="miniconda installed" height="100"/>
<br><br>

> [!IMPORTANT]
> 如果您打开新的终端窗口，您需要再次使用
> “conda activate a0”激活该窗口的环境。

5. 使用 **“pip”** 安装依赖项。Pip 是一个 Python 包管理器。我们可以使用以下命令从 requirements.txt 文件安装所有必需的包：
~~~
pip install -r requirements.txt
~~~
这可能需要一些时间。如果您遇到任何关于版本冲突和兼容性的错误，请仔细检查您的环境是否已激活，并且您是否使用正确的 Python 版本创建了该环境。

<img src="res/setup/image-19.png" alt="conda reqs" height="200"/>
<br><br>

## 4. 安装 Docker (Docker Desktop 应用程序)
简而言之，Docker 是一种在您的机器上运行虚拟计算机的方式。它们轻量、一次性且与您的操作系统隔离，因此它是一种沙盒 Agent Zero 的方式。
- Agent Zero 仅在需要执行代码和命令时才连接到 Docker 容器。框架本身在您的机器上运行。
- Docker 具有适用于所有主要操作系统的桌面应用程序（带 GUI），这是推荐的安装方式。

1. 前往 Docker Desktop 的下载页面[此处](https://www.docker.com/products/docker-desktop/)。如果链接不起作用，只需在网上搜索“docker desktop download”。
2. 下载适用于您操作系统的版本。不要被看似缺少 Windows Intel/AMD 版本的现象所迷惑，它就是按钮本身，而不是下拉菜单中的。

<img src="res/setup/image-8.png" alt="docker download" width="200"/>
<br><br>

3. 运行安装程序并完成安装过程。它应该比 Conda 安装更快，您可以保留所有默认设置。在 macOS 上，安装程序是一个“dmg”镜像，因此像往常一样将应用程序拖放到您的应用程序文件夹中。

<img src="res/setup/image-9.png" alt="docker install" width="300"/>
<img src="res/setup/image-10.png" alt="docker install" width="300"/>

<img src="res/setup/image-12.png" alt="docker install" width="300"/>
<br><br>

4. 安装完成后，您的 Windows/Mac 机器上应该会看到 Docker Desktop 应用程序。

<img src="res/setup/image-11.png" alt="docker installed" height="100"/>
<img src="res/setup/image-13.png" alt="docker installed" height="100"/>
<br><br>

5. 在应用程序中创建帐户。
- 必须登录 Docker Hub，因此请在 Docker Desktop 应用程序中创建一个免费帐户，当应用程序首次运行时会提示您。

> [!IMPORTANT]
> **重要的 macOS 专用 Docker 配置：** 在 Docker Desktop 的偏好设置
>（Docker 菜单）中，转到“设置”，导航到“高级”并选中“允许使用默认
> Docker 套接字（需要密码）”。这允许 Agent Zero 与 Docker 守护程序通信。

![docker socket macOS](res/setup/macsocket.png)

> [!NOTE]
> **Linux 用户：** 您可以安装 Docker Desktop 或 docker-ce（社区版）。
> 对于 Docker Desktop，请按照您特定 Linux 发行版的说明[此处](https://docs.docker.com/desktop/install/linux-install/)。
> 对于 docker-ce，请按照说明[此处](https://docs.docker.com/engine/install/)。
>
> 如果您正在使用 docker-ce，则需要将您的用户添加到 `docker` 组，才能在没有 sudo 的情况下运行 docker 命令。您可以通过在终端中运行以下命令来实现：`sudo usermod -aG docker $USER`。然后注销并重新登录以使更改生效。
>
> 使用 `docker login` 在 Docker CLI 中登录并提供您的 Docker Hub 凭据。

6. 拉取 Docker 镜像
- Agent Zero 需要从 Docker Hub 拉取 Docker 镜像才能运行，即使使用完整二进制文件也是如此。
您可以参考[上述安装说明](#windows-macos-and-linux-setup-guide)来运行 Docker 容器，然后从下一步继续。有两个区别：
  - 您需要映射两个端口而不是一个：
    - 第一个字段中的 55022 用于运行远程函数调用 SSH
    - 第二个字段中的 0 用于在自动端口分配中运行 Web UI
  - 您需要将 `/a0` 卷映射到本地 Agent Zero 文件夹的位置。
- 按照说明运行 Docker 容器。

## 5. 运行本地 Agent Zero 实例
运行带有 Web UI 的 Agent Zero：
~~~
python run_ui.py
~~~

<img src="res/setup/image-21.png" alt="run ui" height="110"/>
<br><br>

- 在您的 Web 浏览器中打开终端中显示的 URL。您应该会看到 Agent Zero 界面。

## 6. 配置 Agent Zero
现在我们可以配置 Agent Zero - 选择模型、设置、API 密钥等。有关如何配置 Agent Zero 的完整指南，请参阅[使用](usage.md#agent-configuration)指南。

## 7. 配置 Agent Zero RFC
Agent Zero 需要进一步配置才能将某些功能重定向到 Docker 容器。这对于开发至关重要，因为 A0 需要在标准化环境中运行才能支持所有功能。
1. 在您的本地实例的 Web UI 中进入“设置”页面，然后进入“开发”部分。
2. 将“RFC 目标 URL”设置为 `http://localhost`
3. 将两个端口（HTTP 和 SSH）设置为创建 Docker 容器时使用的端口
4. 点击“保存”

![rfc local settings](res/setup/9-rfc-devpage-on-local-sbs-1.png)

5. 在您的 Docker 实例的 Web UI 中进入“设置”页面，然后进入“开发”部分。

![rfc docker settings](res/setup/9-rfc-devpage-on-docker-instance-1.png)

6. 这次页面只有密码字段，将其设置为您创建 Docker 容器时使用的相同密码。
7. 点击“保存”
8. 使用开发环境
9. 现在您拥有完整的开发环境，可以开始开发 Agent Zero。

<img src="res/setup/image-22-1.png" alt="run ui" width="400"/>
<img src="res/setup/image-23-1.png" alt="run ui" width="400"/>
<br><br>

### 结论
按照您特定操作系统的说明操作后，您应该已成功安装并运行 Agent Zero。您现在可以开始探索框架的功能并尝试创建您自己的智能代理。

如果您在安装过程中遇到任何问题，请查阅本文档的[故障排除部分](troubleshooting.md)或参考 Agent Zero [Skool](https://www.skool.com/agent-zero) 或 [Discord](https://discord.gg/Z2tun2N3) 社区寻求帮助。 