---
title: Migrate Data from MySQL to TiDB
summary: Use `mydumper` and `loader` to migrate data from MySQL to TiDB.
category: how-to
aliases: ['/docs/op-guide/migration/']
---

# Migrate Data from MySQL to TiDB

## Use the `mydumper`/`loader` tool to export and import all the data

You can use `mydumper` to export data from MySQL and `loader` to import the data into TiDB.

> **Note:**
>
> Although TiDB also supports the official `mysqldump` tool from MySQL for data migration, it is not recommended to use it. Its performance is much lower than `mydumper` / `loader` and it takes much time to migrate large amounts of data. It is important to use the `mydumper` provided by TiDB and not the upstream `mydumper` version.  See [mydumper](/tools/mydumper.md) for more information.

`Mydumper` and `loader` can be [downloaded as part of Enterprise Tools](/tools/download.md).

### Export data from MySQL

Use the `mydumper` tool to export data from MySQL by using the following command:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```
In this command,

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 64`: means a table is partitioned into chunks and one chunk is 64MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

> **Note:**
>
> On the Cloud platforms which require the `super privilege`, such as on the Amazon RDS, add the `--no-locks` parameter to the command. If not, you might get the error message that you don't have the privilege.

### Import data to TiDB

Use `loader` to import the data from MySQL to TiDB. See [Loader instructions](/tools/loader.md) for more information.

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is imported, you can view the data in TiDB using the MySQL client:

```sql
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```

### Best practice

To migrate data quickly, especially for huge amount of data, you can refer to the following recommendations.

- Keep the exported data file as small as possible and it is recommended keep it within 64M. You can use the `-F` parameter to set the value.
- You can adjust the `-t` parameter of `loader` based on the number and the load of TiKV instances. For example, if there are three TiKV instances, `-t` can be set to 3 * (1 ~ n). If the load of TiKV is too high and the log `backoffer.maxSleep 15000ms is exceeded` is displayed many times, decrease the value of `-t`; otherwise, increase it.

### A sample and the configuration

 - The total size of the exported files is 214G. A single table has 8 columns and 2 billion rows.
 - The cluster topology:
    - 12 TiKV instances: 4 nodes, 3 TiKV instances per node
    - 4 TiDB instances
    - 3 PD instances
 - The configuration of each node:
    - CPU: Intel Xeon E5-2670 v3 @ 2.30GHz
    - 48 vCPU [2 x 12 physical cores]
    - Memory: 128G
    - Disk: sda [raid 10, 300G] sdb[RAID 5, 2T]
    - Operating System: CentOS 7.3
 - The `-F` parameter of `mydumper` is set to 16 and the `-t` parameter of `loader` is set to 64.

**Results**: It takes 11 hours to import all the data, which is 19.4G/hour.
