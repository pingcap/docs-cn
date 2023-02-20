---
title: Create a Data Migration Task
summary: Learn how to create a migration task after the DM cluster is deployed.
aliases: ['/docs/tidb-data-migration/dev/create-task-and-verify/']
---

# Create a Data Migration Task

This document describes how to create a simple data migration task after the DM cluster is successfully deployed.

## Sample scenario

Suppose that you create a data migration task based on this sample scenario:

- Deploy two MySQL instances with binlog enabled and one TiDB instance locally
- Use a DM-master of the DM cluster to manage the cluster and data migration tasks.

The information of each node is as follows.

| Instance   | Server Address  | Port  |
| :---------- | :----------- | :--- |
| MySQL1     | 127.0.0.1 | 3306 |
| MySQL2     | 127.0.0.1 | 3307 |
| TiDB       | 127.0.0.1 | 4000 |
| DM-master  | 127.0.0.1 | 8261 |

Based on this scenario, the following sections describe how to create a data migration task.

### Start upstream MySQL

Prepare 2 runnable MySQL instances. You can also use Docker to quickly start MySQL. The commands are as follows:

{{< copyable "shell-regular" >}}

```bash
docker run --rm --name mysql-3306 -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3306 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3306.log 2>&1 &
docker run --rm --name mysql-3307 -p 3307:3307 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3307 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3307.log 2>&1 &
```

### Prepare data

- Write example data into mysql-3306:

    {{< copyable "sql" >}}

    ```sql
    drop database if exists `sharding1`;
    create database `sharding1`;
    use `sharding1`;
    create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2 ,10002, 'Cien años de soledad');
    insert into t2 (id, uid, name) values (3,20001, 'José Arcadio Buendía'), (4,20002, 'Úrsula Iguarán'), (5,20003, 'José Arcadio');
    ```

- Write example data into mysql-3307:

    {{< copyable "sql" >}}

    ```sql
    drop database if exists `sharding2`;
    create database `sharding2`;
    use `sharding2`;
    create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    create table t3 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    insert into t2 (id, uid, name, info) values (6, 40000, 'Remedios Moscote', '{}');
    insert into t3 (id, uid, name, info) values (7, 30001, 'Aureliano José', '{}'), (8, 30002, 'Santa Sofía de la Piedad', '{}'), (9, 30003, '17 Aurelianos', NULL);
    ```

### Start downstream TiDB

To run a TiDB server, use the following command:

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-community-server-v6.6.0-linux-amd64.tar.gz
tar -xzvf tidb-latest-linux-amd64.tar.gz
mv tidb-latest-linux-amd64/bin/tidb-server ./
./tidb-server
```

> **Warning:**
>
> The deployment method of TiDB in this document **do not apply** to production or development environments.

## Configure the MySQL data source

Before starting a data migration task, you need to configure the MySQL data source.

### Encrypt the password

> **Note:**
>
> + You can skip this step if the database does not have a password.
> + You can use the plaintext password to configure the source information in DM v1.0.6 and later versions.

For safety reasons, it is recommended to configure and use encrypted passwords. You can use dmctl to encrypt the MySQL/TiDB password. Suppose the password is "123456":

{{< copyable "shell-regular" >}}

```bash
./dmctl encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

Save this encrypted value, and use it for creating a MySQL data source in the following steps.

### Edit the source configuration file

Write the following configurations to `conf/source1.yaml`.

```yaml
# MySQL1 Configuration.

source-id: "mysql-replica-01"

# Indicates whether GTID is enabled
enable-gtid: true

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

In MySQL2 data source, copy the above configurations to `conf/source2.yaml`. You need to change `name` to `mysql-replica-02` and change `password` and `port` to appropriate values.

### Create a source

To load the data source configurations of MySQL1 into the DM cluster using dmctl, run the following command in the terminal:

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

For MySQL2, replace the configuration file in the above command with that of MySQL2.

## Create a data migration task

After importing [prepared data](#prepare-data), there are several sharded tables on both MySQL1 and MySQL2 instances. These tables have identical structure and the same prefix "t" in the table names; the databases where these tables are located are all prefixed with "sharding"; and there is no conflict between the primary keys or the unique keys (in each sharded table, the primary keys or the unique keys are different from those of other tables).

Now, suppose that you need to migrate these sharded tables to the `db_target.t_target` table in TiDB. The steps are as follows.

1. Create the configuration file of the task:

    {{< copyable "" >}}

    ```yaml
    ---
    name: test
    task-mode: all
    shard-mode: "pessimistic"
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # It is recommended to use password encrypted with dmctl if the password is not empty.

    mysql-instances:
      - source-id: "mysql-replica-01"
        block-allow-list:  "instance"  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
        route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
        mydumper-thread: 4
        loader-thread: 16
        syncer-thread: 16
      - source-id: "mysql-replica-02"
        block-allow-list:  "instance"  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
        route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
        mydumper-thread: 4
        loader-thread: 16
        syncer-thread: 16
    block-allow-list:  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
      instance:
        do-dbs: ["~^sharding[\\d]+"]
        do-tables:
        - db-name: "~^sharding[\\d]+"
          tbl-name: "~^t[\\d]+"
    routes:
      sharding-route-rules-table:
        schema-pattern: sharding*
        table-pattern: t*
        target-schema: db_target
        target-table: t_target
      sharding-route-rules-schema:
        schema-pattern: sharding*
        target-schema: db_target
    ```

2. To create a task using dmctl, write the above configurations to the `conf/task.yaml` file:

    {{< copyable "shell-regular" >}}

    ```bash
    ./dmctl --master-addr 127.0.0.1:8261 start-task conf/task.yaml
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

Now, you have successfully created a task to migrate the sharded tables from the MySQL1 and MySQL2 instances to TiDB.

## Verify data

You can modify data in the upstream MySQL sharded tables. Then use [sync-diff-inspector](/sync-diff-inspector/shard-diff.md) to check whether the upstream and downstream data are consistent. Consistent data means that the migration task works well, which also indicates that the cluster works well.
