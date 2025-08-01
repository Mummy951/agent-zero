Agent Zero 的主要技术栈包括：

*   **后端：** Python (基于 Flask 框架)
*   **LLM 交互：** LiteLLM (用于与各种 LLM 提供商交互)
*   **向量数据库：** FAISS (用于内存管理和知识检索)
*   **文档处理：** Unstructured, PyPDF, PyMuPDF, Playwright (用于解析和处理不同格式的文档和网页内容)
*   **容器化：** Docker
*   **版本控制：** GitPython (用于 Git 交互)
*   **语音：** OpenAI Whisper (语音转文本), Kokoro (文本转语音)
*   **其他库：** sentence-transformers, simpleeval, paramiko (SSH), a2wsgi, flask-basicauth 等。