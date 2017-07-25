---
title: Try TiDB
category: quick start
---

# Try TiDB


`TiDB` 支持 `SQL92` 标准并兼容 `MySQL` 语法，目前已经实现了大多数常用的 `MySQL` 语法。用户可以直接使用现有的 `MySQL` 客户端连接。如果现有的业务已经基于 `MySQL` 开发，大多数情况不需要修改代码即可直接替换单机的 `MySQL`。


## create a DB
使用 `create database` 语句可完成对数据库的创建, 创建命令的格式如下:

    create database 数据库名 [其他选项];
  
例如我们需要创建一个名为 samp_db 的数据库, 在命令行下执行以下命令:

    create database if not exists samp_db;

查看`Tidb`中的所有数据库：

    show databases;

删除数据库：

    drop database samp_db;


## create a table

 使用`CREATE TABLE`  + 表名 + 列名 + 数据类型 + 约束。具体例子如下：

    CREATE TABLE person (
    number INT(11),
    name VARCHAR(255),
    birthday DATE
    );



如果表已存在，则使用关键词 `IF NOT EXISTS` 可以防止发生错误。



    CREATE TABLE IF NOT EXISTS         person (
      number INT(11),
      name VARCHAR(255),
    birthday DATE
    );

查看建表语句

    SHOW CREATE table person;

查看表所有的列：

    SHOW FULL COLUMNS from person;

删除表

    DROP TABLE person;

或者

    DROP TABLE IF EXISTS person;

查看 `samp_db`中的所有表：

    SHOW TABLES FROM samp_db;


## create an index

对于值不唯一的列，可以使用`create index`和`alter table`：

    CREATE INDEX person_num ON person (number );
    ALTER TABLE person ADD INDEX person_num (number )；

对于值唯一的列可以创建唯一索引：

    CREATE UNIQUE INDEX person_num ON person (number );
    ALTER TABLE person ADD UNIQUE person_num  on (number);

可利用`ALTER TABLE`或`DROP INDEX`语句来删除索引。类似于`CREATE INDEX`语句，`DROP INDEX`可以在`ALTER TABLE`内部作为一条语句处理，语法如下。

    DROP INDEX person_num ON person;
    ALTER TABLE person DROP INDEX person_num ;

查看表内所有索引：

    show index from person ;

## CRUD

利用`insert`插入数据

    insert into person values("1","tom","20170912");
    select * from person;
    +--------+------+------------+
    | number | name | birthday   |
    +--------+------+------------+
    |      1 | tom  | 2017-09-12 |
    +--------+------+------------+


修改表内数据：

    UPDATE person SET birthday='20171010' WHERE name='tom';
    select * from person;
    +--------+------+------------+
    | number | name | birthday   |
    +--------+------+------------+
    |      1 | tom  | 2017-10-10 |
    +--------+------+------------+

删除表内数据：

    delete from person where number=1;
    select * from person;
    Empty set (0.00 sec)


## create a user
使用`create user`语句创建一个只在本地登录的用户`tiuser`，密码为‘123456’：

    CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';

授权用户可查询`samp_db`库下的表：

    GRANT SELECT ON samp_db .* TO 'tiuser'@'localhost';
 
查询`tiuser`用户的授权：

    show grants for tiuser@localhost;

删除用户

    DROP USER 'tiuser'@'localhost';


