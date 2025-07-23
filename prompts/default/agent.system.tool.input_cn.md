### input:
使用 `keyboard` 参数进行终端程序输入
使用 `session` 参数指定终端会话编号
回答对话、输入密码等
不适用于浏览器
用法:
~~~json
{
    "thoughts": [
        "程序询问 Y/N...",
    ],
    "headline": "响应终端程序提示",
    "tool_name": "input",
    "tool_args": {
        "keyboard": "Y",
        "session": 0
    }
}
~~~ 