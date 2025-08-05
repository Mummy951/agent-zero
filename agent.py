import asyncio
import nest_asyncio

nest_asyncio.apply()

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Coroutine, Dict
from enum import Enum
import uuid
import models

from python.helpers import extract_tools, files, errors, history, tokens
from python.helpers import dirty_json
from python.helpers.print_style import PrintStyle
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

import python.helpers.log as Log
from python.helpers.dirty_json import DirtyJson
from python.helpers.defer import DeferredTask
from typing import Callable
from python.helpers.localization import Localization


class AgentContextType(Enum):
    USER = "user"
    TASK = "task"
    MCP = "mcp"


class AgentContext:

    _contexts: dict[str, "AgentContext"] = {}
    _counter: int = 0

    def __init__(
        self,
        config: "AgentConfig",
        id: str | None = None,
        name: str | None = None,
        agent0: "Agent|None" = None,
        log: Log.Log | None = None,
        paused: bool = False,
        streaming_agent: "Agent|None" = None,
        created_at: datetime | None = None,
        type: AgentContextType = AgentContextType.USER,
        last_message: datetime | None = None,
    ):
        # 构建上下文
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.config = config
        self.log = log or Log.Log()
        self.agent0 = agent0 or Agent(0, self.config, self)
        self.paused = paused
        self.streaming_agent = streaming_agent
        self.task: DeferredTask | None = None
        self.created_at = created_at or datetime.now(timezone.utc)
        self.type = type
        AgentContext._counter += 1
        self.no = AgentContext._counter
        # 设置为 Unix 纪元开始
        self.last_message = last_message or datetime.now(timezone.utc)

        existing = self._contexts.get(self.id, None)
        if existing:
            AgentContext.remove(self.id)
        self._contexts[self.id] = self

    @staticmethod
    def get(id: str):
        return AgentContext._contexts.get(id, None)

    @staticmethod
    def first():
        if not AgentContext._contexts:
            return None
        return list(AgentContext._contexts.values())[0]

    @staticmethod
    def all():
        return list(AgentContext._contexts.values())

    @staticmethod
    def remove(id: str):
        context = AgentContext._contexts.pop(id, None)
        if context and context.task:
            context.task.kill()
        return context

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": (
                Localization.get().serialize_datetime(self.created_at)
                if self.created_at
                else Localization.get().serialize_datetime(datetime.fromtimestamp(0))
            ),
            "no": self.no,
            "log_guid": self.log.guid,
            "log_version": len(self.log.updates),
            "log_length": len(self.log.logs),
            "paused": self.paused,
            "last_message": (
                Localization.get().serialize_datetime(self.last_message)
                if self.last_message
                else Localization.get().serialize_datetime(datetime.fromtimestamp(0))
            ),
            "type": self.type.value,
        }

    @staticmethod
    def log_to_all(
        type: Log.Type,
        heading: str | None = None,
        content: str | None = None,
        kvps: dict | None = None,
        temp: bool | None = None,
        update_progress: Log.ProgressUpdate | None = None,
        id: str | None = None,  # 添加 id 参数
        **kwargs,
    ) -> list[Log.LogItem]:
        items: list[Log.LogItem] = []
        for context in AgentContext.all():
            items.append(
                context.log.log(
                    type, heading, content, kvps, temp, update_progress, id, **kwargs
                )
            )
        return items

    def kill_process(self):
        if self.task:
            self.task.kill()

    def reset(self):
        self.kill_process()
        self.log.reset()
        self.agent0 = Agent(0, self.config, self)
        self.streaming_agent = None
        self.paused = False

    def nudge(self):
        self.kill_process()
        self.paused = False
        self.task = self.run_task(self.get_agent().monologue)
        return self.task

    def get_agent(self):
        return self.streaming_agent or self.agent0

    def communicate(self, msg: "UserMessage", broadcast_level: int = 1):
        self.paused = False  # 如果已暂停则取消暂停

        current_agent = self.get_agent()

        if self.task and self.task.is_alive():
            # 设置干预消息给代理：
            intervention_agent = current_agent
            while intervention_agent and broadcast_level != 0:
                intervention_agent.intervention = msg
                broadcast_level -= 1
                intervention_agent = intervention_agent.data.get(
                    Agent.DATA_NAME_SUPERIOR, None
                )
        else:
            self.task = self.run_task(self._process_chain, current_agent, msg)

        return self.task

    def run_task(
        self, func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any
    ):
        if not self.task:
            self.task = DeferredTask(
                thread_name=self.__class__.__name__,
            )
        self.task.start_task(func, *args, **kwargs)
        return self.task

    # 此包装器确保如果聊天是从文件加载的并且原始调用堆栈已丢失，则上级代理会被回调。
    async def _process_chain(self, agent: "Agent", msg: "UserMessage|str", user=True):
        try:
            msg_template = (
                agent.hist_add_user_message(msg)  # type: ignore
                if user
                else agent.hist_add_tool_result(
                    tool_name="call_subordinate", tool_result=msg  # type: ignore
                )
            )
            response = await agent.monologue()  # type: ignore
            superior = agent.data.get(Agent.DATA_NAME_SUPERIOR, None)
            if superior:
                response = await self._process_chain(superior, response, False)  # type: ignore
            return response
        except Exception as e:
            agent.handle_critical_exception(e)


@dataclass
class AgentConfig:
    chat_model: models.ModelConfig
    utility_model: models.ModelConfig
    embeddings_model: models.ModelConfig
    browser_model: models.ModelConfig
    mcp_servers: str
    prompts_subdir: str = ""
    memory_subdir: str = ""
    knowledge_subdirs: list[str] = field(default_factory=lambda: ["默认", "自定义"])
    code_exec_docker_enabled: bool = False
    code_exec_docker_name: str = "A0-dev"
    code_exec_docker_image: str = "agent0ai/agent-zero-run:development"
    code_exec_docker_ports: dict[str, int] = field(
        default_factory=lambda: {"22/tcp": 55022, "80/tcp": 55080}
    )
    code_exec_docker_volumes: dict[str, dict[str, str]] = field(
        default_factory=lambda: {
            files.get_base_dir(): {"bind": "/a0", "mode": "rw"},
            files.get_abs_path("work_dir"): {"bind": "/root", "mode": "rw"},
        }
    )
    code_exec_ssh_enabled: bool = True
    code_exec_ssh_addr: str = "localhost"
    code_exec_ssh_port: int = 55022
    code_exec_ssh_user: str = "root"
    code_exec_ssh_pass: str = ""
    additional: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserMessage:
    message: str
    attachments: list[str] = field(default_factory=list[str])
    system_message: list[str] = field(default_factory=list[str])


class LoopData:
    def __init__(self, **kwargs):
        self.iteration = -1
        self.system = []
        self.user_message: history.Message | None = None
        self.history_output: list[history.OutputMessage] = []
        self.extras_temporary: OrderedDict[str, history.MessageContent] = OrderedDict()
        self.extras_persistent: OrderedDict[str, history.MessageContent] = OrderedDict()
        self.last_response = ""
        self.params_temporary: dict = {}
        self.params_persistent: dict = {}

        # 使用 kwargs 覆盖值
        for key, value in kwargs.items():
            setattr(self, key, value)


# 干预异常类 - 跳过消息循环的其余迭代
class InterventionException(Exception):
    pass


# 终止异常类 - 不转发给LLM，无法自行修复，结束消息循环
class RepairableException(Exception):
    pass


class HandledException(Exception):
    """
    一个已处理的异常类，用于终止消息循环。
    """

    pass


class Agent:

    DATA_NAME_SUPERIOR = "_superior"
    DATA_NAME_SUBORDINATE = "_subordinate"
    DATA_NAME_CTX_WINDOW = "ctx_window"

    def __init__(
        self, number: int, config: AgentConfig, context: AgentContext | None = None
    ):

        # 代理配置
        self.config = config

        # 代理上下文
        self.context = context or AgentContext(config=config, agent0=self)

        # 非配置变量
        self.number = number
        self.agent_name = f"A{self.number}"

        self.history = history.History(self)
        self.last_user_message: history.Message | None = None
        self.intervention: UserMessage | None = None
        self.data = {}  # 所有工具都可以使用的自由数据对象

    async def monologue(self):
        while True:
            try:
                # 传递给扩展的循环数据字典
                self.loop_data = LoopData(user_message=self.last_user_message)
                # 调用 monologue_start 扩展
                # monologue_start 扩展在代理的内部“独白”（monologue）阶段开始时执行，主要负责根据当前的对话历史，动态地生成和更新聊天会话的名称。
                await self.call_extensions("monologue_start", loop_data=self.loop_data)

                printer = PrintStyle(italic=True, font_color="#b3ffd9", padding=False)

                # 让代理运行消息循环，直到它使用响应工具停止
                while True:

                    self.context.streaming_agent = self  # 标记自身为当前流处理器
                    self.loop_data.iteration += 1
                    self.loop_data.params_temporary = {}  # 清除临时参数

                    # 调用 message_loop_start 扩展
                    await self.call_extensions(
                        # message_loop_start 扩展在代理的每个消息循环开始时执行，主要功能是跟踪和管理消息循环的迭代次数。
                        "message_loop_start",
                        loop_data=self.loop_data,
                    )

                    try:
                        # 准备LLM链（模型、系统、历史）
                        prompt = await self.prepare_prompt(loop_data=self.loop_data)

                        # 调用 before_main_llm_call 扩展
                        # before_main_llm_call 扩展在主语言模型（LLM）调用之前执行，主要职责是初始化一个日志项，并将其引用存储在 LoopData 对象的临时参数中。
                        await self.call_extensions(
                            "before_main_llm_call", loop_data=self.loop_data
                        )

                        async def reasoning_callback(chunk: str, full: str):
                            if chunk == full:
                                printer.print("Reasoning: ")  # 推理开始
                            printer.stream(chunk)
                            await self.handle_reasoning_stream(full)

                        async def stream_callback(chunk: str, full: str):
                            # 输出代理响应流
                            if chunk == full:
                                printer.print("Response: ")  # 响应开始
                            printer.stream(chunk)
                            await self.handle_response_stream(full)

                        # 调用主LLM
                        agent_response, _reasoning = await self.call_chat_model(
                            messages=prompt,
                            response_callback=stream_callback,
                            reasoning_callback=reasoning_callback,
                        )

                        await self.handle_intervention(agent_response)

                        if (
                            self.loop_data.last_response == agent_response
                        ):  # 如果助手的响应与历史记录中的最后一条消息相同，通知它
                            # 将助手的响应添加到历史记录
                            self.hist_add_ai_response(agent_response)
                            # 将警告消息添加到历史记录
                            # fw.msg_repeat.md: 当助手的回复与历史记录中的最后一条消息相同时，用于生成警告消息，提示用户消息重复。
                            warning_msg = self.read_prompt("fw.msg_repeat.md")
                            self.hist_add_warning(message=warning_msg)
                            PrintStyle(font_color="orange", padding=True).print(
                                warning_msg
                            )
                            self.context.log.log(type="warning", content=warning_msg)

                        else:  # 否则继续使用工具
                            # 将助手的响应添加到历史记录
                            self.hist_add_ai_response(agent_response)
                            # 处理代理消息中请求的工具
                            tools_result = await self.process_tools(agent_response)
                            if tools_result:  # 消息循环的最终响应可用
                                return tools_result  # 如果任务完成，中断执行

                    # 消息循环内部异常:
                    except InterventionException as e:
                        pass  # 干预消息已在 handle_intervention() 中处理，继续对话循环
                    except RepairableException as e:
                        # 将可修复的错误转发给LLM，也许它可以修复它们
                        error_message = errors.format_error(e)
                        self.hist_add_warning(error_message)
                        PrintStyle(font_color="red", padding=True).print(error_message)
                        self.context.log.log(type="error", content=error_message)
                    except Exception as e:
                        # 其他异常终止循环
                        self.handle_critical_exception(e)

                    finally:
                        # 调用 message_loop_end 扩展
                        # message_loop_end 扩展在代理的消息循环结束后执行，主要负责处理聊天历史的组织和聊天会话的持久化。
                        await self.call_extensions(
                            "message_loop_end", loop_data=self.loop_data
                        )

            # 消息循环外部异常:
            except InterventionException as e:
                pass  # 重新开始
            except Exception as e:
                self.handle_critical_exception(e)
            finally:
                self.context.streaming_agent = None  # 取消设置当前流处理器
                # 调用 monologue_end 扩展
                # monologue_end 扩展在代理的内部“独白”（monologue）阶段结束时执行，主要负责将代理在此独白阶段中获得的有用信息（如关键对话片段和解决方案）持久化到记忆系统中，并设置用户界面状态以等待用户输入。
                await self.call_extensions("monologue_end", loop_data=self.loop_data)  # type: ignore

    async def prepare_prompt(self, loop_data: LoopData) -> list[BaseMessage]:
        self.context.log.set_progress("Building prompt")

        # 在设置提示之前调用扩展
        # message_loop_prompts_before 扩展在代理的消息循环中，将提示发送给主语言模型（LLM）之前执行，核心功能是确保聊天历史已被适当地压缩和管理。
        await self.call_extensions("message_loop_prompts_before", loop_data=loop_data)

        # 设置系统提示和消息历史
        loop_data.system = await self.get_system_prompt(self.loop_data)
        loop_data.history_output = self.history.output()

        # 允许扩展编辑提示
        # message_loop_prompts_after 扩展在代理的消息循环中，主语言模型（LLM）生成回复之后，但在将最终提示发送给LLM之前执行，主要负责通过集成相关记忆、解决方案、工具和当前时间信息来增强LLM的提示。
        await self.call_extensions("message_loop_prompts_after", loop_data=loop_data)

        # 连接系统提示
        system_text = "\n\n".join(loop_data.system)

        # 合并额外信息
        # agent.context.extras.md: 提供代理额外上下文的提示词，用于增强LLM的理解。
        extras = history.Message(
            False,
            content=self.read_prompt(
                "agent.context.extras.md",
                extras=dirty_json.stringify(
                    {**loop_data.extras_persistent, **loop_data.extras_temporary}
                ),
            ),
        ).output()
        loop_data.extras_temporary.clear()

        # 将历史记录 + 额外信息转换为LLM格式
        history_langchain: list[BaseMessage] = history.output_langchain(
            loop_data.history_output + extras
        )

        # build full prompt from system prompt, message history and extrS
        full_prompt: list[BaseMessage] = [
            SystemMessage(content=system_text),
            *history_langchain,
        ]
        full_text = ChatPromptTemplate.from_messages(full_prompt).format()

        # store as last context window content
        self.set_data(
            Agent.DATA_NAME_CTX_WINDOW,
            {
                "text": full_text,
                "tokens": tokens.approximate_tokens(full_text),
            },
        )

        return full_prompt

    def handle_critical_exception(self, exception: Exception):
        if isinstance(exception, HandledException):
            raise exception  # Re-raise the exception to kill the loop
        elif isinstance(exception, asyncio.CancelledError):
            # 处理 asyncio.CancelledError
            PrintStyle(font_color="white", background_color="red", padding=True).print(
                f"Context {self.context.id} terminated during message loop"
            )
            raise HandledException(exception)  # 重新抛出异常以取消循环
        else:
            # 处理一般异常
            error_text = errors.error_text(exception)
            error_message = errors.format_error(exception)
            PrintStyle(font_color="red", padding=True).print(error_message)
            self.context.log.log(
                type="error",
                heading="Error",
                content=error_message,
                kvps={"text": error_text},
            )
            raise HandledException(exception)  # 重新抛出异常以终止循环

    async def get_system_prompt(self, loop_data: LoopData) -> list[str]:
        system_prompt = []
        # system_prompt 扩展负责在代理与主语言模型（LLM）交互时，动态地构建和配置传递给LLM的“系统提示”。
        await self.call_extensions(
            "system_prompt", system_prompt=system_prompt, loop_data=loop_data
        )
        return system_prompt

    def parse_prompt(self, file: str, **kwargs):
        prompt_dir = files.get_abs_path("prompts/default")
        backup_dir = []
        if (
            self.config.prompts_subdir
        ):  # 如果代理有自定义文件夹，则使用它，并将默认文件夹作为备用
            prompt_dir = files.get_abs_path("prompts", self.config.prompts_subdir)
            backup_dir.append(files.get_abs_path("prompts/default"))
        prompt = files.parse_file(
            files.get_abs_path(prompt_dir, file), _backup_dirs=backup_dir, **kwargs
        )
        return prompt

    def read_prompt(self, file: str, **kwargs) -> str:
        prompt_dir = files.get_abs_path("prompts/default")
        backup_dir = []
        if (
            self.config.prompts_subdir
        ):  # 如果代理有自定义文件夹，则使用它，并将默认文件夹作为备用
            prompt_dir = files.get_abs_path("prompts", self.config.prompts_subdir)
            backup_dir.append(files.get_abs_path("prompts/default"))
        prompt = files.read_file(
            files.get_abs_path(prompt_dir, file), _backup_dirs=backup_dir, **kwargs
        )
        prompt = files.remove_code_fences(prompt)
        return prompt

    def get_data(self, field: str):
        return self.data.get(field, None)

    def set_data(self, field: str, value):
        self.data[field] = value

    def hist_add_message(
        self, ai: bool, content: history.MessageContent, tokens: int = 0
    ):
        self.last_message = datetime.now(timezone.utc)
        return self.history.add_message(ai=ai, content=content, tokens=tokens)

    def hist_add_user_message(self, message: UserMessage, intervention: bool = False):
        self.history.new_topic()  # 用户消息在历史记录中开始一个新话题

        # 根据干预加载消息模板
        if intervention:
            content = self.parse_prompt(
                "fw.intervention.md",
                message=message.message,
                attachments=message.attachments,
                system_message=message.system_message,
            )
        else:
            content = self.parse_prompt(
                "fw.user_message.md",
                message=message.message,
                attachments=message.attachments,
                system_message=message.system_message,
            )

        # 从模板中移除空部分
        if isinstance(content, dict):
            content = {k: v for k, v in content.items() if v}

        # 添加到历史记录
        msg = self.hist_add_message(False, content=content)  # type: ignore
        self.last_user_message = msg
        return msg

    def hist_add_ai_response(self, message: str):
        self.loop_data.last_response = message
        content = self.parse_prompt("fw.ai_response.md", message=message)
        return self.hist_add_message(True, content=content)

    def hist_add_warning(self, message: history.MessageContent):
        content = self.parse_prompt("fw.warning.md", message=message)
        return self.hist_add_message(False, content=content)

    def hist_add_tool_result(self, tool_name: str, tool_result: str):
        content = self.parse_prompt(
            "fw.tool_result.md", tool_name=tool_name, tool_result=tool_result
        )
        return self.hist_add_message(False, content=content)

    def concat_messages(self, messages):  # TODO 添加消息范围、主题、历史记录参数
        return self.history.output_text(human_label="user", ai_label="assistant")

    def get_chat_model(self):
        return models.get_chat_model(
            self.config.chat_model.provider,
            self.config.chat_model.name,
            **self.config.chat_model.build_kwargs(),
        )

    def get_utility_model(self):
        return models.get_chat_model(
            self.config.utility_model.provider,
            self.config.utility_model.name,
            **self.config.utility_model.build_kwargs(),
        )

    def get_browser_model(self):
        return models.get_browser_model(
            self.config.browser_model.provider,
            self.config.browser_model.name,
            **self.config.browser_model.build_kwargs(),
        )

    def get_embedding_model(self):
        return models.get_embedding_model(
            self.config.embeddings_model.provider,
            self.config.embeddings_model.name,
            **self.config.embeddings_model.build_kwargs(),
        )

    async def call_utility_model(
        self,
        system: str,
        message: str,
        callback: Callable[[str], Awaitable[None]] | None = None,
        background: bool = False,
    ):
        model = self.get_utility_model()

        # 速率限制器
        limiter = await self.rate_limiter(
            self.config.utility_model, f"SYSTEM: {system}\nUSER: {message}", background
        )

        # 在token回调中添加输出token到速率限制器
        async def tokens_callback(delta: str, tokens: int):
            await self.handle_intervention()
            limiter.add(output=tokens)

        # 如果设置了回调，则传播流
        async def stream_callback(chunk: str, total: str):
            if callback:
                await callback(chunk)

        response, _reasoning = await model.unified_call(
            system_message=system,
            user_message=message,
            response_callback=stream_callback,
            tokens_callback=tokens_callback,
        )

        return response

    async def call_chat_model(
        self,
        messages: list[BaseMessage],
        response_callback: Callable[[str, str], Awaitable[None]] | None = None,
        reasoning_callback: Callable[[str, str], Awaitable[None]] | None = None,
    ):
        response = ""

        # 模型类
        model = self.get_chat_model()

        # 速率限制器
        limiter = await self.rate_limiter(
            self.config.chat_model, ChatPromptTemplate.from_messages(messages).format()
        )

        # 在token回调中添加输出token到速率限制器
        async def tokens_callback(delta: str, tokens: int):
            await self.handle_intervention()
            limiter.add(output=tokens)

        # call model
        response, reasoning = await model.unified_call(
            messages=messages,
            reasoning_callback=reasoning_callback,
            response_callback=response_callback,
            tokens_callback=tokens_callback,
        )

        return response, reasoning

    async def rate_limiter(
        self, model_config: models.ModelConfig, input: str, background: bool = False
    ):
        # 速率限制器日志
        wait_log = None

        async def wait_callback(msg: str, key: str, total: int, limit: int):
            nonlocal wait_log
            if not wait_log:
                wait_log = self.context.log.log(
                    type="util",
                    update_progress="none",
                    heading=msg,
                    model=f"{model_config.provider.value}\\{model_config.name}",
                )
            wait_log.update(heading=msg, key=key, value=total, limit=limit)
            if not background:
                self.context.log.set_progress(msg, -1)

        # 速率限制器
        limiter = models.get_rate_limiter(
            model_config.provider,
            model_config.name,
            model_config.limit_requests,
            model_config.limit_input,
            model_config.limit_output,
        )
        limiter.add(input=tokens.approximate_tokens(input))
        limiter.add(requests=1)
        await limiter.wait(callback=wait_callback)
        return limiter

    async def handle_intervention(self, progress: str = ""):
        while self.context.paused:
            await asyncio.sleep(0.1)  # 如果暂停则等待
        if self.intervention:  # 如果有干预消息，但尚未处理
            msg = self.intervention
            self.intervention = None  # 重置干预消息
            if progress.strip():
                self.hist_add_ai_response(progress)
            # 追加干预消息
            self.hist_add_user_message(msg, intervention=True)
            raise InterventionException(msg)

    async def wait_if_paused(self):
        while self.context.paused:
            await asyncio.sleep(0.1)

    async def process_tools(self, msg: str):
        # 在代理消息中搜索工具使用请求
        tool_request = extract_tools.json_parse_dirty(msg)

        if tool_request is not None:
            raw_tool_name = tool_request.get("tool_name", "")  # 获取原始工具名称
            tool_args = tool_request.get("tool_args", {})

            tool_name = raw_tool_name  # 使用原始工具名称初始化 tool_name
            tool_method = None  # 初始化 tool_method

            # 如果适用，将原始工具名称拆分为工具名称和工具方法
            if ":" in raw_tool_name:
                tool_name, tool_method = raw_tool_name.split(":", 1)

            tool = None  # 将工具初始化为 None

            # 首先尝试从MCP获取工具
            try:
                import python.helpers.mcp_handler as mcp_helper

                mcp_tool_candidate = mcp_helper.MCPConfig.get_instance().get_tool(
                    self, tool_name
                )
                if mcp_tool_candidate:
                    tool = mcp_tool_candidate
            except ImportError:
                PrintStyle(
                    background_color="black", font_color="yellow", padding=True
                ).print("MCP helper module not found. Skipping MCP tool lookup.")
            except Exception as e:
                PrintStyle(
                    background_color="black", font_color="red", padding=True
                ).print(f"Failed to get MCP tool '{tool_name}': {e}")

            # 如果MCP工具未找到或MCP查找失败，则回退到本地get_tool
            if not tool:
                tool = self.get_tool(
                    name=tool_name,
                    method=tool_method,
                    args=tool_args,
                    message=msg,
                    loop_data=self.loop_data,
                )

            if tool:
                await self.handle_intervention()
                await tool.before_execution(**tool_args)
                await self.handle_intervention()
                response = await tool.execute(**tool_args)
                await self.handle_intervention()
                await tool.after_execution(response)
                await self.handle_intervention()
                if response.break_loop:
                    return response.message
            else:
                error_detail = (
                    f"Tool '{raw_tool_name}' not found or could not be initialized."
                )
                self.hist_add_warning(error_detail)
                PrintStyle(font_color="red", padding=True).print(error_detail)
                self.context.log.log(
                    type="error", content=f"{self.agent_name}: {error_detail}"
                )
        else:
            # fw.msg_misformat.md: 当代理的消息格式不正确，无法解析出有效的工具请求时，用于生成警告消息。
            warning_msg_misformat = self.read_prompt("fw.msg_misformat.md")
            self.hist_add_warning(warning_msg_misformat)
            PrintStyle(font_color="red", padding=True).print(warning_msg_misformat)
            self.context.log.log(
                type="error",
                content=f"{self.agent_name}: Message misformat, no valid tool request found.",
            )

    async def handle_reasoning_stream(self, stream: str):
        # reasoning_stream 扩展在代理进行内部“推理”（reasoning）过程并流式输出其思考时执行，主要功能是实时捕获并更新这些推理流。
        await self.call_extensions(
            "reasoning_stream",
            loop_data=self.loop_data,
            text=stream,
        )

    async def handle_response_stream(self, stream: str):
        try:
            if len(stream) < 25:
                return  # 没有理由尝试
            response = DirtyJson.parse_string(stream)
            if isinstance(response, dict):
                # response_stream 扩展在代理主语言模型（LLM）生成响应并以流式方式传输时执行，核心功能是实时地捕获、处理和显示LLM的输出。
                await self.call_extensions(
                    "response_stream",
                    loop_data=self.loop_data,
                    text=stream,
                    parsed=response,
                )

        except Exception as e:
            pass

    def get_tool(
        self,
        name: str,
        method: str | None,
        args: dict,
        message: str,
        loop_data: LoopData | None,
        **kwargs,
    ):
        from python.tools.unknown import Unknown
        from python.helpers.tool import Tool

        classes = extract_tools.load_classes_from_folder(
            "python/tools", name + ".py", Tool
        )
        tool_class = classes[0] if classes else Unknown
        return tool_class(
            agent=self,
            name=name,
            method=method,
            args=args,
            message=message,
            loop_data=loop_data,
            **kwargs,
        )

    async def call_extensions(self, folder: str, **kwargs) -> Any:
        from python.helpers.extension import Extension

        cache = {}  # 某些扩展可能被频繁调用，例如 response_stream

        if folder in cache:
            classes = cache[folder]
        else:
            classes = extract_tools.load_classes_from_folder(
                "python/extensions/" + folder, "*", Extension
            )
            cache[folder] = classes

        for cls in classes:
            await cls(agent=self).execute(**kwargs)
