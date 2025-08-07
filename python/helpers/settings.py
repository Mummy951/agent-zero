import base64
import hashlib
import json
import os
import re
import subprocess
from typing import Any, Literal, TypedDict

import models
from python.helpers import runtime, whisper, defer, git
from . import files, dotenv
from python.helpers.print_style import PrintStyle


class Settings(TypedDict):
    version: str

    chat_model_provider: str
    chat_model_name: str
    chat_model_api_base: str
    chat_model_kwargs: dict[str, str]
    chat_model_ctx_length: int
    chat_model_ctx_history: float
    chat_model_vision: bool
    chat_model_rl_requests: int
    chat_model_rl_input: int
    chat_model_rl_output: int

    util_model_provider: str
    util_model_name: str
    util_model_api_base: str
    util_model_kwargs: dict[str, str]
    util_model_ctx_length: int
    util_model_ctx_input: float
    util_model_rl_requests: int
    util_model_rl_input: int
    util_model_rl_output: int

    embed_model_provider: str
    embed_model_name: str
    embed_model_api_base: str
    embed_model_kwargs: dict[str, str]
    embed_model_rl_requests: int
    embed_model_rl_input: int

    browser_model_provider: str
    browser_model_name: str
    browser_model_api_base: str
    browser_model_vision: bool
    browser_model_kwargs: dict[str, str]

    agent_prompts_subdir: str
    agent_memory_subdir: str
    agent_knowledge_subdir: str

    api_keys: dict[str, str]

    auth_login: str
    auth_password: str
    root_password: str

    rfc_auto_docker: bool
    rfc_url: str
    rfc_password: str
    rfc_port_http: int
    rfc_port_ssh: int

    stt_model_size: str
    stt_language: str
    stt_silence_threshold: float
    stt_silence_duration: int
    stt_waiting_timeout: int

    tts_kokoro: bool

    mcp_servers: str
    mcp_client_init_timeout: int
    mcp_client_tool_timeout: int
    mcp_server_enabled: bool
    mcp_server_token: str


class PartialSettings(Settings, total=False):
    pass


class FieldOption(TypedDict):
    value: str
    label: str


class SettingsField(TypedDict, total=False):
    id: str
    title: str
    description: str
    type: Literal[
        "text",
        "number",
        "select",
        "range",
        "textarea",
        "password",
        "switch",
        "button",
        "html",
    ]
    value: Any
    min: float
    max: float
    step: float
    hidden: bool
    options: list[FieldOption]


class SettingsSection(TypedDict, total=False):
    id: str
    title: str
    description: str
    fields: list[SettingsField]
    tab: str  # Indicates which tab this section belongs to


class SettingsOutput(TypedDict):
    sections: list[SettingsSection]


PASSWORD_PLACEHOLDER = "****PSWD****"

SETTINGS_FILE = files.get_abs_path("tmp/settings.json")
_settings: Settings | None = None


def convert_out(settings: Settings) -> SettingsOutput:
    from models import ModelProvider

    default_settings = get_default_settings()

    # main model section
    chat_model_fields: list[SettingsField] = []
    chat_model_fields.append(
        {
            "id": "chat_model_provider",
            "title": "Chat model provider",
            "description": "选择Agent Zero主要聊天模型的提供商",
            "type": "select",
            "value": settings["chat_model_provider"],
            "options": [{"value": p.name, "label": p.value} for p in ModelProvider],
        }
    )
    chat_model_fields.append(
        {
            "id": "chat_model_name",
            "title": "Chat model name",
            "description": "所选提供商的精确模型名称",
            "type": "text",
            "value": settings["chat_model_name"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_api_base",
            "title": "Chat model API base URL",
            "description": "主聊天模型的API基础URL。留空表示使用默认值。仅适用于Azure、本地和自定义（其他）提供商。",
            "type": "text",
            "value": settings["chat_model_api_base"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_ctx_length",
            "title": "Chat model context length",
            "description": "LLM上下文窗口中的最大token数量。系统提示、聊天历史、RAG和响应都计入此限制。",
            "type": "number",
            "value": settings["chat_model_ctx_length"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_ctx_history",
            "title": "Context window space for chat history",
            "description": "上下文窗口中专用于代理可见聊天历史的部分。聊天历史将自动优化以适应。较小的尺寸将导致更短和更简洁的历史记录。剩余空间将用于系统提示、RAG和响应。",
            "type": "range",
            "min": 0.01,
            "max": 1,
            "step": 0.01,
            "value": settings["chat_model_ctx_history"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_vision",
            "title": "Supports Vision",
            "description": "具有视觉能力的模型，例如可以本地查看图像附件的内容。",
            "type": "switch",
            "value": settings["chat_model_vision"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_rl_requests",
            "title": "Requests per minute limit",
            "description": "限制每分钟向聊天模型发出的请求数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["chat_model_rl_requests"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_rl_input",
            "title": "Input tokens per minute limit",
            "description": "限制每分钟向聊天模型输入的token数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["chat_model_rl_input"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_rl_output",
            "title": "Output tokens per minute limit",
            "description": "限制每分钟向聊天模型输出的token数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["chat_model_rl_output"],
        }
    )

    chat_model_fields.append(
        {
            "id": "chat_model_kwargs",
            "title": "Chat model additional parameters",
            "description": "LiteLLM支持的任何其他参数。<a href='https://docs.litellm.ai/docs/set_keys' target='_blank'>LiteLLM</a>。格式为每行KEY=VALUE，就像.env文件一样。",
            "type": "textarea",
            "value": _dict_to_env(settings["chat_model_kwargs"]),
        }
    )

    chat_model_section: SettingsSection = {
        "id": "chat_model",
        "title": "Chat Model",
        "description": "Agent Zero主要聊天模型的选择和设置",
        "fields": chat_model_fields,
        "tab": "agent",
    }

    # main model section
    util_model_fields: list[SettingsField] = []
    util_model_fields.append(
        {
            "id": "util_model_provider",
            "title": "Utility model provider",
            "description": "选择框架使用的实用模型的提供商",
            "type": "select",
            "value": settings["util_model_provider"],
            "options": [{"value": p.name, "label": p.value} for p in ModelProvider],
        }
    )
    util_model_fields.append(
        {
            "id": "util_model_name",
            "title": "Utility model name",
            "description": "所选提供商的精确模型名称",
            "type": "text",
            "value": settings["util_model_name"],
        }
    )

    util_model_fields.append(
        {
            "id": "util_model_api_base",
            "title": "Utility model API base URL",
            "description": "实用模型的API基础URL。留空表示使用默认值。仅适用于Azure、本地和自定义（其他）提供商。",
            "type": "text",
            "value": settings["util_model_api_base"],
        }
    )

    util_model_fields.append(
        {
            "id": "util_model_rl_requests",
            "title": "Requests per minute limit",
            "description": "限制每分钟向实用模型发出的请求数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["util_model_rl_requests"],
        }
    )

    util_model_fields.append(
        {
            "id": "util_model_rl_input",
            "title": "Input tokens per minute limit",
            "description": "限制每分钟向实用模型输入的token数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["util_model_rl_input"],
        }
    )

    util_model_fields.append(
        {
            "id": "util_model_rl_output",
            "title": "Output tokens per minute limit",
            "description": "限制每分钟向实用模型输出的token数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["util_model_rl_output"],
        }
    )

    util_model_fields.append(
        {
            "id": "util_model_kwargs",
            "title": "Utility model additional parameters",
            "description": "LiteLLM支持的任何其他参数。<a href='https://docs.litellm.ai/docs/set_keys' target='_blank'>LiteLLM</a>。格式为每行KEY=VALUE，就像.env文件一样。",
            "type": "textarea",
            "value": _dict_to_env(settings["util_model_kwargs"]),
        }
    )

    util_model_section: SettingsSection = {
        "id": "util_model",
        "title": "Utility model",
        "description": "用于处理内存组织、提示准备、总结等实用任务的更小、更便宜、更快速的模型。",
        "fields": util_model_fields,
        "tab": "agent",
    }

    # embedding model section
    embed_model_fields: list[SettingsField] = []
    embed_model_fields.append(
        {
            "id": "embed_model_provider",
            "title": "Embedding model provider",
            "description": "选择框架使用的嵌入模型的提供商",
            "type": "select",
            "value": settings["embed_model_provider"],
            "options": [{"value": p.name, "label": p.value} for p in ModelProvider],
        }
    )
    embed_model_fields.append(
        {
            "id": "embed_model_name",
            "title": "Embedding model name",
            "description": "所选提供商的精确模型名称",
            "type": "text",
            "value": settings["embed_model_name"],
        }
    )

    embed_model_fields.append(
        {
            "id": "embed_model_api_base",
            "title": "Embedding model API base URL",
            "description": "嵌入模型的API基础URL。留空表示使用默认值。仅适用于Azure、本地和自定义（其他）提供商。",
            "type": "text",
            "value": settings["embed_model_api_base"],
        }
    )

    embed_model_fields.append(
        {
            "id": "embed_model_rl_requests",
            "title": "Requests per minute limit",
            "description": "限制每分钟向嵌入模型发出的请求数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["embed_model_rl_requests"],
        }
    )

    embed_model_fields.append(
        {
            "id": "embed_model_rl_input",
            "title": "Input tokens per minute limit",
            "description": "限制每分钟向嵌入模型输入的token数量。如果超出限制则等待。设置为0表示禁用速率限制。",
            "type": "number",
            "value": settings["embed_model_rl_input"],
        }
    )

    embed_model_fields.append(
        {
            "id": "embed_model_kwargs",
            "title": "Embedding model additional parameters",
            "description": "LiteLLM支持的任何其他参数。<a href='https://docs.litellm.ai/docs/set_keys' target='_blank'>LiteLLM</a>。格式为每行KEY=VALUE，就像.env文件一样。",
            "type": "textarea",
            "value": _dict_to_env(settings["embed_model_kwargs"]),
        }
    )

    embed_model_section: SettingsSection = {
        "id": "embed_model",
        "title": "Embedding Model",
        "description": f"Agent Zero使用的嵌入模型的设置。<br><h4>⚠️ 无需更改</h4>默认的HuggingFace模型{default_settings['embed_model_name']}已预加载并在Docker容器内本地运行，除非您对嵌入有特殊要求，否则无需更改。",
        "fields": embed_model_fields,
        "tab": "agent",
    }

    # embedding model section
    browser_model_fields: list[SettingsField] = []
    browser_model_fields.append(
        {
            "id": "browser_model_provider",
            "title": "Web Browser model provider",
            "description": "选择<a href='https://github.com/browser-use/browser-use' target='_blank'>browser-use</a>框架使用的网页浏览器模型的提供商",
            "type": "select",
            "value": settings["browser_model_provider"],
            "options": [{"value": p.name, "label": p.value} for p in ModelProvider],
        }
    )
    browser_model_fields.append(
        {
            "id": "browser_model_name",
            "title": "Web Browser model name",
            "description": "所选提供商的精确模型名称",
            "type": "text",
            "value": settings["browser_model_name"],
        }
    )

    browser_model_fields.append(
        {
            "id": "browser_model_api_base",
            "title": "Web Browser model API base URL",
            "description": "网页浏览器模型的API基础URL。留空表示使用默认值。仅适用于Azure、本地和自定义（其他）提供商。",
            "type": "text",
            "value": settings["browser_model_api_base"],
        }
    )

    browser_model_fields.append(
        {
            "id": "browser_model_vision",
            "title": "Use Vision",
            "description": "具有视觉能力的模型可以利用它分析网页截图。这会提高质量，但也会增加token使用量。",
            "type": "switch",
            "value": settings["browser_model_vision"],
        }
    )

    browser_model_fields.append(
        {
            "id": "browser_model_kwargs",
            "title": "Web Browser model additional parameters",
            "description": "LiteLLM支持的任何其他参数。<a href='https://docs.litellm.ai/docs/set_keys' target='_blank'>LiteLLM</a>。格式为每行KEY=VALUE，就像.env文件一样。",
            "type": "textarea",
            "value": _dict_to_env(settings["browser_model_kwargs"]),
        }
    )

    browser_model_section: SettingsSection = {
        "id": "browser_model",
        "title": "Web Browser Model",
        "description": "Web浏览器模型的设置。Agent Zero使用<a href='https://github.com/browser-use/browser-use' target='_blank'>browser-use</a>代理框架来处理Web交互。",
        "fields": browser_model_fields,
        "tab": "agent",
    }

    # basic auth section
    auth_fields: list[SettingsField] = []

    auth_fields.append(
        {
            "id": "auth_login",
            "title": "UI Login",
            "description": "设置Web UI的用户名",
            "type": "text",
            "value": dotenv.get_dotenv_value(dotenv.KEY_AUTH_LOGIN) or "",
        }
    )

    auth_fields.append(
        {
            "id": "auth_password",
            "title": "UI Password",
            "description": "设置Web UI的用户密码",
            "type": "password",
            "value": (
                PASSWORD_PLACEHOLDER
                if dotenv.get_dotenv_value(dotenv.KEY_AUTH_PASSWORD)
                else ""
            ),
        }
    )

    if runtime.is_dockerized():
        auth_fields.append(
            {
                "id": "root_password",
                "title": "root Password",
                "description": "更改Docker容器中的Linux root密码。此密码可用于SSH访问。原始密码是在安装过程中随机生成的。",
                "type": "password",
                "value": "",
            }
        )

    auth_section: SettingsSection = {
        "id": "auth",
        "title": "Authentication",
        "description": "使用Agent Zero Web UI的身份验证设置。",
        "fields": auth_fields,
        "tab": "external",
    }

    # api keys model section
    api_keys_fields: list[SettingsField] = []

    for provider in ModelProvider:
        api_keys_fields.append(
            _get_api_key_field(settings, provider.name.lower(), provider.value)
        )

    api_keys_section: SettingsSection = {
        "id": "api_keys",
        "title": "API Keys",
        "description": "Agent Zero使用的模型提供商和服务的API密钥。",
        "fields": api_keys_fields,
        "tab": "external",
    }

    # Agent config section
    agent_fields: list[SettingsField] = []

    agent_fields.append(
        {
            "id": "agent_prompts_subdir",
            "title": "A0 Prompts Subdirectory",
            "description": "用于默认代理0的/prompts文件夹的子目录。下级代理可以使用其他子目录生成，这由它们的上级代理决定。此设置影响您与之通信的顶级代理的行为。",
            "type": "select",
            "value": settings["agent_prompts_subdir"],
            "options": [
                {"value": subdir, "label": subdir}
                for subdir in files.get_subdirectories("prompts")
            ],
        }
    )

    agent_fields.append(
        {
            "id": "agent_memory_subdir",
            "title": "Memory Subdirectory",
            "description": "用于代理内存存储的/memory文件夹的子目录。用于分隔不同实例之间的内存存储。",
            "type": "text",
            "value": settings["agent_memory_subdir"],
            # "options": [
            #     {"value": subdir, "label": subdir}
            #     for subdir in files.get_subdirectories("memory", exclude="embeddings")
            # ],
        }
    )

    agent_fields.append(
        {
            "id": "agent_knowledge_subdir",
            "title": "Knowledge subdirectory",
            "description": "用于代理知识导入的/knowledge文件夹的子目录。'default'子文件夹始终导入并包含框架知识。",
            "type": "select",
            "value": settings["agent_knowledge_subdir"],
            "options": [
                {"value": subdir, "label": subdir}
                for subdir in files.get_subdirectories("knowledge", exclude="default")
            ],
        }
    )

    agent_section: SettingsSection = {
        "id": "agent",
        "title": "Agent Config",
        "description": "代理参数。",
        "fields": agent_fields,
        "tab": "agent",
    }

    dev_fields: list[SettingsField] = []

    if runtime.is_development():
        # dev_fields.append(
        #     {
        #         "id": "rfc_auto_docker",
        #         "title": "RFC Auto Docker Management",
        #         "description": "Automatically create dockerized instance of A0 for RFCs using this instance's code base and, settings and .env.",
        #         "type": "text",
        #         "value": settings["rfc_auto_docker"],
        #     }
        # )

        dev_fields.append(
            {
                "id": "rfc_url",
                "title": "RFC Destination URL",
                "description": "用于远程函数调用的Docker化A0实例的URL。此处不指定端口。",
                "type": "text",
                "value": settings["rfc_url"],
            }
        )

    dev_fields.append(
        {
            "id": "rfc_password",
            "title": "RFC Password",
            "description": "远程函数调用的密码。两个实例上的密码必须匹配。RFC不能使用空密码。",
            "type": "password",
            "value": (
                PASSWORD_PLACEHOLDER
                if dotenv.get_dotenv_value(dotenv.KEY_RFC_PASSWORD)
                else ""
            ),
        }
    )

    if runtime.is_development():
        dev_fields.append(
            {
                "id": "rfc_port_http",
                "title": "RFC HTTP port",
                "description": "Docker化A0实例的HTTP端口。",
                "type": "text",
                "value": settings["rfc_port_http"],
            }
        )

        dev_fields.append(
            {
                "id": "rfc_port_ssh",
                "title": "RFC SSH port",
                "description": "Docker化A0实例的SSH端口。",
                "type": "text",
                "value": settings["rfc_port_ssh"],
            }
        )

    dev_section: SettingsSection = {
        "id": "dev",
        "title": "Development",
        "description": "A0框架开发的参数。RFC（远程函数调用）用于调用另一个A0实例上的函数。您可以在本地系统上原生开发和调试A0，同时将某些函数重定向到docker中的A0实例。这对于开发至关重要，因为A0需要在标准化环境中运行以支持所有功能。",
        "fields": dev_fields,
        "tab": "developer",
    }

    # Speech to text section
    stt_fields: list[SettingsField] = []

    stt_fields.append(
        {
            "id": "stt_microphone_section",
            "title": "Microphone device",
            "description": "选择用于语音转文本的麦克风设备。",
            "value": "<x-component path='/settings/speech/microphone.html' />",
            "type": "html",
        }
    )

    stt_fields.append(
        {
            "id": "stt_model_size",
            "title": "Speech-to-text model size",
            "description": "选择语音转文本模型的大小",
            "type": "select",
            "value": settings["stt_model_size"],
            "options": [
                {"value": "tiny", "label": "Tiny (39M, English)"},
                {"value": "base", "label": "Base (74M, English)"},
                {"value": "small", "label": "Small (244M, English)"},
                {"value": "medium", "label": "Medium (769M, English)"},
                {"value": "large", "label": "Large (1.5B, Multilingual)"},
                {"value": "turbo", "label": "Turbo (Multilingual)"},
            ],
        }
    )

    stt_fields.append(
        {
            "id": "stt_language",
            "title": "Speech-to-text language code",
            "description": "语言代码（例如en，fr，it）",
            "type": "text",
            "value": settings["stt_language"],
        }
    )

    stt_fields.append(
        {
            "id": "stt_silence_threshold",
            "title": "Microphone silence threshold",
            "description": "静音检测阈值。值越低对噪声越敏感。",
            "type": "range",
            "min": 0,
            "max": 1,
            "step": 0.01,
            "value": settings["stt_silence_threshold"],
        }
    )

    stt_fields.append(
        {
            "id": "stt_silence_duration",
            "title": "Microphone silence duration (ms)",
            "description": "系统判定说话结束前的静音持续时间。",
            "type": "text",
            "value": settings["stt_silence_duration"],
        }
    )

    stt_fields.append(
        {
            "id": "stt_waiting_timeout",
            "title": "Microphone waiting timeout (ms)",
            "description": "系统关闭麦克风前的静音持续时间。",
            "type": "text",
            "value": settings["stt_waiting_timeout"],
        }
    )

    # TTS fields
    tts_fields: list[SettingsField] = []

    tts_fields.append(
        {
            "id": "tts_kokoro",
            "title": "Enable Kokoro TTS",
            "description": "启用更高质量的服务器端AI（Kokoro）而不是基于浏览器的文本转语音。",
            "type": "switch",
            "value": settings["tts_kokoro"],
        }
    )

    speech_section: SettingsSection = {
        "id": "speech",
        "title": "Speech",
        "description": "语音转录和语音合成设置。",
        "fields": stt_fields + tts_fields,
        "tab": "agent",
    }

    # MCP section
    mcp_client_fields: list[SettingsField] = []

    mcp_client_fields.append(
        {
            "id": "mcp_servers_config",
            "title": "MCP Servers Configuration",
            "description": "外部MCP服务器可在此处配置。",
            "type": "button",
            "value": "Open",
        }
    )

    mcp_client_fields.append(
        {
            "id": "mcp_servers",
            "title": "MCP Servers",
            "description": "（JSON列表）>> 远程服务器 <<：[名称，URL，请求头，超时（可选），sse_读取超时（可选），禁用（可选）] / >> 本地服务器 <<：[名称，命令，参数，环境变量，编码（可选），编码错误处理器（可选），禁用（可选）]",
            "type": "textarea",
            "value": settings["mcp_servers"],
            "hidden": True,
        }
    )

    mcp_client_fields.append(
        {
            "id": "mcp_client_init_timeout",
            "title": "MCP Client Init Timeout",
            "description": "MCP客户端初始化超时（秒）。对于复杂的MCP，可能需要更高的值，但也可能减慢系统启动速度。",
            "type": "number",
            "value": settings["mcp_client_init_timeout"],
        }
    )

    mcp_client_fields.append(
        {
            "id": "mcp_client_tool_timeout",
            "title": "MCP Client Tool Timeout",
            "description": "MCP客户端工具执行超时。对于复杂的工具，可能需要更高的值，但也可能导致工具失败并产生长时间响应。",
            "type": "number",
            "value": settings["mcp_client_tool_timeout"],
        }
    )

    mcp_client_section: SettingsSection = {
        "id": "mcp_client",
        "title": "External MCP Servers",
        "description": "Agent Zero可以使用外部MCP服务器（本地或远程）作为工具。",
        "fields": mcp_client_fields,
        "tab": "mcp",
    }

    mcp_server_fields: list[SettingsField] = []

    mcp_server_fields.append(
        {
            "id": "mcp_server_enabled",
            "title": "Enable A0 MCP Server",
            "description": "将Agent Zero公开为SSE MCP服务器。这将使此A0实例可供MCP客户端使用。",
            "type": "switch",
            "value": settings["mcp_server_enabled"],
        }
    )

    mcp_server_fields.append(
        {
            "id": "mcp_server_token",
            "title": "MCP Server Token",
            "description": "用于MCP服务器身份验证的令牌。",
            "type": "text",
            "hidden": True,
            "value": settings["mcp_server_token"],
        }
    )

    mcp_server_section: SettingsSection = {
        "id": "mcp_server",
        "title": "A0 MCP Server",
        "description": "Agent Zero可以作为SSE MCP服务器公开。请参见<a href=\"javascript:openModal('settings/mcp/server/example.html')\">连接示例</a>。",
        "fields": mcp_server_fields,
        "tab": "mcp",
    }

    # Backup & Restore section
    backup_fields: list[SettingsField] = []

    backup_fields.append(
        {
            "id": "backup_create",
            "title": "Create Backup",
            "description": "使用可自定义的模式创建选定文件和配置的备份存档。",
            "type": "button",
            "value": "Create Backup",
        }
    )

    backup_fields.append(
        {
            "id": "backup_restore",
            "title": "Restore from Backup",
            "description": "使用基于模式的选择从备份存档中恢复文件和配置。",
            "type": "button",
            "value": "Restore Backup",
        }
    )

    backup_section: SettingsSection = {
        "id": "backup_restore",
        "title": "Backup & Restore",
        "description": "使用基于全局模式的文件选择备份和恢复Agent Zero数据和配置。",
        "fields": backup_fields,
        "tab": "backup",
    }

    # Add the section to the result
    result: SettingsOutput = {
        "sections": [
            agent_section,
            chat_model_section,
            util_model_section,
            browser_model_section,
            embed_model_section,
            speech_section,
            api_keys_section,
            auth_section,
            mcp_client_section,
            mcp_server_section,
            backup_section,
            dev_section,
        ]
    }
    return result


def _get_api_key_field(settings: Settings, provider: str, title: str) -> SettingsField:
    key = settings["api_keys"].get(provider, models.get_api_key(provider))
    return {
        "id": f"api_key_{provider}",
        "title": title,
        "type": "password",
        "value": (PASSWORD_PLACEHOLDER if key and key != "None" else ""),
    }


def convert_in(settings: dict) -> Settings:
    current = get_settings()
    for section in settings["sections"]:
        if "fields" in section:
            for field in section["fields"]:
                if field["value"] != PASSWORD_PLACEHOLDER:
                    if field["id"].endswith("_kwargs"):
                        current[field["id"]] = _env_to_dict(field["value"])
                    elif field["id"].startswith("api_key_"):
                        current["api_keys"][field["id"]] = field["value"]
                    else:
                        current[field["id"]] = field["value"]
    return current


def get_settings() -> Settings:
    global _settings
    if not _settings:
        _settings = _read_settings_file()
    if not _settings:
        _settings = get_default_settings()
    norm = normalize_settings(_settings)
    return norm


def set_settings(settings: Settings, apply: bool = True):
    global _settings
    previous = _settings
    _settings = normalize_settings(settings)
    _write_settings_file(_settings)
    if apply:
        _apply_settings(previous)


def set_settings_delta(delta: dict, apply: bool = True):
    current = get_settings()
    new = {**current, **delta}
    set_settings(new, apply)  # type: ignore


def normalize_settings(settings: Settings) -> Settings:
    copy = settings.copy()
    default = get_default_settings()

    # adjust settings values to match current version if needed
    if "version" not in copy or copy["version"] != default["version"]:
        _adjust_to_version(copy, default)
        copy["version"] = default["version"]  # sync version

    # remove keys that are not in default
    keys_to_remove = [key for key in copy if key not in default]
    for key in keys_to_remove:
        del copy[key]

    # add missing keys and normalize types
    for key, value in default.items():
        if key not in copy:
            copy[key] = value
        else:
            try:
                copy[key] = type(value)(copy[key])  # type: ignore
            except (ValueError, TypeError):
                copy[key] = value  # make default instead

    # mcp server token is set automatically
    copy["mcp_server_token"] = create_auth_token()

    return copy


def _adjust_to_version(settings: Settings, default: Settings):
    # starting with 0.9, the default prompt subfolder for agent no. 0 is agent0
    # switch to agent0 if the old default is used from v0.8
    if "version" not in settings or settings["version"].startswith("v0.8"):
        if (
            "agent_prompts_subdir" not in settings
            or settings["agent_prompts_subdir"] == "default"
        ):
            settings["agent_prompts_subdir"] = "agent0"


def _read_settings_file() -> Settings | None:
    if os.path.exists(SETTINGS_FILE):
        content = files.read_file(SETTINGS_FILE)
        parsed = json.loads(content)
        return normalize_settings(parsed)


def _write_settings_file(settings: Settings):
    _write_sensitive_settings(settings)
    _remove_sensitive_settings(settings)

    # write settings
    content = json.dumps(settings, indent=4)
    files.write_file(SETTINGS_FILE, content)


def _remove_sensitive_settings(settings: Settings):
    settings["api_keys"] = {}
    settings["auth_login"] = ""
    settings["auth_password"] = ""
    settings["rfc_password"] = ""
    settings["root_password"] = ""
    settings["mcp_server_token"] = ""


def _write_sensitive_settings(settings: Settings):
    for key, val in settings["api_keys"].items():
        dotenv.save_dotenv_value(key.upper(), val)

    dotenv.save_dotenv_value(dotenv.KEY_AUTH_LOGIN, settings["auth_login"])
    if settings["auth_password"]:
        dotenv.save_dotenv_value(dotenv.KEY_AUTH_PASSWORD, settings["auth_password"])
    if settings["rfc_password"]:
        dotenv.save_dotenv_value(dotenv.KEY_RFC_PASSWORD, settings["rfc_password"])

    if settings["root_password"]:
        dotenv.save_dotenv_value(dotenv.KEY_ROOT_PASSWORD, settings["root_password"])
    if settings["root_password"]:
        set_root_password(settings["root_password"])


def get_default_settings() -> Settings:
    from models import ModelProvider

    return Settings(
        version=_get_version(),
        chat_model_provider=ModelProvider.OPENROUTER.name,
        chat_model_name="openai/gpt-4.1",
        chat_model_api_base="",
        chat_model_kwargs={"temperature": "0"},
        chat_model_ctx_length=100000,
        chat_model_ctx_history=0.7,
        chat_model_vision=True,
        chat_model_rl_requests=0,
        chat_model_rl_input=0,
        chat_model_rl_output=0,
        util_model_provider=ModelProvider.OPENROUTER.name,
        util_model_name="openai/gpt-4.1-nano",
        util_model_api_base="",
        util_model_ctx_length=100000,
        util_model_ctx_input=0.7,
        util_model_kwargs={"temperature": "0"},
        util_model_rl_requests=0,
        util_model_rl_input=0,
        util_model_rl_output=0,
        embed_model_provider=ModelProvider.HUGGINGFACE.name,
        embed_model_name="sentence-transformers/all-MiniLM-L6-v2",
        embed_model_api_base="",
        embed_model_kwargs={},
        embed_model_rl_requests=0,
        embed_model_rl_input=0,
        browser_model_provider=ModelProvider.OPENROUTER.name,
        browser_model_name="openai/gpt-4.1",
        browser_model_api_base="",
        browser_model_vision=True,
        browser_model_kwargs={"temperature": "0"},
        api_keys={},
        auth_login="",
        auth_password="",
        root_password="",
        agent_prompts_subdir="agent0",
        agent_memory_subdir="default",
        agent_knowledge_subdir="custom",
        rfc_auto_docker=True,
        rfc_url="localhost",
        rfc_password="",
        rfc_port_http=55080,
        rfc_port_ssh=55022,
        stt_model_size="base",
        stt_language="en",
        stt_silence_threshold=0.3,
        stt_silence_duration=1000,
        stt_waiting_timeout=2000,
        tts_kokoro=True,
        mcp_servers='{\n    "mcpServers": {}\n}',
        mcp_client_init_timeout=10,
        mcp_client_tool_timeout=120,
        mcp_server_enabled=False,
        mcp_server_token=create_auth_token(),
    )


def _apply_settings(previous: Settings | None):
    global _settings
    if _settings:
        from agent import AgentContext
        from initialize import initialize_agent

        config = initialize_agent()
        for ctx in AgentContext._contexts.values():
            ctx.config = config  # reinitialize context config with new settings
            # apply config to agents
            agent = ctx.agent0
            while agent:
                agent.config = ctx.config
                agent = agent.get_data(agent.DATA_NAME_SUBORDINATE)

        # reload whisper model if necessary
        if not previous or _settings["stt_model_size"] != previous["stt_model_size"]:
            task = defer.DeferredTask().start_task(
                whisper.preload, _settings["stt_model_size"]
            )  # TODO overkill, replace with background task

        # force memory reload on embedding model change
        if not previous or (
            _settings["embed_model_name"] != previous["embed_model_name"]
            or _settings["embed_model_provider"] != previous["embed_model_provider"]
            or _settings["embed_model_kwargs"] != previous["embed_model_kwargs"]
        ):
            from python.helpers.memory import reload as memory_reload

            memory_reload()

        # update mcp settings if necessary
        if not previous or _settings["mcp_servers"] != previous["mcp_servers"]:
            from python.helpers.mcp_handler import MCPConfig

            async def update_mcp_settings(mcp_servers: str):
                PrintStyle(
                    background_color="black", font_color="white", padding=True
                ).print("Updating MCP config...")
                AgentContext.log_to_all(
                    type="info", content="Updating MCP settings...", temp=True
                )

                mcp_config = MCPConfig.get_instance()
                try:
                    MCPConfig.update(mcp_servers)
                except Exception as e:
                    AgentContext.log_to_all(
                        type="error",
                        content=f"Failed to update MCP settings: {e}",
                        temp=False,
                    )
                    (
                        PrintStyle(
                            background_color="red", font_color="black", padding=True
                        ).print("Failed to update MCP settings")
                    )
                    (
                        PrintStyle(
                            background_color="black", font_color="red", padding=True
                        ).print(f"{e}")
                    )

                PrintStyle(
                    background_color="#6734C3", font_color="white", padding=True
                ).print("Parsed MCP config:")
                (
                    PrintStyle(
                        background_color="#334455", font_color="white", padding=False
                    ).print(mcp_config.model_dump_json())
                )
                AgentContext.log_to_all(
                    type="info", content="Finished updating MCP settings.", temp=True
                )

            task2 = defer.DeferredTask().start_task(
                update_mcp_settings, config.mcp_servers
            )  # TODO overkill, replace with background task

        # update token in mcp server
        current_token = (
            create_auth_token()
        )  # TODO - ugly, token in settings is generated from dotenv and does not always correspond
        if not previous or current_token != previous["mcp_server_token"]:

            async def update_mcp_token(token: str):
                from python.helpers.mcp_server import DynamicMcpProxy

                DynamicMcpProxy.get_instance().reconfigure(token=token)

            task3 = defer.DeferredTask().start_task(
                update_mcp_token, current_token
            )  # TODO overkill, replace with background task


def _env_to_dict(data: str):
    env_dict = {}
    line_pattern = re.compile(r"\s*([^#][^=]*)\s*=\s*(.*)")
    for line in data.splitlines():
        match = line_pattern.match(line)
        if match:
            key, value = match.groups()
            # Remove optional surrounding quotes (single or double)
            value = value.strip().strip('"').strip("'")
            env_dict[key.strip()] = value
    return env_dict


def _dict_to_env(data_dict):
    lines = []
    for key, value in data_dict.items():
        if "\n" in value:
            value = f"'{value}'"
        elif " " in value or value == "" or any(c in value for c in "\"'"):
            value = f'"{value}"'
        lines.append(f"{key}={value}")
    return "\n".join(lines)


def set_root_password(password: str):
    if not runtime.is_dockerized():
        raise Exception("root password can only be set in dockerized environments")
    _result = subprocess.run(
        ["chpasswd"],
        input=f"root:{password}".encode(),
        capture_output=True,
        check=True,
    )
    dotenv.save_dotenv_value(dotenv.KEY_ROOT_PASSWORD, password)


def get_runtime_config(set: Settings):
    if runtime.is_dockerized():
        return {
            "code_exec_ssh_addr": "localhost",
            "code_exec_ssh_port": 22,
            "code_exec_http_port": 80,
            "code_exec_ssh_user": "root",
        }
    else:
        host = set["rfc_url"]
        if "//" in host:
            host = host.split("//")[1]
        if ":" in host:
            host, port = host.split(":")
        if host.endswith("/"):
            host = host[:-1]
        return {
            "code_exec_ssh_addr": host,
            "code_exec_ssh_port": set["rfc_port_ssh"],
            "code_exec_http_port": set["rfc_port_http"],
            "code_exec_ssh_user": "root",
        }


def create_auth_token() -> str:
    username = dotenv.get_dotenv_value(dotenv.KEY_AUTH_LOGIN) or ""
    password = dotenv.get_dotenv_value(dotenv.KEY_AUTH_PASSWORD) or ""
    if not username or not password:
        return "0"
    # use base64 encoding for a more compact token with alphanumeric chars
    hash_bytes = hashlib.sha256(f"{username}:{password}".encode()).digest()
    # encode as base64 and remove any non-alphanumeric chars (like +, /, =)
    b64_token = base64.urlsafe_b64encode(hash_bytes).decode().replace("=", "")
    return b64_token[:16]


def _get_version():
    try:
        git_info = git.get_git_info()
        return str(git_info.get("short_tag", "")).strip() or "unknown"
    except Exception:
        return "unknown"
