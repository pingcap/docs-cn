---
title: 同步数据到存储服务
summary: 了解如何使用 TiCDC 将数据同步到存储服务，以及数据变更记录的存储路径。
---

# 同步数据到存储服务

从 TiDB v6.5.0 开始，TiCDC 支持将行变更事件保存至存储服务，如 Amazon S3、GCS、Azure Blob Storage 和 NFS。本文介绍如何使用 TiCDC 创建同步任务 (Changefeed) 将增量数据同步到这类存储服务，并介绍数据的存储方式。具体如下：

- [如何将变更数据同步至存储服务](#同步变更数据至存储服务)。
- [变更数据如何在存储服务中保存](#存储路径组织结构)。

## 同步变更数据至存储服务

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

输出结果如下：

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2024-08-22T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.3.0"}
```

- `--server`：TiCDC 集群中任意一个 TiCDC 服务器的地址。
- `--changefeed-id`：同步任务的 ID。格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址。具体可参考[配置 Sink URI](#配置-sink-uri)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见 [TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 配置 Sink URI

本章节介绍如何在 Sink URI 中配置存储服务 Amazon S3、GCS、Azure Blob Storage 以及 NFS。Sink URI 用于指定 TiCDC 下游系统的连接信息，遵循以下格式：

```shell
[scheme]://[host]/[path]?[query_parameters]
```

URI 的 `[query_parameters]` 中可配置的参数如下：

| 参数              | 描述                                                   | 默认值      | 取值范围                 |
| :--------------- | :----------------------------------------------------- | :--------- | :--------------------- |
| `worker-count`   | 向下游存储服务保存数据变更记录的并发度                       | `16`       | `[1, 512]`             |
| `flush-interval` | 向下游存储服务保存数据变更记录的间隔                         | `5s`       | `[2s, 10m]`            |
| `file-size`      | 单个数据变更文件的字节数超过 `file-size` 时将其保存至存储服务中| `67108864` | `[1048576, 536870912]` |
| `protocol`       | 输出到存储服务的消息协议                                  | N/A         | `canal-json` 和 `csv`  |
| `enable-tidb-extension` | `protocol` 参数为 `canal-json` 时，如果该值为 `true`，TiCDC 会发送 [WATERMARK 事件](/ticdc/ticdc-canal-json.md#watermark-event)，并在 canal-json 消息中添加 [TiDB 扩展字段](/ticdc/ticdc-canal-json.md#tidb-扩展字段)。 | `false` | `false` 和 `true` |

> **注意：**
>
> `flush-interval` 与 `file-size` 二者只要满足其一就会向下游写入数据变更文件。
> 
> `protocol` 是必选配置，如果 TiCDC 在创建 changefeed 时未解析到该配置，将会返回 `CDC:ErrSinkUnknownProtocol` 错误。

### 配置外部存储

将数据存储到云服务存储系统时，根据云服务供应商的不同，需要设置不同的鉴权参数。本节介绍使用 Amazon S3、Google Cloud Storage (GCS) 及 Azure Blob Storage 时所用存储服务的鉴权方式以及如何配置访问相应存储服务的账户。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

Amazon S3 配置样例如下：

```shell
--sink-uri="s3://bucket/prefix?protocol=canal-json"
```

在同步数据之前，需要为 Amazon S3 中的目录设置相应的访问权限：

- TiCDC 需要的最小权限是：`s3:ListBucket`、`s3:PutObject` 和 `s3:GetObject`。
- 如果 changefeed 的参数 `sink.cloud-storage-config.flush-concurrency` 大于 1，表示开启了单文件的并行上传，需要额外增加 [ListParts](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/API/API_ListParts.html) 相关权限： 
    - `s3:AbortMultipartUpload`
    - `s3:ListMultipartUploadParts`
    - `s3:ListBucketMultipartUploads`

如果你还没有创建同步数据保存目录，可以参考[创建存储桶](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的区域中创建一个 S3 存储桶。如果需要使用文件夹，可以参考[使用文件夹在 Amazon S3 控制台中组织对象](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)在存储桶中创建一个文件夹。

可以通过以下两种方式配置访问 Amazon S3 的账户：

- 方式一：指定访问密钥

    如果指定访问密钥和秘密访问密钥，将按照指定的访问密钥和秘密访问密钥进行鉴权。除了在 URI 中指定密钥外，还支持以下方式：

    - 读取 `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量
    - 读取 `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量
    - 读取共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定
    - 读取共享凭证文件，路径为 `~/.aws/credentials`

- 方式二：基于 IAM Role 进行访问

    为运行 TiCDC Server 的 EC2 实例关联一个[配置了访问 S3 访问权限的 IAM role](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html)。设置成功后，TiCDC 可以直接访问对应的 S3 中的备份目录，而不需要额外的设置。

</div>
<div label="GCS" value="gcs">

GCS 配置样例如下：

```shell
--sink-uri="gcs://bucket/prefix?protocol=canal-json"
```

配置访问 GCS 的账户可以通过指定访问密钥的方式。如果指定了 `credentials-file` 参数，将按照指定的 `credentials-file` 进行鉴权。除了在 URI 中指定密钥文件外，还支持以下方式：

- 读取位于 `$GOOGLE_APPLICATION_CREDENTIALS` 环境变量所指定路径的文件内容
- 读取位于 `~/.config/gcloud/application_default_credentials.json` 的文件内容
- 在 GCE 或 GAE 中运行时，从元数据服务器中获取的凭证

</div>
<div label="Azure Blob Storage" value="azure">

Azure Blob Storage 配置样例如下：

```shell
--sink-uri="azure://bucket/prefix?protocol=canal-json"
```

可以通过以下方式配置访问 Azure Blob Storage 的账户：

- 方式一：指定共享访问签名

    在 URI 中配置 `account-name` 和 `sas-token`，则使用该参数指定的存储账户名和共享访问签名令牌。由于共享访问签名令牌中带有 `&` 的字符，需要将其编码为 `%26` 后再添加到 URI 中。你也可以直接对整个 `sas-token` 进行一次百分号编码。

- 方式二：指定访问密钥

    在 URI 中配置 `account-name` 和 `account-key`，则使用该参数指定的存储账户名和密钥。除了在 URI 中指定密钥文件外，还支持读取 `$AZURE_STORAGE_KEY` 的方式。

- 方式三：使用 Azure AD 备份恢复

    运行环境配置 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

</div>
</SimpleTab>

> **建议：**
>
> 关于 Amazon S3、GCS 以及 Azure Blob Storage 的 URI 参数的详细参数说明，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

### 配置 NFS

NFS 配置样例如下：

```shell
--sink-uri="file:///my-directory/prefix?protocol=canal-json"
```

## 存储路径组织结构

本章节详细介绍数据变更记录、元数据与 DDL 事件的存储路径组织结构。

### 数据变更记录

数据变更记录将会存储到以下路径：

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

- `scheme`：存储服务类型。例如：`s3`、`gcs`、`azure`、`file`。
- `prefix`：用户指定的父目录。例如：<code>s3://**bucket/bbb/ccc**</code>。
- `schema`：表所属的库名。例如：<code>s3://bucket/bbb/ccc/**test**</code>。
- `table`：表名。例如：<code>s3://bucket/bbb/ccc/test/**table1**</code>。
- `table-version-separator`：将文件路径按照表的版本进行分隔。例如：<code>s3://bucket/bbb/ccc/test/table1/**9999**</code>。
- `partition-separator`：将文件路径按照表的分区号进行分隔。例如：<code>s3://bucket/bbb/ccc/test/table1/9999/**20**</code>。
- `date-separator`：将文件路径按照事务提交的日期进行分隔，默认值为 `day`，可选值如下：
    - `none`：不以 `date-separator` 分隔文件路径。例如：`test.table1` 版本号为 `9999` 的所有文件都存到 `s3://bucket/bbb/ccc/test/table1/9999` 路径下。
    - `year`：以事务提交的年份分隔文件路径。例如：<code>s3://bucket/bbb/ccc/test/table1/9999/**2022**</code>。
    - `month`：以事务提交的年份和月份分隔文件路径。例如：<code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01**</code>。
    - `day`：以事务提交的年月日来分隔文件路径。例如：<code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01-02**</code>。
- `num`：存储数据变更记录的目录下文件的序号。例如：<code>s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC**000005**.csv</code>。
- `extension`：文件的扩展名。v6.5.0 支持 CSV 和 Canal-JSON 格式。

> **注意：**
>
> 表的版本在以下情况下会发生变化：
>
> - 上游 TiDB 对该表执行了 DDL 操作
> - TiCDC 对该表进行了节点间的调度
> - 该表所属的 Changefeed 重启
> 
> 注意，表版本的变化并不意味着表结构的变化。例如，在表中的某一列添加注释，不会导致 schema 文件内容发生变化。

### Index 文件

Index 文件用于防止已写入的数据被错误覆盖，与数据变更记录存储在相同路径：

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/meta/CDC.index
```

Index 文件记录了当前目录下所使用到的最大文件名，比如：

```
CDC000005.csv
```

上述内容表明该目录下 `CDC000001.csv` 到 `CDC000004.csv` 文件已被占用，当 TiCDC 集群中发生表调度或者节点重启时，新的节点会读取 Index 文件，并判断 `CDC000005.csv` 是否被占用。如果未被占用，则新节点会从 `CDC000005.csv` 开始写文件。如果已被占用，则从 `CDC000006.csv` 开始写文件，这样可防止覆盖其他节点写入的数据。

### 元数据

元数据信息将会存储到以下路径：

```shell
{scheme}://{prefix}/metadata
```

元数据信息以 JSON 格式存储到如下的文件中：

```json
{
    "checkpoint-ts":433305438660591626
}
```

- `checkpoint-ts`：commit-ts 小于等于此 `checkpoint-ts` 的事务都被写入下游存储当中。

### DDL 事件

#### 表级 DDL 事件

当上游表的 DDL 事件引起表的版本变更时，TiCDC 将会自动进行以下操作：

- 切换到新的路径下写入数据变更记录。例如，当 `test.table1` 的版本变更为 `441349361156227074` 时，TiCDC 将会在 `s3://bucket/bbb/ccc/test/table1/441349361156227074/2022-01-02/` 路径下写入数据。
- 生成一个 schema 文件存储表结构信息，文件路径如下：

    ```shell
    {scheme}://{prefix}/{schema}/{table}/meta/schema_{table-version}_{hash}.json
    ```

以 `schema_441349361156227074_3131721815.json` 为例，表结构信息文件的内容如下：

```json
{
    "Table":"table1",
    "Schema":"test",
    "Version":1,
    "TableVersion":441349361156227074,
    "Query":"ALTER TABLE test.table1 ADD OfficeLocation blob(20)",
    "Type":5,
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
- `Version`：Storage sink 协议版本号。
- `TableVersion`：表的版本号。
- `Query`：DDL 语句。
- `Type`：DDL 类型。
- `TableColumns`：该数组表示表中每一列的详细信息。
    - `ColumnName`：列名。
    - `ColumnType`：该列的类型。详见[数据类型](#数据类型)。
    - `ColumnLength`：该列的长度。详见[数据类型](#数据类型)。
    - `ColumnPrecision`：该列的精度。详见[数据类型](#数据类型)。
    - `ColumnScale`：该列小数位的长度。详见[数据类型](#数据类型)。
    - `ColumnNullable`：值为 `true` 时表示该列可以含 NULL 值。
    - `ColumnIsPk`：值为 `true` 时表示该列是主键的一部分。
- `TableColumnsTotal`：`TableColumns` 数组的大小。

#### 库级 DDL 事件

当上游数据库发生库级 DDL 事件时，TiCDC 将会自动生成一个 schema 文件存储数据库结构信息，文件路径如下：

```shell
{scheme}://{prefix}/{schema}/meta/schema_{table-version}_{hash}.json
```

以 `schema_441349361156227000_3131721815.json` 为例，数据库结构信息文件的内容如下：

```json
{
  "Table": "",
  "Schema": "schema1",
  "Version": 1,
  "TableVersion": 441349361156227000,
  "Query": "CREATE DATABASE `schema1`",
  "Type": 1,
  "TableColumns": null,
  "TableColumnsTotal": 0
}
```

## 数据类型

本章节主要介绍 `schema_{table-version}_{hash}.json` 文件（以下简称为 schema 文件）中使用的各种数据类型。数据类型定义为 `T(M[, D])`，详见[数据类型概述](/data-type-overview.md#数据类型概述)。

### 整数类型

TiDB 中整数类型可被定义为 `IT[(M)] [UNSIGNED]`，其中：

- `IT` 为整数类型，包括 `TINYINT`、`SMALLINT`、`MEDIUMINT`、`INT`、`BIGINT` 和 `BIT`。
- `M` 为该类型的显示宽度。

schema 文件中对整数类型定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

### 小数类型

TiDB 中的小数类型可被定义为 `DT[(M,D)][UNSIGNED]`，其中：

- `DT` 为小数类型，包括 `FLOAT`、`DOUBLE`、`DECIMAL` 和 `NUMERIC`。
- `M` 为该类型数据的精度，即整数位加上小数位的总长度。
- `D` 为小数位的长度。

schema 文件中对小数类型的定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

### 时间和日期类型

TiDB 中的日期类型可被定义为 `DT`，其中：

- `DT` 为日期类型，包括 `DATE` 和 `YEAR`。

schema 文件中对日期类型的定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

TiDB 中的时间类型可被定义为 `TT[(M)]`，其中：

- `TT` 为时间类型，包括 `TIME`、`DATETIME` 和 `TIMESTAMP`。
- `M` 为秒的精度，取值范围为 0~6。

schema 文件中对时间类型的定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

### 字符串类型

TiDB 中的字符串类型可被定义为 `ST[(M)]`，其中：

- `ST` 为字符串类型，包括 `CHAR`、`VARCHAR`、`TEXT`、`BINARY`、`BLOB`、`JSON` 等。
- `M` 表示字符串的最大长度。

schema 文件中对字符串类型的定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

### Enum/Set 类型

schema 文件中对 Enum/Set 类型的定义如下：

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
