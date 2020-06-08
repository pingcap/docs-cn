---
title: 使用 Dumpling 导出或备份 TiDB 数据
summary: 使用新的导出工具 Dumpling 导出或者备份数据。
category: how-to
---

# 使用 Dumpling 导出或备份 TiDB 数据

本文档介绍如何使用数据导出工具 [Dumpling](https://github.com/pingcap/dumpling)。该工具可以把存储在 TiDB 中的数据导出为 SQL 或者 CSV 格式，可以用于完成逻辑上的全量备份或者导出。

如果需要直接备份 SST 文件（KV 对）或者对延迟不敏感的增量备份，请参阅 [BR](/br/backup-and-restore-tool.md)。如果需要实时的增量备份，请参阅 [TiCDC](/ticdc/ticdc-overview.md)。

Dumpling 的更多具体用法可以使用 --help 指令查看，或者查看[中文使用手册](https://github.com/pingcap/dumpling/blob/master/docs/cn/user-guide.md)。

使用 Dumpling 时，需要在已经启动的集群上执行导出命令。本文假设在 `127.0.0.1:4000` 有一个 TiDB 实例，并且这个 TiDB 实例中有无密码的 root 用户。 

## 下载地址

最新版 Dumpling 的下载地址见[下载链接](https://download.pingcap.org/dumpling-nightly-linux-amd64.tar.gz)。

## 从 TiDB 导出数据

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
  -F 256
```

上述命令中，`-h`、`-P`、`-u` 分别是地址，端口，用户。如果需要密码验证，可以用 `-p $YOUR_SECRET_PASSWORD` 传给 Dumpling。

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

### 筛选导出的数据

#### 使用 `--where` 指令筛选数据

默认情况下，除了系统数据库中的表之外，Dumpling 会导出整个数据库的表。你可以使用 `--where <SQL where expression>` 来选定要导出的记录。

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

上述命令将会导出各个表的 id < 100 的数据。

#### 使用 `--filter` 指令筛选数据

Dumpling 可以通过 `--filter` 指定 table-filter 来筛选特定的库表。table-filter 的语法与 .gitignore 相似，[详细语法参考](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)。

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filter "employees.*" \
  --filter "*.WorkOrder"
```

上述命令将会导出 `employees` 数据库的所有表，以及所有数据库中的 `WorkOrder` 表。

#### 使用 `-B` 或 `-T` 指令筛选数据

Dumpling 也可以通过 `-B` 或 `-T` 参数导出特定的数据库/数据表。

> **注意：**
>
> 1. `--filter` 参数与 `-T` 参数不可同时使用。
>
> 2. `-T` 参数只能接受完整的 `库名.表名` 形式，不支持只指定表名。例：Dumpling 无法识别 `-T WorkOrder`。

例如通过指定：

- `-B employees` 导出 `employees` 数据库
- `-T employees.WorkOrder` 导出 `employees.WorkOrder` 数据表

### 通过并发提高 Dumpling 的导出效率

默认情况下，导出的文件会存储到 `./export-<current local time>` 目录下。常用参数如下：

- `-o` 用于选择存储导出文件的目录。
- `-F` 选项用于指定单个文件的最大大小，默认单位为 `MiB`。可以接受类似 `5GiB` 或 `8KB` 的输入。
- `-r` 选项用于指定单个文件的最大记录数（或者说，数据库中的行数），开启后 Dumpling 会开启表内并发，提高导出大表的速度。

利用以上参数可以让 Dumpling 的并行度更高。

### 调整 Dumpling 的数据一致性选项

> **注意：**
>
> 在大多数场景下，用户不需要调整 Dumpling 的默认数据一致性选项。

Dumpling 通过 `--consistency <consistency level>` 标志控制导出数据“一致性保证”的方式。对于 TiDB 来说，默认情况下，会通过获取某个时间戳的快照来保证一致性（即 `--consistency snapshot`）。在使用 snapshot 来保证一致性的时候，可以使用 `--snapshot` 参数指定要备份的时间戳。还可以使用以下的一致性级别：

- `flush`：使用 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) 来保证一致性。
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

另外，假如数据量非常大，可以提前调长 GC 时间，以避免因为导出过程中发生 GC 导致导出失败：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

在操作结束之后，再将 GC 时间调回原样（默认是 `10m`）：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
```

最后，所有的这些导出数据都可以用 [Lightning](/tidb-lightning/tidb-lightning-tidb-backend.md) 导入回 TiDB。
