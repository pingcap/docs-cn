---
title: 将 TiDB Cloud 与 New Relic 集成（Beta）
summary: 了解如何使用 New Relic 集成监控您的 TiDB 集群。
---

# 将 TiDB Cloud 与 New Relic 集成（Beta）

TiDB Cloud 支持 New Relic 集成（beta）。您可以配置 TiDB Cloud 将 TiDB 集群的指标数据发送到 [New Relic](https://newrelic.com/)。之后，您可以直接在 New Relic 仪表板中查看这些指标。

## 前提条件

- 要将 TiDB Cloud 与 New Relic 集成，您必须拥有 New Relic 账号和 [New Relic API 密钥](https://one.newrelic.com/admin-portal/api-keys/home?)。首次创建 New Relic 账号时，New Relic 会授予您一个 API 密钥。

    如果您没有 New Relic 账号，请在[此处](https://newrelic.com/signup)注册。

- 要编辑 TiDB Cloud 的第三方集成设置，您必须拥有组织的**组织所有者**访问权限或目标项目的**项目成员**访问权限。

## 限制

您不能在 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)中使用 New Relic 集成。

## 步骤

### 步骤 1. 与您的 New Relic API 密钥集成

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击**项目设置** > **集成**。
3. 在**集成**页面上，点击 **New Relic 集成（BETA）**。
4. 输入您的 New Relic API 密钥并选择 New Relic 的站点。
5. 点击**测试集成**。

    - 如果测试成功，将显示**确认**按钮。
    - 如果测试失败，将显示错误消息。按照消息进行故障排除并重试集成。

6. 点击**确认**完成集成。

### 步骤 2. 在 New Relic 中添加 TiDB Cloud 仪表板

1. 登录 [New Relic](https://one.newrelic.com/)。
2. 点击**添加数据**，搜索 `TiDB Cloud`，然后转到 **TiDB Cloud 监控**页面。或者，您可以点击[链接](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)直接访问该页面。
3. 选择您的账号 ID 并在 New Relic 中创建仪表板。

## 预构建仪表板

点击集成中 **New Relic** 卡片中的**仪表板**链接。您可以看到 TiDB 集群的预构建仪表板。

## New Relic 可用的指标

New Relic 跟踪您的 TiDB 集群的以下指标数据。

| 指标名称  | 指标类型 | 标签 | 描述                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | TiDB 中运行的所有 SQL 语句每秒消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间。 |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 所有 TiDB 实例每秒执行的 SQL 语句数量，按 `SELECT`、`INSERT`、`UPDATE` 等类型的语句计数。 |
| tidb_cloud.db_average_query_duration| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 从客户端的网络请求发送到 TiDB 到 TiDB 执行后将请求返回给客户端的时间间隔。 |
| tidb_cloud.db_failed_queries| gauge | type: executor:xxxx\|parser:xxxx\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 根据每个 TiDB 实例每秒发生的 SQL 执行错误（如语法错误和主键冲突）统计的错误类型。 |
| tidb_cloud.db_total_connection| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | TiDB 服务器中的当前连接数。 |
| tidb_cloud.db_active_connections| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 活动连接数。 |
| tidb_cloud.db_disconnections| gauge | result: ok\|error\|undetermined<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 断开连接的客户端数量。 |
| tidb_cloud.db_command_per_second| gauge | type: Query\|StmtPrepare\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | TiDB 每秒处理的命令数量，根据命令执行结果的成功或失败进行分类。 |
| tidb_cloud.db_queries_using_plan_cache_ops| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒使用[执行计划缓存](/sql-prepared-plan-cache.md)的查询统计。执行计划缓存仅支持预处理语句命令。 |
| tidb_cloud.db_transaction_per_second| gauge | txn_mode: pessimistic\|optimistic<br/><br/>type: abort\|commit\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒执行的事务数。 |
| tidb_cloud.node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘使用量，以字节为单位。 |
| tidb_cloud.node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘容量，以字节为单位。 |
| tidb_cloud.node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 使用率。 |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 核心限制。 |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的已用内存，以字节为单位。 |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的内存容量，以字节为单位。 |
