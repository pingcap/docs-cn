---
title: Bookshop Example Application
---

# Bookshop Example Application

Bookshop is a virtual online bookstore application through which you can buy books of various categories and rate the books you have read.

To make your reading on the application developer guide more smoothly, we present the example SQL statements based on the [table structures](#description-of-the-tables) and data of the Bookshop application. This document focuses on the methods of importing the table structures and data as well as the definitions of the table structures.

## Import table structures and data

<CustomContent platform="tidb">

You can import Bookshop table structures and data either [via TiUP](#method-1-via-tiup-demo) or [via the import feature of TiDB Cloud](#method-2-via-tidb-cloud-import).

</CustomContent>

<CustomContent platform="tidb-cloud">

For TiDB Cloud, you can skip [Method 1: Via `tiup demo`](#method-1-via-tiup-demo) and import Bookshop table structures [via the import feature of TiDB Cloud](#method-2-via-tidb-cloud-import).

</CustomContent>

### Method 1: Via `tiup demo`

<CustomContent platform="tidb">

If your TiDB cluster is deployed using [TiUP](/tiup/tiup-reference.md#tiup-reference) or you can connect to your TiDB server, you can quickly generate and import sample data for the Bookshop application by running the following command:

</CustomContent>

<CustomContent platform="tidb-cloud">

If your TiDB cluster is deployed using [TiUP](https://docs.pingcap.com/tidb/stable/tiup-reference) or you can connect to your TiDB server, you can quickly generate and import sample data for the Bookshop application by running the following command:

</CustomContent>

```shell
tiup demo bookshop prepare
```

By default, this command enables your application to connect to port `4000` on address `127.0.0.1`, enables you to log in as the `root` user without a password, and creates a [table structure](#description-of-the-tables) in the database named `bookshop`.

#### Configure connection information

The following table lists the connection parameters. You can change their default settings to match your environment.

| Parameter    | Abbreviation | Default value      | Description           |
| ------------ | ---- | ----------- | -------------- |
| `--password` | `-p` | None        | Database user password |
| `--host`     | `-H` | `127.0.0.1` | Database address     |
| `--port`     | `-P` | `4000`      | Database port     |
| `--db`       | `-D` | `bookshop`  | Database name     |
| `--user`     | `-U` | `root`      | Database user     |

For example, if you want to connect to a database on TiDB Cloud, you can specify the connection information as follows:

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### Set the data volume

You can specify the volume of data to be generated in each database table by configuring the following parameters:

| Parameter        | Default value   | Description                              |
| ----------- | -------- | --------------------------------- |
| `--users`   | `10000`  | The number of rows of data to be generated in the `users` table   |
| `--authors` | `20000`  | The number of rows to be generated in the `authors` table |
| `--books`   | `20000`  | The number of rows of data to be generated in the `books` table   |
| `--orders`  | `300000` | The number of rows of data to be generated in the `orders` table  |
| `--ratings` | `300000` | The number of rows of data to be generated in the `ratings` table |

For example, the following command is executed to generate:

- 200,000 rows of user information via the `--users` parameter
- 500,000 rows of book information via the `--books` parameter
- 100,000 rows of author information via the `--authors` parameter
- 1,000,000 rows of rating records via the `--ratings` parameter
- 1,000,000 rows of order records via the `--orders` parameter

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

You can delete the original table structure through the `--drop-tables` parameter. For more parameter descriptions, run the `tiup demo bookshop --help` command.

### Method 2: Via TiDB Cloud Import

On the cluster detail page of TiDB Cloud, click **Import Data** in the **Import** area to enter the **Data Import** page. On this page, perform the following steps to import the Bookshop sample data from AWS S3 to TiDB Cloud.

1. Select **SQL File** for **Data Format**.
2. Copy the following **Bucket URI** and **Role ARN** to the corresponding input boxes:

    **Bucket URI**:

    ```
    s3://developer.pingcap.com/bookshop/
    ```

   **Role ARN**:

    ```
    arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access
    ```

3. Click **Next** to go to the **File and filter** step to confirm the information of the files to be imported.

4. Click **Next** again to go to the **Preview** step to confirm the preview of the data to be imported.

    In this example, the following data is generated in advance:

    - 200,000 rows of user information
    - 500,000 rows of book information
    - 100,000 rows of author information
    - 1,000,000 rows of rating records
    - 1,000,000 rows of order records

5. Click **Start Import** to start the import process and wait for TiDB Cloud to complete the import.

For more information about how to import or migrate data to TiDB Cloud, see [TiDB Cloud Migration Overview](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview).

### View data import status

After the import is completed, you can view the data volume information of each table by executing the following SQL statement:

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

The result is as follows:

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

## Description of the tables

This section describes the database tables of the Bookshop application in detail.

### `books` table

This table stores the basic information of books.

| Field name   | Type          | Description                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | Unique ID of a book                                            |
| title        | varchar(100)  | Title of a book                                                       |
| type         | enum          | Type of a book (for example, magazine, animation, or teaching aids) |
| stock        | bigint(20)    | Stock                                                            |
| price        | decimal(15,2) | Price                                                            |
| published_at | datetime      | Date of publish                                                  |

### `authors` table

This table stores basic information of authors.

| Field name | Type         | Description                                               |
|------------|--------------|-------------------------------------------------------|
| id         | bigint(20)   | Unique ID of an author                               |
| name       | varchar(100) | Name of an author                                                 |
| gender     | tinyint(1)   | Biological gender (0: female, 1: male, NULL: unknown) |
| birth_year | smallint(6)  | Year of birth                                     |
| death_year | smallint(6)  | Year of death                                     |

### `users` table

This table stores information of Bookshop users.

| Field name | Type          | Description               |
|------------|---------------|-----------------------|
| id         | bigint(20)    | Unique ID of a user |
| balance    | decimal(15,2) | Balance               |
| nickname   | varchar(100)  | Nickname              |

### `ratings` table

This table stores records of user ratings on books.

| Field name | Type     | Description                                                    |
|------------|----------|------------------------------------------------------------|
| book_id    | bigint   | Unique ID of a book (linked to [books](#books-table))    |
| user_id    | bigint   | User's unique identifier (linked to [users](#users-table)) |
| score      | tinyint  | User rating (1-5)                                          |
| rated_at   | datetime | Rating time                                                |

### `book_authors` table

An author may write multiple books, and a book may involve more than one author. This table stores the correspondence between books and authors.

| Field name | Type       | Description                                                      |
|------------|------------|--------------------------------------------------------------|
| book_id    | bigint(20) | Unique ID of a book (linked to [books](#books-table))      |
| author_id  | bigint(20) | Unique ID of an author（Link to [authors](#authors-table)） |

### `orders` table

This table stores user purchase information.

| Field name | Type       | Description                                                        |
|------------|------------|----------------------------------------------------------------|
| id         | bigint(20) | Unique ID of an order                                     |
| book_id    | bigint(20) | Unique ID of a book (linked to [books](#books-table))        |
| user_id    | bigint(20) | User unique identifier (associated with [users](#users-table)) |
| quantity   | tinyint(4) | Purchase quantity                                              |
| ordered_at | datetime   | Purchase time                                                  |

## Database initialization script `dbinit.sql`

If you want to manually create database table structures in the Bookshop application, run the following SQL statements:

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
