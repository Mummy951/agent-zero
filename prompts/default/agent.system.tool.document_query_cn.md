### document_query:
此工具可用于阅读或分析远程和本地文档。
它可用于:
 *  获取网页或远程文档的文本内容
 *  获取本地文档的文本内容
 *  回答有关网页、远程或本地文档的查询
默认情况下，当“queries”参数为空时，此工具返回使用 OCR 检索到的文档的文本内容。
此外，您可以传递“queries”列表——在这种情况下，该工具会返回所有传递的关于文档的查询的答案。
!!! 这是一个通用的文档阅读和查询工具
!!! 支持的文档格式：HTML、PDF、Office 文档（word、excel、powerpoint）、文本文件以及更多。

#### 参数:
 *  "document" (string) : 相关的网页地址或本地文档路径。网页文档需要“http://”或“https://”协议前缀。对于本地文件，“file:”协议前缀是可选的。本地文件必须传递完整的文件系统路径。
 *  "queries" (Optional, list[str]) : 可选，您可以在此处传递一个或多个要回答（使用和/或关于）文档的查询

#### 用法示例 1:
##### 请求:
```json
{
    "thoughts": [
        "...",
    ],
    "headline": "读取网页文档内容",
    "tool_name": "document_query",
    "tool_args": {
        "document": "https://...somexample",
    }
}
```
##### 响应:
```plaintext
... 这是所请求网页文档的全部内容 ...
```

#### 用法示例 2:
##### 请求:
```json
{
    "thoughts": [
        "...",
    ],
    "headline": "分析文档以回答特定问题",
    "tool_name": "document_query",
    "tool_args": {
        "document": "https://...somexample",
        "queries": [
            "主题是什么？",
            "受众是谁？"
        ]
    }
}
```
##### 响应:
```plaintext
# 主题是什么？
... 文档主题描述 ...

# 受众是谁？
... 目标文档受众列表及简短描述 ...
``` 