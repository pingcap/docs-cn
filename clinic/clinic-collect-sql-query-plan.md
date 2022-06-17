---
title: 使用 PingCAP Clinic 采集 SQL 查询计划相关信息
summary: 了解如何使用 PingCAP Clinic 采集 TiUP 部署集群的 SQL 查询计划相关信息。
---

# 使用 PingCAP Clinic 采集 SQL 查询计划相关信息

TiDB 在 v5.3.0 中引入了 [`PLAN REPLAYER`](/sql-plan-replayer.md) 功能，能够一键式导入或导出重现查询计划相关的信息。`PLAN REPLAYER` 提供了足够简单、一站式获取并保留线上事故场景的功能，简化了优化器相关问题的排查信息提取步骤。

## 使用说明

Clinic Diag 诊断客户端（下称 Diag）集成了 `PLAN REPLAYER` 功能，支持 TiDB v4.0 以上的集群。你可以使用 Diag 方便快捷地保存查询计划相关的数据。

> **警告：**
>
> - 当前该功能为实验特性，不建议在生产环境中使用。
> - 暂时不支持采集 TiDB Operator 部署集群的数据。

- 导出排查现场 TiDB 集群的相关信息，导出为 ZIP 格式的文件用于保存。
- Diag 中采集的数据与 TiDB 中 `PLAN REPLAYER` 功能采集的数据有少量差距，具体见[采集输出结果](#采集输出结果)。
- 方便快速地将采集的数据上传到 PingCAP Clinic，供技术支持人员查看。

## 使用方法

### 安装 Diag

- 通过 TiUP 一键安装 Diag，默认安装最新版本：

    ```bash
    tiup install diag
    ```

- 若已安装 Diag，请确保 Diag 版本 >= **0.7.3**。

    你可以通过如下命令检查 Diag 版本：

    ```bash
    tiup diag --version
    ```

    如果 Diag 版本不满足要求，可以通过如下命令升级到最新版本：

    ```bash
    tiup update diag
    ```

### 快速采集数据

执行如下 `diag collect` 命令进行数据采集：

```bash
diag collect <clustername> --profile=tidb-plan-replayer --explain-sql=<statementfilepath>
```

> **注意：**
>
> - 通过 `diag` 采集数据，用户需要提供 `sql-statement` 文件，该文件包含了需要采集的 SQL 语句。
> - `statementfilepath` 是指 `sql-statement` 文件的路径。
> - `PLAN REPLAYER` **不会**导出表中数据。
> - 采集数据时只会执行 EXPLAIN，不会真正执行查询，因此采集时对数据库性能影响较小。

`sql-statement` 的文件内容示例：

```sql
SELECT * FROM information_schema.slow_query;SELECT * FROM information_schema.statements_summary
```

`sql-statement` 的文件内容说明：

- 如果有多条 SQL 语句需要分析，可以使用分号（;）分隔。
- 因为 `diag` 都是新建会话进行查询，所以 SQL 文件里的 SQL 语句需要指明所使用的数据库。

#### 采集输出结果

采集输出结果包含以下集群现场信息：

| 序号 | 采集内容 | 调用的 Diag collector | 输出文件 |
| :--- | :--- | :--- | :--- |
| 1 | TiDB 配置信息 | `config` | `tidb.toml` |
| 2 | TiDB Session 系统变量 | `db_vars` | `global_variables.csv`，`mysql.tidb.csv` |
| 3 | TiDB 执行计划绑定信息 (SQL Binding) | `sql_bind` | `sql_bind/global_bind.csv` |
| 4 | `sql-statement` 中所包含的表结构 | `statistics` | `statistics/<db.table>.schema` |
| 5 | `sql-statement` 中所包含表的统计信息 | `statistics` | `statistics/<db.table>.json` |
| 6 | EXPLAIN `sql-statement` 的结果 | `explain` | `explain/sql0` |
| 7 | <ul><li>TiDB 日志</li><li>TiUP Cluster 操作日志</li></ul> | <ul><li>`log`</li><li>`-R=tidb`</li></ul> | `tidb.log`，`tidb_slow_query.log`，`tidb_stdeer.log`，`cluster_audit/$auditfilename` |
| 8 | 默认采集的集群信息<ul><li>集群基础信息</li><li>Diag 本次采集记录</li></ul> | default | `cluster.json`，`meta.yaml`，`$collectid_diag_audit.log` |

### 自定义采集

你可以创建自定义的 profile 文件采集上述[输出结果](#采集输出结果)中的部分数据。下面为一个示例的 profile 文件 `tidb-plan-replayer.toml`：

```toml
name = "tidb-plan-replayer"
version = "0.0.1"
maintainers = [
    "pingcap"
]

# list of data types to collect
collectors = [
    "log",
    "config",
    "db_vars",
    "sql_bind",
    "statistics",
    "explain"
]

# list of component roles to collect
roles = [
    "tidb"
]
```

进行自定义采集，你需要通过 `--profile` 参数指定 profile 文件的路径：

```bash
diag collect <clustername> --profile=<profilefilepath> --explain-sql=<statementfilepath>
```
