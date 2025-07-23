### behaviour_adjustment:
根据用户请求更新代理行为
将要添加或移除的指令写入 `adjustments` 参数
用法:
~~~json
{
    "thoughts": [
        "...",
    ],
    "headline": "根据用户请求调整代理行为",
    "tool_name": "behaviour_adjustment",
    "tool_args": {
        "adjustments": "remove...",
    }
}
~~~ 