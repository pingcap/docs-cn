---
title: 开始使用 Claude Desktop 和 TiDB MCP Server
summary: 本指南将向你展示如何在 Claude Desktop 中配置 TiDB MCP Server。
---

# 开始使用 Claude Desktop 和 TiDB MCP Server

本指南将介绍如何在 Claude Desktop 中配置 TiDB MCP Server。

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Claude Desktop**：从 [claude.ai](https://claude.ai/download) 下载并安装 Claude Desktop。
- **Python (>=3.10) 和 uv**：确保已安装 Python（3.10 或更高版本）和 `uv`。请按照 [安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。

## 设置步骤

按照以下步骤在 Claude Desktop 中设置 TiDB MCP Server：

1. 打开 **Settings** 对话框。
2. 在对话框中点击 **Developers** 标签页。
3. 点击 **Edit Config** 按钮，打开 MCP 配置文件 `claude_desktop_config.json`。
4. 将以下配置复制到 `claude_desktop_config.json` 文件中。

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

5. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
6. 点击右上角的 **Connect**，获取连接参数，并将 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD` 和 `TIDB_DATABASE` 的值替换为你自己的。
7. 重启 Claude Desktop。

如需了解更多详情，请参阅 [如何在 Claude Desktop 中配置 MCP server](https://modelcontextprotocol.io/quickstart/user)。
