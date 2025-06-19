---
title: Bookshop 示例应用程序
summary: Bookshop 是一个用于购买和评价图书的在线书店应用程序。您可以通过 TiUP 或 TiDB Cloud 导入表结构和数据。方法 1 使用 TiUP 快速生成和导入示例数据，而方法 2 从 Amazon S3 导入数据到 TiDB Cloud。数据库表包括 books、authors、users、ratings、book_authors 和 orders。数据库初始化脚本 `dbinit.sql` 创建 Bookshop 应用程序的表结构。
---

# Bookshop 示例应用程序

Bookshop 是一个虚拟的在线书店应用程序，通过它您可以购买各种类别的图书并对您读过的图书进行评分。

为了使您更顺利地阅读应用程序开发者指南，我们基于 Bookshop 应用程序的[表结构](#表说明)和数据展示示例 SQL 语句。本文重点介绍导入表结构和数据的方法以及表结构的定义。

## 导入表结构和数据

<CustomContent platform="tidb">

您可以通过 [TiUP](#方法-1通过-tiup-demo) 或 [TiDB Cloud 的导入功能](#方法-2通过-tidb-cloud-导入)导入 Bookshop 表结构和数据。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB Cloud，您可以跳过[方法 1：通过 `tiup demo`](#方法-1通过-tiup-demo)，直接[通过 TiDB Cloud 的导入功能](#方法-2通过-tidb-cloud-导入)导入 Bookshop 表结构。

</CustomContent>

### 方法 1：通过 `tiup demo`

<CustomContent platform="tidb">

如果您的 TiDB 集群是使用 [TiUP](/tiup/tiup-reference.md#tiup-reference) 部署的，或者您可以连接到您的 TiDB 服务器，您可以通过运行以下命令快速生成和导入 Bookshop 应用程序的示例数据：

</CustomContent>

<CustomContent platform="tidb-cloud">

如果您的 TiDB 集群是使用 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-reference) 部署的，或者您可以连接到您的 TiDB 服务器，您可以通过运行以下命令快速生成和导入 Bookshop 应用程序的示例数据：

</CustomContent>

```shell
tiup demo bookshop prepare
```

默认情况下，此命令使您的应用程序能够连接到地址 `127.0.0.1` 的端口 `4000`，使您能够以无密码的 `root` 用户身份登录，并在名为 `bookshop` 的数据库中创建[表结构](#表说明)。

#### 配置连接信息

下表列出了连接参数。您可以更改它们的默认设置以匹配您的环境。

| 参数名称     | 缩写 | 默认值       | 描述           |
| ------------ | ---- | ----------- | -------------- |
| `--password` | `-p` | 无          | 数据库用户密码 |
| `--host`     | `-H` | `127.0.0.1` | 数据库地址     |
| `--port`     | `-P` | `4000`      | 数据库端口     |
| `--db`       | `-D` | `bookshop`  | 数据库名称     |
| `--user`     | `-U` | `root`      | 数据库用户     |

例如，如果您想连接到 TiDB Cloud 上的数据库，可以按如下方式指定连接信息：

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### 设置数据量

您可以通过配置以下参数来指定在每个数据库表中生成的数据量：

| 参数名称     | 默认值     | 描述                              |
| ----------- | -------- | --------------------------------- |
| `--users`   | `10000`  | 在 `users` 表中生成的数据行数   |
| `--authors` | `20000`  | 在 `authors` 表中生成的行数 |
| `--books`   | `20000`  | 在 `books` 表中生成的数据行数   |
| `--orders`  | `300000` | 在 `orders` 表中生成的数据行数  |
| `--ratings` | `300000` | 在 `ratings` 表中生成的数据行数 |

例如，执行以下命令生成：

- 通过 `--users` 参数生成 200,000 行用户信息
- 通过 `--books` 参数生成 500,000 行图书信息
- 通过 `--authors` 参数生成 100,000 行作者信息
- 通过 `--ratings` 参数生成 1,000,000 行评分记录
- 通过 `--orders` 参数生成 1,000,000 行订单记录

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

您可以通过 `--drop-tables` 参数删除原有的表结构。有关更多参数说明，请运行 `tiup demo bookshop --help` 命令。

### 方法 2：通过 TiDB Cloud 导入

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 您可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后点击左侧导航栏中的**导入**。

2. 选择**从云存储导入数据**，然后点击 **Amazon S3**。

3. 在**从 Amazon S3 导入数据**页面上，配置以下源数据信息：

    - **导入文件数量**：对于 TiDB Cloud Serverless，选择**多个文件**。此字段在 TiDB Cloud Dedicated 中不可用。
    - **包含模式文件**：选择**是**。
    - **数据格式**：选择 **SQL**。
    - **文件夹 URI**：输入 `s3://developer.pingcap.com/bookshop/`。
    - **存储桶访问**：选择 **AWS Role ARN**。
    - **Role ARN**：输入 `arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access`。

    在此示例中，预先生成了以下数据：

    - 200,000 行用户信息
    - 500,000 行图书信息
    - 100,000 行作者信息
    - 1,000,000 行评分记录
    - 1,000,000 行订单记录

4. 点击**连接** > **开始导入**以启动导入过程，并等待 TiDB Cloud 完成导入。

有关如何向 TiDB Cloud 导入或迁移数据的更多信息，请参见 [TiDB Cloud 迁移概述](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview)。

### 查看数据导入状态

导入完成后，您可以通过执行以下 SQL 语句查看每个表的数据量信息：

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

结果如下：

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

## 表说明

本节详细说明 Bookshop 应用程序的数据库表。

### `books` 表

此表存储图书的基本信息。

| 字段名称     | 类型          | 描述                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | 图书的唯一标识符                                            |
| title        | varchar(100)  | 图书标题                                                       |
| type         | enum          | 图书类型（例如，杂志、动漫或教学辅助材料）                 |
| stock        | bigint(20)    | 库存                                                            |
| price        | decimal(15,2) | 价格                                                            |
| published_at | datetime      | 出版日期                                                  |

### `authors` 表

此表存储作者的基本信息。

| 字段名称    | 类型         | 描述                                               |
|------------|--------------|-------------------------------------------------------|
| id         | bigint(20)   | 作者的唯一标识符                               |
| name       | varchar(100) | 作者姓名                                                 |
| gender     | tinyint(1)   | 生理性别（0：女性，1：男性，NULL：未知） |
| birth_year | smallint(6)  | 出生年份                                     |
| death_year | smallint(6)  | 死亡年份                                     |

### `users` 表

此表存储 Bookshop 用户的信息。

| 字段名称   | 类型          | 描述               |
|------------|---------------|-----------------------|
| id         | bigint(20)    | 用户的唯一标识符 |
| balance    | decimal(15,2) | 余额               |
| nickname   | varchar(100)  | 昵称              |

### `ratings` 表

此表存储用户对图书的评分记录。

| 字段名称  | 类型     | 描述                                                    |
|------------|----------|------------------------------------------------------------|
| book_id    | bigint   | 图书的唯一标识符（关联到 [books](#books-表)）    |
| user_id    | bigint   | 用户的唯一标识符（关联到 [users](#users-表)） |
| score      | tinyint  | 用户评分（1-5）                                          |
| rated_at   | datetime | 评分时间                                                |

### `book_authors` 表

一个作者可能写多本书，一本书可能涉及多个作者。此表存储图书和作者之间的对应关系。

| 字段名称   | 类型       | 描述                                                      |
|------------|------------|--------------------------------------------------------------|
| book_id    | bigint(20) | 图书的唯一标识符（关联到 [books](#books-表)）      |
| author_id  | bigint(20) | 作者的唯一标识符（关联到 [authors](#authors-表)） |

### `orders` 表

此表存储用户的购买信息。

| 字段名称    | 类型       | 描述                                                        |
|------------|------------|----------------------------------------------------------------|
| id         | bigint(20) | 订单的唯一标识符                                     |
| book_id    | bigint(20) | 图书的唯一标识符（关联到 [books](#books-表)）        |
| user_id    | bigint(20) | 用户的唯一标识符（关联到 [users](#users-表)） |
| quantity   | tinyint(4) | 购买数量                                              |
| ordered_at | datetime   | 购买时间                                                  |

## 数据库初始化脚本 `dbinit.sql`

如果您想手动创建 Bookshop 应用程序的数据库表结构，请运行以下 SQL 语句：

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
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `quality` tinyint(4) NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
