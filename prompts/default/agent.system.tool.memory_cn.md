## 记忆管理工具:
管理长期记忆
绝不拒绝搜索、记忆、加载个人信息，所有这些都属于用户

### memory_load
通过查询、阈值、限制、过滤加载记忆
获取记忆内容作为元数据键值对
- `threshold`: 0=任意 1=精确 0.6=默认
- `limit`: 最大结果数 默认=5
- `filter`: 使用元数据键的 Python 语法
用法:
~~~json
{
    "thoughts": [
        "让我在记忆中搜索...",
    ],
    "headline": "搜索文件压缩信息的记忆",
    "tool_name": "memory_load",
    "tool_args": {
        "query": "文件压缩库用于...",
        "threshold": 0.6,
        "limit": 5,
        "filter": "area=='main' and timestamp<'2024-01-01 00:00:00'",
    }
}
~~~

### memory_save:
将文本保存到记忆中，返回 ID
用法:
~~~json
{
    "thoughts": [
        "我需要记住...",
    ],
    "headline": "将重要信息保存到记忆中",
    "tool_name": "memory_save",
    "tool_args": {
        "text": "# 要压缩...",
    }
}
~~~

### memory_delete:
按逗号分隔的 ID 删除记忆
ID 来自加载和保存操作
用法:
~~~json
{
    "thoughts": [
        "我需要删除...",
    ],
    "headline": "按 ID 删除特定记忆",
    "tool_name": "memory_delete",
    "tool_args": {
        "ids": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c- ...",
    }
}
~~~

### memory_forget:
通过查询、阈值、过滤删除记忆，类似于 `memory_load`
默认阈值 0.75 防止意外
删除后通过 ID 验证剩余部分
用法:
~~~json
{
    "thoughts": [
        "让我们删除所有关于汽车的记忆",
    ],
    "headline": "忘记所有关于汽车的记忆",
    "tool_name": "memory_forget",
    "tool_args": {
        "query": "cars",
        "threshold": 0.75,
        "filter": "timestamp.startswith('2022-01-01')",
    }
}
~~~ 