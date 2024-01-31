---
title: Migrate Data from MariaDB to TiDB
summary: Learn how to migrate data from MariaDB to TiDB.
---

# Migrate Data from MariaDB to TiDB

This document describes how to migrate data from a MariaDB server installation to a TiDB cluster.

## Prerequisites

Choose the right migration strategy:

- The first strategy is to [dump data with Dumpling and restore data with TiDB Lightning](#dump-data-with-dumpling-and-restore-data-with-tidb-lightning). This works for all versions of MariaDB. The drawback of this strategy is that it needs more downtime.
- The second strategy is to [Replicate data with DM](#replicate-data-with-dm) from MariaDB to TiDB with DM. DM does not support all versions of MariaDB. Supported versions are listed on the [DM Compatibility Catalog](/dm/dm-compatibility-catalog.md#compatibility-catalog-of-tidb-data-migration).

Besides these two strategies, there might be other strategies available specifically to your situation. For example:

- Use the functionality of your Object Relational Mapping (ORM) to re-deploy and migrate your data.
- Modify your application to write from both MariaDB and TiDB while the migration is ongoing.

This document only covers the first two strategies.

Prepare the following based on the strategy you choose:

- For the **dump and restore** strategy:
    - Install [Dumpling](/dumpling-overview.md) and [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md).
    - Make sure you have the [required privileges](/dumpling-overview.md#required-privileges) on the MariaDB server for Dumpling to export data.
- For the **data replication** strategy, set up [Data Migration (DM)](/dm/dm-overview.md).

## Check compatibility

TiDB is [compatible with MySQL](/mysql-compatibility.md), and MySQL and MariaDB have a lot of functionality in common. However, there might be MariaDB-specific features that might not be compatible with TiDB that you should be aware of before migrating.

Besides checking the items in this section, it is recommended that you also check the [Compatibility & Differences](https://mariadb.com/kb/en/compatibility-differences/) in the MariaDB documentation.

### Authentication

The [Security Compatibility with MySQL](/security-compatibility-with-mysql.md) document lists authentication methods that TiDB supports. TiDB does not support a few authentication methods in MariaDB. This means that you might have to create a new password hash for the account or take other specific measures.

To check what authentication methods are used, you can run the following statement:

```sql
SELECT
  plugin,
  COUNT(*)
FROM
  mysql.user
GROUP BY
  plugin;
```

```sql
+-----------------------+----------+
| plugin                | COUNT(*) |
+-----------------------+----------+
| mysql_native_password |       11 |
+-----------------------+----------+
1 row in set (0.002 sec)
```

### System-versioned tables

TiDB does not support [system-versioned tables](https://mariadb.com/kb/en/system-versioned-tables/). However, TiDB does support [`AS OF TIMESTAMP`](/as-of-timestamp.md) which might replace some of the use cases of system-versioned tables.

You can check for affected tables with the following statement:

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SYSTEM VERSIONED';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | t          |
+--------------+------------+
1 row in set (0.005 sec)
```

To remove system versioning, execute the `ALTER TABLE` statement:

```sql
MariaDB [test]> ALTER TABLE t DROP SYSTEM VERSIONING;
Query OK, 0 rows affected (0.071 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### Sequences

Both MariaDB and TiDB support [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md). However, it is currently not supported by DM. It is recommended that you do not create, modify, or remove sequences during the migration and test this specifically after migration.

To check if you are using sequences, execute the following statement:

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SEQUENCE';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | s1         |
+--------------+------------+
1 row in set (0.016 sec)
```

### Storage engines

MariaDB offers storage engines for local data such as `InnoDB`, `MyISAM` and `Aria`. While the data format is not directly supported by TiDB, migrating these works fine. However, some engines place data outside of the server, such as the `CONNECT` storage engine and `Spider`. While you can migrate such tables to TiDB, TiDB does not provide the functionality to store data outside of the TiDB cluster.

To check what storage engines you are using, execute the following statement:

```sql
SELECT
  ENGINE,
  COUNT(*)
FROM
  information_schema.tables
GROUP BY
  ENGINE;
```

```sql
+--------------------+----------+
| ENGINE             | COUNT(*) |
+--------------------+----------+
| NULL               |      101 |
| Aria               |       38 |
| CSV                |        2 |
| InnoDB             |        6 |
| MEMORY             |       67 |
| MyISAM             |        1 |
| PERFORMANCE_SCHEMA |       81 |
+--------------------+----------+
7 rows in set (0.009 sec)
```

### Syntax

MariaDB supports the `RETURNING` keyword for `DELETE`, `INSERT`, and `REPLACE` statements. TiDB does not support them. You might want to look into your application and query logging to see if it affects your migration.

### Data types

MariaDB supports some data types that TiDB does not support, such as `UUID`, `INET4`, and `INET6`.

To check for these datatypes, execute the following statement:

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE
FROM
  information_schema.columns
WHERE
  DATA_TYPE IN('INET4','INET6','UUID');
```

```sql
+--------------+------------+-------------+-----------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
+--------------+------------+-------------+-----------+
| test         | u1         | u           | uuid      |
| test         | u1         | i4          | inet4     |
| test         | u1         | i6          | inet6     |
+--------------+------------+-------------+-----------+
3 rows in set (0.026 sec)

```

### Character set and collation

TiDB does not support the `latin1_swedish_ci` collation that is often used in MariaDB.

To see what collations TiDB supports, execute this statement on TiDB:

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 |
| binary             | binary  |  63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       1 |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
13 rows in set (0.0012 sec)
```

To check what collations the columns of your current tables are using, you can use this statement:

```sql
SELECT
  TABLE_SCHEMA,
  COLLATION_NAME,
  COUNT(*)
FROM
  information_schema.columns
GROUP BY
  TABLE_SCHEMA, COLLATION_NAME
ORDER BY
  COLLATION_NAME;
```

```sql
+--------------------+--------------------+----------+
| TABLE_SCHEMA       | COLLATION_NAME     | COUNT(*) |
+--------------------+--------------------+----------+
| sys                | NULL               |      562 |
| test               | NULL               |       14 |
| mysql              | NULL               |       84 |
| performance_schema | NULL               |      892 |
| information_schema | NULL               |      421 |
| mysql              | latin1_swedish_ci  |       34 |
| performance_schema | utf8mb3_bin        |       38 |
| mysql              | utf8mb3_bin        |       61 |
| sys                | utf8mb3_bin        |       40 |
| information_schema | utf8mb3_general_ci |      375 |
| performance_schema | utf8mb3_general_ci |      244 |
| sys                | utf8mb3_general_ci |      386 |
| mysql              | utf8mb3_general_ci |       67 |
| mysql              | utf8mb4_bin        |        8 |
+--------------------+--------------------+----------+
14 rows in set (0.045 sec)
```

See also [Character Set and Collation](/character-set-and-collation.md).

## Dump data with Dumpling and restore data with TiDB Lightning

This method assumes that you take your application offline, migrate the data, and then re-configure your application to use the migrated data.

> **Note:**
>
> It is strongly recommended to first do this on a test or development instance of your application before doing it in production. This is both to check for possible compatibility issues as to get insight into how much time the migration will take.

Perform the following steps to migrate data from MariaDB to TiDB:

1. Stop your application. Take your application offline. This ensures there are no modifications made to the data in MariaDB during or after the migration.

2. Dump data in MariaDB with the [`tiup dumpling`](/dumpling-overview.md#use-dumpling-to-export-data) command.

    ```shell
    tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
    ```

3. Restore the data by using the `tiup tidb-lightning` command. For more information about how to configure TiDB Lightning and how to run it, see [Get Started with TiDB Lightning](/get-started-with-tidb-lightning.md).

4. Migrate user accounts and permissions. For more information about how to migrate your users and permissions, see [Export users and grants](#export-users-and-grants).

5. Reconfigure your application. You need to change the application configuration so that it can connect to the TiDB server.

6. Clean up. Once you have verified that the migration is successful you can make a final backup of the data in MariaDB and stop the server. This also means you can remove tools such as TiUP, Dumpling, and TiDB Lightning.

## Replicate data with DM

This method assumes you would set up replication, stop your application and wait for the replication to catch up, and then re-configure your application to use TiDB.

To use DM, you need to deploy a set of DM services either with a [TiUP cluster](/dm/deploy-a-dm-cluster-using-tiup.md) or with [TiDB Operator](/tidb-operator-overview.md). After that, use `dmctl` to configure the DM services.

> **Note:**
>
> It is strongly recommended to first do this on a test or development instance of your application before doing it in production. This is both to check for possible compatibility issues as to get insight into how much time the migration will take.

### Step 1. Prepare

Make sure that binlogs are enabled on MariaDB and that the `binlog_format` is set to `ROW`. It is also recommended to set `binlog_annotate_row_events=OFF` and `log_bin_compress=OFF`.

You also need an account with the `SUPER` permission or with the `BINLOG MONITOR` and `REPLICATION MASTER ADMIN` permissions. This account also needs read permission for the schemas you are going to migrate.

If you are not using an account with the `SUPER` permission, then you might have to add the following to the DM configuration, because TiDB does not yet know how to check for MariaDB specific permissions.

```yaml
ignore-checking-items: ["replication_privilege"]
```

Before you use DM to migrate data from upstream to downstream, a precheck helps detect errors in the upstream database configurations and ensures that the migration goes smoothly. For more information, see [Migration Task Precheck](/dm/dm-precheck.md)

### Step 2. Replicate data

Follow the [Quick Start Guide for TiDB Data Migration](/dm/quick-start-with-dm.md) to replicate your data from MariaDB to TiDB.

Note that it is not required to first copy the initial data as you would do with MariaDB to MariaDB replication, DM will do this for you.

### Step 3. Migrate user accounts and permissions

See [Export users and grants](#export-users-and-grants) for how to migrate your users and permissions.

### Step 4. Test your data

Once your data is replicated, you can run read-only queries on it to validate it. For more information, see [Test your application](#test-your-application).

### Step 5. Switch over

To switch over to TiDB, you need to do the following:

1. Stop your application.
2. Monitor the replication delay, which should go to 0 seconds.
3. Change the configuration of your application so that it connects to TiDB and start it again.

To check for replication delay, run [`query-status <taskname>`](/dm/dm-query-status.md#detailed-query-result) via `dmctl` and check for `"synced: true"` in the `subTaskStatus`.

### Step 6. Clean up

Once you have verified that the migration is successful, you can make a final backup of the data in MariaDB and stop the server. It also means you can stop and remove the DM cluster.

## Export users and grants

You can use [`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html). It is part of the Percona Toolkit to export users and grants from MariaDB and load these into TiDB.

## Test your application

While it is possible to use generic tools such as `sysbench` for testing, it is highly recommended to test some specific features of your application. For example, run a copy of your application against a TiDB cluster with a temporary copy of your data.

Such a test makes sure your application compatibility and performance with TiDB is verified. You need to monitor the log files of your application and TiDB to see if there are any warnings that might need to be addressed. Make sure that the database driver that your application is using (for example MySQL Connector/J for Java based applications) is tested. You might want to use an application such as JMeter to put some load on your application if needed.

## Validate data

You can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to validate if the data in MariaDB and TiDB are identical.
