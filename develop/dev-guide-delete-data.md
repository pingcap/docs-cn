---
title: 删除数据
summary: 了解删除数据的 SQL 语法、最佳实践和示例。
---

# 删除数据

本文档介绍如何使用 [DELETE](/sql-statements/sql-statement-delete.md) SQL 语句在 TiDB 中删除数据。如果你需要定期删除过期数据，请使用[数据生命周期管理](/time-to-live.md)功能。

## 开始之前

在阅读本文档之前，你需要准备以下内容：

- [创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- 阅读[架构设计概述](/develop/dev-guide-schema-design-overview.md)、[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md)和[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)
- [插入数据](/develop/dev-guide-insert-data.md)

## SQL 语法

`DELETE` 语句通常采用以下形式：

```sql
DELETE FROM {table} WHERE {filter}
```

| 参数名称 | 描述 |
| :--------: | :------------: |
| `{table}`  | 表名 |
| `{filter}` | 过滤条件的匹配条件 |

此示例仅展示了 `DELETE` 的简单用法。有关详细信息，请参阅 [DELETE 语法](/sql-statements/sql-statement-delete.md)。

## 最佳实践

删除数据时，请遵循以下最佳实践：

- 在 `DELETE` 语句中始终指定 `WHERE` 子句。如果未指定 `WHERE` 子句，TiDB 将删除表中的**_所有行_**。

<CustomContent platform="tidb">

- 当删除大量行（例如，超过一万行）时，请使用[批量删除](#批量删除)，因为 TiDB 限制单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认为 100 MB）。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当删除大量行（例如，超过一万行）时，请使用[批量删除](#批量删除)，因为 TiDB 限制单个事务的大小默认为 100 MB。

</CustomContent>

- 如果要删除表中的所有数据，请不要使用 `DELETE` 语句。相反，请使用 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) 语句。
- 关于性能考虑，请参阅[性能考虑事项](#性能考虑事项)。
- 在需要删除大批量数据的场景中，[非事务性批量删除](#非事务性批量删除)可以显著提高性能。但是，这将失去删除操作的事务性，因此**无法**回滚。请确保你选择了正确的操作。

## 示例

假设你发现在特定时间段内出现了应用程序错误，需要删除这段时间内的所有 [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 数据，例如从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`。在这种情况下，你可以使用 `SELECT` 语句检查要删除的记录数。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

如果返回的记录超过 10,000 条，请使用[批量删除](#批量删除)来删除它们。

如果返回的记录少于 10,000 条，请使用以下示例删除它们。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，示例如下：

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

在 Java 中，示例如下：

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实例

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

<div label="Golang" value="golang">

在 Golang 中，示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        panic(err)
    }
    _, err = result.RowsAffected()
    if err != nil {
        panic(err)
    }
}
```

</div>

<div label="Python" value="python">

在 Python 中，示例如下：

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND `rated_at` <= %s"
        affect_rows = cursor.execute(delete_sql, (start_time, end_time))
        print(f'delete {affect_rows} data')
```

</div>

</SimpleTab>

<CustomContent platform="tidb">

`rated_at` 字段是 [日期和时间类型](/data-type-date-and-time.md) 中的 `DATETIME` 类型。你可以假设它在 TiDB 中存储为一个字面量，与时区无关。另一方面，`TIMESTAMP` 类型存储时间戳，因此在不同的[时区](/configure-time-zone.md)中显示不同的时间字符串。

</CustomContent>

<CustomContent platform="tidb-cloud">

`rated_at` 字段是 [日期和时间类型](/data-type-date-and-time.md) 中的 `DATETIME` 类型。你可以假设它在 TiDB 中存储为一个字面量，与时区无关。另一方面，`TIMESTAMP` 类型存储时间戳，因此在不同的时区中显示不同的时间字符串。

</CustomContent>

> **注意：**
>
> 与 MySQL 一样，`TIMESTAMP` 数据类型受到 [2038 年问题](https://en.wikipedia.org/wiki/Year_2038_problem)的影响。如果你存储大于 2038 年的值，建议使用 `DATETIME` 类型。

## 性能考虑事项

### TiDB GC 机制

TiDB 在执行 `DELETE` 语句后不会立即删除数据。相反，它会将数据标记为准备删除。然后等待 TiDB GC（垃圾回收）清理过期数据。因此，`DELETE` 语句**_不会_**立即减少磁盘使用量。

默认情况下，GC 每 10 分钟触发一次。每次 GC 都会计算一个称为 **safe_point** 的时间点。任何早于此时间点的数据都不会再被使用，因此 TiDB 可以安全地清理它。

有关更多信息，请参阅 [GC 机制](/garbage-collection-overview.md)。

### 更新统计信息

TiDB 使用[统计信息](/statistics.md)来确定索引选择。在删除大量数据后，索引未被正确选择的风险很高。你可以使用[手动收集](/statistics.md#手动收集)来更新统计信息。它为 TiDB 优化器提供更准确的统计信息，以优化 SQL 性能。

## 批量删除

当你需要从表中删除多行数据时，可以选择 [`DELETE` 示例](#示例)并使用 `WHERE` 子句过滤需要删除的数据。

<CustomContent platform="tidb">

但是，如果你需要删除大量行（超过一万行），建议你以迭代方式删除数据，即每次迭代删除一部分数据，直到删除完成。这是因为 TiDB 限制单个事务的大小（[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)，默认为 100 MB）。你可以在程序或脚本中使用循环来执行此类操作。

</CustomContent>

<CustomContent platform="tidb-cloud">

但是，如果你需要删除大量行（超过一万行），建议你以迭代方式删除数据，即每次迭代删除一部分数据，直到删除完成。这是因为 TiDB 限制单个事务的大小默认为 100 MB。你可以在程序或脚本中使用循环来执行此类操作。

</CustomContent>

本节提供了一个编写脚本处理迭代删除操作的示例，演示了如何组合使用 `SELECT` 和 `DELETE` 来完成批量删除。

### 编写批量删除循环

你可以在应用程序或脚本的循环中编写 `DELETE` 语句，使用 `WHERE` 子句过滤数据，并使用 `LIMIT` 限制单个语句要删除的行数。

### 批量删除示例

假设你发现在特定时间段内出现了应用程序错误。你需要删除这段时间内的所有 [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 数据，例如从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`，并且在 15 分钟内写入了超过 10,000 条记录。你可以执行以下操作。

<SimpleTab groupId="language">
<div label="Java" value="java">

在 Java 中，批量删除示例如下：

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
    public static void main(String[] args) throws InterruptedException {
        // 配置示例数据库连接。

        // 创建 mysql 数据源实例。
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 设置服务器名称、端口、数据库名称、用户名和密码。
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        while (true) {
            batchDelete(mysqlDataSource);
            TimeUnit.SECONDS.sleep(1);
        }
    }

    public static void batchDelete (MysqlDataSource ds) {
        try (Connection connection = ds.getConnection()) {
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.MILLISECOND, 0);

            calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
            preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

            calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
            preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

            int count = preparedStatement.executeUpdate();
            System.out.println("delete " + count + " data");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

在每次迭代中，`DELETE` 从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00` 删除最多 1000 行。

</div>

<div label="Golang" value="golang">

在 Golang 中，批量删除示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    affectedRows := int64(-1)
    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    for affectedRows != 0 {
        affectedRows, err = deleteBatch(db, startTime, endTime)
        if err != nil {
            panic(err)
        }
    }
}

// deleteBatch 每批最多删除 1000 行
func deleteBatch(db *sql.DB, startTime, endTime time.Time) (int64, error) {
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        return -1, err
    }
    affectedRows, err := result.RowsAffected()
    if err != nil {
        return -1, err
    }

    fmt.Printf("delete %d data\n", affectedRows)
    return affectedRows, nil
}
```

在每次迭代中，`DELETE` 从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00` 删除最多 1000 行。

</div>

<div label="Python" value="python">

在 Python 中，批量删除示例如下：

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        affect_rows = -1
        while affect_rows != 0:
            delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND  `rated_at` <= %s LIMIT 1000"
            affect_rows = cursor.execute(delete_sql, (start_time, end_time))
            print(f'delete {affect_rows} data')
            time.sleep(1)
```

在每次迭代中，`DELETE` 从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00` 删除最多 1000 行。

</div>

</SimpleTab>

## 非事务性批量删除

> **注意：**
>
> 从 v6.1.0 开始，TiDB 支持[非事务性 DML 语句](/non-transactional-dml.md)。此功能在早于 TiDB v6.1.0 的版本中不可用。

### 非事务性批量删除的前提条件

在使用非事务性批量删除之前，请确保你已经阅读了[非事务性 DML 语句文档](/non-transactional-dml.md)。非事务性批量删除提高了批量数据处理场景下的性能和易用性，但牺牲了事务的原子性和隔离性。

因此，你应该谨慎使用它，以避免由于操作不当而导致严重后果（如数据丢失）。

### 非事务性批量删除的 SQL 语法

非事务性批量删除语句的 SQL 语法如下：

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

| 参数名称 | 描述 |
| :--------: | :------------: |
| `{shard_column}` | 用于划分批次的列。 |
| `{batch_size}`   | 控制每个批次的大小。 |
| `{delete_statement}` | `DELETE` 语句。 |

上述示例仅展示了非事务性批量删除语句的简单用法。有关详细信息，请参阅[非事务性 DML 语句](/non-transactional-dml.md)。

### 非事务性批量删除示例

在与[批量删除示例](#批量删除示例)相同的场景中，以下 SQL 语句展示了如何执行非事务性批量删除：

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
