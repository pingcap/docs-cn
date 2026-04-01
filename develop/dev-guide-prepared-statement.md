---
title: 预处理语句
summary: 介绍 TiDB 的预处理语句功能。
aliases: ['/zh/tidb/dev/prepared-statement','/zh/tidb/stable/dev-guide-prepared-statement/','/zh/tidb/dev/dev-guide-prepared-statement/','/zh/tidbcloud/dev-guide-prepared-statement/']
---

# 预处理语句

[预处理语句](/sql-statements/sql-statement-prepare.md)是一种将多个仅有参数不同的 SQL 语句进行模板化的语句，它让 SQL 语句与参数进行了分离。可以用它提升 SQL 语句的：

- 安全性：因为参数和语句已经分离，所以避免了 [SQL 注入攻击](https://en.wikipedia.org/wiki/SQL_injection)的风险。
- 性能：因为语句在 TiDB 端被预先解析，后续执行只需要传递参数，节省了完整 SQL 解析、拼接 SQL 语句字符串以及网络传输的代价。

在大部分的应用程序中，SQL 语句是可以被枚举的，可以使用有限个 SQL 语句来完成整个应用程序的数据查询，所以使用预处理语句是最佳实践之一。

## SQL 语法

本节将介绍创建、使用及删除预处理语句的 SQL 语法。

### 创建预处理语句

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

|            参数             |                  描述                  |
| :-------------------------: | :------------------------------------: |
| `{prepared_statement_name}` |             预处理语句名称             |
| `{prepared_statement_sql}`  | 预处理语句 SQL，以英文半角问号做占位符 |

你可查看 [PREPARE 语句](/sql-statements/sql-statement-prepare.md)获得更多信息。

### 使用预处理语句

预处理语句仅可使用用户变量作为参数，因此，需先使用 [SET 语句](/sql-statements/sql-statement-set-variable.md)设置变量后，供 [EXECUTE 语句](/sql-statements/sql-statement-execute.md)调用预处理语句。

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

|            参数             |                                 描述                                  |
| :-------------------------: | :-------------------------------------------------------------------: |
|     `{parameter_name}`      |                              用户参数名                               |
|     `{parameter_value}`     |                              用户参数值                               |
| `{prepared_statement_name}` | 预处理语句名称，需和[创建预处理语句](#创建预处理语句)中定义的名称一致 |

你可查看 [EXECUTE 语句](/sql-statements/sql-statement-execute.md)获得更多信息。

### 删除预处理语句

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

|            参数             |                                 描述                                  |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{prepared_statement_name}` | 预处理语句名称，需和[创建预处理语句](#创建预处理语句)中定义的名称一致 |

你可查看 [DEALLOCATE 语句](/sql-statements/sql-statement-deallocate.md)获得更多信息。

## 例子

本节以使用预处理语句，完成查询数据和插入数据两个场景的示例。

### 查询示例

例如，需要查询 [Bookshop 应用](/develop/dev-guide-bookshop-schema-design.md#books-表)中，`id` 为 1 的书籍信息。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

使用 SQL 查询示例：

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

运行结果为：

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SET @id = 1;
```

运行结果为：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_query` USING @id;
```

运行结果为：

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

使用 Java 查询示例：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
    preparedStatement.setLong(1, 1);

    ResultSet res = preparedStatement.executeQuery();
    if(!res.next()) {
        System.out.println("No books in the table with id 1");
    } else {
        // got book's info, which id is 1
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

### 插入示例

还是使用 [books 表](/develop/dev-guide-bookshop-schema-design.md#books-表)为例，需要插入一个 `title` 为 `TiDB Developer Guide`, `type` 为 `Science & Technology`, `stock` 为 `100`, `price` 为 `0.0`, `published_at` 为 `插入的当前时间` 的书籍信息。需要注意的是，`books` 表的主键包含 `AUTO_RANDOM` 属性，无需指定它。如果你对插入数据还不了解，可以在[插入数据](/develop/dev-guide-insert-data.md)一节了解更多数据插入的相关信息。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

使用 SQL 插入数据示例如下：

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

运行结果为：

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

运行结果为：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

运行结果为：

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" value="java">

使用 Java 插入数据示例如下：

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

可以看到，JDBC 帮你管控了预处理语句的生命周期，而无需你在应用程序里手动使用预处理语句的创建、使用、删除等。但值得注意的是，因为 TiDB 兼容 MySQL 协议，在客户端使用 MySQL JDBC Driver 的过程中，其默认配置并非开启 **_服务端_** 的预处理语句选项，而是使用客户端的预处理语句。你需要关注以下配置项，来获得在 JDBC 下 TiDB 服务端预处理语句的支持，及在你的使用场景下的最佳配置：

|          参数           |                 作用                  |           推荐场景           |         推荐配置         |
| :---------------------: | :-----------------------------------: | :--------------------------: | :----------------------: |
|  `useServerPrepStmts`   |   是否使用服务端开启预处理语句支持    |  在需要多次使用预处理语句时  |          `true`          |
|    `cachePrepStmts`     |       客户端是否缓存预处理语句        | `useServerPrepStmts=true` 时 |          `true`          |
| `prepStmtCacheSqlLimit` |  预处理语句最大大小（默认 256 字符）  |  预处理语句大于 256 字符时   | 按实际预处理语句大小配置 |
|   `prepStmtCacheSize`   | 预处理语句最大缓存数量 （默认 25 条） |  预处理语句数量大于 25 条时  | 按实际预处理语句数量配置 |

在此处给出一个较为的通用场景的 JDBC 连接字符串配置，以 Host: `127.0.0.1`，Port: `4000`，用户: `root`，密码: 空，默认数据库: `test`为例：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

你也可以查看[插入行](/develop/dev-guide-insert-data.md#插入行)一章，来查看是否需要在插入数据场景下更改其他 JDBC 的参数。

有关 Java 的完整示例，可参阅：

- [TiDB 和 JDBC 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java-jdbc.md)
- [TiDB 和 Hibernate 的简单 CRUD 应用程序](/develop/dev-guide-sample-application-java-hibernate.md)
- [使用 Spring Boot 构建 TiDB 应用程序](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

</SimpleTab>
