---
title: Dumpling 使用文档
summary: 使用 Dumpling 从 TiDB 导出数据。
aliases: ['/docs-cn/stable/dumpling-overview/','/docs-cn/v4.0/dumpling-overview/']
---

# Dumpling 使用文档

本文档介绍如何使用数据导出工具 [Dumpling](https://github.com/pingcap/dumpling)。该工具可以把存储在 TiDB/MySQL 中的数据导出为 SQL 或者 CSV 格式，可以用于完成逻辑上的全量备份或者导出。

如果需要直接备份 SST 文件（键值对）或者对延迟不敏感的增量备份，请参阅 [BR](/br/backup-and-restore-tool.md)。如果需要实时的增量备份，请参阅 [TiCDC](/ticdc/ticdc-overview.md)。

## 相比于 Mydumper，Dumpling 有哪些改进之处？

1. 支持导出多种数据形式，包括 SQL/CSV
2. 支持全新的 [table-filter](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)，筛选数据更加方便
3. 支持导出到 Amazon S3 云盘
4. 针对 TiDB 进行了更多优化：
    - 支持配置 TiDB 单条 SQL 内存限制
    - 针对 TiDB v4.0.0 以上版本支持自动调整 TiDB GC 时间
    - 使用 TiDB 的隐藏列 `_tidb_rowid` 优化了单表内数据的并发导出性能
    - 对于 TiDB 可以设置 [tidb_snapshot](/read-historical-data.md#操作流程) 的值指定备份数据的时间点，从而保证备份的一致性，而不是通过 `FLUSH TABLES WITH READ LOCK` 来保证备份一致性。

## Dumpling 简介

`Dumpling` 是使用 go 开发的数据备份工具，项目地址可以参考 [`Dumpling`](https://github.com/pingcap/dumpling)。

Dumpling 的更多具体用法可以使用 --help 选项查看，或者查看 [Dumpling 主要选项表](#dumpling-主要选项表)。

使用 Dumpling 时，需要在已经启动的集群上执行导出命令。本文假设在 `127.0.0.1:4000` 有一个 TiDB 实例，并且这个 TiDB 实例中有无密码的 root 用户。

可以通过运行 `tiup install dumpling` 命令来使用 [TiUP]（/tiup/tiup-overview.md）工具获取 Dumpling。之后，可以使用 `tiup dumpling ...` 命令运行 Dumpling。

Dumpling 包含在 tidb-toolkit 安装包中，可[在此下载](/download-ecosystem-tools.md#dumpling)。

## 从 TiDB/MySQL 导出数据

### 需要的权限

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT

### 导出到 sql 文件

Dumpling 默认导出数据格式为 sql 文件。也可以通过设置 `--filetype sql` 导出数据到 sql 文件：

{{< copyable "shell-regular" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  --filetype sql \
  --threads 32 \
  -o /tmp/test \
  -r 200000 \
  -F 256MiB
```

以上命令中：

- `-h`、`-P`、`-u` 分别代表地址、端口、用户。如果需要密码验证，可以使用 `-p $YOUR_SECRET_PASSWORD` 将密码传给 Dumpling。
- `-o` 用于选择存储导出文件的目录，支持本地文件路径或[外部存储 URL](/br/backup-and-restore-storages.md) 格式。
- `-r` 用于指定单个文件的最大行数，指定该参数后 Dumpling 会开启表内并发加速导出，同时减少内存使用。
- `-F` 选项用于指定单个文件的最大大小（单位为 `MiB`，可接受类似 `5GiB` 或 `8KB` 的输入）。如果你想使用 TiDB Lightning 将该文件加载到 TiDB 实例中，建议将 `-F` 选项的值保持在 256 MiB 或以下。

> **注意：**
>
> 如果导出的单表大小超过 10 GB，**强烈建议**使用`-r` 和 `-F` 参数。

### 导出到 csv 文件

假如导出数据的格式是 CSV（使用 `--filetype csv` 即可导出 CSV 文件），还可以使用 `--sql <SQL>` 导出指定 SQL 选择出来的记录，例如，导出 `test.sbtest1` 中所有 `id < 100` 的记录：

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql 'select * from `test`.`sbtest1` where id < 100'
```

> **注意：**
>
> 1. `--sql` 选项暂时仅仅可用于导出 csv 的场景。
>
> 2. 这里需要在要导出的所有表上执行 `select * from <table-name> where id < 100` 语句。如果部分表没有指定的字段，那么导出会失败。
>
> 3. csv 文件不区分`字符串`与`关键字`。如果导入的数据是 Boolean 类型的 `true` 和 `false`，需要转换为 `1` 和 `0` 。

### 输出文件格式

+ `metadata`：此文件包含导出的起始时间，以及 master binary log 的位置。

    {{< copyable "shell-regular" >}}

    ```shell
    cat metadata
    ```

    ```shell
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124

    Finished dump at: 2020-11-10 10:40:20
    ```

+ `{schema}-schema-create.sql`：创建 schema 的 SQL 文件。

    {{< copyable "shell-regular" >}}

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

+ `{schema}.{table}-schema.sql`：创建 table 的 SQL 文件

    {{< copyable "shell-regular" >}}

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
    ```

+ `{schema}.{table}.{0001}.{sql|csv`}：数据源文件

    {{< copyable "shell-regular" >}}

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

+ `*-schema-view.sql`、`*-schema-trigger.sql`、`*-schema-post.sql`：其他导出文件

### 导出到 Amazon S3 云盘

Dumpling 在 v4.0.8 版本及更新版本中支持导出到云盘。如果需要将数据备份到 Amazon 的 S3 后端存储，那么需要在 `-o` 参数中指定 S3 的存储路径。

可以参照 [AWS 官方文档 - 如何创建 S3 存储桶](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的 `Region` 区域中创建一个 S3 桶 `Bucket`。如果有需要，还可以参照 [AWS 官方文档 - 创建文件夹](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html) 在 Bucket 中创建一个文件夹 `Folder`。

将有权限访问该 S3 后端存储的账号的 `SecretKey` 和 `AccessKey` 作为环境变量传入 Dumpling 节点。

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling 同时还支持从 `~/.aws/credentials` 读取凭证文件。更多 Dumpling 存储配置可以参考[外部存储](/br/backup-and-restore-storages.md)。

在进行 Dumpling 备份时，显式指定参数 `--s3.region`，即表示 S3 存储所在的区域。

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -r 200000 \
  -o "s3://${Bucket}/${Folder}" \
  --s3.region "${region}"
```

### 筛选导出的数据

#### 使用 `--where` 选项筛选数据

默认情况下，Dumpling 会导出排除系统数据库（包括 `mysql` 、`sys` 、`INFORMATION_SCHEMA` 、`PERFORMANCE_SCHEMA`、`METRICS_SCHEMA` 和 `INSPECTION_SCHEMA`）外所有其他数据库。你可以使用 `--where <SQL where expression>` 来选定要导出的记录。

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

上述命令将会导出各个表的 id < 100 的数据。注意 `--where` 参数无法与 `--sql` 一起使用。

#### 使用 `--filter` 选项筛选数据

Dumpling 可以通过 `--filter` 指定 table-filter 来筛选特定的库表。table-filter 的语法与 `.gitignore` 相似，详细语法参考[表库过滤](/table-filter.md)。

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  -r 200000 \
  --filter "employees.*" \
  --filter "*.WorkOrder"
```

上述命令将会导出 `employees` 数据库的所有表，以及所有数据库中的 `WorkOrder` 表。

#### 使用 `-B` 或 `-T` 选项筛选数据

Dumpling 也可以通过 `-B` 或 `-T` 选项导出特定的数据库/数据表。

> **注意：**
>
> 1. `--filter` 选项与 `-T` 选项不可同时使用。
>
> 2. `-T` 选项只能接受完整的 `库名.表名` 形式，不支持只指定表名。例：Dumpling 无法识别 `-T WorkOrder`。

例如通过指定：

- `-B employees` 导出 `employees` 数据库
- `-T employees.WorkOrder` 导出 `employees.WorkOrder` 数据表

### 通过并发提高 Dumpling 的导出效率

默认情况下，导出的文件会存储到 `./export-<current local time>` 目录下。常用选项如下：

- `-t` 用于指定导出的线程数。增加线程数会增加 Dumpling 并发度，但也会加大数据库内存消耗，因此不宜设置过大。
- `-r` 选项用于指定单个文件的最大记录数（或者说，数据库中的行数），开启后 Dumpling 会开启表内并发，提高导出大表的速度。

利用以上选项可以提高 Dumpling 的导出速度。

### 调整 Dumpling 的数据一致性选项

> **注意：**
>
> 在大多数场景下，用户不需要调整 Dumpling 的默认数据一致性选项。

Dumpling 通过 `--consistency <consistency level>` 标志控制导出数据“一致性保证”的方式。对于 TiDB 来说，默认情况下，会通过获取某个时间戳的快照来保证一致性（即 `--consistency snapshot`）。在使用 snapshot 来保证一致性的时候，可以使用 `--snapshot` 选项指定要备份的时间戳。还可以使用以下的一致性级别：

- `flush`：使用 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) 短暂地中断备份库的 DML 和 DDL 操作、保证备份连接的全局一致性和记录 POS 信息。所有的备份连接启动事务后释放该锁。推荐在业务低峰或者 MySQL 备份库上进行全量备份。
- `snapshot`：获取指定时间戳的一致性快照并导出。
- `lock`：为待导出的所有表上读锁。
- `none`：不做任何一致性保证。
- `auto`：对 MySQL 使用 `flush`，对 TiDB 使用 `snapshot`。

一切完成之后，你应该可以在 `/tmp/test` 看到导出的文件了：

```shell
$ ls -lh /tmp/test | awk '{print $5 "\t" $9}'

140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

### 导出 TiDB 的历史数据快照

Dumpling 可以通过 `--snapshot` 指定导出某个 [tidb_snapshot](/read-historical-data.md#操作流程) 时的数据。

`--snapshot` 选项可设为 TSO（`SHOW MASTER STATUS` 输出的 `Position` 字段）或有效的 `datetime` 时间，例如：

{{< copyable "shell-regular" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

即可导出 TSO 为 `417773951312461825` 或 `2020-07-02 17:12:45` 时的 TiDB 历史数据快照。

### 控制导出 TiDB 大表时的内存使用

Dumpling 导出 TiDB 较大单表时，可能会因为导出数据过大导致 TiDB 内存溢出 (OOM)，从而使连接中断导出失败。可以通过以下参数减少 TiDB 的内存使用。

+ 设置 `-r` 参数，可以划分导出数据区块减少 TiDB 扫描数据的内存开销，同时也可开启表内并发提高导出效率。
+ 调小 `--tidb-mem-quota-query` 参数到 `8589934592` (8GB) 或更小。可控制 TiDB 单条查询语句的内存使用。
+ 调整 `--params "tidb_distsql_scan_concurrency=5"` 参数，即设置导出时的 session 变量 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 从而减少 TiDB scan 操作的并发度。

### 导出大规模数据时的 TiDB GC 设置

如果导出的 TiDB 版本大于 v4.0.0，并且 Dumpling 可以访问 TiDB 集群的 PD 地址，Dumpling 会自动配置延长 GC 时间且不会对原集群造成影响。v4.0.0 之前的版本依然需要手动修改 GC。

其他情况下，假如导出的数据量非常大，可以提前调长 GC 时间，以避免因为导出过程中发生 GC 导致导出失败：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

在操作结束之后，再将 GC 时间调回原样（默认是 `10m`）：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
```

最后，所有的导出数据都可以用 [TiDB Lightning](/tidb-lightning/tidb-lightning-backends.md) 导入回 TiDB。

## Dumpling 主要选项表

| 主要选项 | 用途 | 默认值 |
| --------| --- | --- |
| -V 或 --version | 输出 Dumpling 版本并直接退出 |
| -B 或 --database | 导出指定数据库 |
| -T 或 --tables-list | 导出指定数据表 |
| -f 或 --filter | 导出能匹配模式的表，语法可参考 [table-filter](/table-filter.md) | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]`（导出除系统库外的所有库表） |
| --case-sensitive | table-filter 是否大小写敏感 | false，大小写不敏感 |
| -h 或 --host| 连接的数据库主机的地址 | "127.0.0.1" |
| -t 或 --threads | 备份并发线程数| 4 |
| -r 或 --rows | 将 table 划分成 row 行数据，一般针对大表操作并发生成多个文件。|
| -L 或 --logfile | 日志输出地址，为空时会输出到控制台 | "" |
| --loglevel | 日志级别 {debug,info,warn,error,dpanic,panic,fatal} | "info" |
| --logfmt | 日志输出格式 {text,json} | "text" |
| -d 或 --no-data | 不导出数据，适用于只导出 schema 场景 |
| --no-header | 导出 csv 格式的 table 数据，不生成 header |
| -W 或 --no-views| 不导出 view | true |
| -m 或 --no-schemas | 不导出 schema，只导出数据 |
| -s 或--statement-size | 控制 `INSERT` SQL 语句的大小，单位 bytes |
| -F 或 --filesize | 将 table 数据划分出来的文件大小，需指明单位（如 `128B`, `64KiB`, `32MiB`, `1.5GiB`） |
| --filetype| 导出文件类型（csv/sql） | "sql" |
| -o 或 --output | 导出本地文件路径或[外部存储 URL](/br/backup-and-restore-storages.md) | "./export-${time}" |
| -S 或 --sql | 根据指定的 sql 导出数据，该选项不支持并发导出 |
| --consistency | flush: dump 前用 FTWRL <br/> snapshot: 通过 TSO 来指定 dump 某个快照时间点的 TiDB 数据 <br/> lock: 对需要 dump 的所有表执行 `lock tables read` 命令 <br/> none: 不加锁 dump，无法保证一致性 <br/> auto: 对 MySQL 使用 --consistency flush；对 TiDB 使用 --consistency snapshot | "auto" |
| --snapshot | snapshot tso，只在 consistency=snapshot 下生效 |
| --where | 对备份的数据表通过 where 条件指定范围 |
| -p 或 --password | 连接的数据库主机的密码 |
| -P 或 --port | 连接的数据库主机的端口 | 4000 |
| -u 或 --user | 连接的数据库主机的用户名 | "root" |
| --dump-empty-database | 导出空数据库的建库语句 | true |
| --ca | 用于 TLS 连接的 certificate authority 文件的地址 |
| --cert | 用于 TLS 连接的 client certificate 文件的地址 |
| --key | 用于 TLS 连接的 client private key 文件的地址 |
| --csv-delimiter | csv 文件中字符类型变量的定界符 | '"' |
| --csv-separator | csv 文件中各值的分隔符 | ',' |
| --csv-null-value | csv 文件空值的表示 | "\\N" |
| --escape-backslash | 使用反斜杠 (`\`) 来转义导出文件中的特殊字符 | true |
| --output-filename-template | 以 [golang template](https://golang.org/pkg/text/template/#hdr-Arguments) 格式表示的数据文件名格式 <br/> 支持 `{{.DB}}`、`{{.Table}}`、`{{.Index}}` 三个参数 <br/> 分别表示数据文件的库名、表名、分块 ID | '{{.DB}}.{{.Table}}.{{.Index}}' |
| --status-addr | Dumpling 的服务地址，包含了 Prometheus 拉取 metrics 信息及 pprof 调试的地址 | ":8281" |
| --tidb-mem-quota-query | 单条 dumpling 命令导出 SQL 语句的内存限制，单位为 byte。对于 v4.0.10 或以上版本，若不设置该参数，默认使用 TiDB 中的 `mem-quota-query` 配置项值作为内存限制值。对于 v4.0.10 以下版本，该参数值默认为 32 GB | 34359738368 |
| --params | 为需导出的数据库连接指定 session 变量，可接受的格式: "character_set_client=latin1,character_set_connection=latin1" |
