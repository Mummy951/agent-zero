### browser_open:

使用 Playwright 控制有状态的 Chromium 浏览器
使用 url 参数打开新页面
所有浏览器工具都返回带有唯一选择器的简化 DOM
页面打开后，使用 `browser_do` 工具进行交互。

```json
{
  "thoughts": ["我需要发送..."],
  "tool_name": "browser_open",
  "tool_args": {
    "url": "https://www.example.com"
  }
}
```

### browser_do:

用于填写表单、按下按键、点击按钮、执行 JavaScript
参数是可选的
`fill` 参数是包含 `selector` 和 `text` 的对象数组
`press` 参数是要按下的按键数组，按顺序 - Enter, Escape...
`click` 参数是要点击的选择器数组，按顺序
`execute` 参数是要执行的 JavaScript 字符串
始终优先点击 `<a>` 或 `<button>` 标签
用 Enter 确认字段或找到提交按钮
同意和弹出窗口可能会阻塞页面，请关闭它们
只使用上次浏览器回复中提到的选择器
如果不起作用，不要重复相同的步骤！寻找解决问题的方法
```json
{
  "thoughts": [
    "需要登录...",
    "我将填写用户名、密码，点击记住我并提交。"
  ],
  "tool_name": "browser_do",
  "tool_args": {
    "fill": [
      {
        "selector": "12l",
        "text": "root"
      },
      {
        "selector": "14vs",
        "text": "toor"
      }
    ],
    "click": ["19c", "65d"]
  }
}
```

```json
{
  "thoughts": [
    "搜索...",
    "我将填写搜索框并按下 Enter。"
  ],
  "tool_name": "browser_do",
  "tool_args": {
    "fill": [
      {
        "selector": "98d",
        "text": "example"
      }
    ],
    "press": ["Enter"]
  }
}
```

```json
{
  "thoughts": [
    "标准交互不可能，我需要执行自定义代码..."
  ],
  "tool_name": "browser_do",
  "tool_args": {
    "execute": "const elem = document.querySelector('[data-uid=\"4z\"]'); elem.click();"
  }
}
``` 