---
title: 使用 tdc 管理 TiDB Cloud Starter 数据库
summary: 管理 Starter 集群和分支、创建 SQL 用户、格式化连接字符串，并使用显式角色执行 SQL。
---

# 使用 tdc 管理 TiDB Cloud Starter 数据库

使用 `tdc db` 管理 TiDB Cloud Starter 集群、分支和 SQL 访问。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

- 使用 `tdc configure` 配置 tdc。
- 确保 API key 能管理所选 project 中的 Starter 集群。
- 自动化使用合成且唯一的名称，使清理过程只识别本次运行创建的资源。

## 管理集群

预览并创建 Starter 集群：

```bash
tdc db create-db-cluster \
  --db-cluster-name demo-cluster \
  --db-cluster-type starter \
  --dry-run

tdc db create-db-cluster \
  --db-cluster-name demo-cluster \
  --db-cluster-type starter
```

除非提供 `--project-id`，否则使用已配置的 virtual project。`--monthly-spending-limit-usd-cents` 是可选项；设置该值可能要求配置 payment method。

列出和筛选集群：

```bash
tdc db list-db-clusters
tdc db list-db-clusters --page-size 20 --order-by "createTime desc"
tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
```

List 命令还支持 `--page-token`、`--filter` 和 `--skip`。

查看和更新集群：

```bash
tdc db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --view FULL

tdc db update-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-name demo-cluster-renamed
```

Update 必须包含新名称或 spending limit。使用 `--dry-run` 预览 mutating command。

删除集群：

```bash
tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run

tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>"
```

tdc 会在内部解析集群名称，无需名称确认 flag。

## 管理分支

创建并列出分支：

```bash
tdc db create-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-name development

tdc db list-db-cluster-branches \
  --db-cluster-id "<cluster-id>" \
  --page-size 20
```

使用 `--page-token` 继续读取分页 branch list。

查看并删除分支：

```bash
tdc db describe-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>" \
  --view FULL

tdc db delete-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>"
```

Create 和 delete 支持 `--dry-run`。

## 创建 SQL 用户

创建或修复三个 tdc 管理的 SQL 角色：

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

该操作可重入。它复用稳定的角色名，并将生成的凭证保存到 `~/.tdc/db_users/<cluster-id>/credentials`：

- `read_only`；
- `read_write`；
- `admin`。

不修改用户地预览操作：

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

## 格式化连接字符串

默认角色是 read-write，但建议显式选择：

```bash
tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --format mysql-uri

tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --format env \
  --env-prefix TIDB_

tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --format jdbc
```

支持 `mysql-uri`、`jdbc`、`go-sql-driver`、`sqlalchemy` 和 `env` 格式。对于 `env`，`--env-include-database-url` 添加 URL 变量，`--env-database-url-name` 修改变量名。

> **警告：**
>
> 连接字符串包含凭证。不要将其写入日志、ticket 或 source control。

## 执行 SQL

每次调用只接受一条 SQL statement。请使用显式角色：

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database app \
  --sql "SELECT COUNT(*) AS row_count FROM messages" \
  --output text

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello')"

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS app"
```

默认 `--transport https` 通过 HTTPS 发送 SQL 请求，不保留数据库连接。`--transport mysql` 是显式兼容回退；它会为当前命令建立连接并在完成后关闭。

## 命令汇总

| 命令 | 用途 |
| --- | --- |
| `create-db-cluster` | 创建 Starter 集群 |
| `list-db-clusters` | 列出 Starter 集群 |
| `describe-db-cluster` | 读取单个集群 |
| `update-db-cluster` | 修改集群名称或 spending limit |
| `delete-db-cluster` | 删除集群 |
| `create-db-cluster-branch` | 创建分支 |
| `list-db-cluster-branches` | 列出分支 |
| `describe-db-cluster-branch` | 读取单个分支 |
| `delete-db-cluster-branch` | 删除分支 |
| `create-db-sql-users` | 创建或修复三个 SQL 角色 |
| `format-db-connection-string` | 格式化已准备的凭证 |
| `execute-sql-statement` | 执行一条 SQL statement |

## 后续步骤

- [使用显式角色查询 SQL](/ai/tdc/examples/tdc-query-sql-with-roles-example.md)
- [tdc CLI 参考](/ai/tdc/reference/tdc-cli-reference.md)
- [tdc 故障排查](/ai/tdc/reference/tdc-troubleshooting.md)
