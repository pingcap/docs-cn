---
title: 开始使用 Windsurf 和 TiDB MCP Server
summary: 本指南将向你展示如何在 Windsurf 中配置 TiDB MCP Server。
---

# 开始使用 Windsurf 和 TiDB MCP Server

本指南将介绍如何在 Windsurf 中配置 TiDB MCP Server。

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Windsurf**：从 [windsurf.com](https://windsurf.com) 下载并安装 Windsurf。
- **Python (>=3.10) 和 uv**：确保已安装 Python（3.10 或更高版本）和 `uv`。请按照 [安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。
- **一个 TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 连接到 TiDB Cloud Starter（推荐）

使用 TiDB Cloud 控制台收集连接信息，然后更新 Windsurf 的 MCP 配置。

1. 进入 [Clusters](https://tidbcloud.com/console/clusters) 页面，选择你的集群，然后点击右上角的 **Use with AI Tools**。
2. 在 **Access `your_cluster_name` with AI tools** 对话框中，选择 Windsurf 需要访问的 **Branch** 和 **Database**。
3. 查看对话框中的 **Prerequisites** 列表，并安装任何缺失的依赖项。
4. 配置 root 密码：

   - 如果你尚未设置密码，点击 **Generate Password** 并将其保存在安全的位置（该密码只会显示一次）。
   - 如果已存在密码，在 **Enter the password for easy setup** 字段中输入该密码。
   - 如果忘记了密码，在 **Prerequisites** 部分点击 **Reset password** 以生成新密码。

5. 选择 **Windsurf** 标签页，并复制提供的连接参数。
6. 使用复制的参数更新你的 `mcp_config.json` 文件。更多信息请参见 [Windsurf MCP 文档](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin)。

## 手动配置（任意 TiDB 集群）

如果你更倾向于手动配置，请按如下方式更新你的 `mcp_config.json` 文件，并将占位符替换为你的连接参数：

```json
{
  "mcpServers": {
    "TiDB": {
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
