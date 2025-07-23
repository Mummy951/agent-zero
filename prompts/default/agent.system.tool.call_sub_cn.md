### call_subordinate

你可以使用下属来完成子任务
下属可以是科学家、程序员、工程师等
`message` 字段：始终为新的下属描述角色、任务细节和目标概述
委派特定的子任务，而不是整个任务
`reset` 参数用法：
  "true": 生成新的下属
  "false": 继续现有下属
如果是上级，则进行协调
使用 `call_subordinate` 工具并设置 `reset` 为 false 来回复现有下属

使用示例
~~~json
{
    "thoughts": [
        "结果看起来还可以，但是...",
        "我将让一名程序员下属来修复...",
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "...",
        "reset": "true"
    }
}
~~~ 