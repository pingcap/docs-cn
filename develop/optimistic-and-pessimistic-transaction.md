---
title: 乐观事务和悲观事务
---

# 乐观事务和悲观事务

简单的讲，[乐观事务](https://docs.pingcap.com/zh/tidb/stable/optimistic-transaction)模型就是直接提交，遇到冲突就回滚，[悲观事务](https://docs.pingcap.com/zh/tidb/stable/pessimistic-transaction)模型就是在真正提交事务前，先尝试对需要修改的资源上锁，只有在确保事务一定能够执行成功后，才开始提交。

对于乐观事务模型来说，比较适合冲突率不高的场景，因为直接提交大概率会成功，冲突是小概率事件，但是一旦遇到事务冲突，回滚的代价会比较大。

悲观事务的好处是对于冲突率高的场景，提前上锁的代价小于事后回滚的代价，而且还能以比较低的代价解决多个并发事务互相冲突导致谁也成功不了的场景。不过悲观事务在冲突率不高的场景并没有乐观事务处理高效。

从应用端实现的复杂度而言，悲观事务更直观，更容易实现。而乐观事务需要复杂的应用端重试机制来保证。

下面用 [bookshop](/develop/bookshop-schema-design.md) 数据库中的表实现一个购书的例子来演示乐观事务和悲观事务的区别以及优缺点。购书流程主要包括：

- 更新库存数量
- 创建订单
- 付款

这三个操作需要保证全部成功或者全部失败，并且在并发情况下要保证不超卖。

## 悲观事务

下面代码以悲观事务的方式，用两个线程模拟了两个用户并发买同一本书的过程，书店剩余 10 本，Bob 购买了 6 本，Alice 购买了 4 本。两个人几乎同一时间完成订单，最终，这本书的剩余库存为零。

<SimpleTab>

<div label="ruby"></div>

<div label="java">

因为我们使用多个线程模拟多用户同时插入的情况，因此我们需要使用一个线程安全的连接对象，这里我们使用 Java 当前较流行的连接池 [HikariCP](https://github.com/brettwooldridge/HikariCP) 作为我们此处 Demo 使用的线程池。

如果您使用 Maven 作为包管理，在 `pom.xml` 中的 `<dependencies>` 节点中，加入以下依赖来引入 `HikariCP`，同时设定打包目标，及 JAR 包启动的主类，完整的 `pom.xml` 如下所示:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.pingcap</groupId>
  <artifactId>plain-java-txn</artifactId>
  <version>0.0.1</version>

  <name>plain-java-jdbc</name>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.13.2</version>
      <scope>test</scope>
    </dependency>

    <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.0.28</version>
    </dependency>

    <dependency>
      <groupId>com.zaxxer</groupId>
      <artifactId>HikariCP</artifactId>
      <version>5.0.1</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
          <archive>
            <manifest>
              <mainClass>com.pingcap.txn.TxnExample</mainClass>
            </manifest>
          </archive>

        </configuration>
        <executions>
          <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>

</project>
```

随后编写代码：

```java
package com.pingcap.txn;

import com.zaxxer.hikari.HikariDataSource;

import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;
import java.util.concurrent.*;

public class TxnExample {
    public static void main(String[] args) throws SQLException, InterruptedException {
        System.out.println(Arrays.toString(args));
        int aliceQuantity = 0;
        int bobQuantity = 0;

        for (String arg: args) {
            if (arg.startsWith("ALICE_NUM")) {
                aliceQuantity = Integer.parseInt(arg.replace("ALICE_NUM=", ""));
            }

            if (arg.startsWith("BOB_NUM")) {
                bobQuantity = Integer.parseInt(arg.replace("BOB_NUM=", ""));
            }
        }

        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/bookshop?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");
        ds.setPassword("");

        // prepare data
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity);
            countDownLatch.countDown();
        });

        countDownLatch.await(5, TimeUnit.SECONDS);
    }

    public static void createUser(Connection connection, Long id, String nickname, BigDecimal balance) throws SQLException  {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, nickname);
        insert.setBigDecimal(3, balance);
        insert.executeUpdate();
    }

    public static void createBook(Connection connection, Long id, String title, String type, Timestamp publishedAt, BigDecimal price, Integer stock) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, title);
        insert.setString(3, type);
        insert.setTimestamp(4, publishedAt);
        insert.setBigDecimal(5, price);
        insert.setInt(6, stock);

        insert.executeUpdate();
    }

    public static void buy (HikariDataSource ds, Integer threadID,
                            Long orderID, Long bookID, Long userID, Integer quantity) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin pessimistic");

                // waiting for other thread ran the 'begin pessimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "select price from books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                }

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                int affectedRows = updateBook.executeUpdate();

                if (affectedRows == 0) {
                    // stock not enough, rollback
                    connection.createStatement().executeUpdate(txnComment + "rollback");
                    return;
                }

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                e.printStackTrace();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

</div>
</SimpleTab>

运行示例程序：

<SimpleTab>
<div label="ruby"></div>
<div label="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=6
```

</div>

</SimpleTab>

SQL 日志：

```sql
/* txn 1 */ begin pessimistic
    /* txn 2 */ begin pessimistic
    /* txn 2 */ select * from books where id = 1 for update
    /* txn 2 */ update books set stock = stock - 4 where id = 1 and stock - 4 >= 0
    /* txn 2 */ insert into orders (id, book_id, user_id, quality) values (1001, 1, 1, 4)
    /* txn 2 */ update users set balance = balance - 400.0 where id = 2
    /* txn 2 */ commit
/* txn 1 */ select * from books where id = 1 for update
/* txn 1 */ update books set stock = stock - 6 where id = 1 and stock - 6 >= 0
/* txn 1 */ insert into orders (id, book_id, user_id, quality) values (1000, 1, 1, 6)
/* txn 1 */ update users set balance = balance - 600.0 where id = 1
/* txn 1 */ commit
```

最后，我们检验一下订单创建、用户余额扣减、图书库存扣减情况，都符合预期。

```sql
mysql> select * from books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> select * from orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 10:58:12 |
| 1001 |       1 |       1 |       4 | 2022-04-19 10:58:11 |
+------+---------+---------+---------+---------------------+
2 rows in set (0.01 sec)

mysql> select * from users;
+----+---------+----------+
| id | balance | nickname |
+----+---------+----------+
|  1 | 9400.00 | Bob      |
|  2 | 9600.00 | Alice    |
+----+---------+----------+
2 rows in set (0.00 sec)
```

可以再把难度加大，如果图书的库存剩余 10 本，Bob 购买 7 本， Alice 购买 4 本，两人几乎同时下单，结果会是怎样？我们继续复用上个例子里的代码来解决这个需求，只不过把 Bob 购买数量从 6 改成 7:

运行示例程序：

<SimpleTab>
<div label="ruby"></div>
<div label="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=7
```

</div>

</SimpleTab>

```sql
/* txn 1 */ begin pessimistic
    /* txn 2 */ begin pessimistic
    /* txn 2 */ select * from books where id = 1 for update
    /* txn 2 */ update books set stock = stock - 4 where id = 1 and stock - 4 >= 0
    /* txn 2 */ insert into orders (id, book_id, user_id, quality) values (1001, 1, 1, 4)
    /* txn 2 */ update users set balance = balance - 400.0 where id = 2
    /* txn 2 */ commit
/* txn 1 */ select * from books where id = 1 for update
/* txn 1 */ update books set stock = stock - 7 where id = 1 and stock - 7 >= 0
/* txn 1 */ rollback
```

由于 `txn 2` 抢先获得锁资源，更新了 stock，`txn 1` 里面 `affected_rows` 返回值为 0，进入了 `rollback` 流程。

我们再检验一下订单创建、用户余额扣减、图书库存扣减情况。Alice 下单 4 本书成功，Bob 下单 7 本书失败，库存剩余 6 本符合预期。

```sql
mysql> select * from books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     6 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> select * from orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1001 |       1 |       1 |       4 | 2022-04-19 11:03:03 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> select * from users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.01 sec)
```

## 乐观事务

下面代码以乐观事务的方式，用两个线程模拟了两个用户并发买同一本书的过程，和悲观事务的示例一样。书店剩余 10 本，Bob 购买了 6 本，Alice 购买了 4 本。两个人几乎同一时间完成订单，最终，这本书的剩余库存为零。

<SimpleTab>
<div label="ruby"></div>
<div label="java">

```java
package com.pingcap.txn.optimistic;

import com.zaxxer.hikari.HikariDataSource;

import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;
import java.util.concurrent.*;

public class TxnExample {
    public static void main(String[] args) throws SQLException, InterruptedException {
        System.out.println(Arrays.toString(args));
        int aliceQuantity = 0;
        int bobQuantity = 0;

        for (String arg: args) {
            if (arg.startsWith("ALICE_NUM")) {
                aliceQuantity = Integer.parseInt(arg.replace("ALICE_NUM=", ""));
            }

            if (arg.startsWith("BOB_NUM")) {
                bobQuantity = Integer.parseInt(arg.replace("BOB_NUM=", ""));
            }
        }

        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/bookshop?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");
        ds.setPassword("");

        // prepare data
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity, 5);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity, 5);
            countDownLatch.countDown();
        });

        countDownLatch.await(5, TimeUnit.SECONDS);
    }

    public static void createUser(Connection connection, Long id, String nickname, BigDecimal balance) throws SQLException  {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, nickname);
        insert.setBigDecimal(3, balance);
        insert.executeUpdate();
    }

    public static void createBook(Connection connection, Long id, String title, String type, Timestamp publishedAt, BigDecimal price, Integer stock) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, title);
        insert.setString(3, type);
        insert.setTimestamp(4, publishedAt);
        insert.setBigDecimal(5, price);
        insert.setInt(6, stock);

        insert.executeUpdate();
    }

    public static void buy (HikariDataSource ds, Integer threadID, Long orderID, Long bookID,
                            Long userID, Integer quantity, Integer retryTimes) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {

                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin optimistic");

                // waiting for other thread ran the 'begin optimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "select * from books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                    int stock = res.getInt("stock");
                    if (stock < quantity) {
                        throw new RuntimeException("book not enough");
                    }
                }

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                updateBook.executeUpdate();

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                System.out.println("error occurred: " + e.getMessage());

                if (e instanceof SQLException sqlException) {
                    switch (sqlException.getErrorCode()) {
                        // You can get all error codes at https://docs.pingcap.com/tidb/stable/error-codes
                        case 9007: // Transactions in TiKV encounter write conflicts.
                        case 8028: // table schema changes
                        case 8002: // "SELECT FOR UPDATE" commit conflict
                        case 8022: // The transaction commit fails and has been rolled back
                            if (retryTimes != 0) {
                                System.out.println("rest " + retryTimes + " times. retry for " + e.getMessage());
                                buy(ds, threadID, orderID, bookID, userID, quantity, retryTimes - 1);
                            }
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

此处，需将 `pom.xml` 中启动类

```xml
<mainClass>com.pingcap.txn.TxnExample</mainClass>
```

更改为：

```xml
<mainClass>com.pingcap.txn.optimistic.TxnExample</mainClass>
```

来指向乐观事务的例子

</div>
</SimpleTab>

运行示例程序：

<SimpleTab>
<div label="ruby"></div>
<div label="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=6
```

</div>

</SimpleTab>

SQL 语句执行过程：

```sql
    /* txn 2 */ begin optimistic
/* txn 1 */ begin optimistic
    /* txn 2 */ select * from books where id = 1 for update
    /* txn 2 */ update books set stock = stock - 4 where id = 1 and stock - 4 >= 0
    /* txn 2 */ insert into orders (id, book_id, user_id, quality) values (1001, 1, 1, 4)
    /* txn 2 */ update users set balance = balance - 400.0 where id = 2
    /* txn 2 */ commit
/* txn 1 */ select * from books where id = 1 for update
/* txn 1 */ update books set stock = stock - 6 where id = 1 and stock - 6 >= 0
/* txn 1 */ insert into orders (id, book_id, user_id, quality) values (1000, 1, 1, 6)
/* txn 1 */ update users set balance = balance - 600.0 where id = 1
retry 1 times for 9007 Write conflict, txnStartTS=432618733006225412, conflictStartTS=432618733006225411, conflictCommitTS=432618733006225414, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ begin optimistic
/* txn 1 */ select * from books where id = 1 for update
/* txn 1 */ update books set stock = stock - 6 where id = 1 and stock - 6 >= 0
/* txn 1 */ insert into orders (id, book_id, user_id, quality) values (1000, 1, 1, 6)
/* txn 1 */ update users set balance = balance - 600.0 where id = 1
/* txn 1 */ commit
```

在乐观事务模式下，由于中间状态不一定正确，不能像悲观事务模式一样，通过 `affected_rows` 来判断某个语句是否执行成功。我们需要把事务看做一个整体，通过最终的 COMMIT 语句是否返回异常来判断当前事务是否发生写冲突。

从上面 SQL 日志可以看出，由于两个事务并发执行，并且对同一条记录做了修改，`txn 1` COMMIT 之后抛出了 `9007 Write conflict` 异常。对于乐观事务写冲突，在应用端可以进行安全的重试，重试一次之后提交成功，最终执行结果符合预期：

```sql
mysql> select * from books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.01 sec)

mysql> select * from orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 03:18:19 |
| 1001 |       1 |       1 |       4 | 2022-04-19 03:18:17 |
+------+---------+---------+---------+---------------------+
2 rows in set (0.01 sec)

mysql> select * from users;
+----+---------+----------+
| id | balance | nickname |
+----+---------+----------+
|  1 | 9400.00 | Bob      |
|  2 | 9600.00 | Alice    |
+----+---------+----------+
2 rows in set (0.00 sec)
```

再来看一下用乐观事务防止超卖的例子，如果图书的库存剩余 10 本，Bob 购买 7 本， Alice 购买 4 本，两人几乎同时下单，结果会是怎样？我们继续复用乐观事务例子里的代码来解决这个需求，只不过把 Bob 购买数量从 6 改成 7:

运行示例程序：

<SimpleTab>

<div label="ruby">

```shell
BOB_NUM=7 ALICE_NUM=4 ./optimistic_txn
```

</div>

<div label="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=7
```

</div>

</SimpleTab>

```sql
/* txn 1 */ begin optimistic
    /* txn 2 */ begin optimistic
    /* txn 2 */ select * from books where id = 1 for update
    /* txn 2 */ update books set stock = stock - 4 where id = 1 and stock - 4 >= 0
    /* txn 2 */ insert into orders (id, book_id, user_id, quality) values (1001, 1, 1, 4)
    /* txn 2 */ update users set balance = balance - 400.0 where id = 2
    /* txn 2 */ commit
/* txn 1 */ select * from books where id = 1 for update
/* txn 1 */ update books set stock = stock - 7 where id = 1 and stock - 7 >= 0
/* txn 1 */ insert into orders (id, book_id, user_id, quality) values (1000, 1, 1, 7)
/* txn 1 */ update users set balance = balance - 700.0 where id = 1
retry 1 times for 9007 Write conflict, txnStartTS=432619094333980675, conflictStartTS=432619094333980676, conflictCommitTS=432619094333980678, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ begin optimistic
/* txn 1 */ select * from books where id = 1 for update
Fail -> out of stock
/* txn 1 */ rollback
```

从上面的 SQL 日志可以看出，第一次执行由于写冲突，`txn 1` 在应用端进行了重试，从获取到的最新快照对比发现，剩余库存不够，应用端抛出 `out of stock` 异常结束。

```sql
mysql> select * from books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     6 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> select * from orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1001 |       1 |       1 |       4 | 2022-04-19 03:41:16 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> select * from users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.00 sec)
```
