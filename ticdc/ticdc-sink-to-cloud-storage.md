---
title: 同步数据到存储服务
summary: 了解如何使用 TiCDC 将数据同步到存储服务，同时理解数据的存储方式
---

# 同步数据到存储服务

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

从 v6.5.0 开始，TiCDC 支持将行变更事件保存至 S3、Azure Blob Storage 和 NFS 中。本文介绍如何使用 TiCDC 创建同步任务 (Changefeed) 将增量数据同步到云存储。本文组织如下：

- 如何将变更数据同步至存储服务。
- 变更数据如何在存储服务中保存。

## 同步变更数据至存储服务

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2022-11-29T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0-master-dirty"}
```

- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，需在此参数中配置 S3、Azure Blob Storage 和 NFS 的相关参数，TiCDC 中存储服务的 URI 参数与 BR 中存储 URL 相同，具体可参考[备份存储 URL 格式说明](/br/backup-and-restore-storages.md#格式说明)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 配置 Sink URI

本章节介绍如何在 Changefeed URI 中配置 `S3`、`Azure Blob Storage` 和 `NFS`。

### Sink URI 配置 S3

S3 的 URL 参数与 BR 相同，详细参数请参考 [S3 的 URL 参数](/br/backup-and-restore-storages.md#s3-的-url-参数)。

### Sink URI 配置 Azure Blob Storage

Azure Blob Storage 的 URL 参数与 BR 相同，详细参数请参考 [Azblob 的 URL 参数](/br/backup-and-restore-storages.md#azblob-的-url-参数)

### Sink URI 配置 NFS

NFS 配置样例如下：

```
shell
--sink-uri="file:///my-directory/prefix"
```

URI 中其他可配置的参数如下：

| 参数         | 描述                                             |
| :------------ | :------------------------------------------------ |
| `worker-count` | 向下游云存储保存数据变更记录的并发度（可选，默认值为 `16`，取值范围：[1, 512]）。 |
| `flush-interval` | 向下游云存储保存数据变更记录的间隔（可选，默认值为 `5s`，取值范围：[2s, 10m]) 。 |
| `file-size` | 单个数据变更文件的字节数超过 `file-size` 时将其保存至云存储中（可选，默认值为 `67108864`，取值范围：[1048576, 536870912])。 |
| `protocol` | 输出到存储服务的消息协议，可选值有 `canal-json` 和 `csv`。 |

> **注意：**
>
> `flush-interval` 与 `file-size` 二者只要满足其一就会向下游写入数据变更文件。

## 存储路径组织结构

本部分详细介绍数据变更记录、元数据与 DDL 事件的存储路径组织结构。

### 数据变更记录

数据变更记录将会存储到以下路径：

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

- `scheme`：`scheme` 为数据传输协议，即存储类型。例如：`s3://xxxxx`。
- `prefix`：`prefix` 为用户指定的父目录。例如：`s3://bucket/bbb/ccc`。
- `schema`：`schema` 为表所属的库名。例如：`s3://bucket/bbb/ccc/test`。
- `table`：`table` 为表名。例如：`s3://bucket/bbb/ccc/test/table1`。
- `table-version-separator`：将文件路径按照表的版本进行分隔。例如：`s3://bucket/bbb/ccc/test/table1/9999`。
- `partition-separator`：将文件路径按照表的分区号进行分隔。例如：`s3://bucket/bbb/ccc/test/table1/9999/20`。
- `date-separator`：将文件路径按照事务提交的日期进行分隔。date-separator 可选值如下：
    - `none`：不以 date-separator 分隔文件路径。例如：`test.table1` 版本号为 9999 的所有文件都存到 `s3://bucket/bbb/ccc/test/table1/9999` 路径下。
    - `year`：以事务提交的年份分隔文件路径。例如：`s3://bucket/bbb/ccc/test/table1/9999/2022`。
    - `month`：以事务提交的年份和月份分隔文件路径。例如：`s3://bucket/bbb/ccc/test/table1/9999/2022-01`。
    - `day`：以事务提交的年月日来分隔文件路径。例如：`s3://bucket/bbb/ccc/test/table1/9999/2022-01-02`。
- `num`：存储数据变更记录的目录下文件的序号。例如：`s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC000005.csv`。
- `extension`：文件的扩展名，v6.5.0 支持 csv 和 canal-json 格式。

> **注意：**
> 
> 表的版本会在以下两种情况下发生变化：
> 
> - 发生过对该表的 DDL 操作，表的版本为该 DDL 在上游 TiDB 执行结束的 TSO，但表版本的变化并不意味着表结构的变化，如为表中某一列添加 comment，并不会造成 `schema.json` 文件内容相较于旧版本发生变化。
> - 进程重启，表的版本为进程重启时 changefeed 的 checkpoint TSO。之所以不在旧版本的目录下继续写入数据而是在一个以 checkpoint TSO 为版本的新目录下写入数据，是因为在表数量多的情况下重启时需要遍历出所有的目录并找出上一次重启每张表写入的位置，该操作较为耗时进而影响同步进度。

### 元数据

元数据信息将会存储到以下路径：

```shell
{scheme}://{prefix}/metadata
```

元数据信息以 JSON 格式存储到如下的文件中：

```shell
{
    "checkpoint-ts":433305438660591626
}
```

- checkpoint-ts: commit-ts 小于等于此 checkpoint-ts 的事务都被写入下游存储当中。

### DDL 事件

当 DDL 事件引起表的版本变更时，TiCDC 将会切换到新的路径下写入数据变更记录，例如 `test.table1` 的版本从 `9999` 变更为 `10000` 时将会在 `s3://bucket/bbb/ccc/test/table1/10000/2022-01-02/CDC000001.csv` 路径中写入数据。并且，当 DDL 事件发生时，TiCDC 将生成一个 `schema.json` 文件存储表结构信息。

表结构信息将会存储到以下路径：

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/schema.json
```

一个示例 `schema.json` 文件如下：

```shell
{
    "Table":"table1",
    "Schema":"test",
    "Version":123123,
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

- `Table`：表名。
- `Schema`：表所属的库名。
- `Version`：表的版本号。
- `TableColumns`：该数组表示表中每一列的详细信息。
    - `ColumnName`：列名。
    - `ColumnType`：该列的类型。详见 [数据类型](/ticdc/ticdc-sink-to-cloud-storage.md#数据类型)。
    - `ColumnLength`：该列的长度。详见 [数据类型](/ticdc/ticdc-sink-to-cloud-storage.md#数据类型)。
    - `ColumnPrecision`：该列的精度。详见 [数据类型](/ticdc/ticdc-sink-to-cloud-storage.md#数据类型)。
    - `ColumnScale`：该列小数位的长度。详见 [数据类型](/ticdc/ticdc-sink-to-cloud-storage.md#数据类型)。
    - `ColumnNullable`：值为 true 时表示该列可以含 NULL 值。
    - `ColumnIsPk`：值为 true 时表示该列是主键的一部分。
- `TableColumnsTotal`：TableColumns 数组的大小。

## 数据类型

本部分主要介绍 `schema.json` 文件中使用的各种数据类型。数据类型定义为 `T(M[, D])`，详见[数据类型概述](/data-type-overview.md#数据类型概述)。

### 整数类型

TiDB 中整数类型可被定义为 `IT[(M)] [UNSIGNED]`，其中：

- IT 为整数类型，包括 `TINYINT`、`SMALLINT`、`MEDIUMINT`、`INT`、`BIGINT` 和 `BIT`。
- M 为该类型的显示宽度。

故 `schema.json` 文件中对整数类型定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

### 小数类型

TiDB 中的小数类型可被定义为 `DT[(M,D)][UNSIGNED]`，其中：

- DT 为小数类型，包括 `FLOAT`、`DOUBLE`、`DECIMAL` 和 `NUMERIC`。
- M 为该类型数据的精度，即整数位加上小数位的总长度。
- D 为小数位的长度。

故 `schema.json` 文件中对小数类型的定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

### 时间和日期类型

TiDB 中的日期类型可被定义为 `DT`，其中：

- DT 为日期类型，包括 `DATE` 和 `YEAR`。

故 `schema.json` 文件中对日期类型的定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

TiDB 中的时间类型可被定义为 `TT[(M)]`，其中：

- TT 为时间类型，包括 `TIME`、`DATETIME` 和 `TIMESTAMP`。
- M 为秒的精度，取值范围为 0~6。

故 `schema.json` 文件中对时间类型的定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

### 字符串类型

TiDB 中的字符串类型可被定义为 `ST[(M)]`，其中：

- ST 为字符串类型，包括 `CHAR`、`VARCHAR`、`TEXT`、`BINARY`、`BLOB`、`JSON` 等。
- M 表示字符串的最大长度。

故 `schema.json` 文件中对字符串类型的定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

### Enum/Set 类型

`schema.json` 文件中对 enum/set 类型的定义如下：

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
