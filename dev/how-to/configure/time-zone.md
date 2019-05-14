---
title: 时区支持
category: how-to
aliases: ['/docs-cn/sql/time-zone/']
---

# 时区支持

TiDB 使用的时区由 `time_zone` 全局变量和 session 变量决定。`time_zone` 的默认值是 `System`，`System` 对应的实际时区在 `TiDB` 集群 bootstrap 初始化时设置。具体逻辑如下:

* 优先使用 `TZ` 环境变量
* 如果失败，则从 `/etc/localtime` 的实际软链地址提取。
* 如果上面两种都失败则使用 `UTC` 作为系统时区。

在运行过程中可以修改全局时区：

```sql
mysql> SET GLOBAL time_zone = timezone;
```

TiDB 还可以通过设置 session 变量 `time_zone` 为每个连接维护各自的时区。默认条件下，这个值取的是全局变量 `time_zone` 的值。修改 session 使用的时区：

```sql
mysql> SET time_zone = timezone;
```

查看当前使用的时区的值：

```sql
mysql> SELECT @@global.time_zone, @@session.time_zone;
```

设置 `time_zone` 的值的格式：

* 'SYSTEM' 表明使用系统时间
* 相对于 UTC 时间的偏移，比如 '+10:00' 或者 '-6:00'
* 某个时区的名字，比如 'Europe/Helsinki'， 'US/Eastern' 或 'MET'

`NOW()` 和 `CURTIME()` 的返回值都受到时区设置的影响。

> **注意：**
>
> 只有 Timestamp 数据类型的值是受时区影响的。可以理解为， Timestamp 数据类型的实际表示使用的是 (字面值 + 时区信息)。其它时间和日期类型，比如 Datetime/Date/Time 是不包含时区信息的，所以也不受到时区变化的影响。

```sql
mysql> create table t (ts timestamp, dt datetime);
Query OK, 0 rows affected (0.02 sec)

mysql> set @@time_zone = 'UTC';
Query OK, 0 rows affected (0.00 sec)

mysql> insert into t values ('2017-09-30 11:11:11', '2017-09-30 11:11:11');
Query OK, 1 row affected (0.00 sec)

mysql> set @@time_zone = '+8:00';
Query OK, 0 rows affected (0.00 sec)

mysql> select * from t;
+---------------------|---------------------+
| ts                  | dt                  |
+---------------------|---------------------+
| 2017-09-30 19:11:11 | 2017-09-30 11:11:11 |
+---------------------|---------------------+
1 row in set (0.00 sec)
```

上面的例子中，无论怎么调整时区的值， Datetime 类型字段的值是不受影响的，而 Timestamp 则随着时区改变，显示的值会发生变化。其实 Timestamp 持久化到存储的值始终没有变化过，只是根据时区的不同显示值不同。

Timestamp 类型和 Datetime 等类型的值，两者相互转换的过程中，会涉及到时区。这种情况一律基于 session 的当前 `time_zone` 时区处理。

另外，用户在导数据的过程中，也要需注意主库和从库之间的时区设定是否一致。
