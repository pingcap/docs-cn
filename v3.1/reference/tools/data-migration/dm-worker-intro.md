---
title: DM-worker 简介
category: reference
---

# DM-worker 简介

DM-worker 是 DM (Data Migration) 的一个组件，负责执行具体的数据同步任务。

其主要功能如下：

- 注册为一台 MySQL 或 MariaDB 服务器的 slave。
- 读取 MySQL 或 MariaDB 的 binlog event，并将这些 event 持久化保存在本地 (relay log)。
- 单个 DM-worker 支持同步一个 MySQL 或 MariaDB 实例的数据到下游的多个 TiDB 实例。
- 多个 DM-Worker 支持同步多个 MySQL 或 MariaDB 实例的数据到下游的一个 TiDB 实例。

## DM-worker 处理单元

DM-worker 任务包含如下多个逻辑处理单元。

### Relay log

Relay log 持久化保存从上游 MySQL 或 MariaDB 读取的 binlog，并对 binlog replication 处理单元提供读取 binlog event 的功能。

其原理和功能与 MySQL slave relay log 类似，详见 [Slave Relay Log](https://dev.mysql.com/doc/refman/5.7/en/slave-logs-relaylog.html)。

### Dumper

Dumper 从上游 MySQL 或 MariaDB 导出全量数据到本地磁盘。

### Loader

Loader 读取 dumper 处理单元的数据文件，然后加载到下游 TiDB。

### Binlog replication/Syncer

Binlog replication/Syncer 读取 relay log 处理单元的 binlog event，将这些 event 转化为 SQL 语句，再将这些 SQL 语句应用到下游 TiDB。

## DM-worker 所需权限

本小节主要介绍使用 DM-worker 时所需的上下游数据库用户权限以及各处理单元所需的用户权限。

### 上游数据库用户权限

上游数据库 (MySQL/MariaDB) 用户必须拥有以下权限：

| 权限 | 作用域 |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

如果要同步 `db1` 的数据到 TiDB，可执行如下的 `GRANT` 语句：

{{< copyable "sql" >}}

```sql
GRANT RELOAD,REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host'
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

如果还要同步其他数据库的数据到 TiDB, 请确保已赋予这些库跟 `db1` 一样的权限。

### 下游数据库用户权限

下游数据库 (TiDB) 用户必须拥有以下权限：

| 权限 | 作用域 |
|:----|:----|
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE`| Tables |
| `DELETE` | Tables |
| `CREATE` | Databases，tables |
| `DROP` | Databases，tables |
| `ALTER` | Tables |
| `INDEX` | Tables |

对要执行同步操作的数据库或表执行下面的 `GRANT` 语句：

{{< copyable "sql" >}}

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX  ON db.table TO 'your_user'@'your_wildcard_of_host';
```

### 处理单元所需的最小权限

| 处理单元 | 最小上游 (MySQL/MariaDB) 权限 | 最小下游 (TiDB) 权限 | 最小系统权限 |
|:----|:--------------------|:------------|:----|
| Relay log | `REPLICATION SLAVE` (读取 binlog）<br>`REPLICATION CLIENT` (`show master status`, `show slave status`) | 无 | 本地读/写磁盘 |
| Dumper | `SELECT`<br>`RELOAD`（获取读锁将表数据刷到磁盘，进行一些操作后，再释放读锁对表进行解锁）| 无 | 本地写磁盘 |
| Loader | 无 | `SELECT`（查询 checkpoint 历史）<br>`CREATE`（创建数据库或表）<br>`DELETE`（删除 checkpoint）<br>`INSERT`（插入 dump 数据）| 读/写本地文件 |
| Binlog replication | `REPLICATION SLAVE`（读 binlog）<br>`REPLICATION CLIENT` (`show master status`, `show slave status`) | `SELECT`（显示索引和列）<br>`INSERT` (DML)<br>`UPDATE` (DML)<br>`DELETE` (DML)<br>`CREATE`（创建数据库或表）<br>`DROP`（删除数据库或表）<br>`ALTER`（修改表）<br>`INDEX`（创建或删除索引）| 本地读/写磁盘 |

> **注意：**
>
> 这些权限并非一成不变。随着需求改变，这些权限也可能会改变。
