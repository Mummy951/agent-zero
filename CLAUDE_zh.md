# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述
Agent Zero 是一个个人的、有机的代理框架，能够与您一起成长和学习。它被设计为动态的、有机增长的，并在您使用时不断学习。该框架使用计算机作为工具来完成任务，完全透明、可读、可理解、可定制和可交互。

## 关键架构组件

### 核心结构
- `agent.py` - 主要代理实现
- `models.py` - 模型配置和 LLM 集成
- `initialize.py` - 框架初始化
- `run_ui.py` - Web UI 和 API 的主要入口点
- `run_cli.py` - CLI 接口（已弃用）

### 关键目录
- `/python` - 核心 Python 代码库
  - `/api` - API 端点
  - `/extensions` - 模块化扩展
  - `/helpers` - 实用函数
  - `/tools` - 内置工具
- `/prompts` - 系统和工具提示
- `/memory` - 持久化代理内存
- `/knowledge` - 知识库
- `/instruments` - 自定义脚本和工具
- `/docs` - 文档

## 开发环境

### 先决条件
1. Docker Desktop（主要运行时环境）
2. Python 3.10+ 用于本地开发
3. LLM 提供商的 API 密钥（OpenAI、Anthropic 等）

### 设置
```bash
# 安装依赖
pip install -r requirements.txt

# 复制并配置环境
cp example.env .env
# 编辑 .env 文件添加您的 API 密钥
```

## 常用命令

### 运行应用程序
```bash
# 主要运行方式（包括 UI 和 API）
python run_ui.py

# 访问地址 http://localhost:50001
```

### Docker 运行时（推荐）
```bash
# 拉取镜像
docker pull agent0ai/agent-zero

# 运行并持久化数据
docker run -p 50001:80 -v ./data:/a0 agent0ai/agent-zero
```

## 测试
测试文件位于 `tests/` 目录中，主要集中在 MCP 功能上。

## 需要理解的关键特性

1. **分层代理结构** - 代理可以创建下属进行任务委派
2. **工具系统** - `python/tools/` 中的可扩展工具，提示定义在 `prompts/` 中
3. **内存系统** - `/memory` 中的持久化存储，支持自动和手动管理
4. **提示架构** - `prompts/default/` 中的模块化提示，可自定义
5. **MCP 集成** - 支持外部工具集成的模型上下文协议
6. **Instruments** - `/instruments` 中的自定义脚本，不影响令牌计数
7. **扩展** - `python/extensions/` 中的模块化系统，用于扩展功能

## 自定义点

1. **提示** - 修改 `prompts/default/` 中的文件或创建自定义提示集
2. **工具** - 按照现有模式在 `python/tools/` 中添加新工具
3. **Instruments** - 在 `instruments/custom/` 中添加脚本
4. **扩展** - 在 `python/extensions/` 的相应子目录中添加 Python 文件