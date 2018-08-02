---
title: TiDB 快速入门指南
category: deployment
---

# TiDB 快速入门指南

## 关于 TiDB

TiDB 是 PingCAP 公司受 Google [Spanner](http://research.google.com/archive/spanner.html) / [F1](http://research.google.com/pubs/pub41344.html) 论文启发而设计的开源分布式 HTAP (Hybrid Transactional and Analytical Processing) 数据库，结合了传统的 RDBMS 和 NoSQL 的最佳特性。TiDB 兼容 MySQL，支持无限的水平扩展，具备强一致性和高可用性。TiDB 的目标是为 OLTP (Online Transactional Processing) 和 OLAP (Online Analytical Processing) 场景提供一站式的解决方案。

## 关于本指南

本指南为您介绍如何使用 TiDB-Ansible 快速部署一个 TiDB 集群，并了解 TiDB 的基本操作和管理。

## TiDB 集群部署

本节具体介绍如何部署一个 TiDB 集群。一个 TiDB 集群由不同的模块组成，包括：TiDB 服务器、TiKV 服务器、Placement Driver (PD) 服务器。

架构图如下所示：

![TiDB Architecture](media/tidb-architecture.png)

参考 [TiDB Ansible 部署方案](../op-guide/ansible-deployment.md)。

## TiDB 基本操作

本节具体介绍 TiDB 中基本的增删改查操作。

### 创建、查看和删除数据库

使用 `CREATE DATABASE` 语句创建数据库。语法如下：

```sql
CREATE DATABASE db_name [options];
```

例如，要创建一个名为 `samp_db` 的数据库，可使用以下语句：

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

使用 `SHOW DATABASES` 语句查看数据库：

```sql
SHOW DATABASES;
```

使用 `DROP DATABASE` 语句删除数据库，例如：

```sql
DROP DATABASE samp_db;
```

### 创建、查看和删除表

使用 `CREATE TABLE` 语句创建表。语法如下：

```sql
CREATE TABLE table_name column_name data_type constraint;
```

例如：

```sql
CREATE TABLE person (
    number INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

如果表已存在，添加 `IF NOT EXISTS` 可防止发生错误：

```sql
CREATE TABLE IF NOT EXISTS person (
      number INT(11),
      name VARCHAR(255),
      birthday DATE
);
```

使用 `SHOW CREATE` 语句查看建表语句。例如：

```sql
SHOW CREATE table person;
```

使用 `SHOW FULL COLUMNS` 语句查看表的列。 例如：

```sql
SHOW FULL COLUMNS FROM person;
```

使用 `DROP TABLE` 语句删除表。例如：

```sql
DROP TABLE person;
```

或者

```sql
DROP TABLE IF EXISTS person;
```

使用 `SHOW TABLES` 语句查看数据库中的所有表。例如：

```sql
SHOW TABLES FROM samp_db;
```

### 创建、查看和删除索引

对于值不唯一的列，可使用 `CREATE INDEX` 或 `ALTER TABLE` 语句。例如：

```sql
CREATE INDEX person_num ON person (number);
```

或者

```sql
ALTER TABLE person ADD INDEX person_num (number);
```

对于值唯一的列，可以创建唯一索引。例如：

```sql
CREATE UNIQUE INDEX person_num ON person (number);
```

或者

```sql
ALTER TABLE person ADD UNIQUE person_num  on (number);
```

使用 `SHOW INDEX` 语句查看表内所有索引：

```sql
SHOW INDEX from person;
```

使用 `ALTER TABLE` 或 `DROP INDEX` 语句来删除索引。与 `CREATE INDEX` 语句类似，`DROP INDEX` 也可以嵌入 `ALTER TABLE` 语句。例如：

```sql
DROP INDEX person_num ON person;
ALTER TABLE person DROP INDEX person_num;
```

### 增删改查数据

使用 `INSERT` 语句向表内插入数据。例如：

```sql
INSERT INTO person VALUES("1","tom","20170912");
```

使用 `SELECT` 语句检索表内数据。例如：

```sql
SELECT * FROM person;
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-09-12 |
+--------+------+------------+
```
使用 `UPDATE` 语句修改表内数据。例如：

```sql
UPDATE person SET birthday='20171010' WHERE name='tom';

SELECT * FROM person;
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-10-10 |
+--------+------+------------+
```

使用 `DELETE` 语句删除表内数据：

```sql
DELETE FROM person WHERE number=1;
SELECT * FROM person;
Empty set (0.00 sec)
```

### 创建、授权和删除用户

使用 `CREATE USER` 语句创建一个用户 `tiuser`，密码为 `123456`：

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

授权用户 `tiuser` 可检索数据库 `samp_db` 内的表：

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

查询用户 `tiuser` 的权限：

```sql
SHOW GRANTS for tiuser@localhost;
```

删除用户 `tiuser`：

```sql
DROP USER 'tiuser'@'localhost';
```

## TiDB 集群监控

打开浏览器，访问以下监控平台：

地址：`http://172.16.10.3:3000`，
默认帐户和密码为：`admin`@`admin`。

### 重要监控指标详解

+ PD
    -   Storage Capacity  :  TiDB 集群总可用数据库空间大小
    -   Current Storage Size  :  TiDB 集群目前已用数据库空间大小
    -   Store Status  -- up store  :  TiKV 正常节点数量
    -   Store Status  -- down store  :  TiKV 异常节点数量

        如果大于 0，证明有节点不正常
    -   Store Status  -- offline store  :  手动执行下线操作 TiKV 节点数量
    -   Store Status  -- Tombstone store  :  下线成功的 TiKV 节点数量
    -   Current storage usage  :  TiKV 集群存储空间占用率

        超过 80% 应考虑添加 TiKV 节点
    -   99% completed_cmds_duration_seconds  :  99% pd-server 请求完成时间

        小于 5ms
    -   average completed_cmds_duration_seconds  :  pd-server 请求平均完成时间

        小于 50ms
    -   leader balance ratio  :  leader ratio 最大的节点与最小的节点的差

        均衡状况下一般小于 5%，节点重启时会比较大
    -   region balance ratio  :  region ratio 最大的节点与最小的节点的差

        均衡状况下一般小于 5%，新增/下线节点时会比较大

+ TiDB
    -   handle_requests_duration_seconds  :  请求 PD 获取 TSO 响应时间

        小于 100ms
    -   tidb server QPS  :  集群的请求量

    -   connection count  :  从业务服务器连接到数据库的连接数

        和业务相关。但是如果连接数发生跳变，需要查明原因。比如突然掉为 0，可以检查网络是否中断；
        如果突然上涨，需要检查业务。
    -   statement count  :  单位时间内不同类型语句执行的数目
    -   Query Duration 99th percentile  :  99% 的 query 时间

+ TiKV
    -    99% & 99.99%  scheduler command duration  :  99% & 99.99% 命令执行的时间

        99% 小于 50ms；99.99% 小于 100ms
    -   95% & 99% storage async_request duration  :  95%  & 99% Raft 命令执行时间

        95% 小于 50ms；99% 小于 100ms
    -   server report failure message  :  发送失败或者收到了错误的 message

        如果出现了大量的 unreachadble 的消息，表明系统网络出现了问题。如果有 store not match 这样的错误，
        表明收到了不属于这个集群发过来的消息
    -   Vote  :  Raft vote 的频率

        通常这个值只会在发生 split 的时候有变动，如果长时间出现了 vote 偏高的情况，证明系统出现了严重的问题，
        有一些节点无法工作了
    -   95% & 99% coprocessor request duration  :  95% & 99%  coprocessor 执行时间

        和业务相关，但通常不会出现持续高位的值
    -   Pending task  :  累积的任务数量

        除了 pd worker，其他任何偏高都属于异常
    -   stall  :  RocksDB Stall 时间

        大于 0，表明 RocksDB 忙不过来，需要注意 IO 和 CPU 了
    -   channel full  :  channel 满了，表明线程太忙无法处理

        如果大于 0，表明线程已经没法处理了
    -   95% send_message_duration_seconds  :  95% 发送消息的时间

        小于 50ms
    -   leader/region  :  每个 TiKV 的 leader/region 数量
