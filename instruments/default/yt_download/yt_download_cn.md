# 问题
下载一个 YouTube 视频
# 解决方案
1. 如果指定了文件夹，则 cd 到该文件夹
2. 运行带有您的视频 URL 的 shell 脚本：

```bash
bash /a0/instruments/default/yt_download/yt_download.sh <url>
```
3. 将 `<url>` 替换为您的视频 URL。
4. 脚本将处理 yt-dlp 的安装和下载过程。 