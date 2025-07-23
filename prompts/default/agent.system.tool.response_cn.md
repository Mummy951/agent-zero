### response:
给用户的最终答案
结束任务处理，仅在完成或没有活跃任务时使用
将结果放入 `text` 参数
用法:
~~~json
{
    "thoughts": [
        "...",
    ],
    "headline": "向用户提供最终答案",
    "tool_name": "response",
    "tool_args": {
        "text": "给用户的答案",
    }
}
~~~ 