---
title: 预处理语句
summary: 了解如何使用 TiDB 预处理语句。
---

# 预处理语句

[预处理语句](/sql-statements/sql-statement-prepare.md)将多个只有参数不同的 SQL 语句模板化。它将 SQL 语句与参数分离。你可以使用它来改进 SQL 语句的以下方面：

- **安全性**：由于参数和语句是分离的，避免了 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)攻击的风险。
- **性能**：由于语句在 TiDB 服务器上预先解析，后续执行时只传递参数，节省了解析整个 SQL 语句、拼接 SQL 语句字符串和网络传输的成本。

在大多数应用程序中，SQL 语句是可枚举的。你可以使用有限数量的 SQL 语句来完成整个应用程序的数据查询。因此使用预处理语句是一种最佳实践。

## SQL 语法

本节描述创建、运行和删除预处理语句的 SQL 语法。

### 创建预处理语句

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

| 参数名称 | 描述 |
| :-------------------------: | :------------------------------------: |
| `{prepared_statement_name}` | 预处理语句的名称 |
| `{prepared_statement_sql}`  | 使用问号作为占位符的预处理语句 SQL |

更多信息请参见 [PREPARE 语句](/sql-statements/sql-statement-prepare.md)。

### 使用预处理语句

预处理语句只能使用**用户变量**作为参数，因此在使用 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md)调用预处理语句之前，需要使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md)设置变量。

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

| 参数名称 | 描述 |
| :-------------------------: | :-------------------------------------------------------------------: |
|     `{parameter_name}`      | 用户变量名称 |
|     `{parameter_value}`     | 用户变量值 |
| `{prepared_statement_name}` | 预处理语句的名称，必须与[创建预处理语句](#创建预处理语句)中定义的名称相同 |

更多信息请参见 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md)。

### 删除预处理语句

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

| 参数名称 | 描述 |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{prepared_statement_name}` | 预处理语句的名称，必须与[创建预处理语句](#创建预处理语句)中定义的名称相同 |

更多信息请参见 [`DEALLOCATE` 语句](/sql-statements/sql-statement-deallocate.md)。

## 示例

本节描述预处理语句的两个示例：`SELECT` 数据和 `INSERT` 数据。

### `SELECT` 示例

例如，你需要在 [`bookshop` 应用程序](/develop/dev-guide-bookshop-schema-design.md#books-table)中查询 `id = 1` 的图书。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

运行结果：

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SET @id = 1;
```

运行结果：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_query` USING @id;
```

运行结果：

```
+---------+---------------------------------+--------+---------------------+-------+--------+
| id      | title                           | type   | published_at        | stock | price  |
+---------+---------------------------------+--------+---------------------+-------+--------+
| 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
+---------+---------------------------------+--------+---------------------+-------+--------+
1 row in set (0.05 sec)
```

</div>

<div label="Java" value="java">

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实例
try (Connection connection = ds.getConnection()) {
    PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
    preparedStatement.setLong(1, 1);

    ResultSet res = preparedStatement.executeQuery();
    if(!res.next()) {
        System.out.println("No books in the table with id 1");
    } else {
        // 获取 id 为 1 的图书信息
        System.out.println(res.getLong("id"));
        System.out.println(res.getString("title"));
        System.out.println(res.getString("type"));
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

</SimpleTab>

### `INSERT` 示例

以 [`books` 表](/develop/dev-guide-bookshop-schema-design.md#books-table)为例，你需要插入一本 `title = TiDB Developer Guide`、`type = Science & Technology`、`stock = 100`、`price = 0.0` 和 `published_at = NOW()`（插入时的当前时间）的图书。注意，你不需要在 `books` 表的**主键**中指定 `AUTO_RANDOM` 属性。有关插入数据的更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

运行结果：

```
Query OK, 0 rows affected (0.03 sec)
```

```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

运行结果：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

运行结果：

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" value="java">

```java
try (Connection connection = ds.getConnection()) {
    String sql = "INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);

    preparedStatement.setString(1, "TiDB Developer Guide");
    preparedStatement.setString(2, "Science & Technology");
    preparedStatement.setInt(3, 100);
    preparedStatement.setBigDecimal(4, new BigDecimal("0.0"));
    preparedStatement.setTimestamp(5, new Timestamp(Calendar.getInstance().getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

如你所见，JDBC 帮助你控制预处理语句的生命周期，你不需要在应用程序中手动创建、使用或删除预处理语句。但是请注意，由于 TiDB 兼容 MySQL，在客户端使用 MySQL JDBC Driver 的默认配置是不启用**_服务器端_**预处理语句选项，而是使用客户端预处理语句。

以下配置可帮助你在 JDBC 下使用 TiDB 服务器端预处理语句：

|            参数            |                 含义                  |   推荐场景   | 推荐配置 |
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    是否使用服务器端启用预处理语句    |  当你需要多次使用预处理语句时                                                             |          `true`          |
|      `cachePrepStmts`      |       客户端是否缓存预处理语句        |                                                           `useServerPrepStmts=true`                                                             |          `true`          |
|  `prepStmtCacheSqlLimit`   |  预处理语句的最大大小（默认 256 字符）  | 当预处理语句大于 256 字符时 | 根据预处理语句的实际大小配置 |
|    `prepStmtCacheSize`     | 预处理语句的最大数量（默认 25 个） | 当预处理语句数量大于 25 个时  | 根据预处理语句的实际数量配置 |

以下是 JDBC 连接字符串配置的典型场景。主机：`127.0.0.1`，端口：`4000`，用户名：`root`，密码：null，默认数据库：`test`：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

如果你在插入数据时需要更改其他 JDBC 参数，也可以参见[插入行](/develop/dev-guide-insert-data.md#插入行)章节。

有关 Java 的完整示例，请参见：

- [使用 JDBC 连接到 TiDB](/develop/dev-guide-sample-application-java-jdbc.md)
- [使用 Hibernate 连接到 TiDB](/develop/dev-guide-sample-application-java-hibernate.md)
- [使用 Spring Boot 连接到 TiDB](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

</SimpleTab>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
