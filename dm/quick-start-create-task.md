---
title: 创建数据迁移任务
summary: 了解在部署 DM 集群后，如何快速创建数据迁移任务。
---

# 创建数据迁移任务

本文档介绍在 DM 集群部署成功后，如何快速创建简单的数据迁移任务。

## 使用样例

在本地部署两个开启 binlog 的 MySQL 实例和一个 TiDB 实例；使用 DM 集群的一个 DM-master 来管理集群和数据迁移任务。各个节点的信息如下：

| 实例        | 服务器地址   | 端口   |
| :---------- | :----------- | :--- |
| MySQL1     | 127.0.0.1 | 3306 |
| MySQL2     | 127.0.0.1 | 3307 |
| TiDB       | 127.0.0.1 | 4000 |
| DM-master  | 127.0.0.1 | 8261 |

下面以此为例，说明如何创建数据迁移任务。

### 运行上游 MySQL

准备 2 个可运行的 MySQL 实例，也可以使用 Docker 快速启动 MySQL，示例命令如下：

{{< copyable "shell-regular" >}}

```bash
docker run --rm --name mysql-3306 -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3306 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3306.log 2>&1 &
docker run --rm --name mysql-3307 -p 3307:3307 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3307 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3307.log 2>&1 &
```

### 准备数据

- 向 mysql-3306 写入示例数据。

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

- 向 mysql-3307 写入示例数据。

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

### 运行下游 TiDB

使用以下命令运行一个 TiDB server：

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-community-server-v6.0.0-linux-amd64.tar.gz
tar -xzvf tidb-latest-linux-amd64.tar.gz
mv tidb-latest-linux-amd64/bin/tidb-server ./
./tidb-server -P 4000 --store mocktikv --log-file "./tidb.log" &
```

> **警告：**
>
> 本文档中 TiDB 的部署方法并**不适用**于生产或开发环境。

## 配置 MySQL 数据源

运行数据迁移任务前，需要对 source 进行配置，也就是 MySQL 的相关设置。

### 对密码进行加密

> **注意：**
>
> + 如果数据库没有设置密码，则可以跳过该步骤。
> + DM v1.0.6 及其以后版本可以使用明文密码配置 source 信息。

为了安全，可配置及使用加密后的密码。使用 dmctl 对 MySQL/TiDB 的密码进行加密，以密码为 "123456" 为例：

{{< copyable "shell-regular" >}}

```bash
./dmctl encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

记录该加密后的密码，用于下面新建 MySQL 数据源。

### 编写 source 配置文件

把以下配置文件内容写入到 `conf/source1.yaml` 中。

MySQL1 的配置文件：

```yaml
# MySQL1 Configuration.

source-id: "mysql-replica-01"

# 是否开启 GTID
enable-gtid: true

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

对于 MySQL2 数据源，将以上内容复制到文件 `conf/source2.yaml` 中，将 `conf/source2.yaml` 配置文件中的 `name` 修改为 `mysql-replica-02`，并将 `password` 和 `port` 改为相应的值。

### 创建 source

在终端中执行下面的命令，使用 dmctl 将 MySQL1 的数据源配置加载到 DM 集群中：

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

对于 MySQL2，将上面命令中的配置文件替换成 MySQL2 对应的配置文件。

## 创建数据迁移任务

在导入[准备数据](#准备数据)后，MySQL1 和 MySQL2 实例中有若干个分表，这些分表的结构相同，所在库的名称都以 "sharding" 开头，表名称都以 "t" 开头，并且主键或唯一键不存在冲突（即每张分表的主键或唯一键各不相同）。现在需要把这些分表迁移到 TiDB 中的 `db_target.t_target` 表中。

首先创建任务的配置文件：

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
  password: "" # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

mysql-instances:
  - source-id: "mysql-replica-01"
    block-allow-list:  "instance"   # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
    mydumper-thread: 4
    loader-thread: 16
    syncer-thread: 16

  - source-id: "mysql-replica-02"
    block-allow-list:  "instance"  # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
    mydumper-thread: 4
    loader-thread: 16
    syncer-thread: 16

block-allow-list:                  # 如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
  instance:
    do-dbs: ["~^sharding[\\d]+"]
    do-tables:
    -  db-name: "~^sharding[\\d]+"
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

将以上配置内容写入到 `conf/task.yaml` 文件中，使用 dmctl 创建任务：

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr 127.0.0.1:8261 start-task conf/task.yaml
```

结果如下：

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

这样就成功创建了一个将 MySQL1 和 MySQL2 实例中的分表数据迁移到 TiDB 的任务。

## 数据校验

修改上游 MySQL 分表中的数据，然后使用 [sync-diff-inspector](/sync-diff-inspector/shard-diff.md) 校验上下游数据是否一致，如果一致则说明迁移任务运行正常。
