---
title: 开始使用 Cursor 和 TiDB MCP Server
summary: 本指南将演示如何在 Cursor 编辑器中配置 TiDB MCP Server。
---

# 开始使用 Cursor 和 TiDB MCP Server

本指南将演示如何在 Cursor 编辑器中配置 TiDB MCP Server。

如需一键安装，请点击下方按钮：

<p><a href="cursor://anysphere.cursor-deeplink/mcp/install?name=TiDB&amp;config=eyJjb21tYW5kIjoidXZ4IC0tZnJvbSBweXRpZGJbbWNwXSB0aWRiLW1jcC1zZXJ2ZXIiLCJlbnYiOnsiVElEQl9IT1NUIjoibG9jYWxob3N0IiwiVElEQl9QT1JUIjoiNDAwMCIsIlRJREJfVVNFUk5BTU0iOiJyb290IiwiVElEQl9QQVNTV09SRCI6IiIsIlRJREJfREFUQUJBU0UiOiJ0ZXN0In19"><img alt="Install TiDB MCP Server" src="https://cursor.com/deeplink/mcp-install-dark.svg"></img></a></p>

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Cursor**：从 [cursor.com](https://cursor.com) 下载并安装 Cursor。
- **Python (>=3.10) 和 uv**：确保已安装 Python（3.10 或更高版本）和 `uv`。可参考 [安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。
- **一个 TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 连接到 TiDB Cloud Starter（推荐）

使用 TiDB Cloud 控制台，通过你的集群凭证创建 Cursor 配置。

1. 进入 [Clusters](https://tidbcloud.com/console/clusters) 页面，选择你的集群，然后点击右上角的 **Use with AI Tools**。
2. 在 **Access `your_cluster_name` with AI tools** 对话框中，选择 Cursor 需要访问的 **Branch** 和 **Database**。
3. 查看对话框中的 **Prerequisites** 列表，并安装任何缺失的依赖项。
4. 配置 root 密码：

   - 如果你尚未设置密码，点击 **Generate Password** 并将其保存在安全的位置（该密码只会显示一次）。
   - 如果已存在密码，在 **Enter the password for easy setup** 字段中输入该密码。
   - 如果忘记密码，在 **Prerequisites** 部分点击 **Reset password** 以生成新密码。

5. 选择 **Cursor** 标签页，点击 **Add to Cursor**，然后在 Cursor 中点击 **Install**。

## 手动配置（适用于任意 TiDB 集群）

如果你更倾向于手动配置，请将以下配置添加到你的 `.cursor/mcp.json` 文件中，并将占位符替换为你的连接参数：

```json
{
  "mcpServers": {
    "TiDB": {
      "command": "uvx --from pytidb[mcp] tidb-mcp-server",
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

更多详情请参阅 [Model Context Protocol 文档](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)。

## 故障排查

如果你在安装 TiDB MCP Server 时遇到问题，请在 Cursor 中查看 MCP 日志。

1. 在编辑器顶部主菜单点击 **View** > **Output**。
2. 在 **Output** 面板的下拉菜单中选择 **MCP**。
3. 如果你看到类似 `[error] Could not start MCP server tidb-mcp-server: Error: spawn uvx ENOENT` 的错误，说明你的系统 `$PATH` 环境变量中可能不存在 `uvx` 命令。对于 macOS 用户，可以通过运行 `brew install uv` 安装 `uvx`。