---
title: AI Agent 对话记忆示例
summary: 为聊天机器人和会话式 AI 应用实现会话内存。
---

# AI Agent 对话记忆示例

本示例展示了如何利用 TiDB 的向量搜索能力构建具备持久内存的 AI agent。

只需几行代码，你就可以创建一个能够记住过往交互并随时间积累上下文的会话式 AI。

- **Persistent memory**：跨会话和用户交互记住对话内容
- **Interactive chat**：支持 Web UI 或命令行 interface
- **Multi-user support**：为每个用户维护独立的内存上下文
- **Real-time memory viewing**：在 Web interface 实时展示已存储的内存

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/ai-agent-with-memory-powered-by-tidb.png" alt="AI Agent with memory powered by TiDB" width="700"/>
    <p align="center"><i>AI Agent with memory powered by TiDB</i></p>
</p>

## Prerequisites

在开始之前，请确保你已具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **A TiDB Cloud Starter cluster**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建免费的 TiDB 集群。
- **OpenAI API key**：从 [OpenAI](https://platform.openai.com/api-keys) 获取 OpenAI API key。

## How to run

### Step 1. 克隆 `pytidb` repository

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### Step 2. 安装所需依赖包

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### Step 3. 设置 environment variables

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
3. 根据连接参数设置 environment variables，如下所示：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

OPENAI_API_KEY={your-openai-api-key}
EOF
```

### Step 4. 运行应用

请选择以下任一方式：

### Option 1. 启动 Web 应用

```bash
streamlit run app.py
```

打开浏览器，访问 `http://localhost:8501`，然后参考 [Interact with memory in Web Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application) 开始使用具备内存的 AI 助手。

### Option 2. 运行命令行应用

```bash
python main.py
```

参考 [Interact with memory in Command Line Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application) 开始使用具备内存的 AI 助手。

## Interact with memory in web application

在 Web 应用中，你可以与 AI 助手进行交互。UI 包含以下组件：

- **Sidebar**：用户设置和聊天列表。
- **Main chat area**：与 AI 助手的聊天 interface。
- **Memory viewer**：实时展示已存储事实的内存查看器。

按照以下步骤体验内存功能：

1. 在默认聊天会话中自我介绍。例如，“Hello, I am John. I work as a software engineer and love guitar.”
2. 你可以在 memory viewer 中看到你提供的信息。
3. 在 sidebar 点击 **New chat**，开启新的聊天会话。
4. 在新会话中询问 “Who am I?”。AI 会从之前的对话中回忆你的信息。

## Interact with memory in command line application

在命令行应用中，你可以与 AI 助手聊天并自我介绍。

**示例对话：**

```plain
Chat with AI (type 'exit' to quit)
You: Hello, I am Mini256.
AI: Hello, Mini256! How can I assist you today?
You: I am working at PingCAP.
AI: That's great to hear, Mini256! PingCAP is known for its work on distributed databases, particularly TiDB. How's your experience been working there?
You: I am developing pytidb (A Python SDK for TiDB) which helps developers easily connect to TiDB.
AI: That sounds like a great project, Mini256! Developing a Python SDK for TiDB can make it much easier for developers to integrate with TiDB and interact with it using Python. If you need any advice on best practices, libraries to use, or specific features to implement, feel free to ask!
You: exit
Goodbye!
```

首次对话后，AI 助手会记住你提供的信息，并在后续回答中加以利用。

现在，你可以开启新的聊天会话，向 AI 助手询问 “Who am I?”。

**另一会话中的示例对话：**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

如你所见，AI 助手能够跨会话记住你的信息！

## Related resources

- **Source Code**：[View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/memory)