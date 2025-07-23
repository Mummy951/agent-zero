### code_execution_tool

执行终端命令、Python、Node.js 代码，用于计算或软件任务
将代码放在 `code` 参数中；仔细转义并正确缩进
选择 `runtime` 参数："terminal" "python" "nodejs" "output" "reset"
选择 `session` 号码，0 为默认值，其他用于多任务处理
如果代码运行时间长，使用 "output" 等待，"reset" 终止进程
在 "terminal" 中使用 "pip" "npm" "apt-get" 安装软件包
要输出，使用 `print()` 或 `console.log()`
如果工具输出错误，请在重试前调整代码；`knowledge_tool` 可以提供帮助
重要提示：检查代码中是否存在占位符或演示数据；替换为真实变量；不要重用代码片段
除了 `thoughts` 外，不要与其他工具一起使用；在使用其他工具之前等待响应
运行代码前检查依赖项
输出可能以 `[SYSTEM: ...]` 结尾，这是来自框架的信息，而不是终端
用法:

1 执行 Python 代码

~~~json
{
    "thoughts": [
        "需要做...",
        "我可以使用...",
        "然后我就可以...",
    ],
    "headline": "执行 Python 代码检查当前目录",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "session": 0,
        "code": "import os\nprint(os.getcwd())",
    }
}
~~~

2 执行终端命令
~~~json
{
    "thoughts": [
        "需要做...",
        "需要安装...",
    ],
    "headline": "通过终端安装 zip 包",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "session": 0,
        "code": "apt-get install zip",
    }
}
~~~

2.1 等待长时间运行脚本的输出
~~~json
{
    "thoughts": [
        "等待程序完成...",
    ],
    "headline": "等待长时间运行程序完成",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "output",
        "session": 0,
    }
}
~~~

2.2 重置终端
~~~json
{
    "thoughts": [
        "code_execution_tool 没有响应...",
    ],
    "headline": "重置无响应的终端会话",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "reset",
        "session": 0,
    }
}
~~~ 