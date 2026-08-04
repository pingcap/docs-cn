---
title: DM-worker 简介
aliases: ['/docs-cn/tidb-data-migration/dev/dm-worker-intro/']
summary: DM-worker 是 DM (Data Migration) 的一个组件，负责执行数据迁移任务。主要功能包括注册为 MySQL 或 MariaDB 服务器的 slave，读取 binlog event 并持久化保存在本地，支持迁移一个 MySQL 或 MariaDB 实例的数据到多个 TiDB 实例，以及支持迁移多个 MySQL 或 MariaDB 实例的数据到一个 TiDB 实例。处理单元包括 Relay log、dump、load 和 Binlog replication/sync。上游数据库用户需具有 SELECT、RELOAD、REPLICATION SLAVE 和 REPLICATION CLIENT 权限，下游数据库用户需具有 SELECT、INSERT、UPDATE、DELETE、CREATE、DROP 和 INDEX 权限。处理单元所需的最小权限根据具体情况可能会改变。
---

# DM-worker 简介

DM-worker 是 TiDB Data Migration (DM) 的一个组件，负责执行 DM-master 分配的任务和子任务。对于全量和增量迁移，它会从一个兼容 MySQL 的上游源实例导出数据，并将导出的数据加载到目标 TiDB 集群中。随后，它作为复制客户端读取上游 binlog，对事件进行转换和过滤，并将其应用到目标端。DM-master 会向 DM-worker 查询数据源和子任务状态。

## 关键概念

- 如果某个 worker 实例离线，DM-master 可以自动将其任务重新调度到另一个可用 worker 上，以恢复数据复制。注意，这不适用于全量导出/导入阶段。
- 单个 DM-worker 进程一次只能连接到**一个**上游源数据库实例。要从多个数据源迁移数据，例如合并分表时，必须运行多个 DM-worker 进程。

> **注意：**
>
> DM-worker 是一个兼容 MySQL 的 binlog 客户端，而不是备用数据库副本服务器。它从兼容 MySQL 的数据源读取并重放数据到 TiDB 目标端。要从源 TiDB 集群复制数据，请使用 [TiCDC](/ticdc/ticdc-overview.md)。

## DM-worker 处理单元

根据任务模式的不同，DM-worker 子任务会运行 dump、load 和 binlog replication 处理单元。DM-worker 还可以为其绑定的数据源运行可选的 relay log 处理单元。

### Relay 日志

Relay log 是可选功能，默认关闭。启用后，DM-worker 会先将上游 binlog event 存储到本地磁盘，然后 binlog replication 处理单元再读取这些 event。当长时间的全量迁移或阻塞任务可能持续超过上游 binlog 保留时间，或者同一数据源的多个任务需要复用同一条 binlog 流时，建议启用 relay log。relay log 会消耗磁盘、I/O 和 CPU 资源，并可能增加复制延时。有关配置和运维细节，请参见 [DM relay log](/dm/relay-log.md)。

### dump 处理单元

dump 处理单元从上游 MySQL 或 MariaDB 导出全量数据到本地磁盘。

### load 处理单元

load 处理单元读取 dump 处理单元导出的数据文件，然后加载到下游 TiDB。

### Binlog replication/sync 处理单元

Binlog replication/sync 处理单元读取上游 MySQL/MariaDB 的 binlog event 或 relay log 处理单元的 binlog event，将这些 event 转化为 SQL 语句，再将这些 SQL 语句应用到下游 TiDB。

## DM-worker 所需权限

本小节主要介绍使用 DM-worker 时所需的上下游数据库用户权限以及各处理单元所需的用户权限。

### 上游数据库用户权限

上游数据库用户所需的权限取决于数据库类型（MySQL/MariaDB）和版本。

> **注意：**
>
> - 如果从托管型 MySQL 服务（例如 Amazon RDS、Aurora、ApsaraDB RDS for MySQL、Azure Database for MySQL 或 Google Cloud SQL）迁移数据，且该服务不允许执行 `FLUSH TABLES WITH READ LOCK` (FTWRL)，还需要授予 `LOCK TABLES` 权限。使用默认的 `consistency=auto` 设置时，如果 FTWRL 不可用，DM 会回退到 `LOCK TABLES`。
>
>     ```sql
>     GRANT LOCK TABLES ON db1.* TO 'your_user'@'your_wildcard_of_host';
>     ```
>
> - 如果还需要将其他数据库的数据迁移到 TiDB，请确保已向相应数据库的用户授予相同的权限。

#### MySQL 和 MariaDB（MariaDB 10.5.2 之前）

对于 MySQL，以及早于 10.5.2 的 MariaDB 版本，用户必须具有以下权限：

| 权限 | 作用域 |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

要授予这些权限，请执行以下语句：

```sql
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

对于从早于 10.5.2 的 MariaDB 执行全量数据导出，还需要授予 `PROCESS`，以便 dump 处理单元可以查询 InnoDB 元信息：

```sql
GRANT PROCESS ON *.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.2 到 10.5.8

从 [MariaDB 10.5.2](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.2) 开始，`REPLICATION CLIENT` 权限被重命名为 `BINLOG MONITOR`，并且多个复制语句使用了通过切分 `SUPER` 而新建的权限。对于 MariaDB 10.5.2 到 10.5.8，用户必须具有以下权限：

| 权限 | 作用域 | 说明 |
|:---|:---|:---|
| `SELECT` | Tables | 全量数据导出所需。 |
| `PROCESS` | Global | 全量数据导出期间查询 InnoDB 元信息所需。 |
| `RELOAD` | Global | `FLUSH TABLES WITH READ LOCK` 所需。 |
| `BINLOG MONITOR` | Global | 由 `REPLICATION CLIENT` 重命名而来；允许监控 binlog。 |
| `REPLICATION SLAVE` | Global | 允许读取 binlog event。 |
| `REPLICATION SLAVE ADMIN` | Global | 允许管理复制状态（例如 `SHOW SLAVE STATUS`）。 |
| `REPLICATION MASTER ADMIN`| Global | 允许监控主库（例如 `SHOW SLAVE HOSTS`）。 |

要授予这些权限，请执行以下语句：

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.9 或更高版本

从 [MariaDB 10.5.9](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.9) 开始，`SHOW SLAVE STATUS` 和 `SHOW REPLICA STATUS` 需要 `REPLICA MONITOR` 权限。MariaDB 在 `SHOW GRANTS` 中将此权限显示为 `SLAVE MONITOR`。请授予 MariaDB 10.5.2 到 10.5.8 中列出的权限，并额外授予 `REPLICA MONITOR`：

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN, REPLICA MONITOR ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

> **注意：**
>
> 由于 MariaDB 报告这些权限的方式与 MySQL 不同，即使账户已具备所需权限，`dmctl check-task` 也可能报告权限错误。
>
> 对于 DM v8.5.6，如果前置检查在复制权限、dump 权限或 dump 连接数检查中返回 `[code=26005] fail to check synchronization configuration`，请仅将以下内容添加到任务配置文件中：
>
> ```yaml
> ignore-checking-items:
>   - replication_privilege
>   - dump_privilege
>   - conn_number
> ```
>
> 此变通方法仅跳过受 MariaDB 权限解析器影响的这三项检查。使用前，请手动验证相应权限和连接数限制。更多信息，请参见 [DM precheck](/dm/dm-precheck.md)。

> **注意：**
>
> 在某些较旧的 MariaDB 版本中，`PROCESS` 对于 dump 处理单元查询 InnoDB 元信息来说并不充分。在 DM v8.5.6 中，当 dump 处理单元在 MariaDB 10.4.34 上查询 `INNODB_TABLESPACES_SCRUBBING`，或在 MariaDB 10.5.1 和 10.5.2 上查询 `INNODB_TABLESPACES_ENCRYPTION` 时，会出现此行为。在相同的冒烟测试中，MariaDB 10.5.9、10.6.13 和 10.11.16 无需 `SUPER` 即可完成。如果 dump 处理单元返回 `Error 1227 (42000): Access denied; you need (at least one of) the SUPER privilege(s) for this operation`，请授予 `SUPER`。由于 `SUPER` 是一个范围较广的权限，因此仅当出现此确切错误且你的安全策略允许时才授予它。

### 下游数据库用户权限

下游数据库 (TiDB) 用户必须拥有以下权限：

| 权限 | 作用域 |
|:----|:----|
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE` | Tables |
| `DELETE` | Tables |
| `CREATE` | Databases，tables |
| `DROP` | Databases，tables |
| `ALTER` | Tables |
| `INDEX` | Tables |

对要执行迁移操作的数据库或表执行下面的 `GRANT` 语句：

{{< copyable "sql" >}}

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX  ON db.table TO 'your_user'@'your_wildcard_of_host';
GRANT ALL ON dm_meta.* TO 'your_user'@'your_wildcard_of_host';
```

### 处理单元所需的最小权限

下表列出了 MySQL 和早于 10.5.2 的 MariaDB 版本中，各处理单元所需的最小权限。对于 MariaDB 10.5.2 及更高版本，请参见前一节中的权限表。

| 处理单元 | 最小上游 (MySQL/MariaDB) 权限 | 最小下游 (TiDB) 权限 | 最小系统权限 |
|:----|:--------------------|:------------|:----|
| Relay log | `REPLICATION SLAVE` (读取 binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | 无 | 本地读/写磁盘 |
| Dump | `SELECT`<br/>`RELOAD` (`FLUSH TABLES WITH READ LOCK`)<br/>`PROCESS`（仅 MariaDB，用于查询 InnoDB 元信息） | 无 | 本地写磁盘 |
| Load | 无 | `SELECT`（查询 checkpoint 历史）<br/>`CREATE`（创建数据库或表）<br/>`DELETE`（删除 checkpoint）<br/>`INSERT`（插入 dump 数据）| 读/写本地文件 |
| Binlog replication | `REPLICATION SLAVE` (reads the binlog)<br/>`REPLICATION CLIENT` (`SHOW MASTER STATUS`, `SHOW SLAVE STATUS`) | `SELECT`（显示索引和列）<br/>`INSERT` (DML)<br/>`UPDATE` (DML)<br/>`DELETE` (DML)<br/>`CREATE`（创建数据库或表）<br/>`DROP`（删除数据库或表）<br/>`ALTER`（修改表）<br/>`INDEX`（创建或删除索引）| 本地读/写磁盘 |
