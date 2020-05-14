---
title: TiCDC Open Protocol
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/open-protocol/']
---

# TiCDC Open Protocol

## 概述

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ(Message Queue) 等第三方数据媒介复制 TiDB 的数据变更。

TiCDC Open Protocol 以 Event 为基本单位向下游复制数据变更事件，Event 分为三类：

* Row Changed Event：代表一行的数据变化，在行发生变更时该 Event 被发出，包含变更后该行的相关信息。
* DDL Event：代表 DDL 变更，在上游成功执行 DDL 后发出，DDL Event 会广播到每一个 MQ Partition 中
* Resolved Event：代表一个特殊的时间点，表示在这个时间点前的收到的 Event 是完整的

## 协议约束

* 在绝大多数情况下，一个版本的 Row Changed Event 只会发出一次，但是特殊情况（节点故障、网络分区等）下，同一版本的 Row Changed Event 可能会多次发送。
* 同一张表中的每一个版本第一次发出的 Row Changed Event 在 Event 流中一定是按 TS (timestamp) 顺序递增的。
* Resolved Event 会被周期性的广播到各个 MQ Partition，Resolved Event 意味着任何 TS 小于 Resolved Event TS 的 Event 已经发送给下游。
* DDL Event 将被广播到各个 MQ Partition。
* 一行数据的多个 Row Changed Event 一定会被发送到同一个 MQ Partition 中。

## Message 格式定义

一个 Message 中包含一个或多个 Event，按照以下格式排列：

Key:

| Offset(Byte) | 0~7     | 8~15 | 16~(15+长度1) | ... | ... |
| :----------- | :------ | :--- | :----------- | :--- | :----------- |
| 参数         | 协议版本号 | 长度1 | Event Key1         | 长度N | Event KeyN         |

Value:

| Offset(Byte) | 0~7 | 8~(7+长度1) | ... | ... |
| :----------- | :--- | :-------- | :--- | :------ |
| 参数         | 长度1 | Event Value1     | 长度N | Event ValueN |

* `长度N`代表第 `N` 个 Key/Value 的长度
* 长度及协议版本号均为大端序 int64 类型
* 当前协议版本号为 `1`

## Event 格式定义

本部分介绍 Row Changed Event、DDL Event 和 Resolved Event 的格式定义。

### Row Changed Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":1
    }
    ```

    | 参数         | 类型   | 说明                    |
    | :---------- | :----- | :--------------------- |
    | TS          | Number | 造成 Row 变更的事务的 TS  |
    | Schema Name | String | Row 所在的 Schema 的名字 |
    | Table Name  | String | Row 所在的 Table 的名字  |

+ **Value:**

    ```
    {
        <UpdateOrDelete>:{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            }
        }
    }
    ```

    | 参数         | 类型   | 说明                    |
    | :---------- | :----- | :--------------------- |
    | UpdateOrDelete | String | 标识该 Event 是增加 Row 还是删除 Row，取值只可能是 "u"/"d" |
    | Column Name    | String | 列名   |
    | Column Type    | Number | 列类型，详见：[Column 和 DDL 的类型码](/ticdc/column-ddl-type-codes.md) |
    | Where Handle   | Bool   | 表示该列是否可以作为 Where 筛选条件，当该列在表内具有唯一性时，Where Handle 为 true |
    | Column Value   | Any    | 列值   |

### DDL Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | 参数         | 类型   | 说明                                 |
    | :---------- | :----- | :---------------------------------- |
    | TS          | Number | 进行 DDL 变更的事务的 TS               |
    | Schema Name | String | DDL 变更的 Schema 的名字，可能为空字符串 |
    | Table Name  | String | DDL 变更的 Table 的名字，可能为空字符串  |

+ **Value:**

    ```
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | 参数       | 类型   | 说明           |
    | :-------- | :----- | :------------ |
    | DDL Query | String | DDL Query SQL |
    | DDL Type  | String | DDL 类型，详见：[Column 和 DDL 的类型码](/ticdc/column-ddl-type-codes.md)      |

### Resolved Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | 参数         | 类型   | 说明                                         |
    | :---------- | :----- | :------------------------------------------ |
    | TS          | Number | Resolved TS，任意小于该 TS 的 Event 已经发送完毕 |

+ **Value:** None

## Event 流的输出示例

本部分展示并描述 Event 流的输出日志。

假设在上游执行以下 SQL 语句，MQ Partition 数量为 2：

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

如以下执行日志中的 Log 1、Log 3 所示，DDL Event 将被广播到所有 MQ Partition，Resolved Event 会被周期性地广播到各个 MQ Partition：

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

在上游执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

+ 如以下执行日志中的 Log 5 和 Log 6 所示，同一张表内的 Row Changed Event 可能会根据主键被分派到不同的 Partition，但同一行的变更一定会分派到同一个 Partition，方便下游并发处理。
+ 如 Log 6 所示，在一个事务内对同一行进行多次修改，只会发出一个 Row Changed Event。
+ Log 8 是 Log 7 的重复 Event。Row Changed Event 可能重复，但每个版本的 Event 第一次发出的次序一定是有序的。

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

在上游执行以下 SQL 语句：

{{< copyable "sql" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

+ Log 9 是 `Delete` 类型的 Row Changed Event，这种类型的 Event 只包含主键列或唯一索引列。
+ Log 13 和 Log 14 是 Resolved Event。Resolved Event 意味着在这个 Partition 中，任意小于 Resolved TS 的 Event（包括 Row Changed Event 和 DDL Event）已经发送完毕。

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```
