---
title: 使用 mysql2 连接 TiDB
summary: 了解如何使用 Ruby mysql2 连接 TiDB。本教程提供使用 mysql2 gem 操作 TiDB 的 Ruby 示例代码片段。
---

# 使用 mysql2 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [mysql2](https://github.com/brianmario/mysql2) 是 Ruby 最流行的 MySQL 驱动程序之一。

在本教程中，您可以学习如何使用 TiDB 和 mysql2 完成以下任务：

- 设置环境。
- 使用 mysql2 连接到 TiDB 集群。
- 构建并运行应用程序。您也可以查看基本 CRUD 操作的[示例代码片段](#示例代码片段)。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- 在您的机器上安装 [Ruby](https://www.ruby-lang.org/en/) >= 3.0
- 在您的机器上安装 [Bundler](https://bundler.io/)
- 在您的机器上安装 [Git](https://git-scm.com/downloads)
- 一个正在运行的 TiDB 集群

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

## 运行示例应用程序连接到 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `mysql2` 和 `dotenv`）：

```shell
bundle install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于您的现有项目，运行以下命令安装包：

```shell
bundle add mysql2 dotenv
```

</details>

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

   - **连接类型**设置为 `Public`。
   - **分支**设置为 `main`。
   - **连接工具**设置为 `General`。
   - **操作系统**与您运行应用程序的操作系统匹配。

4. 如果您还没有设置密码，点击**生成密码**生成随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下设置环境变量，并将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    ```

   > **注意**
   >
   > 对于 TiDB Cloud Serverless，使用公共端点时**必须**通过 `DATABASE_ENABLE_SSL` 启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请在首次连接之前点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下设置环境变量，并将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    DATABASE_SSL_CA={downloaded_ssl_ca_path}
    ```

   > **注意**
   >
   > 使用公共端点连接到 TiDB Cloud Dedicated 集群时，建议启用 TLS 连接。
   >
   > 要启用 TLS 连接，将 `DATABASE_ENABLE_SSL` 修改为 `true`，并使用 `DATABASE_SSL_CA` 指定从连接对话框下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下设置环境变量，并将相应的占位符 `{}` 替换为您自己的 TiDB 连接信息：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    ```

   如果您在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并检查结果

运行以下命令执行示例代码：

```shell
ruby app.rb
```

如果连接成功，控制台将输出 TiDB 集群的版本，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和如何运行它，请查看 [tidb-samples/tidb-ruby-mysql2-quickstart](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart) 仓库。

### 使用连接选项连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```ruby
require 'dotenv/load'
require 'mysql2'
Dotenv.load # 从 .env 文件加载环境变量

options = {
  host: ENV['DATABASE_HOST'] || '127.0.0.1',
  port: ENV['DATABASE_PORT'] || 4000,
  username: ENV['DATABASE_USER'] || 'root',
  password: ENV['DATABASE_PASSWORD'] || '',
  database: ENV['DATABASE_NAME'] || 'test'
}
options.merge(ssl_mode: :verify_identity) unless ENV['DATABASE_ENABLE_SSL'] == 'false'
options.merge(sslca: ENV['DATABASE_SSL_CA']) if ENV['DATABASE_SSL_CA']
client = Mysql2::Client.new(options)
```

> **注意**
>
> 对于 TiDB Cloud Serverless，使用公共端点时，您**必须**通过 `DATABASE_ENABLE_SSL` 启用 TLS 连接，但您**不需要**通过 `DATABASE_SSL_CA` 指定 SSL CA 证书，因为 mysql2 gem 会按特定顺序搜索现有的 CA 证书，直到找到一个文件。

### 插入数据

以下查询创建一个具有两个字段的玩家，并返回 `last_insert_id`：

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询通过 ID 返回特定玩家的记录：

```ruby
def get_player_by_id(client, id)
  result = client.query(
    "SELECT id, coins, goods FROM players WHERE id = #{id};"
  )
  result.first
end
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询通过 ID 更新特定玩家的记录：

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

更多信息，请参见[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除特定玩家的记录：

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，mysql2 gem 可以按特定顺序搜索现有的 CA 证书，直到找到一个文件。

1. `/etc/ssl/certs/ca-certificates.crt` 用于 Debian、Ubuntu、Gentoo、Arch 或 Slackware
2. `/etc/pki/tls/certs/ca-bundle.crt` 用于 RedHat、Fedora、CentOS、Mageia、Vercel 或 Netlify
3. `/etc/ssl/ca-bundle.pem` 用于 OpenSUSE
4. `/etc/ssl/cert.pem` 用于 macOS 或 Alpine（docker 容器）

虽然可以手动指定 CA 证书路径，但在多环境部署场景中这样做可能会带来很大的不便，因为不同的机器和环境可能会将 CA 证书存储在不同的位置。因此，建议将 `sslca` 设置为 `nil`，以便在不同环境中灵活且易于部署。

## 下一步

- 从 [mysql2 文档](https://github.com/brianmario/mysql2#readme)了解更多 mysql2 驱动程序的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
