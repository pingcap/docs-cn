---
title: 使用 PingCAP Clinic Diag 采集 SQL 查询计划信息
summary: 了解如何使用 PingCAP Clinic Diag 采集 TiUP 部署集群的 SQL 查询计划信息。
---

# 使用 PingCAP Clinic Diag 采集 SQL 查询计划信息

TiDB 在 v5.3.0 中引入了 [`PLAN REPLAYER`](/sql-plan-replayer.md) 命令，能够快速保存和恢复查询计划相关的信息，简化了排查优化器相关问题时提取排查信息的步骤。[Clinic Diag 诊断客户端](https://github.com/pingcap/diag)（下称 Diag）集成了 `PLAN REPLAYER` 功能，你可以使用 Diag 方便快捷地保存查询计划相关的数据。

## 使用说明

在排查 TiDB v4.0 及以上版本的集群问题时，你可以使用 Diag 将排查现场的相关数据以 ZIP 格式导出，并将导出的数据快速上传到 PingCAP Clinic 供技术支持人员查看。在使用 Diag 采集数据前，你需要提供需要采集的 SQL 语句文件。Diag 采集的数据相较于 TiDB 中 `PLAN REPLAYER` 功能采集的数据多了日志信息和集群信息，具体见[全量数据采集的输出结果](#输出结果)。

> **警告：**
>
> - 当前该功能为实验特性，不建议在生产环境中使用。
> - 暂时不支持采集使用 TiDB Operator 部署的 TiDB 集群的数据。

## 使用方法

本部分介绍如何使用 Diag 采集 SQL 查询计划信息。你需要先安装 Diag，再使用 Diag 采集数据。

### 安装 Diag

- 通过 TiUP 安装 Diag，默认安装最新版本：

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

### 全量数据采集

使用如下 `diag collect` 命令进行数据采集。你需要将 `<cluster-name>` 和 `<statement-filepath>` 占位符替换为实际的值：

```bash
diag collect <cluster-name> --profile=tidb-plan-replayer --explain-sql=<statement-filepath>
```

> **注意：**
>
> - 通过 `diag` 采集数据前，你需要通过 `--explain-sql` 指定 `sql-statement` 文件：
>
>     - 以上命令中 `<statement-filepath>` 是指 `sql-statement` 文件的路径。
>     - 该文件包含了需要采集的 SQL 语句。
>     - 如果有多条 SQL 语句需要分析，可以使用分号 `;` 分隔。
>     - 因为以上 `diag` 命令会新建会话进行查询，所以 SQL 文件里的 SQL 语句必须显示指明所使用的数据库，如 `SELECT * FROM test.t1`。
>
> - `PLAN REPLAYER` **不会**导出表中数据。
> - 采集数据时只会执行 `EXPLAIN`，不会真正执行查询。因此采集时对数据库性能影响较小。

`sql-statement` 的文件内容示例：

```sql
SELECT * FROM test.t1;SELECT * FROM test.t2;
```

`--explain-sql` 指定的 `sql-statement` 文件内容说明：

- 如果有多条 SQL 语句需要分析，可以使用分号 `;` 分隔。
- 因为以上 `diag` 命令会新建会话进行查询，所以 SQL 文件里的 SQL 语句必须显示指明所使用的数据库，如 `SELECT * FROM test.t1`。

#### 输出结果

全量数据采集的输出结果包含以下集群现场信息：

| 序号 | 采集内容 | 调用的 Diag collector | 输出文件 |
| :--- | :--- | :--- | :--- |
| 1 | TiDB 配置信息 | `config` | `tidb.toml` |
| 2 | TiDB Session 系统变量 | `plan_replayer` | `plan_replayer.zip/variables.toml` |
| 3 | TiDB 执行计划绑定信息 (SQL Binding) | `sql_bind` | `sql_bind/global_bind.csv` |
| 4 | `sql-statement` 中所包含的表结构 | `plan_replayer` | `plan_replayer.zip/schema/<db.table>.schema.txt` |
| 5 | `sql-statement` 中所包含表的统计信息 | `plan_replayer` | `plan_replayer.zip/stats/<db.table>.json` |
| 6 | `EXPLAIN sql-statement` 的结果 | `explain` | `explain/sql0` |
| 7 | 默认采集的集群信息<ul><li>集群基础信息</li><li>Diag 本次采集记录</li></ul> | default | `cluster.json`，`meta.yaml`，`$collectid_diag_audit.log` |

### 自定义数据采集

你可以自定义配置文件使 Diag 采集上述[输出结果](#输出结果)中的部分数据。下面为一个示例的配置文件 `tidb-plan-replayer.toml`：

```toml
name = "tidb-plan-replayer"
version = "0.0.1"
maintainers = [
    "pingcap"
]

# 要采集的数据类型
collectors = [
    "config",
    "sql_bind",
    "plan_replayer"
]

# 要采集的组件
roles = [
    "tidb"
]
```

通过 `--profile` 参数指定配置文件的路径来进行自定义采集。你需要将 `<cluster-name>`、`<profile-filepath>` 和 `<statement-filepath>` 替换为实际的值：

```bash
diag collect <cluster-name> --profile=<profile-filepath> --explain-sql=<statement-filepath>
```

### 将结果导入到 TiDB 集群

采集结果中的 `plan_replayer.zip` 可以通过 `PLAN REPLAYER LOAD` 语句直接导入到 TiDB 集群中进行信息查看，具体方法可参考[使用 `PLAN REPLAYER` 导入集群信息](/sql-plan-replayer.md#使用-plan-replayer-导入集群信息)
