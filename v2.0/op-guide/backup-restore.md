---
title: 备份与恢复
category: advanced
---

# 备份与恢复

## 概述

该文档详细介绍了如何对 TiDB 进行备份恢复。本文档暂时只考虑全量备份与恢复。

这里我们假定 TiDB 服务信息如下：

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|

在这个备份恢复过程中，我们会用到下面的工具:

- mydumper 从 TiDB 导出数据
- loader 导入数据到 TiDB

### 下载 TiDB 工具集 (Linux)

```bash
# 下载 tool 压缩包
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
# 解开压缩包
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```

## 使用 `mydumper`/`loader` 全量备份恢复数据

`mydumper` 是一个强大的数据备份工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

我们使用 `mydumper` 从 TiDB 导出数据进行备份，然后用 `loader` 将其导入到 TiDB 里面进行恢复。

> 注意：虽然 TiDB 也支持使用 MySQL 官方的 `mysqldump` 工具来进行数据的备份恢复工作，但相比于 `mydumper` / `loader`，性能会慢很多，大量数据的备份恢复会花费很多时间，这里我们并不推荐。

### `mydumper`/`loader` 全量备份恢复最佳实践

为了快速的备份恢复数据 (特别是数据量巨大的库), 可以参考下面建议

* 使用 mydumper 导出来的数据文件尽可能的小, 最好不要超过 64M, 可以设置参数 -F 64
* loader的 `-t` 参数可以根据 tikv 的实例个数以及负载进行评估调整，例如 3个 tikv 的场景， 此值可以设为 `3 *(1 ～ n)`；当 tikv 负载过高，loader 以及 tidb 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 可以适当调小该值，当 tikv 负载不是太高的时候，可以适当调大该值。

#### 某次数据恢复示例，以及相关的配置

- mydumper 导出后总数据量 214G，单表 8 列，20 亿行数据
- 集群拓扑
    - TIKV * 12
    - TIDB * 4
    - PD * 3
- mydumper -F 设置为 16, loader -t 参数 64

结果：导入时间 11 小时左右，19.4 G/小时

### 从 TiDB 备份数据

我们使用 `mydumper` 从 TiDB 备份数据，如下:

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 16` 表明使用 16 个线程去导出数据。`-F 64` 是将实际的 table 切分成多大的 chunk，这里就是 64MB 一个 chunk。

`--skip-tz-utc` 添加这个参数忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

### 向 TiDB 恢复数据

我们使用 `loader` 将之前导出的数据导入到 TiDB，完成恢复操作。Loader 的下载和具体的使用方法见 [Loader 使用文档](../tools/loader.md)

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

导入成功之后，我们可以用 MySQL 官方客户端进入 TiDB，查看:

```sql
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```
