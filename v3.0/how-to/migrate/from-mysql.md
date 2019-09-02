---
title: 全量数据迁移
category: how-to
aliases: ['/docs-cn/op-guide/migration/']
---

# 全量数据迁移

`mydumper` 是一个强大的数据迁移工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。你可以使用 `mydumper` 从 MySQL 导出数据，然后用 `loader` 将其导入到 TiDB。

> **注意：**
>
> 虽然 TiDB 也支持使用 MySQL 官方的 `mysqldump` 工具来进行数据的迁移工作，但相比于 `mydumper`/`loader`，性能会慢很多，大量数据的迁移会花费很多时间，这里我们并不推荐。

## `mydumper`/`loader` 全量导入数据最佳实践

为了快速的迁移数据 (特别是数据量巨大的库)，可以参考以下建议：

* Mydumper 导出数据至少要拥有 `SELECT`，`RELOAD`，`LOCK TABLES` 权限
* 使用 Mydumper 导出来的数据文件尽可能的小，最好不要超过 64M，可以设置参数 -F 64
* loader的 `-t` 参数可以根据 TiKV 的实例个数以及负载进行评估调整，例如 3个 TiKV 的场景，此值可以设为 `3 *（1 ～ n)`；当 TiKV 负载过高，loader 以及 TiDB 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 可以适当调小该值，当 TiKV 负载不是太高的时候，可以适当调大该值。

导入示例及相关配置：

- Mydumper 导出后总数据量 214G，单表 8 列，20 亿行数据
- 集群拓扑
    - TiKV * 12
    - TiDB * 4
    - PD * 3
- Mydumper `-F` 设置为 16，Loader `-t` 参数设置为 64

结果：导入时间 11 小时左右，19.4 G/小时

## 从 MySQL 导出数据

我们使用 `mydumper` 从 MySQL 导出数据，如下:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 16` 表明使用 16 个线程去导出数据。`-F 64` 是将实际的 table 切分成多大的 chunk，这里就是 64MB 一个 chunk。

`--skip-tz-utc` 添加这个参数忽略掉 MySQL 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

> **注意：**
>
> 在阿里云等一些需要 `super privilege` 的云上面，`mydumper` 需要加上 `--no-locks` 参数，否则会提示没有权限操作。

## 向 TiDB 导入数据

> **注意：**
>
> 目前 TiDB 支持 UTF8mb4 [字符编码](/reference/sql/character-set.md)，假设 Mydumper 导出数据为 latin1 字符编码，请使用 `iconv -f latin1 -t utf-8 $file -o /data/imdbload/$basename` 命令转换，$file 为已有文件，$basename 为转换后文件。

> **注意：**
>
> 如果 Mydumper 使用 -m 参数，会导出不带表结构的数据，这时 loader 无法导入数据。

我们使用 `loader` 将之前导出的数据导入到 TiDB。Loader 的下载和具体的使用方法见 [Loader 使用文档](/reference/tools/loader.md)

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
