---
title: 开始使用 Claude Code 和 TiDB MCP Server
summary: 本指南将向你展示如何在 Claude Code 中配置 TiDB MCP Server。
---

# 开始使用 Claude Code 和 TiDB MCP Server

本指南将介绍如何在 Claude Code 中配置 TiDB MCP Server。

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Claude Code**：可从 [claude.com](https://claude.com/product/claude-code) 安装。
- **Python (>=3.10) 和 uv**：确保已安装 Python（3.10 或更高版本）和 `uv`。可按照 [安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。
- **一个 TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 连接到 TiDB Cloud Starter（推荐）

使用 TiDB Cloud 控制台生成可直接运行的 Claude Code 命令。

1. 进入 [Clusters](https://tidbcloud.com/console/clusters) 页面，选择你的集群，然后点击右上角的 **Use with AI Tools**。
2. 在 **Access `your_cluster_name` with AI tools** 对话框中，选择 Claude Code 需要访问的 **Branch** 和 **Database**。
3. 查看对话框中的 **Prerequisites** 列表，并安装所有缺失的依赖项。
4. 配置 root 密码：

   - 如果你尚未设置密码，点击 **Generate Password** 并将其保存在安全的位置（该密码只会显示一次）。
   - 如果已存在密码，在 **Enter the password for easy setup** 字段中输入该密码。
   - 如果忘记密码，在 **Prerequisites** 部分点击 **Reset password** 以生成新密码。

5. 选择 **Claude Code** 标签页，复制设置命令，并在终端中运行。

## 手动配置（任意 TiDB 集群）

如果你更倾向于手动设置，可使用以下任一方法，并将占位符替换为你的连接参数。

### 方法 1：CLI 命令

```bash
claude mcp add --transport stdio TiDB \
  --env TIDB_HOST='<YOUR_TIDB_HOST>' \
  --env TIDB_PORT=<YOUR_TIDB_PORT> \
  --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
  --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
  --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
  -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
```

### 方法 2：项目配置文件

将以下配置添加到你的项目级 `.mcp.json` 文件中。详细信息请参见 [Claude Code MCP 文档](https://code.claude.com/docs/en/mcp#project-scope)。

```json
{
  "mcpServers": {
    "TiDB": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
      "env": {
        "TIDB_HOST": "<YOUR_TIDB_HOST>",
        "TIDB_PORT": "<YOUR_TIDB_PORT>",
        "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
        "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
        "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
      }
    }
  }
}
```

## 另请参阅

- [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md)
