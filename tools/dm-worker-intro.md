---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
category: tools
---

# DM-worker Introduction

DM-worker is a tool used to synchronize data from MySQL/MariaDB to TiDB. 

It has the following features:

- Acts as a slave of any MySQL or MariaDB server
- Reads the binlog events from MySQL/MariaDB and persists them to the local storage
- A single DM-worker supports synchronizing the data of one MySQL/MariaDB instance to multiple TiDB instances
- Multiple DM-workers support synchronizing the data of multiple MySQL/MariaDB instances to one TiDB instance

## DM-worker processing unit

A DM-worker task contains multiple logic units, including relay log, Dumper, Loader, and binlog replication.

### Relay log

The relay log persistently stores the binlog data from the upstream MySQL/MariaDB and provides the feature of accessing binlog events for the binlog replication.

Its rationale and features are similar to the slave relay log of MySQL. For details, see [The Slave Relay Log](https://dev.mysql.com/doc/refman/5.7/en/slave-logs-relaylog.html).

### Dumper

Dumper dumps the full data from the upstream MySQL/MariaDB to the local disk.

### Loader

Loader reads the files of Dumper and then loads these files to the downstream TiDB.

### Binlog replication/Syncer

Binlog replication/Syncer reads the binlog events of the relay log, transforms these events to SQL statements, and then applies these statements to the downstream TiDB.

## Privileges DM-worker needs

### Privileges the upstream needs

The upstream (MySQL/mariaDB) needs the following privileges:

- `SELECT`
- `RELOAD`
- `RELICATION SLAVE`
- `REPLICATION CLIENT`

```sql
GRANT SELECT,RELOAD,REPLICATION SLAVE, REPLICATION CLIENT  ON *.* TO 'your_user'@'your_wildcard_of_host';
```

#### Privileges the downstream needs

The downstream (TiDB) needs the following privileges:

- `SELECT` 
- `INSERT`
- `UPDATE`
- `DELETE`
- `CREATE`
- `DROP`
- `ALTER`
- `INDEX`

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX  ON *.* TO 'your_user'@'your_wildcard_of_host';
```

### Minimal privilege each processing unit needs

| Processing Unit | Minimal Privilege for Upstream (MySQL/MariaDB) | Minimal Privilege for Downstream (TiDB) | Minimal Privilege for the System |
|----:|:--------------------|:------------|:----|
| Relay log | `SELECT` (checks some upstream environment variables, like `binlog_format`)<br>`REPLICATION SLAVE` (reads the binlog)<br>`REPLICATION CLIENT` (`show master status`, `show slave status`) | NULL | Read/Write local files |
| Dumper | `SELECT`<br>`RELOAD` (flushes tables with Read lock and unlocks tables）| NULL | Write local files |
| Loader | NULL | `SELECT` (Query the checkpoint history)<br>`CREATE` (creates a database/table)<br>`DELETE` (deletes checkpoint)<br>`INSERT` (Inserts the Dump data) | Read/Write local files |
| Binlog replication | `SELECT` (checks some upstream environment variables, like `binlog_format`)<br>`REPLICATION SLAVE` (reads the binlog)<br>`REPLICATION CLIENT` (`show master status`, `show slave status`) | `SELECT` (shows the index and column)<br>`INSERT` (DML)<br>`UPDATE` (DML)<br>`DELETE` (DML)<br>`CREATE` (creates a database/table)<br>`DROP` (drops databases/tables)<br>`ALTER` (alters a table)<br>`INDEX` (creates/drops an index)| Read/Write local files |

> **Note:** These privileges are not static and they change as the request changes.
