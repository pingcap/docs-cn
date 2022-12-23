---
title: Storage sink 消费程序开发指引
summary: 了解如何设计与实现一个 storage sink 的消费程序。
---

# Storage sink 消费程序设计

本文介绍如何设计和实现一个 TiDB 数据变更的消费程序。

> **注意：**
> 当前 Storage sink 无法处理 drop schema DDL，请你尽量避免执行 Drop schema DDL。如果你需要执行 drop schema DDL，请你也在下游 MySQL 手动执行。

TiCDC 不提供消费存储服务的数据的标准实现，以下介绍一个 Golang 版本的消费示例程序，该示例程序会读取存储服务中的数据并写入到下游 MySQL 兼容数据库。你可以参考本文档提供的数据格式和以下例子实现消费端。

[Golang 例子](https://github.com/pingcap/tiflow/tree/master/cmd/storage-consumer)

## Consumer 设计

下图是 Consumer 的整体消费流程：
![TiCDC storage consumer overview](/media/ticdc/ticdc-storage-consumer-overview.png)

以下是 Consumer 消费路程中的组件和功能定义，及其功能注释:

```
type StorageReader struct {
}

// Read the files from storage
// Add newly added files and delete files that not exist in storage
func (c *Consumer) ReadFiles() {}

// Query newly added files and the latest checkpoint from storage，one file can only be returned once
func (c *Consumer) ExposeNewFiles() (int64, []string) {}


// ConsumerManager is responsible for assigning tasks to TableConsumer.
// Different consumers can consume data concurrently,
// but data of one table must be processed by the same TableConsumer.
type ConsumerManager struct {
  // StorageCheckpoint indicates that the data whose transaction commit time is less than this checkpoint has been stored in storage
  StorageCheckpoint int64
  // it indicates where the consumer has consumed
  // ConsumerManager periodically collects TableConsumer.Checkpoint, 
  // then Checkpoint is updated to the minimum value of all TableConsumer.Checkpoint
  Checkpoint int64

  tableFiles[schema][table]*TableConsumer
}

// Query newly files from StorageReader
// For new created table, create a TableConsumer for the new table
// If any, send new files to the corresponding TableConsumer
func (c *ConsumerManager) Dispatch() {}


type TableConsumer struct {
  // it indicates where this TableConsumer has consumed
  // Its initial value is ConsumerManager.Checkpoint
  // TableConsumer.Checkpoint is equal to TableVersionConsumer.Checkpoint
  Checkpoint int64

  schema,table string
  // Must be consumed sequentially according to the table version order
  verConsumers map[version int64]*TableVersionConsumer
  currentVer, previousVer int64
}

// Send newly files to the corresponding TableVersionConsumer
// For any DDL, assign a TableVersionConsumer for the new table version
func (tc *TableConsumer) Dispatch() {}

// If DDL query is empty or its tableVersion is less than TableConsumer.Checkpoint, 
// - ignore this DDL, and consume the data under the table version
// Otherwise, 
// - execute DDL first, and then consume the data under the table version
// - But for dropped table, self recycling after drop table DDL is executed
func (tc *TableConsumer) ExecuteDDL() {}


type TableVersionConsumer struct {
  // it indicates where the TableVersionConsumer has consumed
  // Its initial value is TableConsumer.Checkpoint
  Checkpoint int64

  schema,table,version string
  // For same table version, data in different partitions can be consumed concurrently
  # partitionNum int64
  // Must be consumed sequentially according to the data file number
  fileSet map[filename string]*TableVersionConsumer
  currentVersion 
}

// If data commit ts is less than TableConsumer.Checkpoint 
// or bigger than ConsumerManager.StorageCheckpoint, 
// - ignore this data
// Otherwise, 
// - process this data and write it to MySQL
func (tc *TableVersionConsumer) ExecuteDML() {}
```

## DDL 事件的处理

举例来说，第一次遍历目录时目录内容如下：

```
├── metadata
└── test
    ├── tbl_1
    │   └── 437752935075545091
    │       ├── CDC000001.json
    │       └── schema.json
```

此时需要先解析 `schema.json` 文件中的表结构信息，从中获取 DDL query 语句，分为三种情况处理，接着再开始同步数据文件 `CDC000001.json`:

- 如果 Query 为空则忽略；
- 如果 TableVersion 小于 consumer checkpoint 则忽略；
- 否则，执行到下游 MySQL。

例如 `test/tbl_1/437752935075545091/schema.json` 文件内容如下：

```
{
    "Table":"test",
    "Schema":"tbl_1",
    "Version": 1,
    "TableVersion":437752935075545091,
    "Query": "create table tbl_1 (Id int primary key, LastName char(20), FirstName varchar(30), HireDate datetime, OfficeLocation Blob(20))",
    "TableColumns":[
        {
            "ColumnName":"Id",
            "ColumnType":"INT",
            "ColumnNullable":"false",
            "ColumnIsPk":"true"
        },
        {
            "ColumnName":"LastName",
            "ColumnType":"CHAR",
            "ColumnLength":"20"
        },
        {
            "ColumnName":"FirstName",
            "ColumnType":"VARCHAR",
            "ColumnLength":"30"
        },
        {
            "ColumnName":"HireDate",
            "ColumnType":"DATETIME"
        },
        {
            "ColumnName":"OfficeLocation",
            "ColumnType":"BLOB",
            "ColumnLength":"20"
        }
    ],
    "TableColumnsTotal":"5"
}
```

然后当程序又一次遍历目录，发现该表多出了一个新的版本目录。注意要在 `test/tbl_1/437752935075545091` 目录下所有文件消费完成后，然后才能开始消费新的目录下的数据。

```
├── metadata
└── test
    ├── tbl_1
    │   ├── 437752935075545091
    │   │   ├── CDC000001.json
    │   │   └── schema.json
    │   └── 437752935075546092
    │   │   └── CDC000001.json
    │   │   └── schema.json
```

消费逻辑跟上述一致，先解析 `schema.json` 文件中的表结构信息，从中获取 DDL query 语句，分为前文中提到的三种情况处理，接着再开始同步数据文件 `CDC000001.json`。

## 数据事件的处理

根据 `{schema}/{table}/{table-version-separator}/schema.json` 文件处理好 DDL 事件后，就可以在 `{schema}/{table}/{table-version-separator}/` 目录下，根据具体的文件格式并按照文件序号依次处理数据变更事件。

因为 TiCDC 提供 At Least Once 语义，可能出现重复发送数据的情况，所以需要在消费程序中对比数据事件的 commit ts 和 consumer checkpoint，如果 commit ts 小于 consumer checkpoint 则做去重处理。
