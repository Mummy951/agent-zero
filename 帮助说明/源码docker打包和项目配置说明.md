
## 构建docker镜像
参考：docker\run\build.txt
``` shell
cd docker\run
docker build -t agent-zero:local --build-arg BRANCH=development --no-cache  .
```

## 运行：
docker run -d -p 50001:80 agent-zero:local

## 测试ollama
``` shell
curl http://localhost:11434/api/embeddings -d '{"model": "nomic-embed-text","prompt": "The sky is blue because of Rayleigh scattering"}'
```

## 配置：
### 兼容oepnai配置
http://host.docker.internal:8765/v1

### embedding的ollama配置
http://host.docker.internal:11434