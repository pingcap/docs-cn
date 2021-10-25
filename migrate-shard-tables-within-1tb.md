---
title: 使用 DM 进行分库分表合并迁移（ 1 TB以内）
summary: 介绍 使用 DM 进行分库分表合并迁移（ 1 TB以内）的操作步骤。
---

# 使用 DM 进行分库分表合并迁移（ 1 TB以内）

如果你想把上游多个 MySQL 数据库实例合并迁移到下游的同一个 TiDB 数据库中，且数据量不太大（比如所有分表的总和小于 1 TB），你可以使用 DM 工具进行分库分表的合并迁移。本文举例介绍了合并迁移的操作步骤、注意事项、故障排查等。

本文档适用于：

- TB 级以内的分库分表数据合并迁移
- 基于 MySQL binlog 的增量、持续分库分表合并迁移

若要迁移分表总和 1 TB 以上的数据，则 DM 工具耗时较长，可参考 [使用 Dumpling 和 TiDB Lightning 合并导入分表数据](/sync-diff-inspector/sync-diff-inspector-overview.md)。

## 迁移场景介绍

本文以一个简单的场景为例，示例中的两个数据源 MySQL 实例的分库和分表数据迁移至下游 TiDB 集群。示意图如下。

![使用 DM 进行分库分表合并迁移](/media/migrate-shard-tables-within-1tb.png)

假设两个数据源实例的 schema 和表结构如下：

数据源 MySQL 实例 1：

  | Schema | Tables |
  |:------|:------|
  | user  | information, log_bak |
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

数据源 MySQL 实例 2：

  | Schema | Tables |
  |:------|:------|
  | user  | information, log_bak |
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

迁移目标库的结构如下：

| Schema | Tables |
|:------|:------|
| user | information |
| store | sale |

## 前提条件

在开始迁移之前，请完成以下任务：

- 部署 DM 集群
- 上下游数据库权限
- 分表数据冲突检查
- 了解 DM 基本功能

### 部署 DM 集群

你可以通过多种方式部署 DM 集群。目前推荐使用 TiUP 部署 DM 集群。具体部署方法，请参考[使用 TiUP 部署 DM 集群](https://docs.pingcap.com/zh/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)。

### 上下游数据库权限

上下游数据库用户必须拥有相应的读写权限。关于权限要求的详情，请参考 [DM-worker 所需权限](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-worker-intro#dm-worker-%E6%89%80%E9%9C%80%E6%9D%83%E9%99%90)。

### 分表数据冲突检查

迁移中如果涉及合库合表，来自多张分表的数据可能引发主键或唯一索引的数据冲突。因此在迁移之前，需要检查各分表数据的业务特点。详情请参考[跨分表数据在主键或唯一索引冲突处理](https://docs.pingcap.com/zh/tidb-data-migration/stable/shard-merge-best-practices#%e8%b7%a8%e5%88%86%e8%a1%a8%e6%95%b0%e6%8d%ae%e5%9c%a8%e4%b8%bb%e9%94%ae%e6%88%96%e5%94%af%e4%b8%80%e7%b4%a2%e5%bc%95%e5%86%b2%e7%aa%81%e5%a4%84%e7%90%86)。

在本示例中：user.information 表结构如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE `information` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

其中 id 列为主键，uid 列为唯一索引。id 列具有自增属性，多个分表范围重复会引发数据冲突。 uid 可以保证全局满足唯一索引，因此可以按照参考[去掉自增主键的主键属性](https://docs.pingcap.com/zh/tidb-data-migration/stable/shard-merge-best-practices#%e5%8e%bb%e6%8e%89%e8%87%aa%e5%a2%9e%e4%b8%bb%e9%94%ae%e7%9a%84%e4%b8%bb%e9%94%ae%e5%b1%9e%e6%80%a7)中介绍的操作绕过 id 列。store_{01|02}.sale_{01|02} 的表结构如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE `sale_01` (
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

其中 sid 是分片键，可以保证同一个 sid 只会划分到一个分表中，因此不会引发数据冲突，无需进行额外操作。

### 了解 DM 基本功能

DM 提供了 [Table routing](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#table-routing)、[Block & Allow Table Lists](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#block--allow-table-lists)、[Binlog event filter](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#binlog-event-filter) 等基本功能，适用于不同的迁移场景。在迁移之前，建议先了解下这些基本功能，根据需求进行选择和配置。

#### Table routing

Table routing 可以将上游 MySQL/MariaDB 实例的某些表迁移到下游指定表。它也是分库分表合并迁移所需的一个核心功能。在分库分表合并迁移场景，假如需要将上游两个 MySQL 实例的表 store_{01|02}.sale_{01|02} 表合并至下游 TiDB 中的 store.sale 表，可以通过以下 table routing 规则实现：

```
routes:
  ...
  store-route-rule: #将上游的 store_{01|02} 迁移到下游的 store 中。
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule: #将上游的 store_{01|02}.sale_{01|02} 迁移到下游的 store.sale 中。
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"
```

更多详情，请参考 [Table routing](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#table-routing)。

#### Block & Allow Table Lists

上游数据库实例表的黑白名单过滤规则，可以用来过滤或者只迁移某些 database/table 的所有操作。更多详情，请参考 [Block & Allow Table Lists](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#block--allow-table-lists)。

#### Binlog event filter

Binlog event filter 是比迁移表黑白名单更加细粒度的过滤规则，可以指定只迁移或者过滤掉某些 
schema / table 的指定类型 binlog，比如 INSERT、TRUNCATE TABLE。更多详情，请参考 [Binlog event filter](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#binlog-event-filter)。

## 迁移方案

你可以根据实际需求，选择不同的迁移方案。下面举例介绍了几种常见的迁移需求和适用的方案。

### 场景一：上下游同名数据库合并迁移

user.information 需要合并到下游 TiDB 中的 user.information 表。要满足该迁移需求 ，无需配置 table routing 规则。按照去掉自增主键的主键属性的要求，在下游手动建表。

```sql
CREATE TABLE `information` (
  `id` bigint(20) NOT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

并在配置文件中跳过前置检查。

```
ignore-checking-items: ["auto_increment_ID"]
```

### 场景二：使用 Table routing 合并迁移

示例中的 store_{01|02}.sale_{01|02} 表合并至下游 TiDB 中的 store.sale 表。要满足该迁移需求 ，需要配置 table routing 规则 如下：

```
routes:
  store-route-rule: #将上游的 store_{01|02} 迁移到下游的 store 中。
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule: #将上游的 store_{01|02}.sale_{01|02} 迁移到下游的 store.sale 中。
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"
```

### 场景三：使用 Block & Allow Lists 过滤迁移

同步 user，store_{01|02} 库，但不同步两个实例的 user.log_bak 表。要满足该迁移需求，需要配置 Block & Allow Lists 如下：

```
block-allow-list:
  log-bak-ignored:
    do-dbs: ["user", "store_*"]
    ignore-tables:
    - db-name: "user"
      tbl-name: "log_bak"
```

### 场景四：使用 Binlog event filter 过滤迁移

过滤掉两个实例中 store_{01|02}.sale_{01|02} 表的所有删除操作，并过滤该库的 drop database 操作。要满足该迁移需求，需要配置 Binlog event filter 规则如下：

```
filters:
  sale-filter-rule:     # 过滤掉 store_* 库下面任何表的任何删除操作
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:   # 过滤掉删除 store_* 库的操作
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore
```

### 场景五：使用 SQL 表达式过滤行变更

从 v2.0.5 起，DM 支持使用 SQL 表达式过滤某些行变更。DM 支持的 ROW 格式的 binlog 中，binlog event 带有所有列的值。你可以基于这些值配置 SQL 表达式。如果该表达式对于某条行变更的计算结果是 TRUE，DM 就不会向下游迁移该条行变更。更多详情，请参考[使用 SQL 表达式过滤某些行变更](https://docs.pingcap.com/zh/tidb-data-migration/stable/feature-expression-filter)。

在确定好迁移方案之后，你就可以按照下面的操作步骤迁移数据了。

## 第 1 步：加载数据源

运行数据迁移任务前，需要加载数据源的配置到 DM，包括访问密码加密、编写数据源配置文件、加载数据源配置。

### 对数据源访问密码进行加密

为了安全，建议使用加密后的 MySQL 访问密码。DM v2.0 可以使用明文密码配置数据源的访问密码信息。如果数据源没有设置密码，则可以跳过该步骤。

以密码为 "123456" 为例：

```
tiup dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

记录该加密后的密码，用于下面新建 MySQL 数据源。

### 编写数据源配置文件

把 MySQL1 的配置文件内容写入到 mysql-source1-conf.yaml 中。配置文件如下：

```
# MySQL Configuration.

source-id: "mysql1"

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

把 MySQL2 的配置文件内容写入到 mysql-source2-conf.yaml 中。配置文件如下：

```
# MySQL Configuration.

source-id: "mysql2"

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

### 加载数据源配置

在终端中执行下面的命令，使用 dmctl 先将 MySQL1 的数据源配置加载到 DM 集群中：

```shell
tiup dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-source1-conf.yaml
```

结果如下：

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql1",
            "worker": "worker1"
        }
    ]
}
```

这样就成功将 MySQL1 添加到了 DM 集群。

再用同样的方法将 MySQL2 添加到 DM 集群。

## 第 2 步：配置任务

迁移任务的完整配置 task.yaml 如下，更多详情请参考[数据迁移任务配置向导](https://docs.pingcap.com/zh/tidb-data-migration/stable/task-configuration-guide)。该配置中包含了上述迁移方案中的多种场景的配置。

```
name: "shard_merge"
task-mode: all                                   # 进行全量数据迁移 + 增量数据迁移
meta-schema: "dm_meta"
ignore-checking-items: ["auto_increment_ID"]

target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "mysql1"        # 数据源 ID，可以从数据源配置中获取
    route-rules: ["store-route-rule", "sale-route-rule"] # 应用于该数据源的 table route 规则
    filter-rules: ["store-filter-rule", "sale-filter-rule"] # 应用于该数据源的 binlog event filter 规则
    block-allow-list:  "log-bak-ignored" # 应用于该数据源的 Block & Allow Lists 规则
  -
    source-id: "mysql2"
    route-rules: ["store-route-rule", "sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# 所有实例共享的其他通用配置

routes:
  store-route-rule:
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"

filters:
  sale-filter-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore

block-allow-list:
  log-bak-ignored:
    do-dbs: ["user", "store_*"]
    ignore-tables:
    - db-name: "user"
      tbl-name: "log_bak"
```

## 第 3 步：启动任务

为了提前发现数据迁移任务的一些配置错误，DM 中增加了[前置检查](https://docs.pingcap.com/zh/tidb-data-migration/stable/precheck)功能，在开始数据迁移的时候，DM 会自动检查相关权限和配置。你也可以使用 `check-task` 命令手动检查上游 MySQL 实例的配置是否满足要求。

使用 `dmctl` 命令开始执行迁移任务：

```shell
tiup dmctl --master-addr 127.0.0.1:8261 start-task task.yaml
```

迁移任务顺利启动后，会显示类似下面的信息：

```
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8261",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.2:8262",
            "msg": ""
        }
    ]
}
```

如果迁移任务启动失败，请根据提升修改配置信息，然后再次执行 `start-task task.yaml` 启动迁移任务。遇到问题请参考[故障及处理方法](https://docs.pingcap.com/zh/tidb-data-migration/stable/error-handling)，以及[常见问题](https://docs.pingcap.com/zh/tidb-data-migration/stable/faq)。

## 第 4 步：查看任务

在启动迁移任务之后，可以用 `dmtcl query-status` 来查看任务的状态。

```shell
tiup dmctl --master-addr 127.0.0.1:8261 query-status
```

如果某个任务遇到了错误，可以使用 `query-status <出错任务的taskName>` 查看更多详细信息。 关于`query-status` 命令的查询结果、任务状态与子任务状态的详情，请参考 [TiDB Data Migration 查询状态](https://docs.pingcap.com/zh/tidb-data-migration/stable/query-status)。

## 第 5 步：监控任务和检查日志

如果使用 TiUP 部署 DM 集群时正确部署了 Prometheus 与 Grafana，如 Grafana 的地址为 172.16.10.71，可在浏览器中打开 http://172.16.10.71:3000 进入 Grafana，选择 DM 的 Dashboard 即可查看 DM 相关监控项。具体监控指标请参考[监控与告警设置](https://docs.pingcap.com/zh/tidb-data-migration/stable/monitor-a-dm-cluster)。

你也可以通过日志文件查看 DM 运行状态和相关错误。

- DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 /dm-deploy/dm-master-8261/log/。
- DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 /dm-deploy/dm-worker-8262/log/。

## 探索更多

- [使用 Dumpling 和 TiDB Lightning 合并导入分表数据（大于1TB）](/migrate-from-mysql-shard-merge-using-lightning.md)。
- [分库分表合并迁移](https://docs.pingcap.com/zh/tidb-data-migration/stable/feature-shard-merge)
- [分表合并数据迁移最佳实践](https://docs.pingcap.com/zh/tidb-data-migration/stable/shard-merge-best-practices)
- [故障及处理方法](https://docs.pingcap.com/zh/tidb-data-migration/stable/error-handling)
- [常见问题](https://docs.pingcap.com/zh/tidb-data-migration/stable/faq)
