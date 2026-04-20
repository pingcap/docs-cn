---
title: 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB
summary: 本文描述了 TiDB 和 Rails 框架的连接步骤，并给出了使用 Rails 框架和 ActiveRecord ORM 连接 TiDB 的简单示例代码片段。
---

# 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[Rails](https://github.com/rails/rails) 是用 Ruby 编写的流行的 Web 框架，而 [ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord) 是 Rails 中的对象关系映工具。

本文档将展示如何使用 TiDB 和 Rails 来完成以下任务：

- 设置你的环境。
- 使用 Rails 连接你的 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意：**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 以及本地部署的 TiDB。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [Ruby](https://www.ruby-lang.org/en/) 3.0 或以上版本。
- 在你的机器上安装 [Bundler](https://bundler.io/)。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

如果你还没有 TiDB 集群，可以按照以下方式创建：

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行示例应用程序并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

在你的终端窗口中运行以下命令，将示例代码仓库克隆到本地：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 `mysql2` 和 `dotenv` 依赖包）：

```shell
bundle install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于你的现有项目，运行以下命令以安装这些包：

```shell
bundle add mysql2 dotenv
```

</details>

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你的目标集群的名称，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 在连接对话框中，从 **Connect With** 下拉列表中选择 `Rails`，并保持 **Endpoint Type** 的默认设置为 `Public`。

4. 如果你还没有设置密码，点击 **Create password** 生成一个随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照以下方式设置 `DATABASE_URL` 环境变量，并将占位符 `{}` 替换为连接对话框中相应的连接参数：

    ```dotenv
    DATABASE_URL=mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity
    ```

   > **注意**
   >
   > 对于 TiDB Serverless，当使用 Public Endpoint 时，必须使用 `ssl_mode=verify_identity` 查询参数启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你的目标集群的名称，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 在对话框中点击 **Allow Access from Anywhere**，然后点击 **Download CA cert** 下载 TiDB Cloud 提供的 CA 证书。

   更多配置细节，可参考 [TiDB Dedicated 标准连接教程（英文）](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照以下方式设置 `DATABASE_URL` 环境变量，将占位符 `{}` 替换为连接对话框中相应的连接参数，并将 `sslca` 查询参数设置为从连接对话框下载的 CA 证书的文件路径：

    ```dotenv
    DATABASE_URL=mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem
    ```

   > **注意**
   >
   > 当使用 Public Endpoint 连接到 TiDB Dedicated 集群时，建议启用 TLS 连接。
   >
   > 要启用 TLS 连接，请将 `ssl_mode` 查询参数的值修改为 `verify_identity`，并将 `sslca` 的值设置为从连接对话框下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>
<div label="本地部署的 TiDB">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照以下方式设置 `DATABASE_URL` 环境变量，并将 `{user}`、`{password}`、`{host}`、`{port}` 和 `{database}` 替换为你自己的 TiDB 连接信息：

    ```dotenv
    DATABASE_URL=mysql2://{user}:{password}@{host}:{port}/{database}
    ```

   如果你在本地运行 TiDB，那么默认的主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 4 步：运行代码并查看结果

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

如果连接成功，你的终端将会输出所连接集群的版本信息：

```
🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v7.1.0)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart)。

### 连接到 TiDB

`config/database.yml` 中的以下代码使用 `DATABASE_URL` 系统变量的配置连接到 TiDB：

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
> 对于 TiDB Serverless，当使用 Public Endpoint 时，**必须**通过在 `DATABASE_URL` 中设置 `ssl_mode` 查询参数为 `verify_identity` 来启用 TLS 连接，但是你**不需要**通过 `DATABASE_URL` 指定 SSL CA 证书，因为 mysql2 gem 会按照特定的顺序搜索现有的 CA 证书，直到找到相应的文件。

### 插入数据

以下查询创建了一个具有两个字段的 Player，并返回创建的 `Player` 对象：

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下通过 ID 查询返回特定 `Player` 的记录：

```ruby
player = Player.find_by(id: new_player.id)
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询更新特定 `Player` 对象：

```ruby
player.update(coins: 50, goods: 50)
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除特定 `Player` 对象：

```ruby
player.destroy
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，mysql2 gem 可以按照特定的顺序搜索现有的 CA 证书，直到找到相应的文件。

1. 对于 Debian、Ubuntu、Gentoo、Arch 或 Slackware，证书的默认存储路径为 `/etc/ssl/certs/ca-certificates.crt`。
2. 对于 RedHat、Fedora、CentOS、Mageia、Vercel 或 Netlify，证书的默认存储路径为 `/etc/pki/tls/certs/ca-bundle.crt`。
3. 对于 OpenSUSE，证书的默认存储路径为 `/etc/ssl/ca-bundle.pem`。
4. 对于 macOS 或 Alpine（docker 容器），证书的默认存储路径为 `/etc/ssl/cert.pem`。

尽管可以手动指定 CA 证书路径，但在多环境部署场景中这可能会引起不必要的麻烦，因为不同的机器和环境可能存储 CA 证书的位置不同。因此，建议将 `sslca` 设置为 `nil`，方便在不同环境中灵活且方便地部署。

## 下一步

- 从 [ActiveRecord 文档](https://guides.rubyonrails.org/active_record_basics.html)中了解更多关于 ActiveRecord ORM 的用法。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://pingkai.cn/learn)支持，并在考试后提供相应的[资格认证](https://learn.pingkai.cn/learner/certification-center)。

## 需要帮助？

在 [AskTUG](https://pingkai.cn/tidbcommunity/forum/) 论坛上提问。