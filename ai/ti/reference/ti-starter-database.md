---
title: TiDB Cloud Starter CLI 命令参考
summary: 参考适用于 Starter 实例、分支、SQL 用户、连接字符串和 SQL 执行的每个 `ti db` 命令。
---

# TiDB Cloud Starter CLI 命令参考

使用 `ti db` 管理 TiDB Cloud Starter 实例、分支和 SQL 访问。当目标不是 TiDB Cloud Starter 实例，或者无法验证其服务计划时，CLI 会拒绝执行实例作用域的操作。

分支是一个独立的 TiDB Cloud Starter 实例，包含其父实例数据的一个分叉副本。你可以使用分支在隔离环境中测试变更，而不会影响父实例。更多信息，请参阅 [TiDB Cloud Branching](https://docs.pingcap.com/tidbcloud/branch-overview)。

## 命令 {#commands}

| 命令 | 描述 |
|---|---|
| [`create-db-cluster`](/ai/ti/reference/ti-db-create-db-cluster.md) | 创建一个 TiDB Cloud Starter 实例。 |
| [`list-db-clusters`](/ai/ti/reference/ti-db-list-db-clusters.md) | 列出当前生效 Region 中的 Starter 实例。 |
| [`describe-db-cluster`](/ai/ti/reference/ti-db-describe-db-cluster.md) | 描述一个 TiDB Cloud Starter 实例。 |
| [`update-db-cluster`](/ai/ti/reference/ti-db-update-db-cluster.md) | 修改一个 TiDB Cloud Starter 实例。 |
| [`delete-db-cluster`](/ai/ti/reference/ti-db-delete-db-cluster.md) | 删除一个 TiDB Cloud Starter 实例。 |
| [`create-db-cluster-branch`](/ai/ti/reference/ti-db-create-db-cluster-branch.md) | 为 TiDB Cloud Starter 实例创建一个分支。 |
| [`list-db-cluster-branches`](/ai/ti/reference/ti-db-list-db-cluster-branches.md) | 列出 TiDB Cloud Starter 实例的分支。 |
| [`describe-db-cluster-branch`](/ai/ti/reference/ti-db-describe-db-cluster-branch.md) | 描述 TiDB Cloud Starter 实例的一个分支。 |
| [`delete-db-cluster-branch`](/ai/ti/reference/ti-db-delete-db-cluster-branch.md) | 从 TiDB Cloud Starter 实例中删除一个分支。 |
| [`create-db-sql-users`](/ai/ti/reference/ti-db-create-db-sql-users.md) | 创建或修复基于角色的 SQL 用户。 |
| [`format-db-connection-string`](/ai/ti/reference/ti-db-format-db-connection-string.md) | 将已存储的 SQL 凭据格式化为连接字符串。 |
| [`execute-sql-statement`](/ai/ti/reference/ti-db-execute-sql-statement.md) | 执行一条 SQL 语句。 |

## 另请参阅 {#see-also}

- [管理 TiDB Cloud Starter 实例](/ai/ti/guides/manage-starter-instances.md)
- [使用显式 SQL 角色查询 TiDB Cloud Starter](/ai/ti/guides/ti-query-sql-with-roles-example.md)