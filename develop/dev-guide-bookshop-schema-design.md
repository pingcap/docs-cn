---
title: Bookshop 应用
summary: Bookshop 应用设计、数据导入、连接数据库等操作。
aliases: ['/zh/tidb/dev/bookshop-schema-design']
---

# Bookshop 应用

Bookshop 是一个虚拟的在线书店应用，你可以在 Bookshop 当中便捷地购买到各种类别的书，也可以对你看过的书进行点评。

为了方便你阅读应用开发指南中的内容，我们将以 Bookshop 应用的[数据表结构](#数据表详解)和数据为基础来编写示例 SQL。本章节将为你介绍如何导入该应用的表结构和数据，以及其数据表结构的定义。

## 导入表结构和数据

你可以[通过 TiUP](#方法一通过-tiup-demo-命令行) 或[通过 TiDB Cloud Import](#方法二通过-tidb-cloud-import-功能) 两种方式导入 Bookshop 应用的表结构和数据。

### 方法一：通过 `tiup demo` 命令行

如果你使用 [TiUP](/tiup/tiup-reference.md#tiup-命令概览) 部署 TiDB 集群或者你可以直接连接到你的 TiDB 服务器，你可以通过如下命令快速生成并导入 Bookshop 应用的示例数据：

```shell
tiup demo bookshop prepare
```

该命令默认会连接到 `127.0.0.1` 地址上的 `4000` 端口，使用 `root` 用户名进行无密码登录，默认在名为 `bookshop` 的数据库中创建[表结构](#数据表详解)。

#### 配置连接信息

你可以通过如下参数修改默认的连接信息：

| 参数         | 简写 | 默认值      | 解释           |
| ------------ | ---- | ----------- | -------------- |
| `--host`     | `-H` | `127.0.0.1` | 数据库地址     |
| `--port`     | `-P` | `4000`      | 数据库端口     |
| `--user`     | `-U` | `root`      | 数据库用户     |
| `--password` | `-p` | 无          | 数据库用户密码 |
| `--db`       | `-D` | `bookshop`  | 数据库名称     |

例如，你想要连接到 TiDB Cloud 上的数据库，你可以如下命令指定连接信息进行连接：

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### 设置数据量

另外，你还可以通过如下参数指定各个数据库表生成的数据量：

| 参数        | 默认值   | 解释                              |
| ----------- | -------- | --------------------------------- |
| `--users`   | `10000`  | 指定在 `users` 表生成的数据行数   |
| `--authors` | `20000`  | 指定在 `authors` 表生成的数据行数 |
| `--books`   | `20000`  | 指定在 `books` 表生成的数据行数   |
| `--orders`  | `300000` | 指定在 `orders` 表生成的数据行数  |
| `--ratings` | `300000` | 指定在 `ratings` 表生成的数据行数 |

例如，以下命令通过 `--users` 参数指定生成 20 万行用户信息，通过 `--books` 参数指定生成 50 万行书籍的基本信息，通过 `--authors` 参数指定生成 10 万的作者信息，通过 `--ratings` 参数指定生成 100 万的评分记录，通过 `--orders` 参数指定生成 100 万的订单记录。

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

通过 `--drop-tables` 参数你可以删除原有的表结构，更多的参数说明你可以通过命令 `tiup demo bookshop --help` 进行了解。

### 方法二：通过 TiDB Cloud Import 功能

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud](https://tidbcloud.com/)，导航至 [**Clusters**](https://tidbcloud.com/console/clusters) 页面。

        > **Tip:**
        >
        > 如果你有多个 TiDB Cloud 项目，可以点击左下角的 <MDSvgIcon name="icon-left-projects" /> 切换项目。

    2. 点击目标集群的名称，进入集群的 **Overview** 页面，然后在左侧导航栏中点击 **Import**。

2. 选择 **Import data from S3**。

    如果这是你第一次使用 TiDB Cloud 的导入功能，选择 **Import From Amazon S3**。

3. 在 **Import Data from Amazon S3** 页面，配置以下源数据信息：

    - **Import File Count**：选择 **Multiple files**
    - **Included Schema Files**：选择 **Yes**
    - **Data Format**：选择 **SQL**
    - **Folder URI**：输入 `s3://developer.pingcap.com/bookshop/`
    - **Bucket Access**：选择 **AWS Role ARN**
    - **Role ARN**：输入 `arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access`

    在这个示例数据当中，预先生成了 20 万的用户信息、50 万条书籍信息、10 万条作者信息、100 万条评分记录以及 100 万条订单信息。

4. 点击 **Connect** > **Start Import** 开始导入数据，等待 TiDB Cloud 完成数据导入。

你可以通过 [TiDB Cloud Migration Overview](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview) 文档获取更多有关 TiDB Cloud 数据导入和迁移的信息。

### 查看数据导入情况

导入完成后，你可以通过下面的 SQL 语句查看各个表的数据量信息：

```sql
SELECT
    CONCAT(table_schema,'.',table_name) AS 'Table Name',
    table_rows AS 'Number of Rows',
    CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size',
    CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size',
    CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS 'Total'
FROM
    information_schema.TABLES
WHERE table_schema LIKE 'bookshop';
```

运行结果为：

```
+-----------------------+----------------+-----------+------------+---------+
| Table Name            | Number of Rows | Data Size | Index Size | Total   |
+-----------------------+----------------+-----------+------------+---------+
| bookshop.orders       |        1000000 | 0.0373G   | 0.0075G    | 0.0447G |
| bookshop.book_authors |        1000000 | 0.0149G   | 0.0149G    | 0.0298G |
| bookshop.ratings      |        4000000 | 0.1192G   | 0.1192G    | 0.2384G |
| bookshop.authors      |         100000 | 0.0043G   | 0.0000G    | 0.0043G |
| bookshop.users        |         195348 | 0.0048G   | 0.0021G    | 0.0069G |
| bookshop.books        |        1000000 | 0.0546G   | 0.0000G    | 0.0546G |
+-----------------------+----------------+-----------+------------+---------+
6 rows in set (0.03 sec)
```

## 数据表详解

以下将详细介绍 Bookshop 应用程序的数据库表结构：

### `books` 表

该表用于存储书籍的基本信息。

| 字段名        | 类型          | 含义                                  |
|--------------|---------------|---------------------------------------|
| id           | bigint    | 书籍的唯一标识                        |
| title        | varchar(100)  | 书籍名称                              |
| type         | enum          | 书籍类型（如：杂志、动漫、教辅等）    |
| stock        | bigint    | 库存                                  |
| price        | decimal(15,2) | 价格                                  |
| published_at | datetime      | 出版时间                              |

### `authors` 表

该表用于存储作者的基本信息。

| 字段名      | 类型         | 含义                                |
|------------|--------------|-------------------------------------|
| id         | bigint   | 作者的唯一标识                       |
| name       | varchar(100) | 姓名                                |
| gender     | tinyint   | 生理性别 (0: 女, 1: 男，NULL: 未知)   |
| birth_year | smallint  | 生年                                |
| death_year | smallint  | 卒年                                |

### `users` 表

该表用于存储使用 Bookshop 应用程序的用户。

| 字段名    | 类型          | 含义            |
|----------|---------------|----------------|
| id       | bigint    | 用户的唯一标识   |
| balance  | decimal(15,2) | 余额           |
| nickname | varchar(100)  | 昵称           |

### `ratings` 表

该表用于存储用户对书籍的评分记录。

| 字段名    | 类型     | 含义                                        |
|----------|----------|---------------------------------------------|
| book_id  | bigint   | 书籍的唯一标识（关联至 [books](#books-表)）     |
| user_id  | bigint   | 用户的唯一标识（关联至 [users](#users-表)）    |
| score    | tinyint  | 用户评分 (1-5)                              |
| rated_at | datetime | 评分时间                                    |

### `book_authors` 表

一个作者可能会编写多本书，一本书可能需要多个作者同时编写，该表用于存储书籍与作者之间的对应关系。

| 字段名     | 类型       | 含义                                        |
|-----------|------------|--------------------------------------------|
| book_id   | bigint | 书籍的唯一标识（关联至 [books](#books-表)）     |
| author_id | bigint | 作者的唯一标识（关联至 [authors](#authors-表)） |

### `orders` 表

该表用于存储用户购买书籍的订单信息。

| 字段名      | 类型       | 含义                                        |
|------------|------------|--------------------------------------------|
| id         | bigint | 订单的唯一标识                               |
| book_id    | bigint | 书籍的唯一标识（关联至 [books](#books-表)）    |
| user_id    | bigint | 用户唯一标识（关联至 [users](#users-表)）      |
| quantity   | tinyint | 购买数量                                    |
| ordered_at | datetime   | 购买时间                                    |

## 数据库初始化 `dbinit.sql` 脚本

如果你希望手动创建 Bookshop 应用的数据库表结构，你可以运行以下 SQL 语句：

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint DEFAULT NULL,
  `birth_year` smallint DEFAULT NULL,
  `death_year` smallint DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`ratings`;
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `score` tinyint NOT NULL,
  `rated_at` datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED,
  UNIQUE KEY `uniq_book_user_idx` (`book_id`,`user_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;

DROP TABLE IF EXISTS `bookshop`.`users`;
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.0',
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`orders`;
CREATE TABLE `bookshop`.`orders` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `quality` tinyint NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```
