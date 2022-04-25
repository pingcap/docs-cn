---
title: Bookshop 应用
---

# Bookshop 应用

Bookshop 是一个虚拟的在线书店应用，你可以在 Bookshop 当中便捷地购买到各种类别的书，也可以对你看过的书进行点评。

## 导入数据

### 方式 1: 通过 `tiup demo` 命令行

如果你使用 [TiUP](https://docs.pingcap.com/zh/tidb/stable/tiup-reference#tiup) 部署 TiDB 集群或者你可以直接连接到你的 TiDB 服务器，你可以通过如下命令快速生成并导入 Bookshop 应用的示例数据：

```shell
tiup demo bookshop prepare
```

该命令默认会连接到 `127.0.0.1` 地址上的 `4000` 端口，使用 `root` 账号进行无密码登录，默认在名为 `bookshop` 的数据库中创建[表结构](#数据表详解)。

#### 配置连接信息

你可以通过如下参数修改默认的连接信息：

| 参数         | 简写  | 默认值      | 解释            |
|--------------|------|-------------|---------------|
| `--host`     | `-H` | `127.0.0.1` | 数据库地址     |
| `--port`     | `-P` | `4000`      | 数据库端口     |
| `--user`     | `-U` | `root`      | 数据库用户     |
| `--password` | `-p` | 无          | 数据库用户密码  |
| `--db`       | `-D` | `bookshop`  | 数据库名称     |

例如，你想要连接到 TiDB Cloud 上的数据库，你可以如下命令指定连接信息进行连接：

```
tiup demo bookshop prepare -U root -H tidb.xxx.yyy.ap-northeast-1.prod.aws.tidbcloud.com -P 4000 -p
```

#### 设置数据量

另外，你还可以通过如下参数指定各个数据库表生成的数据量：

| 参数        | 默认值   | 解释                             |
|-------------|----------|-------------------------------|
| `--users`   | `10000`  | 指定在 `users` 表生成的数据行数   |
| `--authors` | `20000`  | 指定在 `authors` 表生成的数据行数 |
| `--books`   | `20000`  | 指定在 `books` 表生成的数据行数   |
| `--orders`  | `300000` | 指定在 `orders` 表生成的数据行数  |
| `--ratings` | `300000` | 指定在 `ratings` 表生成的数据行数 |

例如，以下命令通过 `--books` 参数指定生成 50 万行书籍的基本信息，通过 `--authors` 参数指定生成 10 万的作者信息，通过 `--ratings` 参数指定生成 100 万的评分记录，通过 `--orders` 参数指定生成 100 万的订单记录。

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

通过 `--drop-tables` 参数你可以删除原有的表结构，更多的参数说明你可以通过命令 `tiup demo bookshop --help` 进行了解。

### 方式 2: 通过 TiDB Cloud Import 功能

在 TiDB Cloud 的数据库详情页面，你可以通过点击**Import**按钮，进入到**Data Import Task**页面，在该页面当中，按照以下步骤将 Bookshop 示例数据从 AWS S3 中导入到你的 TiDB Cloud：

1. 将以下 **Bucket URL** 和 **Role-ARN** 复制到页面上对应的输入框当中

    **Bucket URL**:

    ```
    s3://developer.pingcap.com/bookshop/
    ```

    **Role-ARN**:

    ```
    arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access
    ```

    在这个示例数据当中，预先生成了 20 万的用户信息、50 万条书籍信息、10 万条作者信息、100 万条评分记录以及 100 万条订单信息。

2. 选择 **Bucket Region** 为 **US West (Oregon)**
3. 选择 **Data Format** 为 **TiDB Dumpling**

    ![在 TiDB Cloud 中导入 Bookshop 数据](media/tidb_cloud_import_bookshop_data.png)

4. 输入你的数据库登录信息
5. 点击 **Import** 按钮确认导入
6. 等待 TiDB Cloud 完成数据导入

    ![Bookshop 数据导入中](media/importing_bookshop_data.png)

    如果导入过程中出现如下错误信息，你需要通过 `DROP bookshop;` 命令将原来创建的示例数据库进行清除后再重新导入。

    > table(s) [`bookshop`.`authors`, `bookshop`.`book_authors`, `bookshop`.`books`, `bookshop`.`orders`, `bookshop`.`ratings`, `bookshop`.`users`] are not empty.


### 查看数据导入情况

导入完成后，你可以通过下面的 SQL 语句各个表的数据量信息：

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

|    字段名    |     类型      |                 含义                  |
| :----------: | :-----------: | :-----------------------------------: |
|      id      |  bigint(20)   |            书籍的唯一标识             |
|    title     | varchar(100)  |               书籍名称                |
|     type     |     enum      | 书籍类型（如：杂志 / 动漫 / 教辅 等） |
|    stock     |  bigint(20)   |                 库存                  |
|    price     | decimal(15,2) |                 价格                  |
| published_at |   datetime    |               出版时间                |

### `authors` 表

该表用于存储作者的基本信息。

|   字段名   |     类型     |                含义                 |
| :--------: | :----------: | :---------------------------------: |
|     id     |  bigint(20)  |           作者的唯一标识            |
|    name    | varchar(100) |                姓名                 |
|   gender   |  tinyint(1)  | 生理性别 (0: 女, 1: 男，NULL: 未知) |
| birth_year | smallint(6)  |                生年                 |
| death_year | smallint(6)  |                卒年                 |

### `users` 表

该表用于存储使用 Bookshop 应用程序的用户。

|  字段名  |     类型      |      含义      |
| :------: | :-----------: | :------------: |
|    id    |  bigint(20)   | 用户的唯一标识 |
| balance  | decimal(15,2) |      余额      |
| nickname | varchar(100)  |      昵称      |

### `ratings` 表

该表用于存储用户对书籍的评分记录，并开启 1 个 TiFlash 列存副本。

|  字段名  |   类型   |                    含义                     |
| :------: | :------: | :-----------------------------------------: |
| book_id  |  bigint  | 书籍的唯一标识（关联至 [books](#books-表)） |
| user_id  |  bigint  | 用户的唯一标识（关联至 [users](#users-表)） |
|  score   | tinyint  |               用户评分 (1-5)                |
| rated_at | datetime |                  评分时间                   |

### `book_authors` 表

一个作者可能会编写多本书，一本书可能需要多个作者同时编写，该表用于存储书籍与作者之间的对应关系。

|  字段名   |    类型    |                      含义                       |
| :-------: | :--------: | :---------------------------------------------: |
|  book_id  | bigint(20) |   书籍的唯一标识（关联至 [books](#books-表)）   |
| author_id | bigint(20) | 作者的唯一标识（关联至 [authors](#authors-表)） |

### `orders` 表

存储 用户购买书籍票信息

|   字段名   |    类型    |                    含义                     |
| :--------: | :--------: | :-----------------------------------------: |
|     id     | bigint(20) |               订单的唯一标识                |
|  book_id   | bigint(20) | 书籍的唯一标识（关联至 [books](#books-表)） |
|  user_id   | bigint(20) |  用户唯一标识（关联至 [users](#users-表)）  |
|  quantity  | tinyint(4) |                  购买数量                   |
| ordered_at |  datetime  |                  购买时间                   |

## 数据库初始化 `dbinit.sql` 脚本

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `birth_year` smallint(6) DEFAULT NULL,
  `death_year` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint(20) NOT NULL,
  `author_id` bigint(20) NOT NULL,
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
ALTER TABLE `bookshop`.`rating` SET TIFLASH REPLICA 1;

DROP TABLE IF EXISTS `bookshop`.`users`;
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.0',
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`orders`;
CREATE TABLE `bookshop`.`orders` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `quality` tinyint(4) NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```
