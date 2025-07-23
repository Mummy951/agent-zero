### browser_agent:

下属代理控制 Playwright 浏览器
`message` 参数用于与代理对话，提供清晰的指令、凭据和基于任务的信息
`reset` 参数会生成新的代理
如果正在迭代，请勿重置
描述要精确，例如：打开 Google 登录并结束任务，使用...登录并结束任务
在后续操作时，以“考虑到已打开的页面”开头
不要使用“等待指令”之类的短语，请使用“结束任务”
下载默认在 `/a0/tmp/downloads`

用法:
```json
{
  "thoughts": ["我需要登录..."],
  "headline": "为登录打开新的浏览器会话",
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "打开并登录我到...",
    "reset": "true"
  }
}
```

```json
{
  "thoughts": ["我需要登录..."],
  "headline": "继续使用现有浏览器会话",
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "考虑到已打开的页面，点击...",
    "reset": "false"
  }
}
``` 