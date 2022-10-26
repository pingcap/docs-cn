---
title: Placement Rules in SQL
summary: 了解如何通过 SQL 接口调度表和分区的放置位置。
---

# Placement Rules in SQL

> **警告：**
>
> Placement Rules in SQL 是 TiDB 在 v5.3.0 中引入的实验特性，其语法在 GA 前可能会发生变化，还可能存在 bug。如果你知晓潜在的风险，可通过执行 `SET GLOBAL tidb_enable_alter_placement = 1;` 来开启该实验特性。

Placement Rules in SQL 特性用于通过 SQL 接口配置数据在 TiKV 集群中的放置位置。通过该功能，用户可以将表和分区指定部署至不同的地域、机房、机柜、主机。适用场景包括低成本优化数据高可用策略、保证本地的数据副本可用于本地 Stale Read 读取、遵守数据本地要求等。

该功能可以实现以下业务场景：

- 合并多个不同业务的数据库，大幅减少数据库常规运维管理的成本
- 增加重要数据的副本数，提高业务可用性和数据可靠性
- 将最新数据存入 SSD，历史数据存入 HDD，降低归档数据存储成本
- 把热点数据的 leader 放到高性能的 TiKV 实例上
- 将冷数据分离到不同的存储中以提高可用性

## 指定放置选项

要使用 Placement Rules in SQL 特性，你需要在 SQL 语句中指定一个或多个放置选项 (placement option)。可通过*直接放置 (direct placement)* 或*放置策略 (placement policy)* 来指定放置选项。

以下示例中，表 `t1` 和 `t2` 的放置规则相同。`t1` 是通过直接放置指定的规则，而 `t2` 是通过放置策略来指定的规则。

```sql
CREATE TABLE t1 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t2 (a INT) PLACEMENT POLICY=eastandwest;
```

为了能够更轻松地管理放置规则，推荐使用放置策略来指定规则。当你通过 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 更改放置策略后，此更改会自动传播至所有数据库对象。

如果你使用直接放置选项，你需要为每个对象（例如表和分区）都单独更改放置规则。

`PLACEMENT POLICY` 为全局作用域，不与任何数据库表结构相关联。因此，通过 `CREATE TABLE` 指定放置策略时，无需任何额外的权限。

## 放置选项参考

> **注意：**
>
> 放置选项依赖于正确地指定在每个 TiKV 节点配置中的标签 (label)。例如，`PRIMARY_REGION` 选项依赖 TiKV 中的 `region` 标签。若要查看当前 TiKV 集群中所有可用的标签，可执行 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句。
>
> ```sql
> mysql> show placement labels;
> +--------+----------------+
> | Key    | Values         |
> +--------+----------------+
> | disk   | ["ssd"]        |
> | region | ["us-east-1"]  |
> | zone   | ["us-east-1a"] |
> +--------+----------------+
> 3 rows in set (0.00 sec)
> ```

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Raft leader 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。     |
| `REGIONS`                  | Raft followers 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。 |
| `SCHEDULE`                 |  用于调度 follower 放置位置的策略。可选值为 `EVEN`（默认值）或 `MAJORITY_IN_PRIMARY`。 |
| `FOLLOWERS`                |  Follower 的数量。例如 `FOLLOWERS=2` 表示数据有 3 个副本（2 个 follower 和 1 个 leader）。 |

除以上配置选项外，你还可以使用高级配置，详细介绍见[高级放置](#高级放置)。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `CONSTRAINTS`              |  适用于所有角色 (role) 的约束列表。例如，`CONSTRAINTS="[+disk=ssd]`。      |
| `FOLLOWER_CONSTRAINTS`     |  仅适用于 follower 的约束列表。                                           |

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

> **注意：**
>
> 以下示例使用的 List 分区目前为 TiDB 实验特性。在表的分区功能中，要求主键里包含所有分区函数中使用的列。

除了将放置选项分配给表之外，你还可以将选项分配给表分区。示例如下：

```sql
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica
);
```

### 为数据库配置默认的放置规则

你可以为某个数据库指定默认的放置选项，类似于为数据库设置默认字符集或排序规则。如果没有指定其他选项，就会使用数据库上指定的配置。示例如下：

```sql
CREATE TABLE t1 (a INT);  -- 创建表 t1，且未指定放置选项。

ALTER DATABASE test FOLLOWERS=4;  -- 更改默认的放置选项，但更改不影响已有的表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2，默认的放置规则 FOLLOWERS=4 在 t2 上生效。

CREATE TABLE t3 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建表 t3。因为语句中已经指定了其他放置规则，默认的 FOLLOWERS=4 规则在 t3 上不生效。

ALTER DATABASE test FOLLOWERS=2;  -- 再次更改默认的放置选项，此更改不影响已有的表。

CREATE TABLE t4 (a INT);  -- 创建表 t4，默认的放置规则 FOLLOWERS=2 生效。
```

由于只有在创建表时才会从数据库继承放置选项，因此推荐使用 `PLACEMENT POLICY` 放置策略来设置默认的放置选项。使用后，用户可以通过改动放置策略，改变继承自数据库的放置选项。

### 高级放置

放置选项 `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 可满足数据放置的基本需求，但会缺乏一些灵活性。在较复杂的场景下，若需要更灵活地放置数据，可以使用高级放置选项 `CONSTRAINTS` 和 `FOLLOWER_CONSTRAINTS`。`PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不可与 `CONSTRAINTS` 选项同时指定，否则会报错。

以下示例设置了一个约束，要求数据必须位于某个 TiKV 节点，且该节点的 `disk` 标签必须匹配特定的值：

```sql
CREATE PLACEMENT POLICY storeonfastssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY storeonhdd CONSTRAINTS="[+disk=hdd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storeonhdd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storeonfastssd
);
```

该约束可通过列表格式 (`[+disk=ssd]`) 或字典格式 (`{+disk=ssd:1,+disk=hdd:2}`) 指定。

在列表格式中，约束以键值对列表格式。键以 `+` 或 `-` 开头。`+disk=ssd` 表示 `disk` 标签必须设为 `ssd`，`-disk=hdd` 表示 `disk` 标签值不能为 `hdd`。

在字典格式中，约束还指定了适用于该规则的多个实例。例如，`FOLLOWER_CONSTRAINTS="{+region=us-east-1:1,+region=us-east-2:1,+region=us-west-1:1,+any:1}";` 表示 1 个 follower 位于 `us-east-1`，1 个 follower 位于 `us-east-2`，1 个 follower 位于 `us-west-1`，1 个 follower 可位于任意区域。再例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=hdd":1,"+region=us-west-1":1}';` 表示 1 个 follower 位于 `us-east-1` 区域中有 `hdd` 硬盘的机器上，1 个 follower 位于 `us-west-1`。

> **注意：**
>
> 字典和列表格式都基于 YAML 解析，但 YAML 语法有些时候不能被正常解析。例如 YAML 会把 `"{+disk=ssd:1,+disk=hdd:2}"`（`:` 后无空格）错误地解析成 `'{"+disk=ssd:1": null, "+disk=hdd:1": null}'`，不符合预期。但 `"{+disk=ssd: 1,+disk=hdd: 1}"`（`:` 后有空格）能被正确解析成 `'{"+disk=ssd": 1, "+disk=hdd": 1}'`。

## 使用限制

目前已知 Placement Rules in SQL 存在以下限制：

* Dumpling 不支持导出放置策略，见 [issue #29371](https://github.com/pingcap/tidb/issues/29371)。
* TiDB 生态工具，包括 TiCDC、TiDB Lightning 和 TiDB Data Migration (DM)，不支持放置规则。
* 使用 BR 来恢复一个设置了放置规则的库或者表时会失败。见 [issue #31455](https://github.com/pingcap/tidb/issues/31455)。
* 临时表不支持放置选项，直接放置和放置策略均不支持。
* 设置 `PRIMARY_REGION` 和 `REGIONS` 时允许存在语法糖。但在未来版本中，我们计划为 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 添加变体支持，见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。
* 不能通过放置规则语法配置 TiFlash 副本。
* 放置规则仅保证静态数据被放置在正确的 TiKV 节点上。该规则不保证传输中的数据（通过用户查询或内部操作）只出现在特定区域内。
