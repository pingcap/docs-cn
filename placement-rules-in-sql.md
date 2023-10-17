---
title: Placement Rules in SQL
summary: 了解如何通过 SQL 接口调度表和分区的放置位置。
---

# Placement Rules in SQL

Placement Rules in SQL 特性用于通过 SQL 接口配置数据在 TiKV 集群中的放置位置。通过该功能，用户可以将表和分区或指定数据范围部署至不同的地域、机房、机柜、主机。适用场景包括低成本优化数据高可用策略、数据隔离要求等。

该功能可以实现以下业务场景：

- 优化数据高可用策略，多数据中心部署
- 合并多个不同业务的数据库，物理隔离不同用户的数据，满足实例内部不同用户的隔离需求
- 增加重要数据的副本数，提高业务可用性和数据可靠性

限制和注意事项：

- 不建议创建过多的 placement policy 增加运维复杂度，一个集群 policy 个数建议在 10 个以内
- 不建议使用复杂的放置策略，使用推荐的[常见场景](#常用场景示例)应用
- 限制绑定 policy 的表和分区数总数在 10000 以内。为过多的表，分区绑定 policy，会增加 PD 上规则计算的负担，从而影响服务。

> **提示：**
>
> Placement Rules in SQL 底层的实现依赖 PD 提供的放置规则 (placement rules) 功能，参考 [Placement Rules 使用文档](/configure-placement-rules.md)。在 Placement Rules in SQL 语境下，放置规则既可以代指绑定对象的放置策略 (placement policy)，也可以代指 TiDB 发给 PD 的放置规则。

## 概览

通过  `Placement Rules in SQL`, 可以为不同的数据级别配置放置策略，从粗到细为：

| 级别                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `Cluster`          | TiDB 默认会配置为集群设置 3 副本的策略，你可以另外为全局放置策略进行置配置，参考[集群配置](#为集群指定全局的副本数)  |
| `Database`         | 你可以另外对 Databases 配置放置策略，参考[为数据库配置默认的放置规则](#为数据库配置默认的放置规则) | 
| `Table`            | 你可以另外对 Tables 配置放置策略，参考[为表指定放置规则](#为表指定放置规则)  |
| `Row`              | 你可以另外对特定的 Row 通过定义 Partition 来配置放置策略，参考[为分区表指定放置规则](#为分区表指定放置规则) |

这些对象绑定 PLACEMENT POLICY， 都可以使用 `ALTER .... PLACEMENT POLICY policy_name` 语法，具体可参考示例。 `PLACEMENT POLICY` 具体的放置规则需要提前创建好。创建 POLICY 方式下面会介绍。 

## 创建放置规则

创建放置规则，首先需要通过 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句创建**放置策略 (placement policy)**。

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

可以用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 来查看已经创建的指定放置策略。如果一张表绑定了放置规则，你可以用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 来查看。

```sql
tidb> SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
*************************** 1. row ***************************
       Policy: myplacementpolicy
Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
1 row in set (0.00 sec)


tidb> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
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

### 高级配置选项

除以上配置选项外，你还可以使用更高级的配置选项，使用起来相对更复杂一些，需要对集群拓扑和 TiDB 数据分片有更近一步了解才能使用得当。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `CONSTRAINTS`              | 适用于所有角色 (role) 的约束列表。例如，`CONSTRAINTS="[+disk=ssd]"`。      |
| `LEADER_CONSTRAINTS`       | 仅适用于 leader 的约束列表。                                         |
| `FOLLOWER_CONSTRAINTS`     | 仅适用于 follower 的约束列表。                                           |
| `LEARNER_CONSTRAINTS`      | 仅适用于 learner 的约束列表。                                           |
| `LEARNERS`                 | 指定 learner 的数量。     |
| `SURVIVAL_PREFERENCE`      | 指定按 label 容灾等级的优先级放置副本。例如 `SURVIVAL_PREFERENCE="[region, zone, host]"`。    |

### CONSTRAINTS 格式

`CONSTRAINTS` 支持两种类型的格式:

| Constraint Type | 描述 |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| 列表格式 (All Replicas) | 约束以键值对列表格式。键以 `+` 或 `-` 开头。`+disk=nvme` 表示 `disk` 标签必须设为 `nvme`，`-disk=nvme` 表示 `disk` 标签值不能为 `nvme`。 |
| 字典格式 (Per Replica) | 在字典格式中，约束还指定了适用于该规则的多个实例。例如，`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示 1 个 follower 位于 `us-east-1`，1 个 follower 位于 `us-east-2`，1 个 follower 位于 `us-west-1`。再例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme": 1,"+region=us-west-1": 1}';` 表示 1 个 follower 位于 `us-east-1` 区域中有 `nvme` 硬盘的机器上，1 个 follower 位于 `us-west-1`。|

> **注意：**
>
> LEADER_CONSTRAINTS 只支持列表格式。
>
> 字典和列表格式都基于 YAML 解析，但 YAML 语法有些时候不能被正常解析。例如 YAML 会把 `"{+disk=ssd:1,+disk=nvme:2}"`（`:` 后无空格）错误地解析成 `'{"+disk=ssd:1": null, "+disk=nvme:2": null}'`，不符合预期。但 `"{+disk=ssd: 1,+disk=nvme: 2}"`（`:` 后有空格）能被正确解析成 `'{"+disk=ssd": 1, "+disk=nvme": 2}'`。
>
> 字典格式支持以 `+` 或 `-` 开头的键，还支持另外一个特殊的属性 `#reject-leader`, 如 `FOLLOWER_CONSTRAINTS='{ "+region=us-east-1":1, "+region=us-east-2": 2}' FOLLOWER_CONSTRAINTS='{"+region=us-west-1,#reject-leader": 1}'` 表示当进行容灾时，`us-west-1` 上尽可能驱逐当选的 leader。  

## 基础示例

### 为集群指定全局的副本数

集群初始化后，副本数默认值为 `3`。如要为特定的表调大该值，可使用配置策略，示例如下：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

注意，配置中默认会认定 leader 数是 1。因此，5 个副本为 4 个 follower + 1 个 leader。

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

### 为表指定放置规则

你可以为某个表制定默认的放置策略。

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- 创建表 t。绑定放置策略为 five_replicas。

ALTER TABLE t PLACEMENT POLICY=default; -- 删除已绑定的放置策略

```

### 为分区表指定放置规则

除了给表绑定放置策略之外，你还可以给表分区绑定放置策略。示例如下：

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

如果分区没有绑定任何放置策略，分区将尝试继承表上可能存在的策略。比如，`p0` 分区将会应用 `storageonssd` 策略，`p4`  分区将会应用 `storageonnvme` 策略，而 `p1`,`p2`,`p3` 分区将会应用表 `t1` 的放置策略 `companystandardpolicy`。如果 `t1` 没有绑定任何策略，`p1`,`p2`,`p3`  就不会应用任何策略，即继承表或数据库或全局的默认策略。

给分区绑定放置策略后，你可以更改指定分区的放置策略。示例如下：

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageonssd;
```

## 常用场景示例

放置选项 `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 可满足数据放置的基本需求，但会缺乏一些灵活性。在较复杂的场景下，若需要更灵活地放置数据，可以使用高级放置选项 `CONSTRAINTS` 和 `FOLLOWER_CONSTRAINTS`。其中 `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不可与 `CONSTRAINTS` 选项同时指定，否则会报错。具体可参考[放置选项参考](#放置选项参考)。

**如何给节点打上标签**

放置规则依赖给存储节点标记上相应的属性，才能正常使用。 标记方式为：

{{< copyable "" >}}

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

详细可参考相关示例:

| 方式 | 示例 |
| --- | --- |
| 手动部署 | [通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md) |
| TiUP 部署 | [跨机房部署拓扑结构](/geo-distributed-deployment-topology.md) |
| Operator 部署| [在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster#高数据的高可用) |

### 高可用场景

假设集群的拓扑扑结构如下：

```sql
mysql> SELECT store_id,address,label from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
| store_id | address         | label                                                                                                                    |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
|        1 | 127.0.0.1:20163 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1a"}, {"key": "host", "value": "host1"}]     |
|        2 | 127.0.0.1:20162 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1b"}, {"key": "host", "value": "host2"}]     |
|        3 | 127.0.0.1:20164 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1c"}, {"key": "host", "value": "host3"}]     |
|        4 | 127.0.0.1:20160 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2a"}, {"key": "host", "value": "host4"}]     |
|        5 | 127.0.0.1:20161 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2b"}, {"key": "host", "value": "host5"}]     |
|        6 | 127.0.0.1:20165 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2c"}, {"key": "host", "value": "host6"}]     |
|        7 | 127.0.0.1:20166 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1a"}, {"key": "host", "value": "host7"}]     |
|        8 | 127.0.0.1:20167 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1b"}, {"key": "host", "value": "host8"}]     |
|        9 | 127.0.0.1:20168 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1c"}, {"key": "host", "value": "host9"}]     |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+

```

集群的 TiKV 数据节点分布在 3 个 `region` 区域，每个中心有两个可用的 `zone`。

#### 指定生存偏好

如果你不特别在意数据的分布，只希望能满足容灾生存要求，你可以使用 `SURVIVAL_PREFERENCES` 选项设置数据的生存能力偏好。

例如，在例子中 TiDB 集群分布在 3 个 `region`（区域），且每个区域有多个 `zone`（即可用区）。在为该集群创建放置策略时，假设 `SURVIVAL_PREFERENCES` 的设置如下：

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

创建好放置策略后，你可以按需将放置策略绑定到对应的表上：

- 对于绑定了 `multiaz` 放置策略的表，数据将以 3 副本的形式放置在不同的可用区里，优先满足跨 `region` 级别的生存目标，再满足跨 `zone` 级别的生存目标, 再满足跨 `host` 级别的生存目标。
- 对于绑定了 `singleaz` 放置策略的表，数据会优先以 3 副本的形式全部放置在 `us-east-1` 这个可用区里，再满足跨 `zone` 级别的数据隔离的生存目标。

> **注意：**
>
> `SURVIVAL_PREFERENCES` 和 PD 中的 `location-labels` 是等价的，更多信息可以参考[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)。

#### 指定集群多数据中心 5 副本 2:2:1 分布

如果要特定的数据分布，可以使用 `CONSTRAINTS` 配置 `Per-Replica` [字典格式](#constraints-格式)的策略:

```sql
tidb> CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

tidb> ALTER RANGE global PLACEMENT POLICY = "deploy221";

mysql> show placement;
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| Target            | Placement                                                                                   | Scheduling_State |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| POLICY deploy221  | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | NULL             |
| RANGE TiDB_GLOBAL | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | SCHEDULED        |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
```

通过为系统全局设置 `deploy221` 的放置规则后，TiDB 调度器会将数据根据该规则来分布数据： `us-east-1` 区域放置两个副本，`us-east-2` 区域放置两个副本，`us-west-1` 区域放置一个副本。

#### 指定 Leader/Follower 分布

以下两种方式都可以制定特殊的 Leader/Follower 的分布

##### 使用 Constraints 指定

如果你对 Leader 的分布要要求，可以使用如下语句指定。

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1: 1}';
```

该语句创建好后，绑定改策略的数据会将副本组的 Raft Leader 放置在 `us-east-1` 中，其他副本在其他区域。值得注意的是，如果集群发生故障，比如 leader 所在区域 `us-east-1` 的节点都挂了，这时候即时其他区域设置的都是 FOLLOWER_CONSTRAINTS, 也会选举出一个新的 leader，也就是说保证服务可用的优先级是最高的。如果希望在 `us-east-1` 区域故障发生时，leader 不要在 `us-west-1`，可以配置特殊的属性，驱逐上面新的 leader:

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#reject-leader: 1}';
```

##### 使用 PRIMARY_REGION 指定

如果你的集群拓扑是使用 `region` label 标记的，上面例子你还可使用 `PRIMARY_REGION` 和 `REGIONS` 选项来描述 follower 的放置规则：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

`PRIMARY_REGION` 为 LEADER 分布的 REGION，只能指定一个。

`SCHEDULE` 选项指示 TiDB 如何平衡 follower。该选项默认的 `EVEN` 调度规则确保 follower 在所有区域内分布平衡。

如要保证在主区域内 (`us-east-1`) 放置足够多的 follower 副本，你可以使用 `MAJORITY_IN_PRIMARY` 调度规则来使该区域的 follower 达到指定数量。该调度牺牲一些可用性来换取更低的事务延迟。如果主区域宕机，`MAJORITY_IN_PRIMARY` 无法提供自动故障转移。

### 数据隔离场景

以下示例设置了一个约束，要求数据必须位于某个 TiKV 节点，且该节点的 `disk` 标签必须匹配特定的值：

```sql
CREATE PLACEMENT POLICY storageonnvme CONSTRAINTS="[+disk=nvme]";
CREATE PLACEMENT POLICY storageonssd CONSTRAINTS="[+disk=ssd]";
CREATE TABLE tpapp (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=storageonnvme；
CREATE TABLE apapp (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=storageonssd
```

该约束可通过列表格式 (`[+disk=ssd]`) 或字典格式 (`{+disk=ssd: 1,+disk=nvme: 2}`) 指定。将应用 `tpapp` 数据放置在 `disk` 为 `nvme` 的 tikv 节点上，应用 `apapp` 的数据放置在 `disk` 为 `ssd` 的 tikv 节点上，从而在存储上达到了物理隔离的效果。

## 工具兼容性

| 工具名称 | 最低兼容版本 | 说明 |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | BR 在 v6.0 之前不支持放置规则的备份与恢复，见[恢复 Placement Rule 到集群时为什么会报错？](/faq/backup-and-restore-faq.md#恢复-placement-rule-到集群时为什么会报错) |
| TiDB Lightning | 暂时不兼容 | 导入包含放置策略的数据时会报错 |
| TiCDC | 6.0 | 忽略放置规则，不同步规则到下游集群 |
| TiDB Binlog | 6.0 | 忽略放置规则，不同步规则到下游集群 |

## 使用限制

目前已知 Placement Rules in SQL 特性存在以下限制：

* 临时表不支持放置规则。
* 放置规则仅保证静态数据被放置在正确的 TiKV 节点上。该规则不保证传输中的数据（通过用户查询或内部操作）只出现在特定区域内。
* 设置 `TiFlash` 的副本要通过[构建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)的方式创建，不能使用该特性。 
* 设置 `PRIMARY_REGION` 和 `REGIONS` 时允许存在语法糖。但在未来版本中，我们计划为 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 添加变体支持，见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。
