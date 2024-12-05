---
title: 时区支持
summary: TiDB 的时区设置由 `time_zone` 系统变量控制，可以在会话级别或全局级别进行设置。`TIMESTAMP` 数据类型的的显示值受时区设置影响，但 `DATETIME`、`DATE` 或 `TIME` 数据类型不受影响。在数据迁移时，需要特别注意主库和从库的时区设置是否一致。
---

# 时区支持

TiDB 使用的时区由 [`time_zone`](/system-variables.md#time_zone) 系统变量决定，该变量可以在会话级别或全局级别设置。`time_zone` 的默认值为 `SYSTEM`。`SYSTEM` 对应的实际时区是在 TiDB 集群 bootstrap 初始化时配置的，具体逻辑如下：

1. TiDB 优先使用 `TZ` 环境变量。
2. 如果 `TZ` 环境变量不可用，TiDB 会从 `/etc/localtime` 的软链接中读取时区信息。
3. 如果上述方法均失败，TiDB 将使用 `UTC` 作为系统时区。

## 查看时区

要查看当前全局时区、客户端时区或系统时区的值，可以执行以下语句：

```sql
SELECT @@global.time_zone, @@session.time_zone, @@global.system_time_zone;
```

## 设置时区

在 TiDB 中，`time_zone` 系统变量的值可以设置为以下格式之一：

- `SYSTEM`（默认值），表示使用系统时间。
- 相对于 UTC 时间的偏移，比如 `'+10:00'` 或 `'-6:00'`。
- 某个时区的名字，比如 `'Europe/Helsinki'`、`'US/Eastern'` 或 `'MET'`。

根据需要，你可以在全局级别或会话级别设置 TiDB 的时区：

- 设置全局时区：

    ```sql
    SET GLOBAL time_zone = ${time-zone-value};
    ```

    例如，执行以下语句可以将全局时区设置为 UTC：

    ```sql
    SET GLOBAL time_zone = 'UTC';
    ```

- 设置会话的时区：

    ```sql
    SET time_zone = ${time-zone-value};
    ```

    例如，执行以下语句可以将当前会话的时区设置为 US/Pacific：

    ```sql
    SET time_zone = 'US/Pacific';
    ```

## 受时区设置影响的函数和数据类型

对于时区敏感的时间值，例如由 [`NOW()`](/functions-and-operators/date-and-time-functions.md) 和 `CURTIME()` 函数返回的值，它们的显示和处理会受到当前会话时区设置的影响。如需进行时区转换，可以使用 `CONVERT_TZ()` 函数。若要获取基于 UTC 的时间戳以避免时区相关问题，可以使用 `UTC_TIMESTAMP()` 函数。

在 TiDB 中，`TIMESTAMP` 数据类型会记录时间戳的具体数值和时区信息，因此它的显示值会受到时区设置的影响。其他数据类型（如 `DATETIME`、`DATE` 和 `TIME`）不记录时区信息，因此它们的值不会受到时区变化的影响。

例如：

```sql
create table t (ts timestamp, dt datetime);
```

```
Query OK, 0 rows affected (0.02 sec)
```

```sql
set @@time_zone = 'UTC';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
insert into t values ('2017-09-30 11:11:11', '2017-09-30 11:11:11');
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
set @@time_zone = '+8:00';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+---------------------|---------------------+
| ts                  | dt                  |
+---------------------|---------------------+
| 2017-09-30 19:11:11 | 2017-09-30 11:11:11 |
+---------------------|---------------------+
1 row in set (0.00 sec)
```

在以上示例中，无论如何调整时区值，`DATETIME` 数据类型的值不会受到影响。然而，`TIMESTAMP` 数据类型的显示值会根据时区的变化而变化。事实上，存储在数据库中的 `TIMESTAMP` 值始终没有变化过，只是根据时区的不同显示的值不同。

## 时区设置的注意事项

- 在 `TIMESTAMP` 和 `DATETIME` 值的转换过程中，会涉及到时区。这种情况一律基于当前会话的 `time_zone` 时区处理。
- 数据迁移时，需要特别注意主库和从库的时区设置是否一致。
- 为了获取准确的时间戳，强烈建议使用网络时间协议 (NTP) 或精确时间协议 (PTP) 服务配置可靠的时钟。有关如何检查 NTP 服务的信息，请参考[检测及安装 NTP 服务](/check-before-deployment.md#检测及安装-ntp-服务)。
- 当使用遵循夏令时 (Daylight Saving Time, DST) 的时区时，请注意可能出现时间戳不明确或不存在的情况，特别是在对这些时间戳进行计算时。
- MySQL 需要使用 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.4/en/mysql-tzinfo-to-sql.html) 将操作系统的时区数据库转换为 `mysql` 数据库中的表。TiDB 则可以利用 Go 编程语言的内置时区处理能力，直接从操作系统的时区数据库中读取时区数据文件。

## 另请参阅

- [日期和时间类型](/data-type-date-and-time.md)
- [日期和时间函数](/functions-and-operators/date-and-time-functions.md)