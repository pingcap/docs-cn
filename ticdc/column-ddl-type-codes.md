---
title: Column 和 DDL 的类型码
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/column-ddl-type/']
---

# Column 和 DDL 的类型码

Column 和 DDL 的类型码是由 [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md) 定义的 Column 和 DDL 类型编码，Column Type Code 标识 Row Changed Event 中的列数据类型，DDL Type Code 标识 DDL Event 中的 DDL 语句类型。

## Column Type Code

| 类型         | Code | 输出示例 | 说明 |
| :---------- | :--- | :------ | :-- |
| Decimal     | 0    | {"t":0,"v":"129012.1230000"} | |
| Tiny/Bool   | 1    | {"t":1,"v":1} | |
| Short       | 2    | {"t":2,"v":1} | |
| Long        | 3    | {"t":3,"v":123} | |
| Float       | 4    | {"t":4,"v":153.123} | |
| Double      | 5    | {"t":5,"v":153.123} | |
| Null        | 6    | {"t":6,"v":null} | |
| Timestamp   | 7    | {"t":7,"v":"1973-12-30 15:30:00"} | |
| Longlong    | 8    | {"t":8,"v":123} | |
| Int24       | 9    | {"t":9,"v":123} | |
| Date        | 10   | {"t":10,"v":"2000-01-01"} | |
| Duration    | 11   | {"t":11,"v":"23:59:59"} | |
| Datetime    | 12   | {"t":12,"v":"2015-12-20 23:58:58"} | |
| Year        | 13   | {"t":13,"v":1970} | |
| New Date    | 14   | {"t":14,"v":"2000-01-01"} | |
| Varchar     | 15   | {"t":15,"v":"测试"} | value 编码为 UTF-8 |
| Bit         | 16   | {"t":16,"v":81} | |
| JSON        | 245  | {"t":245,"v":"{\\"key1\\": \\"value1\\"}"} | |
| New Decimal | 246  | {"t":246,"v":"129012.1230000"} | |
| Enum        | 247  | {"t":247,"v":1} | |
| Set         | 248  | {"t":248,"v":3} | |
| Tiny Blob   | 249  | {"t":249,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| Medium Blob | 250  | {"t":250,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| Long Blob   | 251  | {"t":251,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| Blob        | 252  | {"t":252,"v":"5rWL6K+VdGV4dA=="} | value 编码为 Base64 |
| Var String  | 253  | {"t":253,"v":"测试"} | value 编码为 UTF-8 |
| String      | 254  | {"t":254,"v":"测试"} | value 编码为 UTF-8 |
| Geometry    | 255  |  | 尚不支持 |

## DDL Type Code

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
