# 后端架构核心类图

以下是 Agent Zero 后端架构的核心类图，主要展示了 `run_ui.py`、`initialize.py` 和 `preload.py` 以及它们所依赖或初始化的关键模块和类之间的关系。

```mermaid
classDiagram
    direction LR

    class run_ui {
        +run()
        +init_a0()
    }
    class initialize {
        +initialize_agent()
        +initialize_chats()
        +initialize_mcp()
        +initialize_job_loop()
        +initialize_preload()
    }
    class preload {
        +preload()
    }
    class ApiHandler {
        <<interface>>
        +handle_request()
    }
    class Message {
        +process()
        +communicate()
        +respond()
    }
    class Flask {
        <<framework>>
    }
    class AgentConfig {
        <<data>>
    }
    class ModelConfig {
        <<data>>
    }
    class DeferredTask {
        +start_task()
    }
    class MCPConfig {
        <<data>>
    }
    class TaskScheduler {
        <<service>>
    }
    class Whisper {
        <<service>>
    }
    class Agent {
        <<core>>
    }
    class Request {
        <<data>>
    }
    class Response {
        <<data>>
    }


    run_ui -- initialize : calls init_a0()
    initialize --> preload : calls initialize_preload()
    initialize --|> AgentConfig : creates
    initialize --|> ModelConfig : creates
    initialize ..> DeferredTask : uses for async init
    initialize ..> MCPConfig : initializes
    initialize ..> TaskScheduler : initializes
    initialize ..> Whisper : preloads (via preload)

    run_ui --> Flask : initializes webapp
    run_ui --> ApiHandler : registers handlers
    Message --|> ApiHandler : implements
    Message ..> Agent : communicates with
    AgentConfig ..> Agent : configures

    ApiHandler <.. Agent : interacts with
    ApiHandler <.. Request : uses
    ApiHandler <.. Response : uses

    Agent --> ApiHandler : (may call tools/APIs)
    Agent --> AgentConfig : (uses config)
