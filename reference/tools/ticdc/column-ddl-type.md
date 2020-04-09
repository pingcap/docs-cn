---
title: Column 和 DDL 的类型码
category: reference
---

# Column 和 DDL 的类型码

Column 和 DDL 的类型码是由 Open TiCDC Protocol 定义的 Column 和 DDL 类型编码，Column Type Code 标识 Row Changed Event 中的列数据类型，DDL Type Code 标识 DDL Event 中的 DDL 语句类型。

## Column Type Code

| 类型         | Code | 
| :---------- | :--- | 
| Decimal     | 0    |
| Tiny        | 1    |
| Short       | 2    |
| Long        | 3    |
| Float       | 4    |
| Double      | 5    |
| Null        | 6    |
| Timestamp   | 7    |
| Longlong    | 8    |
| Int24       | 9    |
| Date        | 10   |
| Duration    | 11   |
| Datetime    | 12   |
| Year        | 13   |
| New Date    | 14   |
| Varchar     | 15   |
| Bit         | 16   |
| JSON        | 0xf5 |
| New Decimal | 0xf6 |
| Enum        | 0xf7 |
| Set         | 0xf8 |
| Tiny Blob   | 0xf9 |
| Medium Blob | 0xfa |
| Long Blob   | 0xfb |
| Blob        | 0xfc |
| Var String  | 0xfd |
| String      | 0xfe |
| Geometry    | 0xff |

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
