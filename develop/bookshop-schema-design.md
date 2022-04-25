---
title: Bookshop 应用
---

# Bookshop 应用

Bookshop 是一个虚拟的在线书店应用，你可以在 Bookshop 当中便捷地购买到各种类别的书，也可以对你看过的书进行点评。

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
