---
title: Placement Rules in SQL
summary: 了解如何通过 SQL 接口调度表和分区的放置位置。
---

# Placement Rules in SQL

Placement Rules in SQL 特性用于通过 SQL 接口配置数据在 TiKV 集群中的放置位置。通过该功能，用户可以将表和分区指定部署至不同的地域、机房、机柜、主机。适用场景包括低成本优化数据高可用策略、保证本地的数据副本可用于本地 Stale Read 读取、遵守数据本地要求等。

> **注意：**
>
> Placement Rules in SQL 底层的实现依赖 PD 提供的放置规则 (placement rules) 功能，参考 [Placement Rules 使用文档](/configure-placement-rules.md)。在 Placement Rules in SQL 语境下，放置规则既可以代指绑定对象的放置策略 (placement policy)，也可以代指 TiDB 发给 PD 的放置规则。

该功能可以实现以下业务场景：

- 合并多个不同业务的数据库，大幅减少数据库常规运维管理的成本
- 增加重要数据的副本数，提高业务可用性和数据可靠性
- 将最新数据存入 NVMe，历史数据存入 SSD，降低归档数据存储成本
- 把热点数据的 leader 放到高性能的 TiKV 实例上
- 将冷数据分离到不同的存储中以提高可用性
- 支持物理隔离不同用户之间的计算资源，满足实例内部不同用户的隔离需求，以及不同混合负载 CPU、I/O、内存等资源隔离的需求

## 指定放置规则

指定放置规则，首先需要通过 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句创建**放置策略 (placement policy)**。

```sql
CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

然后可以使用 `CREATE TABLE` 或者 `ALTER TABLE` 将规则绑定至表或分区表，这样就在表或分区上指定了放置规则：

```sql
CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
CREATE TABLE t2 (a INT);
ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
```

`PLACEMENT POLICY` 为全局作用域，不与任何数据库表结构相关联。因此，通过 `CREATE TABLE` 指定放置规则时，无需任何额外的权限。

要修改放置策略，你可以使用 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 语句。修改将传播到所有绑定此放置策略的对象。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=5;
```

要删除没有绑定任何分区或表的放置策略，你可以使用 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)：

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 查看放置规则

如果一张表绑定了放置规则，你可以用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 来查看。还可以用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 来查看已经创建的放置策略。

```sql
tidb> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
1 row in set (0.00 sec)
tidb> SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
*************************** 1. row ***************************
       Policy: myplacementpolicy
Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
1 row in set (0.00 sec)
```

你也可以用 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) 系统表查看所有放置策略的定义。

```sql
tidb> select * from information_schema.placement_policies\G
***************************[ 1. row ]***************************
POLICY_ID            | 1
CATALOG_NAME         | def
POLICY_NAME          | p1
PRIMARY_REGION       | us-east-1
REGIONS              | us-east-1,us-west-1
CONSTRAINTS          | 
LEADER_CONSTRAINTS   | 
FOLLOWER_CONSTRAINTS | 
LEARNER_CONSTRAINTS  | 
SCHEDULE             | 
FOLLOWERS            | 4
LEARNERS             | 0
1 row in set
```

`information_schema.tables` 表和 `information_schema.partitions` 表也有一列 `tidb_placement_policy_name`，用于展示所有绑定了放置规则的对象：

```sql
SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
```

所有绑定规则的对象都是异步调度的。可以用 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) 来查看放置规则的调度进度。

## 放置选项参考

> **注意：**
>
> - 放置选项依赖于正确地指定在每个 TiKV 节点配置中的标签 (label)。例如，`PRIMARY_REGION` 选项依赖 TiKV 中的 `region` 标签。若要查看当前 TiKV 集群中所有可用的标签，可执行 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句。
>
>     ```sql
>     mysql> show placement labels;
>     +--------+----------------+
>     | Key    | Values         |
>     +--------+----------------+
>     | disk   | ["ssd"]        |
>     | region | ["us-east-1"]  |
>     | zone   | ["us-east-1a"] |
>     +--------+----------------+
>     3 rows in set (0.00 sec)
>     ```
>
> - 使用 `CREATE PLACEMENT POLICY` 创建放置规则时，TiDB 不会检查标签是否存在，而是在绑定表的时候进行检查。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Raft leader 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。     |
| `REGIONS`                  | Raft followers 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。 |
| `SCHEDULE`                 |  用于调度 follower 放置位置的策略。可选值为 `EVEN`（默认值）或 `MAJORITY_IN_PRIMARY`。 |
| `FOLLOWERS`                |  Follower 的数量。例如 `FOLLOWERS=2` 表示数据有 3 个副本（2 个 follower 和 1 个 leader）。 |

除以上配置选项外，你还可以使用高级配置，详细介绍见[高级放置选项](#高级放置选项)。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `CONSTRAINTS`              | 适用于所有角色 (role) 的约束列表。例如，`CONSTRAINTS="[+disk=ssd]"`。      |
| `LEADER_CONSTRAINTS`       | 仅适用于 leader 的约束列表。                                         |
| `FOLLOWER_CONSTRAINTS`     | 仅适用于 follower 的约束列表。                                           |
| `LEARNER_CONSTRAINTS`     | 仅适用于 learner 的约束列表。                                           |
| `LEARNERS`                 | 指定 learner 的数量。     |

## 示例

### 增加副本数

[`max-replicas`](/pd-configuration-file.md#max-replicas) 配置项的默认值为 `3`。如要为特定的表调大该值，可使用配置策略，示例如下：

```sql
CREATE PLACEMENT POLICY fivereplicas FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=fivereplicas;
```

注意，PD 配置中包含了 leader 数和 follower 数。因此，5 个副本为 4 个 follower + 1 个 leader。

对于以上示例，你还可使用 `PRIMARY_REGION` 和 `REGIONS` 选项来描述 follower 的放置规则：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

`SCHEDULE` 选项指示 TiDB 如何平衡 follower。该选项默认的 `EVEN` 调度规则确保 follower 在所有区域内分布平衡。

如要保证在主区域内 (`us-east-1`) 放置足够多的 follower 副本，你可以使用 `MAJORITY_IN_PRIMARY` 调度规则来使该区域的 follower 达到指定数量。该调度牺牲一些可用性来换取更低的事务延迟。如果主区域宕机，`MAJORITY_IN_PRIMARY` 无法提供自动故障转移。

### 为分区表指定放置规则

除了给表绑定放置策略之外，你还可以给表分区绑定放置策略。示例如下：

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=5;
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PLACEMENT POLICY=p1 PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica,
  PARTITION pAsia VALUES IN ('CN', 'KR', 'JP')
);
```

如果分区没有绑定任何放置策略，分区将尝试继承表上可能存在的策略。比如，`pEurope` 分区将会应用 `europe` 策略，而 `pAsia` 分区将会应用表 `t1` 的放置策略 `p1`。如果 `t1` 没有绑定任何策略，`pAsia` 就不会应用任何策略。

给分区绑定放置策略后，你可以更改指定分区的放置策略。示例如下：

```sql
ALTER TABLE t1 PARTITION pEurope PLACEMENT POLICY=p1;
```

### 为数据库配置默认的放置规则

你可以为某个数据库指定默认的放置策略，类似于为数据库设置默认字符集或排序规则。如果没有指定其他选项，就会使用数据库上指定的配置。示例如下：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建放置策略

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- 创建表 t1，且未指定放置规则。

ALTER DATABASE test PLACEMENT POLICY=p2;  -- 更改默认的放置规则，但更改不影响已有的表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2，默认的放置策略 p2 在 t2 上生效。

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- 创建表 t3。因为语句中已经指定了其他放置规则，默认的 p2 策略在 t3 上不生效。

ALTER DATABASE test PLACEMENT POLICY=p3;  -- 再次更改默认的放置规则，此更改不影响已有的表。

CREATE TABLE t4 (a INT);  -- 创建表 t4，默认的放置策略 p3 生效。

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- 绑定策略 p3 的表，也就是 t4，会采用 FOLLOWERS=3。
```

注意分区与表之间的继承和这里的继承不同。改变表的放置策略，也会让分区应用新的策略。但是只有建表时没有指定放置策略的时候，表才会从数据库继承放置策略，且之后再改变数据库也不影响已经继承的表。

### 高级放置选项

放置选项 `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 可满足数据放置的基本需求，但会缺乏一些灵活性。在较复杂的场景下，若需要更灵活地放置数据，可以使用高级放置选项 `CONSTRAINTS` 和 `FOLLOWER_CONSTRAINTS`。`PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不可与 `CONSTRAINTS` 选项同时指定，否则会报错。

以下示例设置了一个约束，要求数据必须位于某个 TiKV 节点，且该节点的 `disk` 标签必须匹配特定的值：

```sql
CREATE PLACEMENT POLICY storageonnvme CONSTRAINTS="[+disk=nvme]";
CREATE PLACEMENT POLICY storageonssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageonssd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storageonnvme
);
```

该约束可通过列表格式 (`[+disk=ssd]`) 或字典格式 (`{+disk=ssd: 1,+disk=nvme: 2}`) 指定。

在列表格式中，约束以键值对列表格式。键以 `+` 或 `-` 开头。`+disk=nvme` 表示 `disk` 标签必须设为 `nvme`，`-disk=nvme` 表示 `disk` 标签值不能为 `nvme`。

在字典格式中，约束还指定了适用于该规则的多个实例。例如，`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示 1 个 follower 位于 `us-east-1`，1 个 follower 位于 `us-east-2`，1 个 follower 位于 `us-west-1`。再例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme": 1,"+region=us-west-1": 1}';` 表示 1 个 follower 位于 `us-east-1` 区域中有 `nvme` 硬盘的机器上，1 个 follower 位于 `us-west-1`。

> **注意：**
>
> 字典和列表格式都基于YAML解析，但 YAML 语法有些时候不能被正常解析。例如 YAML 会把 "{+disk=ssd:1,+disk=nvme:2}" 错误地解析成 '{"+disk=ssd:1": null, "+disk=nvme:2": null}'，不符合预期。但 "{+disk=ssd: 1,+disk=nvme: 2}" 能被正确解析成 '{"+disk=ssd": 1, "+disk=nvme": 2}'。

## 工具兼容性

| 工具名称 | 最低兼容版本 | 说明 |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | 支持放置规则的导入与导出，见 [BR 兼容性](/br/backup-and-restore-overview.md#功能的兼容性) |
| TiDB Lightning | 暂时不兼容 | 导入包含放置策略的数据时会报错 |
| TiCDC | 6.0 | 忽略放置规则，不同步规则到下游集群 |
| TiDB Binlog | 6.0 | 忽略放置规则，不同步规则到下游集群 |

## 使用限制

目前已知 Placement Rules in SQL 特性存在以下限制：

* 临时表不支持放置规则。
* 设置 `PRIMARY_REGION` 和 `REGIONS` 时允许存在语法糖。但在未来版本中，我们计划为 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 添加变体支持，见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。
* 放置规则仅保证静态数据被放置在正确的 TiKV 节点上。该规则不保证传输中的数据（通过用户查询或内部操作）只出现在特定区域内。
