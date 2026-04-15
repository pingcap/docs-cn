---
title: TiDB MCP Server
summary: 使用自然语言指令，通过 TiDB MCP Server 管理你的 TiDB 数据库。
---

# TiDB MCP Server

TiDB MCP Server 是一个开源工具，可以让你通过自然语言指令与 TiDB 数据库进行交互。

## 理解 MCP 及 TiDB MCP Server

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 是一种标准化 LLM 与外部工具之间通信的协议。

MCP 采用 client-server 架构，允许主机应用连接到多个外部 server：

- **Hosts**：由 AI 驱动的应用，例如 Claude Desktop 或像 Cursor 这样的 IDE，会主动发起与 MCP server 的连接。

- **Clients**：嵌入在主机应用中的组件，用于与单个 MCP server 建立一对一连接。

- **Servers**：外部 service，例如 **TiDB MCP Server**，为 client 提供工具、上下文和 prompt，以便与外部系统交互。

**TiDB MCP Server** 是一个 MCP 兼容的 server，为 MCP client 提供与 TiDB 数据库交互所需的工具和上下文。

## 前置条件

在开始之前，请确保你具备以下条件：

- **一个 MCP 兼容的 client**：例如 [Cursor](/ai/integrations/tidb-mcp-cursor.md) 或 [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)。
- **Python (>=3.10) 和 uv**：确保已安装 Python（3.10 或更高版本）和 `uv`。请按照 [安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。
- **一个 TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 支持的 MCP client

请参考以下指南，了解如何在特定 MCP client 中使用 TiDB MCP Server 的详细示例：

- [Cursor](/ai/integrations/tidb-mcp-cursor.md)
- [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)

如果上述列表中没有你的 MCP client，请按照下方的设置步骤进行配置。

## 设置步骤

TiDB MCP Server 支持两种与 MCP client 集成的模式：

- 标准输入/输出（STDIO）模式（默认）
- Server-Sent Events（SSE）模式

TiDB MCP Server 默认使用 STDIO 模式，因此你无需提前启动独立的 server。

你可以根据需要选择其中一种模式，在 MCP client 中设置 TiDB MCP Server。

### STDIO 模式

要在 MCP client 中以 STDIO 模式设置 TiDB MCP Server，请按照以下步骤操作：

1. 参考你的 MCP client 文档，了解如何配置 MCP server。

2. 进入你的 [TiDB Cloud 集群](https://tidbcloud.com/console/clusters)页面，导航到你的集群概览页。

3. 在集群概览页点击 **Connect**，获取连接参数。

4. 在 AI 应用的 `mcpServers` 配置文件 section 中，使用你的连接参数配置 TiDB MCP Server。

      MCP 配置文件示例：

      ```json
      {
        "mcpServers": {
          "TiDB": {
            "command": "uvx --from pytidb[mcp] tidb-mcp-server",
            "env": {
              "TIDB_HOST": "localhost",
              "TIDB_PORT": "4000",
              "TIDB_USERNAME": "root",
              "TIDB_PASSWORD": "",
              "TIDB_DATABASE": "test"
            }
          }
        }
      }
      ```

### Server-Sent Events（SSE）模式

要在 MCP client 中以 SSE 模式设置 TiDB MCP Server，请按照以下步骤操作：

1. 参考你的 MCP client 文档，了解如何配置 MCP server。

2. 进入你的 [TiDB Cloud 集群](https://tidbcloud.com/console/clusters)页面，选择你的集群。

3. 在集群页面点击 **Connect**，获取连接参数。

4. 使用你的连接参数创建一个 `.env` 文件。

    `.env` 文件示例：

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    EOF
    ```

5. 使用 `--transport sse` 选项启动 TiDB MCP Server：

    ```bash
    uvx --from "pytidb[mcp]" tidb-mcp-server --transport sse
    ```

6. 在 AI 应用的 `mcpServers` 配置文件 section 中添加 `TiDB` MCP server 配置。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "url": "http://localhost:8000/sse"
        }
      }
    }
    ```

## 支持的操作（工具）

TiDB MCP Server 向 MCP client 提供以下操作（工具）。你可以通过自然语言指令，使用它们与 TiDB 项目和数据库进行交互。

**数据库管理**

- `show_databases` - 显示 TiDB 集群中的所有数据库

    * `username`：数据库用户名（string，可选）
    * `password`：数据库密码（string，可选）

- `switch_database` - 切换到指定数据库

    * `db_name`：要切换的数据库名（string，必填）
    * `username`：数据库用户名（string，可选）
    * `password`：数据库密码（string，可选）

- `show_tables` - 显示当前数据库中的所有表

**SQL 查询与执行**

- `db_query` - 执行只读 SQL 查询

    * `sql_stmt`：SQL 查询语句（string，必填）

- `db_execute` - 执行 SQL 语句（DML 或 DDL）

    * `sql_stmts`：单条 SQL 语句或 SQL 语句数组（string 或 array，必填）

**用户管理**

- `db_create_user` - 创建新数据库用户

    * `username`：新用户名称（string，必填）
    * `password`：新用户密码（string，必填）

- `db_remove_user` - 移除已有数据库用户

    * `username`：要移除的用户名（string，必填）