---
title: TiCDC Open Protocol
category: reference
---

# TiCDC Open Protocol

## 概述

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ 等第三方数据媒介复制 TiDB 的数据变更。

TiCDC Open Protocol 以 Event 为基本单位向下游复制数据变更事件，Event 分为三类：

* Row Changed Event：代表一行的数据变化，在 Row 发生变更时被发出，包含变更后 Row 的相关信息
* DDL Event：代表 DDL 变更，在上游成功执行 DDL 后发出，DDL Event 会广播到每一个 MQ Partition 中
* Resolved Event：代表一个特殊的时间点，表示在这个时间点前的收到的 Event 是完整的

## 协议约束

* 在绝大多数情况下，一个版本的 Row Changed Event 只会发出一次，但是特殊情况（节点故障、网络分区等）下，同一版本的 Row Changed Event 可能会多次发送。
* 对于同一张表的 Row Changed Event 组成的 Event 流，对于每一个版本第一次发出的 Row Changed Event 一定是按 TS 顺序递增的。
* Resolved Event 会被周期性的广播到各个 MQ Partition，Resolved Event 意味着任何 TS 小于 Resolved Event TS 的 Event 已经发送给下游。
* DDL Event 将被广播到各个 MQ Partition。
* 对于一行数据的多个 Row Changed Event 一定会被发送到同一个 MQ Partition 中。

## Event 格式定义

### Row Changed Event

**Key:**

```json
{
    "ts":<TS>,
    "schema":<Schema Name>,
    "table":<Table Name>,
    "type":1
}
```

| 参数         | 类型   | 说明                    |
| :---------- | :----- | :--------------------- |
| TS          | Number | 造成 Row 变更的事务的 TS  |
| Schema Name | String | Row 所在的 Schema 的名字 |
| Table Name  | String | Row 所在的 Table 的名字  |

**Value:**

```json
{
    <UpdateOrDelete>:{
        <Column Name>:{
            "type":<Column Type>,
            "where_handle":<Where Handle>,
            "value":<Column Value>
        },
        <Column Name>:{
            "type":<Column Type>,
            "where_handle":<Where Handle>,
            "value":<Column Value>
        }
    }
}
```

| 参数         | 类型   | 说明                    |
| :---------- | :----- | :--------------------- |
| UpdateOrDelete | String | 标识该 Event 是增加 Row 还是删除 Row，取值只可能是 "update"/"delete" |
| Column Name    | String | 列名   |
| Column Type    | Number | 列类型，详见：[Column 和 DDL 的类型码](/reference/tools/ticdc/column-ddl-type.md) |
| Where Handle   | Bool   | 表示该列是否可以作为 Where 筛选条件，当该列在表内具有唯一性时，Where Handle 为 true |
| Column Value   | Any    | 列值   |

### DDL Event

**Key:**

```json
{
    "ts":<TS>,
    "schema":<Schema Name>,
    "table":<Table Name>,
    "type":2
}
```

| 参数         | 类型   | 说明                                 |
| :---------- | :----- | :---------------------------------- |
| TS          | Number | 进行 DDL 变更的事务的 TS               |
| Schema Name | String | DDL 变更的 Schema 的名字，可能为空字符串 |
| Table Name  | String | DDL 变更的 Table 的名字，可能为空字符串  |

**Value:**

```json
{
    "query":<DDL Query>,
    "type":<DDL Type>
}
```

| 参数       | 类型   | 说明           |
| :-------- | :----- | :------------ |
| DDL Query | String | DDL Query SQL |
| DDL Type  | String | DDL 类型，详见：[Column 和 DDL 的类型码](/reference/tools/ticdc/column-ddl-type.md)       |

### Resolved Event

**Key:**

```json
{
    "ts":<TS>,
    "type":3
}
```

**Value:**

None

## 示例

设上游执行以下 SQL, MQ Partition 数量为 2：
```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));

BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;

BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

在 MQ 中将接收到：

```json
# DDL Event 将广播到所有 Partition
[partition=0] [key="{\"ts\":415508856908021766,\"schema\":\"test\",\"table\":\"t1\",\"type\":2}"] [value="{\"query\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"type\":3}"]
[partition=0] [key="{\"ts\":415508856908021766,\"type\":3}"] [value=]
[partition=1] [key="{\"ts\":415508856908021766,\"schema\":\"test\",\"table\":\"t1\",\"type\":2}"] [value="{\"query\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"type\":3}"]
[partition=1] [key="{\"ts\":415508856908021766,\"type\":3}"] [value=]

# 同一张表内的 Row Changed Event 可能会根据主键被分派到不同的 Partition，但同一行的变更一定会分派到同一个 Partition，方便下游并发处理。
[partition=0] [key="{\"ts\":415508878783938562,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":1},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"YWE=\"}}}"]
# 在一个事务内对同一行进行多次修改，只会发出一个 Row Changed Event
[partition=1] [key="{\"ts\":415508878783938562,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":2},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"YmI=\"}}}"]
[partition=0] [key="{\"ts\":415508878783938562,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":3},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"Y2M=\"}}}"]
# Row Changed Event 可能重复，但每个版本的 Event 第一次收到的次序一定是有序的
[partition=0] [key="{\"ts\":415508878783938562,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":3},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"Y2M=\"}}}"]

# Delete 类型的 Row Changed Event 只包含主键列或唯一索引列
[partition=0] [key="{\"ts\":415508881418485761,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"delete\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":1}}}"]
[partition=1] [key="{\"ts\":415508881418485761,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"delete\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":2}}}"]
[partition=0] [key="{\"ts\":415508881418485761,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":3},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"ZGQ=\"}}}"]
[partition=0] [key="{\"ts\":415508881418485761,\"schema\":\"test\",\"table\":\"t1\",\"type\":1}"] [value="{\"update\":{\"id\":{\"type\":3,\"where_handle\":true,\"value\":4},\"val\":{\"type\":15,\"where_handle\":false,\"value\":\"ZWU=\"}}}"]

# Resolved Event 意味着在这个 Partition 中，任意小于 Resolved TS 的 Event（包括 Row Changed Event 和 DDL Event） 已经发送完毕。
[partition=0] [key="{\"ts\":415508881038376963,\"type\":3}"] [value=]
[partition=1] [key="{\"ts\":415508881038376963,\"type\":3}"] [value=]
```