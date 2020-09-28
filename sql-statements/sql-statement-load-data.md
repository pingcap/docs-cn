---
title: LOAD DATA
summary: TiDB 数据库中 LOAD DATA 的使用概况。
aliases: ['/docs-cn/v3.1/sql-statements/sql-statement-load-data/','/docs-cn/v3.1/reference/sql/statements/load-data/']
---

# LOAD DATA

`LOAD DATA` 语句用于将数据批量加载到 TiDB 表中。

## 语法图

**LoadDataStmt:**

![LoadDataStmt](/media/sqlgram/LoadDataStmt.png)

## 参数说明

用户可以使用 `FIELDS` 参数来指定如何处理数据格式，使用 `FIELDS TERMINATED BY` 来指定每个数据的分隔符号，使用 `FIELDS ENCLOSED BY` 来指定消除数据的包围符号。如果用户希望以某个字符为结尾切分每行数据，可以使用 `LINES TERMINATED BY` 来指定行的终止符。

例如对于以下格式的数据：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果想分别提取 `bob`、`20`、`street 1`，可以指定数据的分隔符号为 `','`，数据的包围符号为 `'\"'`。
可以写成：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

如果不指定处理数据的参数，将会按以下参数处理

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY ''
LINES TERMINATED BY '\n'
```

用户可以通过 `IGNORE number LINES` 参数来忽略文件开始的 `number` 行，例如可以使用 `IGNORE 1 LINES` 来忽略文件的首行。

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE trips (
    ->  trip_id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ->  duration integer not null,
    ->  start_date datetime,
    ->  end_date datetime,
    ->  start_station_number integer,
    ->  start_station varchar(255),
    ->  end_station_number integer,
    ->  end_station varchar(255),
    ->  bike_number varchar(255),
    ->  member_type varchar(255)
    -> );
```

```
Query OK, 0 rows affected (0.14 sec)
```

通过 `LOAD DATA` 导入数据，指定数据的分隔符为逗号，忽略包围数据的引号，并且忽略文件的第一行数据。

如果此时遇到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version` 报错信息。可以参考以下文档解决：

[ERROR 1148 (42000): the used command is not allowed with this TiDB version 问题的处理方法](/faq/tidb-faq.md#923-error-1148-42000-the-used-command-is-not-allowed-with-this-tidb-version-问题的处理方法)

{{< copyable "sql" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

## MySQL 兼容性

* 默认情况下，TiDB 每 20,000 行会进行一次提交。这类似于 MySQL NDB Cluster，但并非 InnoDB 存储引擎的默认配置。

> **注意：**
>
> 这种拆分事务提交的方式是以打破事务的原子性和隔离性为代价的，使用该特性时，使用者需要保证没有其他对正在处理的表的**任何**操作，并且在出现报错时，需要及时**人工介入，检查数据的一致性和完整性**。因此，不建议对读写频繁的表使用 `LOAD DATA` 语句。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
