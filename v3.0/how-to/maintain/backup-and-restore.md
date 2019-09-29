---
title: 备份与恢复
category: how-to
---

# 备份与恢复

本文档将详细介绍如何对 TiDB 进行全量备份与恢复。增量备份与恢复可使用 [TiDB Binlog](/v3.0/reference/tidb-binlog-overview.md)。

这里我们假定 TiDB 服务信息如下：

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|

在这个备份恢复过程中，我们会用到下面的工具：

- Mydumper 从 TiDB 导出数据
- Loader 导入数据到 TiDB

## 下载 TiDB 工具集 (Linux)

下载 tool 压缩包：

{{< copyable "shell-regular" >}}

```bash
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz && \
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256
```

检查文件完整性，返回 ok 则正确：

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
```

解开压缩包：

{{< copyable "shell-regular" >}}

```bash
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz && \
cd tidb-enterprise-tools-latest-linux-amd64
```

## 使用 `mydumper`/`loader` 全量备份恢复数据

`mydumper` 是一个强大的数据备份工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

可使用 [`mydumper`](/v3.0/reference/tools/mydumper.md) 从 TiDB 导出数据进行备份，然后用 [`loader`](/v3.0/reference/tools/loader.md) 将其导入到 TiDB 里面进行恢复。

> **注意：**
>
> 必须使用企业版工具集包的 `mydumper`，不要使用你的操作系统的包管理工具提供的 `mydumper`。`mydumper` 的上游版本并不能对 TiDB 进行正确处理 ([#155](https://github.com/maxbube/mydumper/pull/155))。由于使用 `mysqldump` 进行数据备份和恢复都要耗费许多时间，这里也并不推荐。

### `mydumper`/`loader` 全量备份恢复最佳实践

为了快速地备份恢复数据 (特别是数据量巨大的库)，可以参考以下建议：

* 使用 Mydumper 导出来的数据文件尽可能的小，最好不要超过 64M，可以将参数 `-F` 设置为 64。
* Loader的 `-t` 参数可以根据 TiKV 的实例个数以及负载进行评估调整，推荐设置为 32。当 TiKV 负载过高，Loader 以及 TiDB 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 时，可以适当调小该值；当 TiKV 负载不是太高的时候，可以适当调大该值。

## 从 TiDB 备份数据

我们使用 `mydumper` 从 TiDB 备份数据，如下:

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 32 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 32` 表明使用 32 个线程去导出数据。`-F 64` 是将实际的 table 切分成多大的 chunk，这里就是 64MB 一个 chunk。

`--skip-tz-utc` 添加这个参数忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

如果 `mydumper` 出现以下报错：

```
** (mydumper:27528): CRITICAL **: 13:25:09.081: Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

就再执行两步命令：

1. 执行 `mydumper` 命令前，查询 TiDB 集群的 GC 值并使用 MySQL 客户端将其调整为合适的值。

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 执行 `mydumper` 命令后，将 TiDB 集群的 GC 值恢复到第 1 步中的初始值。

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## 向 TiDB 恢复数据

我们使用 `loader` 将之前导出的数据导入到 TiDB，完成恢复操作。Loader 的下载和具体的使用方法见 [Loader 使用文档](/v3.0/reference/tools/loader.md)

{{< copyable "shell-regular" >}}

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

导入成功之后，我们可以用 MySQL 官方客户端进入 TiDB，查看：

{{< copyable "shell-regular" >}}

```bash
mysql -h127.0.0.1 -P4000 -uroot
```

{{< copyable "sql" >}}

```sql
show tables;
```

```

{{< copyable "sql" >}}

```sql
select * from t1;
```

```
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+
```

{{< copyable "sql" >}}

```sql
select * from t2;
```

```
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```
