---
title: Geo-Partition 使用文档
summary: 如何配置 Geo-Partition
aliases: ['/docs-cn/dev/configure-geo-partition/']
---

# Geo-Partition 使用文档

## 场景描述

在跨地域部署的 TiDB 集群中，由于 TiDB 实例与 TiKV 实例分布在不同的地区，TiDB 常常需要跨地区访问数据，导致较高的延时。

为了减少跨地区数据访问，可以人为地控制数据的位置，使得数据离业务端更近。为此，TiDB 5.0 提供了 Geo-Partition。用户把表进行分区，然后把分区和 TiKV 实例关联起来，以指导 PD 把该分区的数据调度到对应的 TiKV 实例上。

当场景同时满足以下条件时，推荐使用 Geo-Partition：

- 对读或写延时要求高
- 表内的数据与地域强关联
- 表中有与地区相关的字段，通过该字段的值能指导数据放置的地理位置

## 原理介绍

TiDB 4.0 中，PD 组件内部提供了 [Placement Rules](/configure-placement-rules.md) 的功能，使得用户可以通过 Placement Rules 配置数据的副本数量、存放位置、主机类型等放置策略。

TiDB 5.0 的 Geo-Partition 是在 Placement Rules 的基础上，提供了 SQL 语法，方便用户新增、更改、删除、查看分区的放置策略。用户在定义、更改分区的放置策略，或是执行分区相关的 DDL 语句时，TiDB 实例生成对应的 Placement Rules，并向 PD 发送更新 Placement Rules 的请求。PD 根据用户在 SQL 语句配置的 Placement Rules 执行相应的数据放置策略。

## 使用方法

Partition 上有 3 种定义放置策略的操作：

- 新增副本放置策略
- 更改副本放置策略
- 删除副本放置策略

这 3 种操作都只能通过 `ALTER TABLE table_name ALTER PARTITION partition_name` 语句实现，只是后面的子句不同。

本节先介绍以上 3 种操作的语法，再依次介绍子句中每个选项的使用方法。

### 新增副本放置策略

当需要给特定数据的特定副本角色增加副本时，使用 `ADD PLACEMENT POLICY` 子句：

```sql
ALTER TABLE table_name ALTER PARTITION partition_name
	ADD PLACEMENT POLICY [CONSTRAINTS=constraints] ROLE=role [REPLICAS=replicas],
	...
```

该语句会在原来的副本数量基础上，再给 `partition_name` 增加 `replicas` 个 `role` 角色的副本，包括索引。当存在 `CONSTRAINT` 选项时，新增的副本要满足 `CONSTRAINT` 里的限制。

可以在一条 SQL 语句里定义多个放置策略，用逗号分隔。例如：

```sql
ALTER TABLE user ALTER PARTITION p0
	ADD PLACEMENT POLICY CONSTRAINTS='["+zone=sh"]' ROLE=follower REPLICAS=1,
	ADD PLACEMENT POLICY CONSTRAINTS='["+zone=gz"]' ROLE=follower REPLICAS=1;
```

该语句使 `sh` 和 `gz` 各新增一个 follower 副本。

### 更改副本放置策略

当需要更改数据的放置策略时，使用 `ALTER PLACEMENT POLICY` 子句：

```sql
ALTER TABLE table_name ALTER PARTITION partition_name
	ALTER PLACEMENT POLICY [CONSTRAINTS=constraints] ROLE=role [REPLICAS=replicas],
	...
```

该语句会把 `partition_name` 的 `role` 角色的副本数量更改为 `replicas` 个。当存在 `CONSTRAINT` 选项时，这些副本要同时满足 `CONSTRAINT` 里的限制。

```sql
ALTER TABLE user ALTER PARTITION p0
	ADD PLACEMENT POLICY CONSTRAINTS='["+zone=sh"]' ROLE=voter REPLICAS=2,
	ALTER PLACEMENT POLICY CONSTRAINTS='["+zone=bj"]' ROLE=voter REPLICAS=3;
```

假设 `p0` 原先有 3 个副本。第一条子句给 `p0` 再增加 2 个 `voter` 副本，随后第二条子句将 `voter` 副本的数量覆盖为 3，并且更改了 `CONSTRAINTS`。最终，分区 `p0` 有 3 个副本，并且全部在 `bj`。

### 删除副本放置策略

当需要删除特定角色的所有副本时，使用 `DROP PLACEMENT POLICY` 子句：

```sql
ALTER TABLE table_name ALTER PARTITION partition_name
	DROP PLACEMENT POLICY ROLE=role,
	...
```

该语句只需要 `ROLE` 选项，它会删除 `partition_name` 的所有 `role` 角色的副本。

### CONSTRAINTS 配置

`CONSTRAINTS` 选项通过 store 的 label 来限制副本的放置策略。`CONSTRAINTS` 是一个字符串类型的值，它有 2 种可选的格式：

- 数组格式：`[{+|-}key=value,...]`，例如 `["+zone=bj","-disk=hdd"]`
- 字典格式：`{"{+|-}key=value,...":count,...}`，例如 `{"+zone=bj,-disk=hdd":1, "+zone=sh":2}`

`+` 代表数据只能放在有这些 label 的 store 上；`-` 代表数据不能放在有这些 label 的 store 上。例如 `["+zone=bj","-disk=hdd"]` 代表数据要放在 `bj` 的非 `hdd` 的 store 上，`"+zone=sh","+zone=bj"` 代表数据可以放在 `sh` 或 `bj` 的 store 上。

`key` 是 label 的名字，`value` 是 label 的值。label 的名字必须已经在 store 的配置上定义过，例如 store 上如下定义了 label：

```
[server]
labels = "zone=bj,rack=rack0,disk=hdd"
```

那么 `CONSTRAINTS` 中就可以使用 `zone`、`rack`、`disk` 这 3 种 label。例如 `+zone=bj` 匹配该 store，而 `+disk=ssd` 不匹配该 store。

`count` 是受限制的副本数量，无论前缀是 `+` 还是 `-` 都有意义。例如 `{"+zone=sh":1,"-zone=bj":2}` 指把 1 个副本调度到 `sh` 上，2 个副本调度到除了 `bj` 以外的 store 上。

只有字典格式有 `count`，数组格式没有 `count`，副本的总数受 `REPLICAS` 限制。例如 `CONSTRAINTS='["+zone=sh","+zone=bj"]' REPLICAS=3` 指把 3 个副本放在 `sh` 或 `bj`。

### ROLE 配置

`ROLE` 选项定义受影响的副本的角色。副本有 4 种角色：

- leader，只能有一个 leader
- follower
- voter，包含 leader 和 follower
- learner，TiFlash 或 TiKV 都可以是 learner

如果在同一个分区中同时定义了 voter 和 follower 的放置策略，follower 的副本数不包含在 voter 中。leader 同理。例如：

```sql
ALTER TABLE user ALTER PARTITION p0
	ADD PLACEMENT POLICY CONSTRAINTS='["+zone=bj"]' ROLE=follower REPLICAS=2,
	ALTER PLACEMENT POLICY CONSTRAINTS='["+zone=sh"]' ROLE=voter REPLICAS=3;
```

在这条 SQL 中，分区 `p0` 有 5 个副本，其中 2 个在 `bj`，3 个在 `sh`。Leader 只能在 `sh`。

### REPLICAS 配置

`REPLICAS` 选项定义特定副本角色的个数。

Leader 可以省略 `REPLICAS` 选项，因为 leader 的个数永远是 1。当 `CONSTRAINTS` 中定义了副本角色的个数，`REPLICAS` 选项也可以省略，因为总的副本数可以计算出来。例如，从 `CONSTRAINTS='{"+zone=bj":2,"+zone=sh":1}', ROLE=voter` 可以推断出 `REPLICAS` 是 3。

当 `REPLICAS` 和 `CONSTRAINTS` 中的 `count` 都出现的时候，`REPLICAS` 必须大于等于 `count` 之和，`REPLICAS` 多出来的副本可以放置在任意位置。例如，`CONSTRAINTS='{"+zone=bj":2,"+zone=sh":1}', ROLE=voter, REPLICAS=4`，该例子中，2 个副本在 `sh`，1 个副本在 `bj`，还剩余 1 个副本，它可以放置在任意位置，包括 `bj` 和 `sh`。

### 注意事项

在执行以上操作时，必须要遵守 Raft 协议，即 leader 个数必须等于 1。

例如，如下两种语句都会报错：

```sql
ALTER TABLE user ALTER PARTITION p0
	ADD PLACEMENT POLICY ROLE=leader REPLICAS=2;
```

```sql
ALTER TABLE user ALTER PARTITION p0
	DROP PLACEMENT POLICY ROLE=leader,
	DROP PLACEMENT POLICY ROLE=voter;
```

## 使用示例

设想如下一个场景：数据库中有一张 `user` 表，存放了业务的所有用户数据。用户分布在世界各个国家，他们经常需要访问自己的数据。TiDB 集群有 2 个数据中心，分别在中国和美国。用户向最近的应用端发起前端请求，应用端也向最近的 TiDB 实例发起数据库请求。

在不使用 Geo-Partition 的情况下，用户数据随意地放置在任意一个数据中心。例如，中国用户的数据可能放置在美国数据中心上，那么中国数据中心的 TiDB 实例从美国数据中心的 TiKV 实例获取数据，导致非常高的访问延时。这种场景就需要 Geo-Partition 来定义放置策略。

在使用 Geo-Partition 之前，需要先给 TiKV 实例打上代表数据中心的 label，例如 `zone=chn` 和 `zone=usa`。

接下来把 `user` 表进行分区，使得单个分区内的所有用户都靠近同一个数据中心。例如按 `country` 字段进行分区：

```sql
CREATE TABLE user (
	id INT,
	name varchar(100),
	country varchar(100)
)
PARTITION BY LIST COLUMNS(country) (
	PARTITION east VALUES IN('china', 'japan', 'singapore'),
	PARTITION west VALUES IN('usa', 'canada', 'england', 'france')
);
```

最后把分区 `east` 的 leader 副本放置在中国数据中心，把 `west` 的 leader 放置在美国数据中心：

```sql
ALTER TABLE user ALTER PARTITION east
	ALTER PLACEMENT POLICY ROLE=leader CONSTRAINTS='["+zone=chn"]';
ALTER TABLE user ALTER PARTITION west
	ALTER PLACEMENT POLICY ROLE=leader CONSTRAINTS='["+zone=usa"]';
```
