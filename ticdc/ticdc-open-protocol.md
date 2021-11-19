---
title: TiCDC Open Protocol
---

# TiCDC Open Protocol

## 概述

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ(Message Queue) 等第三方数据媒介复制 TiDB 的数据变更。

TiCDC Open Protocol 以 Event 为基本单位向下游复制数据变更事件，Event 分为三类：

* Row Changed Event：代表一行的数据变化，在行发生变更时该 Event 被发出，包含变更后该行的相关信息。
* DDL Event：代表 DDL 变更，在上游成功执行 DDL 后发出，DDL Event 会广播到每一个 MQ Partition 中。
* Resolved Event：代表一个特殊的时间点，表示在这个时间点前的收到的 Event 是完整的。

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

    `Insert` 事件，输出新增的行数据。

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Update` 事件，输出新增的行数据 ("u") 以及修改前的行数据 ("p")，仅当 Old Value 特性开启时，才会输出修改前的行数据。

    ```
    {
        "u":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        },
        "p":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

    `Delete` 事件，输出被删除的行数据。当 Old Value 特性开启时，`Delete` 事件中包含被删除的行数据中的所有列；当 Old Value 特性关闭时，`Delete` 事件中仅包含 [HandleKey](#列标志位) 列。

    ```
    {
        "d":{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "f":<Flag>,
                "v":<Column Value>
            }
        }
    }
    ```

| 参数         | 类型   | 说明                    |
| :---------- | :----- | :--------------------- |
| Column Name    | String | 列名   |
| Column Type    | Number | 列类型，详见：[Column 的类型码](#column-的类型码) |
| Where Handle   | Bool   | 表示该列是否可以作为 Where 筛选条件，当该列在表内具有唯一性时，Where Handle 为 true。 |
| Flag           | Number | 列标志位，详见：[列标志位](#列标志位) |
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
    | DDL Type  | String | DDL 类型，详见：[DDL 的类型码](#ddl-的类型码)  |

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

## 消费端协议解析

目前 TiCDC 没有提供 Open Protocol 协议解析的标准实现，但是提供了 Golang 版本和 Java 版本的解析 demo。用户可以参考本文档提供的数据格式和以下 demo 实现消费端协议解析。

- [Golang demo](https://github.com/pingcap/ticdc/tree/master/cmd/kafka-consumer)
- [Java demo](https://github.com/pingcap/ticdc/tree/master/demo/java)

## Column 的类型码

Column 的类型码用于标识 Row Changed Event 中列的数据类型。

| 类型                   | Code | 输出示例 | 说明 |
| :-------------------- | :--- | :------ | :-- |
| TINYINT/BOOL          | 1    | {"t":1,"v":1} | |
| SMALLINT              | 2    | {"t":2,"v":1} | |
| INT                   | 3    | {"t":3,"v":123} | |
| FLOAT                 | 4    | {"t":4,"v":153.123} | |
| DOUBLE                | 5    | {"t":5,"v":153.123} | |
| NULL                  | 6    | {"t":6,"v":null} | |
| TIMESTAMP             | 7    | {"t":7,"v":"1973-12-30 15:30:00"} | |
| BIGINT                | 8    | {"t":8,"v":123} | |
| MEDIUMINT             | 9    | {"t":9,"v":123} | |
| DATE                  | 10/14   | {"t":10,"v":"2000-01-01"} | |
| TIME                  | 11   | {"t":11,"v":"23:59:59"} | |
| DATETIME              | 12   | {"t":12,"v":"2015-12-20 23:58:58"} | |
| YEAR                  | 13   | {"t":13,"v":1970} | |
| VARCHAR/VARBINARY     | 15/253   | {"t":15,"v":"测试"} / {"t":15,"v":"\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n"} | value 编码为 UTF-8；当上游类型为 VARBINARY 时，将对不可见的字符转义 |
| BIT                   | 16   | {"t":16,"v":81} | |
| JSON                  | 245  | {"t":245,"v":"{\\"key1\\": \\"value1\\"}"} | |
| DECIMAL               | 246  | {"t":246,"v":"129012.1230000"} | |
| ENUM                  | 247  | {"t":247,"v":1} | |
| SET                   | 248  | {"t":248,"v":3} | |
| TINYTEXT/TINYBLOB     | 249  | {"t":249,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| MEDIUMTEXT/MEDIUMBLOB | 250  | {"t":250,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| LONGTEXT/LONGBLOB     | 251  | {"t":251,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| TEXT/BLOB             | 252  | {"t":252,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| CHAR/BINARY           | 254  | {"t":254,"v":"测试"} / {"t":254,"v":"\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n"} | value 编码为 UTF-8；当上游类型为 BINARY 时，将对不可见的字符转义 |
| GEOMETRY              | 255  |  | 尚不支持 |

## DDL 的类型码

DDL 的类型码用于标识 DDL Event 中的 DDL 语句的类型。

| 类型                               | Code |
| :-------------------------------- | :- |
| Create Schema                     | 1  |
| Drop Schema                       | 2  |
| Create Table                      | 3  |
| Drop Table                        | 4  |
| Add Column                        | 5  |
| Drop Column                       | 6  |
| Add Index                         | 7  |
| Drop Index                        | 8  |
| Add Foreign Key                   | 9  |
| Drop Foreign Key                  | 10 |
| Truncate Table                    | 11 |
| Modify Column                     | 12 |
| Rebase Auto ID                    | 13 |
| Rename Table                      | 14 |
| Set Default Value                 | 15 |
| Shard RowID                       | 16 |
| Modify Table Comment              | 17 |
| Rename Index                      | 18 |
| Add Table Partition               | 19 |
| Drop Table Partition              | 20 |
| Create View                       | 21 |
| Modify Table Charset And Collate  | 22 |
| Truncate Table Partition          | 23 |
| Drop View                         | 24 |
| Recover Table                     | 25 |
| Modify Schema Charset And Collate | 26 |
| Lock Table                        | 27 |
| Unlock Table                      | 28 |
| Repair Table                      | 29 |
| Set TiFlash Replica               | 30 |
| Update TiFlash Replica Status     | 31 |
| Add Primary Key                   | 32 |
| Drop Primary Key                  | 33 |
| Create Sequence                   | 34 |
| Alter Sequence                    | 35 |
| Drop Sequence                     | 36 |

## 列标志位

列标志位以 Bit flags 形式标记列的相关属性。

| 位移 | 值 | 名称 | 说明 |
| :-- | :- | :- | :- |
| 1   | 0x01 | BinaryFlag          | 该列是否为二进制编码列  |
| 2   | 0x02 | HandleKeyFlag       | 该列是否为 Handle 列 |
| 3   | 0x04 | GeneratedColumnFlag | 该列是否为生成列      |
| 4   | 0x08 | PrimaryKeyFlag      | 该列是否为主键列      |
| 5   | 0x10 | UniqueKeyFlag       | 该列是否为唯一索引列   |
| 6   | 0x20 | MultipleKeyFlag     | 该列是否为组合索引列   |
| 7   | 0x40 | NullableFlag        | 该列是否为可空列       |
| 8   | 0x80 | UnsignedFlag        | 该列是否为无符号列     |

示例：

若某列 Flag 值为 85，则代表这一列为可空列、唯一索引列、生成列、二进制编码列。

```
85 == 0b_101_0101
   == NullableFlag | UniqueKeyFlag | GeneratedColumnFlag | BinaryFlag
```

若某列 Flag 值为 46，则代表这一列为组合索引列、主键列、生成列、Handle 列。

```
46 == 0b_010_1110
   == MultipleKeyFlag | PrimaryKeyFlag | GeneratedColumnFlag | HandleKeyFlag
```

> **注意：**
>
> + BinaryFlag 仅在列为 BLOB/TEXT（包括 TINYBLOB/TINYTEXT、BINARY/CHAR 等）类型时才有意义。当上游列为 BLOB 类型时，BinaryFlag 置 `1`；当上游列为 TEXT 类型时，BinaryFlag 置 `0`。
> + 若要同步上游的一张表，TiCDC 会选择一个[有效索引](/ticdc/ticdc-overview.md#同步限制)作为 Handle Index。Handle Index 包含的列的 HandleKeyFlag 置 `1`。
