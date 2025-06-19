---
title: 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB
summary: 学习如何使用 Rails 框架连接 TiDB。本教程提供使用 Rails 框架和 ActiveRecord ORM 操作 TiDB 的 Ruby 示例代码片段。
---

# 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[Rails](https://github.com/rails/rails) 是一个用 Ruby 编写的流行 Web 应用框架，[ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord) 是 Rails 中的对象关系映射工具。

在本教程中，你将学习如何使用 TiDB 和 Rails 完成以下任务：

- 设置开发环境
- 使用 Rails 连接到 TiDB 集群
- 构建并运行应用程序。你还可以找到使用 ActiveRecord ORM 进行基本 CRUD 操作的[示例代码片段](#sample-code-snippets)

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程需要：

- 在你的机器上安装 [Ruby](https://www.ruby-lang.org/en/) >= 3.0
- 在你的机器上安装 [Bundler](https://bundler.io/)
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 一个正在运行的 TiDB 集群

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 运行示例应用程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `mysql2` 和 `dotenv`）：

```shell
bundle install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于你的现有项目，运行以下命令安装包：

```shell
bundle add mysql2 dotenv
```

</details>

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群名称进入集群概览页面。

2. 点击右上角的**连接**按钮。将显示连接对话框。

3. 在连接对话框中，从**连接方式**下拉列表中选择 `Rails`，并保持**连接类型**的默认设置为`公共`。

4. 如果你还没有设置密码，点击**生成密码**生成随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，设置 `DATABASE_URL` 环境变量如下，并从连接对话框中复制连接字符串作为变量值：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity'
    ```

   > **注意**
   >
   > 对于 TiDB Cloud Serverless，使用公共端点时**必须**通过 `ssl_mode=verify_identity` 查询参数启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群名称进入集群概览页面。

2. 点击右上角的**连接**按钮。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果你还没有配置 IP 访问列表，在首次连接之前，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**专用端点**和 **VPC 对等连接**连接类型。更多信息，请参阅[连接到 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，设置 `DATABASE_URL` 环境变量如下，从连接对话框中复制连接字符串作为变量值，并将 `sslca` 查询参数设置为从连接对话框下载的 CA 证书的文件路径：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem'
    ```

   > **注意**
   >
   > 使用公共端点连接到 TiDB Cloud Dedicated 时，建议启用 TLS 连接。
   >
   > 要启用 TLS 连接，请将 `ssl_mode` 查询参数的值修改为 `verify_identity`，并将 `sslca` 的值修改为从连接对话框下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，设置 `DATABASE_URL` 环境变量如下，并将 `{user}`、`{password}`、`{host}`、`{port}` 和 `{database}` 替换为你自己的 TiDB 连接信息：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}'
    ```

   如果你在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并检查结果

1. 创建数据库和表：

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2. 填充示例数据：

    ```shell
    bundle exec rails db:seed
    ```

3. 运行以下命令执行示例代码：

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

如果连接成功，控制台将输出 TiDB 集群的版本信息如下：

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

你可以参考以下示例代码片段来完成自己的应用程序开发。

完整的示例代码和运行方法，请查看 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart) 仓库。

### 使用连接选项连接到 TiDB

以下 `config/database.yml` 中的代码使用环境变量中定义的选项建立与 TiDB 的连接：

```yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  url: <%= ENV["DATABASE_URL"] %>

development:
  <<: *default

test:
  <<: *default
  database: quickstart_test

production:
  <<: *default
```

> **注意**
>
> 对于 TiDB Cloud Serverless，使用公共端点时**必须**通过在 `DATABASE_URL` 中设置 `ssl_mode` 查询参数为 `verify_identity` 来启用 TLS 连接，但你**不需要**通过 `DATABASE_URL` 指定 SSL CA 证书，因为 mysql2 gem 会按特定顺序搜索现有的 CA 证书，直到找到一个文件。

### 插入数据

以下查询创建一个具有两个字段的 Player 并返回创建的 `Player` 对象：

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询通过 ID 返回特定玩家的记录：

```ruby
player = Player.find_by(id: new_player.id)
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询更新一个 `Player` 对象：

```ruby
player.update(coins: 50, goods: 50)
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除一个 `Player` 对象：

```ruby
player.destroy
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，mysql2 gem（由 ActiveRecord ORM 用于连接 TiDB）会按特定顺序搜索现有的 CA 证书，直到找到一个文件。

1. /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2. /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3. /etc/ssl/ca-bundle.pem # OpenSUSE
4. /etc/ssl/cert.pem # MacOS / Alpine (docker container)

虽然可以手动指定 CA 证书路径，但这种方法可能会在多环境部署场景中造成很大的不便，因为不同的机器和环境可能会将 CA 证书存储在不同的位置。因此，建议将 `sslca` 设置为 `nil`，以便在不同环境中灵活部署。

## 下一步

- 从 [ActiveRecord 文档](https://guides.rubyonrails.org/active_record_basics.html)中了解更多 ActiveRecord ORM 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
