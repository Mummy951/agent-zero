## “多模态（视觉）代理工具”可用:

### vision_load:
将图像数据加载到 LLM
使用 `paths` 参数进行附件
如果需要，可包含多张图像
仅支持位图，如果需要请先转换

**使用示例**:
```json
{
    "thoughts": [
        "我需要查看图像...",
    ],
    "headline": "加载图像进行视觉分析",
    "tool_name": "vision_load",
    "tool_args": {
        "paths": ["/path/to/image.png"],
    }
}
``` 