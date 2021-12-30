---
title: TiDB Data Migration Quick Start
summary: Learn how to quickly deploy a DM cluster using binary packages.
aliases: ['/docs/tidb-data-migration/dev/get-started/']
---

# Quick Start Guide for TiDB Data Migration

This document describes how to migrate data from MySQL to TiDB using [TiDB Data Migration](https://github.com/pingcap/dm) (DM).

If you need to deploy DM in the production environment, refer to the following documents:

- [Deploy a DM cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md)
- [Create a Data Source](/dm/quick-start-create-source.md)
- [Create a Data Migration Task](/dm/quick-create-migration-task.md)

## Sample scenario

Suppose you deploy DM-master and DM-worker instances in an on-premise environment, and migrate data from an upstream MySQL instance to a downstream TiDB instance.

The detailed information of each instance is as follows:

| Instance        | Server Address   | Port |
| :---------- | :----------- | :----------- |
| DM-master  | 127.0.0.1 | 8261, 8291 (Internal port) |
| DM-worker  | 127.0.0.1 | 8262 |
| MySQL-3306 | 127.0.0.1 | 3306 |
| TiDB       | 127.0.0.1 | 4000 |

## Deploy DM using the binary package

### Download DM binary package

Download DM latest binary package or compile the package manually.

#### Method 1: Download the latest version of binary package

{{< copyable "shell-regular" >}}

```bash
wget http://download.pingcap.org/dm-nightly-linux-amd64.tar.gz
tar -xzvf dm-nightly-linux-amd64.tar.gz
cd dm-nightly-linux-amd64
```

#### Method 2: Compile the latest version of binary package

{{< copyable "shell-regular" >}}

```bash
git clone https://github.com/pingcap/dm.git
cd dm
make
```

### Deploy DM-master

Execute the following command to start the DM-master:

{{< copyable "shell-regular" >}}

```bash
nohup bin/dm-master --master-addr='127.0.0.1:8261' --log-file=/tmp/dm-master.log --name="master1" >> /tmp/dm-master.log 2>&1 &
```

### Deploy DM-worker

Execute the following command to start the DM-worker:

{{< copyable "shell-regular" >}}

```bash
nohup bin/dm-worker --worker-addr='127.0.0.1:8262' --log-file=/tmp/dm-worker.log --join='127.0.0.1:8261' --name="worker1" >> /tmp/dm-worker.log 2>&1 &
```

### Check deployment status

To check whether the DM cluster has been deployed successfully, execute the following command:

{{< copyable "shell-regular" >}}

```bash
bin/dmctl --master-addr=127.0.0.1:8261 list-member
```

A normal DM cluster returns the following information:

```bash
{
    "result": true,
    "msg": "",
    "members": [
        {
            "leader": {
                "msg": "",
                "name": "master1",
                "addr": "127.0.0.1:8261"
            }
        },
        {
            "master": {
                "msg": "",
                "masters": [
                    {
                        "name": "master1",
                        "memberID": "11007177379717700053",
                        "alive": true,
                        "peerURLs": [
                            "http://127.0.0.1:8291"
                        ],
                        "clientURLs": [
                            "http://127.0.0.1:8261"
                        ]
                    }
                ]
            }
        },
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "worker1",
                        "addr": "127.0.0.1:8262",
                        "stage": "free",
                        "source": ""
                    }
                ]
            }
        }
    ]
}
```

## Migrate data from MySQL to TiDB

### Prepare sample data

Before using DM, insert the following sample data to `MySQL-3306`:

{{< copyable "sql" >}}

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

### Load data source configurations

Before running a data migration task, you need to first load the configuration file of the corresponding data source (that is, `MySQL-3306` in the example) to DM.

#### Encrypt the data source password

> **Note:**
>
> + You can skip this step if the data source does not have a password.
> + You can use the plaintext password to configure the data source information in DM v2.0 and later versions.

For safety reasons, it is recommended to configure and use encrypted passwords for data sources. Suppose the password is "123456":

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

Save this encrypted value, and use it for creating a MySQL data source in the following steps.

#### Edit the source configuration file of the MySQL instance

Write the following configurations to `conf/source1.yaml`.

```yaml
# MySQL1 Configuration.
source-id: "mysql-replica-01"
from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

#### Load data source configuration file

To load the data source configuration file of MySQL to the DM cluster using dmctl, run the following command in the terminal:

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

The following is an example of the returned results:

```bash
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

Now you successfully add the data source `MySQL-3306` to the DM cluster.

### Create a data migration task

After inserting the [sample data](#prepare-sample-data) into `MySQL-3306`, take the following steps to migrate the tables `testdm`.`t1` and `testdm`.`t2` to the downstream TiDB instance:

1. Create a task configuration file `testdm-task.yaml`, and add the following configurations to the file.

    {{< copyable "" >}}

    ```yaml
    ---
    name: testdm
    task-mode: all
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # If the password is not null, it is recommended to use password encrypted with dmctl.
    mysql-instances:
      - source-id: "mysql-replica-01"
        block-allow-list:  "ba-rule1"
    block-allow-list:
      ba-rule1:
        do-dbs: ["testdm"]
    ```

2. Load the task configuration file using dmctl:

    {{< copyable "shell-regular" >}}

    ```bash
    ./bin/dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

    The following is an example of the returned results:

    ```bash
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

Now you successfully create a data migration task that migrates data from `MySQL-3306` to the downstream TiDB instance.

### Check status of the data migration task 

After the data migration task is created, you can use `dmtcl query-status` to check the status of the task. See the following example:

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --master-addr 127.0.0.1:8261 query-status
```

The following is an example of the returned results:

```bash
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "testdm",
            "taskStatus": "Running",
            "sources": [
                "mysql-replica-01"
            ]
        }
    ]
}
```
