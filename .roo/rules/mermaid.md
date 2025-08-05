Mermaid是一种基于文本的图表和流程图语言，使用简单的语法来创建各种类型的图表。以下是主要的语法规则：

## 基本结构

每个Mermaid图表都以图表类型声明开始，然后是具体的图表内容。

## 主要图表类型

### 1. 流程图 (Flowchart)
```
flowchart TD
    A[开始] --> B{判断}
    B -->|是| C[执行A]
    B -->|否| D[执行B]
    C --> E[结束]
    D --> E
```

**节点形状：**
- `A[矩形]` - 矩形
- `B(圆角矩形)` - 圆角矩形
- `C{菱形}` - 菱形（判断）
- `D((圆形))` - 圆形
- `E[[子程序]]` - 子程序
- `F[/平行四边形/]` - 平行四边形

**方向：**
- `TD` 或 `TB` - 从上到下
- `BT` - 从下到上  
- `LR` - 从左到右
- `RL` - 从右到左

### 2. 序列图 (Sequence Diagram)
```
sequenceDiagram
    participant A as 用户
    participant B as 系统
    A->>B: 发送请求
    B-->>A: 返回响应
    Note over A,B: 这是一个注释
```

**交互类型：**
- `->` 实线箭头
- `-->` 虚线箭头
- `->>` 实线箭头（异步）
- `-->>` 虚线箭头（异步）

### 3. 甘特图 (Gantt Chart)
```
gantt
    title 项目计划
    dateFormat YYYY-MM-DD
    section 阶段1
    任务A :a1, 2024-01-01, 30d
    任务B :after a1, 20d
    section 阶段2
    任务C :2024-02-01, 25d
```

### 4. 类图 (Class Diagram)
```
classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    class Dog {
        +bark()
    }
    Animal <|-- Dog
```

**关系类型：**
- `<|--` 继承
- `*--` 组合
- `o--` 聚合
- `-->` 关联
- `--` 链接

### 5. 状态图 (State Diagram)
```
stateDiagram-v2
    [*] --> 待机
    待机 --> 运行 : 启动
    运行 --> 暂停 : 暂停
    暂停 --> 运行 : 继续
    运行 --> [*] : 停止
```

### 6. ER图 (Entity Relationship Diagram)
```
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        string name
        string email
    }
    ORDER {
        int orderNumber
        date orderDate
    }
```

### 7. 饼图 (Pie Chart)
```
pie title 销售占比
    "产品A" : 42.96
    "产品B" : 50.05
    "产品C" : 10.01
```

## 通用语法规则

### 样式和主题
```
%%{init: {'theme':'dark'}}%%
flowchart TD
    A[节点A]
    classDef default fill:#f9f,stroke:#333,stroke-width:2px
```

### 注释
```
%% 这是注释
flowchart TD
    A --> B %% 行内注释
```

### 子图
```
flowchart TD
    subgraph 子系统A
        A1 --> A2
    end
    subgraph 子系统B
        B1 --> B2
    end
    A2 --> B1
```

### 链接样式
```
flowchart TD
    A --> B
    linkStyle 0 stroke:#ff3,stroke-width:4px,color:red
```

这些是Mermaid的主要语法规则。每种图表类型都有其特定的语法细节，但都遵循简洁、易读的文本格式原则。