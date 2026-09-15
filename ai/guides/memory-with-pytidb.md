---
title: AI Agent Memory 示例
summary: 为聊天机器人和对话式 AI 应用实现对话记忆。
---

# AI Agent Memory 示例

本示例展示了如何借助 TiDB 的向量搜索能力构建一个具有持久记忆的 AI agent。

只需几行代码，你就可以创建一个能够记住过往交互并随着时间推移逐步建立上下文的对话式 AI。

- **持久记忆**：可跨会话和用户交互记住对话内容
- **交互式聊天**：支持使用 Web UI 或命令行接口
- **多用户支持**：为每个用户保留独立的记忆上下文
- **实时记忆查看**：可在 Web 界面中查看已存储的记忆

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/ai-agent-with-memory-powered-by-tidb.png" alt="AI Agent with memory powered by TiDB" width="700"/>
    <p align="center"><i>由 TiDB 提供记忆能力支持的 AI Agent</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你已具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- **OpenAI API key**：从 [OpenAI](https://platform.openai.com/api-keys) 获取 OpenAI API key。

## 运行方式 {#how-to-run}

### 步骤 1：克隆 `pytidb` 仓库 {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### 步骤 2：安装所需软件包 {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### 步骤 3：设置环境变量 {#step-3-set-environment-variables}

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页。
2. 点击右上角的 **Connect**。此时会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

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

### 步骤 4：运行应用 {#step-4-run-the-application}

从以下选项中选择一种：

### 选项 1：启动 Web 应用 {#option-1-launch-the-web-application}

```bash
streamlit run app.py
```

打开浏览器，访问 `http://localhost:8501`，然后按照 [在 Web 应用中与记忆交互](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application) 开始使用支持记忆功能的 AI 助手。

### 选项 2：运行命令行应用 {#option-2-run-the-command-line-application}

```bash
python main.py
```

按照 [在命令行应用中与记忆交互](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application) 开始使用支持记忆功能的 AI 助手。

## 在 Web 应用中与记忆交互 {#interact-with-memory-in-web-application}

在 Web 应用中，你可以与 AI 助手进行交互。UI 包含以下组件：

- **侧边栏**：用户设置和聊天列表。
- **主聊天区域**：与 AI 助手交互的聊天界面。
- **记忆查看器**：实时显示已存储事实的记忆查看器。

按照以下步骤体验记忆功能的工作方式：

1. 在默认聊天会话中介绍你自己。例如：“Hello, I am John. I work as a software engineer and love guitar.”
2. 你可以在记忆查看器中看到你提供的信息。
3. 点击侧边栏中的 **New chat**，开始一个新的聊天会话。
4. 在新的聊天会话中提问 “Who am I?”。AI 会从之前的对话中回忆起你的信息。

## 在命令行应用中与记忆交互 {#interact-with-memory-in-command-line-application}

在命令行应用中，你可以与 AI 助手聊天并介绍自己。

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

在第一次对话之后，AI 助手会记住你提供的信息，并在后续回答问题时使用这些信息。

现在，你可以开始一个新的聊天会话，并向 AI 助手提问 “Who am I?”。

**另一个聊天会话中的示例对话：**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

如你所见，AI 助手可以跨会话记住你！

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/memory)