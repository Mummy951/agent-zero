### knowledge_tool:
将你的问题作为搜索引擎就绪的查询提供
第一个响应者将是搜索引擎，而不是 AI 或人类
尽可能简洁准确地 formulate 你的查询
提供 `question` 参数以获取在线和记忆响应
强大的工具可以直接回答特定问题
首先询问结果而不是指导
记忆提供指导，在线提供当前信息
在线验证记忆
**使用示例**:
~~~json
{
    "thoughts": [
        "...",
    ],
    "headline": "搜索知识库和在线资源",
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "如何...",
    }
}
~~~ 