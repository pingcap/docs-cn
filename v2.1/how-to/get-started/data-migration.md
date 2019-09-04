---
title: TiDB DM (Data Migration) Tutorial
summary: Learn the basics of the TiDB DM (Data Migration) platform, to migrate a simple sharded schema from MySQL to TiDB.
category: how-to
---

# TiDB DM (Data Migration) Tutorial

TiDB DM (Data Migration) is a platform that supports migrating large, complex, production data sets from MySQL or MariaDB to TiDB.

DM supports creating and importing an initial dump of data, as well as keeping data replicated during migration by reading and applying binary logs from the source data store. DM can migrate sharded topologies from in-production databases by merging tables from multiple separate upstream MySQL/MariaDB instances/clusters. In addition to its use for migrations, DM is often used on an ongoing basis by existing MySQL or MariaDB users who deploy a TiDB cluster as a slave, to either provide improved horizontal scalability or run real-time analytical workloads on TiDB without needing to manage an ETL pipeline.

In this tutorial, we'll see how to migrate a sharded table from multiple upstream MySQL instances. We'll do this a couple of different ways. First, we'll merge several tables/shards that do not conflict; that is, they're partitioned using a scheme that does not result in conflicting unique key values. Then, we'll merge several tables that **do** have conflicting unique key values.

This tutorial assumes you're using a new, clean CentOS 7 instance. You can virtualize locally (using VMware, VirtualBox, etc.), or deploy a small cloud VM on your favorite provider. You'll have the best luck if you have at least 1GB of memory, since we're going to run quite a few services.

> **Warning:**
>
> The methodology used to deploy TiDB in this tutorial should **not** be used to deploy TiDB in a production or development setting.

## Architecture

![TiDB DM architecture](/media/dm-architecture.png)

The TiDB DM (Data Migration) platform consists of 3 components: DM-master, DM-worker, and dmctl.

* DM-master manages and schedules the operation of data replication tasks.
* DM-worker executes specific data replication tasks.
* dmctl is the command line tool used to control the DM cluster.

Individual tasks are defined in .yaml files that are read by dmctl and submitted to DM-master. DM-master then informs each instance of DM-worker of its responsibilities for a given task.

For additional information about DM, please consult [Data Migration Overview](/v2.1/reference/tools/data-migration/overview.md) in the TiDB documentation.

## Setup

We're going to deploy 3 instances of MySQL Server, and 1 instance each of pd-server, tikv-server, and tidb-server. Then we'll start a single DM-master and 3 instances of DM-worker.

First, install MySQL 5.7 and download/extract the TiDB packages we'll use:

```bash
sudo yum install -y http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm
sudo yum install -y mysql-community-server
curl http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz | tar xzf -
curl http://download.pingcap.org/dm-latest-linux-amd64.tar.gz | tar xzf -
curl -L https://github.com/pingcap/docs/raw/master/dev/how-to/get-started/dm-cnf/dm-cnf.tgz | tar xvzf -
```

Create some directories and symlinks:

```bash
mkdir -p bin data logs
ln -sf -t bin/ "$HOME"/*/bin/*
[[ :$PATH: = *:$HOME/bin:* ]] || echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile && . ~/.bash_profile
```

Set up configuration for the 3 instances of MySQL Server we'll start:

```bash
tee -a "$HOME/.my.cnf" <<EoCNF
[server]
socket=mysql.sock
pid-file=mysql.pid
log-error=mysql.err
log-bin
auto-increment-increment=5
[server1]
datadir=$HOME/data/mysql1
server-id=1
port=3307
auto-increment-offset=1
[server2]
datadir=$HOME/data/mysql2
server-id=2
port=3308
auto-increment-offset=2
[server3]
datadir=$HOME/data/mysql3
server-id=3
port=3309
auto-increment-offset=3
EoCNF
```

Initialize and start our MySQL instances:

```bash
for i in 1 2 3
do
    echo  "mysql$i"
    mysqld --defaults-group-suffix="$i" --initialize-insecure
    mysqld --defaults-group-suffix="$i" &
done
```

To make sure your MySQL server instances are all running, you can execute `jobs` and/or `pgrep -a mysqld`:

```
$ jobs
[1]   Running                 mysqld --defaults-group-suffix="$i" &
[2]-  Running                 mysqld --defaults-group-suffix="$i" &
[3]+  Running                 mysqld --defaults-group-suffix="$i" &
$ pgrep -a mysqld
17672 mysqld --defaults-group-suffix=1
17727 mysqld --defaults-group-suffix=2
17782 mysqld --defaults-group-suffix=3
```

## Non-overlapping shards

Our first scenario consists of 3 "shards" with the same schema, but non-overlapping auto-increment primary keys.

We achieve that by having set `auto-increment-increment=5` and `auto-increment-offset` in our .my.cnf file. `auto-increment-increment` tells each instance to increment by 5 for each new auto-increment ID it generates, and `auto-increment-offset`, set differently for each instance, tells that instance the offset from 0 to start counting. For example, an instance with `auto-increment-increment=5` and `auto-increment-offset=2` will generate the auto-increment ID sequence {2,7,12,17,22,…}.

Create our MySQL database and table in each of the 3 MySQL Server instances:

```bash
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest1;
        create table dmtest1.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
EoSQL
done
```

Insert a few hundred rows into each of the MySQL instances:

```bash
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest1 <<EoSQL
        insert into t1 values (),(),(),(),(),(),(),();
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        update t1 set c=md5(id), port=@@port;
EoSQL
done
```

Select the rows back from the MySQL instances to make sure things look right:

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from dmtest1.t1'
done | sort -n
```

Note that we have incrementing, non-overlapping IDs in the left-hand column. The port number in the right-hand column shows which instance the rows were inserted into and are being selected from:

```
...
1841    e8dfff4676a47048d6f0c4ef899593dd        3307
1842    57c0531e13f40b91b3b0f1a30b529a1d        3308
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

## Starting DM master and workers

Our goal in this exercise is to use DM to combine the data from these distinct MySQL instances into a single table in TiDB.

The package of configuration files we unpacked earlier (dm-cnf.tgz) contains the configuration for the components of the TiDB cluster, the DM components, and for the 2 DM tasks we'll explore in this tutorial.

We'll start a single tidb-server instance, one DM-worker process for each of the MySQL server instances (3 total), and a single DM-master process:

```bash
tidb-server --log-file=logs/tidb-server.log &
for i in 1 2 3; do dm-worker --config=dm-cnf/dm-worker$i.toml & done
dm-master --config=dm-cnf/dm-master.toml &
```

You can execute `jobs` and/or `ps -a` to make sure these processes are all running:

```
$ jobs
[1]   Running                 mysqld --defaults-group-suffix="$i" &
[2]   Running                 mysqld --defaults-group-suffix="$i" &
[3]   Running                 mysqld --defaults-group-suffix="$i" &
[4]   Running                 tidb-server --log-file=logs/tidb-server.log &
[5]   Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
[6]   Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
[7]-  Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
[8]+  Running                 dm-master --config=dm-cnf/dm-master.toml &
$ ps -a
   PID TTY          TIME CMD
 17317 pts/0    00:00:00 screen
 17672 pts/1    00:00:04 mysqld
 17727 pts/1    00:00:04 mysqld
 17782 pts/1    00:00:04 mysqld
 18586 pts/1    00:00:02 tidb-server
 18587 pts/1    00:00:00 dm-worker
 18588 pts/1    00:00:00 dm-worker
 18589 pts/1    00:00:00 dm-worker
 18590 pts/1    00:00:00 dm-master
 18892 pts/1    00:00:00 ps
```

Each of the upstream MySQL Server instances corresponds to a separate DM-worker instance, each of which has its own configuration file. These files describe the details of the connection to the upstream MySQL Server as well as where to store the relay log files (the local copy of the upstream server's binary log) and the output of Mydumper. Each DM-worker should listen on a different port (defined by `worker-addr`). Here's dm-worker1.toml, for example:

```toml
# Worker Configuration.

server-id = 1
source-id = "mysql1"
flavor = "mysql"
worker-addr = ":8262"
log-file = "logs/worker1.log"
relay-dir = "data/relay1"
meta-dir = "data/meta1"
dir = "data/dump1"

[from]
host = "127.0.0.1"
user = "root"
password = ""
port = 3307
```

The `flavor` option should be set to `"mysql"` (the default value, and 5.5 < MySQL versions < 8.0 are supported) if migrating from MySQL Server, Percona Server, Percona XtraDB Cluster, or Amazon Aurora or RDS. If migrating from MariaDB Server or MariaDB (Galera) Cluster, use `flavor = "mariadb"` (only MariaDB versions greater than 10.1.2 are supported).

Tasks are defined in YAML files. First, let's look at dmtask1.yaml:

```yaml
name: dmtask1
task-mode: all
is-sharding: true
enable-heartbeat: true
ignore-checking-items: ["auto_increment_ID"]

target-database:
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  - source-id: "mysql1"
    server-id: 1
    black-white-list: "dmtest1"
    loader-config-name: "loader1"
  - source-id: "mysql2"
    server-id: 2
    black-white-list: "dmtest1"
    loader-config-name: "loader2"
  - source-id: "mysql3"
    server-id: 3
    black-white-list: "dmtest1"
    loader-config-name: "loader3"

black-white-list:
  dmtest1:
    do-dbs: ["dmtest1"]

loaders:
  loader1:
    dir: "data/dump1"
  loader2:
    dir: "data/dump2"
  loader3:
    dir: "data/dump3"
```

There are a number of global options, and several groups of options that define various behaviors.

* `task-mode: all` tells DM to both import a full backup of the upstream instances as well as replicate incremental updates using the upstream MySQL server's binary log.

    * Alternatively, you can give `task-mode` the `full` or `incremental` value, respectively, to get only one of those two behaviors.

* `is-sharding: true` tells DM that we want multiple DM-worker instances to work on a single task to merge several upstream shards into a single downstream table.

* `ignore-checking-items: ["auto_increment_ID"]` disables DM's detection of potential auto-increment conflicts among the upstream instances. DM can detect that all 3 upstream MySQL servers have an auto-increment column for a table with the same name in the same schema, and that this situation would be expected to lead to conflicts among the several tables. We've avoided that by setting `auto-increment-increment` and `auto-increment-offset` so that each of the MySQL servers gives non-overlapping IDs. So, we tell DM to ignore checking for overlapping auto-increment IDs in this task.

* We use `black-white-list` to limit the scope of this task to database `dmtest`.

* The `loaders` section defines where to find the output of each instance of Mydumper that was executed by the respective instance of DM-worker.

The `dmctl` tool is an interactive client that facilitates interaction with the DM cluster. You use it to start tasks, query task status, et cetera. Start the tool by executing `dmctl -master-addr :8261` to get the interactive prompt:

```
$ dmctl -master-addr :8261
Welcome to dmctl
Release Version: v1.0.0-alpha-69-g5134ad1
Git Commit Hash: 5134ad19fbf6c57da0c7af548f5ca2a890bddbe4
Git Branch: master
UTC Build Time: 2019-04-29 09:36:42
Go Version: go version go1.12 linux/amd64

»
```

To start dmtask1, execute `start-task dm-cnf/dmtask1.yaml`:

```
» start-task dm-cnf/dmtask1.yaml
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8263",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8264",
            "msg": ""
        }
    ]
}
```

Starting the task will kick off the actions defined in the task configuration file. That includes executing instances of Mydumper and loader, and connecting the workers to the upstream MySQL servers as replication slaves after the initial data dump has been loaded.

We can see that all rows have been migrated to the TiDB server:

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:

```
...
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

DM is now acting as a slave to each of the MySQL servers, reading their binary logs to apply updates in realtime to the downstream TiDB server:

```bash
for i in 1 2 3
do
     mysql -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select host, command, state from information_schema.processlist where command="Binlog Dump"'
done
```

Expect this output:

```
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42168 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42922 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:56798 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
```

We can see that this is the case by inserting some rows into the upstream MySQL servers, selecting those rows from TiDB, updating those same rows in MySQL, and selecting them again:

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'insert into t1 (id) select null from t1' dmtest1
done
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:

```
6313    NULL    NULL
6316    NULL    NULL
6317    NULL    NULL
6318    NULL    NULL
6321    NULL    NULL
6322    NULL    NULL
6323    NULL    NULL
6326    NULL    NULL
6327    NULL    NULL
6328    NULL    NULL
```

Now update those rows, so we can see that changes to data are correctly propagated to TiDB:

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'update t1 set c=md5(id), port=@@port' dmtest1
done | sort -n
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:

```
6313    2118d8a1b7004ed5baf5347a4f99f502        3309
6316    6107d91fc9a0b04bc044aa7d8c1443bd        3307
6317    0e9b734aa25ca8096cb7b56dc0dd8929        3308
6318    b0eb9a95e8b085e4025eae2f0d76a6a6        3309
6321    7cb36e23529e4de4c41460940cc85e6e        3307
6322    fe1f9c70bdf347497e1a01b6c486bdb9        3308
6323    14eac0d254a6ccaf9b67584c7830a5c0        3309
6326    17b65afe58c49edc1bdd812c554ee3bb        3307
6327    c54bc2ded4480856dc9f39bdcf35a3e7        3308
6328    b294504229c668e750dfcc4ea9617f0a        3309
```

As long as the DM master and workers are running the "dmtest1" task, they'll continue to keep the downstream TiDB server replicated with the upstream MySQL server instances.

## Overlapping shards

The first step of the next exercise will be to create a second database and set of tables across the MySQL instances.

```bash
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest2;
        create table dmtest2.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
EoSQL
done
```

Insert a few hundred rows into each of the MySQL instances. By setting `auto_increment_increment=1` and `auto_increment_offset=1`, we'll ensure that all 3 MySQL servers allocate the same sequence of auto-increment IDs:

```bash
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest2 <<EoSQL
        set auto_increment_increment=1, auto_increment_offset=1;
        insert into t1 values (),(),(),(),(),(),(),();
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        update t1 set c=md5(id), port=@@port;
EoSQL
done
```

Select the rows back from the MySQL instances to make sure things look right:

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from t1' dmtest2
done | sort -n
```

Unlike the last exercise, this time you can see that the same auto-increment IDs (the left-most column) are duplicated across multiple upstream instances (identified by the port number in the right-most column):

```
...
370     d709f38ef758b5066ef31b18039b8ce5        3307
370     d709f38ef758b5066ef31b18039b8ce5        3308
370     d709f38ef758b5066ef31b18039b8ce5        3309
371     41f1f19176d383480afa65d325c06ed0        3307
371     41f1f19176d383480afa65d325c06ed0        3308
371     41f1f19176d383480afa65d325c06ed0        3309
372     24b16fede9a67c9251d3e7c7161c83ac        3307
372     24b16fede9a67c9251d3e7c7161c83ac        3308
372     24b16fede9a67c9251d3e7c7161c83ac        3309
```

If we try to migrate these rows as-is into a single table in a downstream TiDB instance, the Primary Key auto-increment values will collide and cause duplicate key errors to be issued. We'll use the "partition id" expression of the "column mappings" feature of DM to transform the auto-increment values so that they no longer collide.

Let's take a look at dmtask2.yaml：

```yaml
name: dmtask2
task-mode: all
is-sharding: true
enable-heartbeat: true

target-database:
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""

# The column-mappings section tells DM how we want it to combine
# the data from the 3 upstream instances.
column-mappings:
  mysql1:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["1", "", ""]
    source-column: "id"
    target-column: "id"
  mysql2:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["2", "", ""]
    source-column: "id"
    target-column: "id"
  mysql3:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["3", "", ""]
    source-column: "id"
    target-column: "id"

mysql-instances:
  - source-id: "mysql1"
    server-id: 1
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql1"]
    loader-config-name: "loader1"
  - source-id: "mysql2"
    server-id: 2
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql2"]
    loader-config-name: "loader2"
  - source-id: "mysql3"
    server-id: 3
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql3"]
    loader-config-name: "loader3"

black-white-list:
  dmtest2:
    do-dbs: ["dmtest2"]

loaders:
  loader1:
    dir: "data/dump1"
  loader2:
    dir: "data/dump2"
  loader3:
    dir: "data/dump3"
```

* We aren't using `ignore-checking-items: ["auto_increment_ID"]` anymore, because the upstream auto-increment IDs **do** collide.

* We use `column-mappings` to tell DM how we want it to handle the shard merge operation.

    * We have a single upstream schema and table, so our `schema-pattern` and `table-pattern` are actually just strings.

        * You can include wildcards in these if you want to merge multiple schemas and/or tables into a single downstream table.

    * The `partition id` expression has a corresponding `arguments` section that controls the algorithm used to transform upstream IDs into those used in the downstream TiDB cluster. There's a more in-depth discussion of this algorithm later in this tutorial.

    * `source_column` and `target_column` are pretty self-explanatory, but it's worth noting that they offer the possibility of merging upstream inserts into a downstream table with a different structure, for example if you need to preserve the original values.

    * Each entry in `mysql-instances` has a different column mapping because different arguments to the `partition id` algorithm needs to be used for each.

Let's start dmtask2:

```bash
dmctl -master-addr :8261 <<<"start-task dm-cnf/dmtask2.yaml"
```

Expect this output:

```
Welcome to dmctl
Release Version: v1.0.0-alpha-76-g9fa6918
Git Commit Hash: 9fa6918c4b698e742a9893fa22235ee6ffcfa3b1
Git Branch: master
UTC Build Time: 2019-05-14 06:17:31
Go Version: go version go1.12 linux/amd64

{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8263",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8264",
            "msg": ""
        }
    ]
}
```

And let's see what the data looks like after it's been imported into the downstream TiDB instance:

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest2 | tail
```

Expect this output:

```
1729382256910270827     00411460f7c92d2124a67ea0f4cb5f85        3309
1729382256910270828     bac9162b47c56fc8a4d2a519803d51b3        3309
1729382256910270829     9be40cee5b0eee1462c82c6964087ff9        3309
1729382256910270830     5ef698cd9fe650923ea331c15af3b160        3309
1729382256910270831     05049e90fa4f5039a8cadc6acbb4b2cc        3309
1729382256910270832     cf004fdc76fa1a4f25f62e0eb5261ca3        3309
1729382256910270833     0c74b7f78409a4022a2c4c5a5ca3ee19        3309
1729382256910270834     d709f38ef758b5066ef31b18039b8ce5        3309
1729382256910270835     41f1f19176d383480afa65d325c06ed0        3309
1729382256910270836     24b16fede9a67c9251d3e7c7161c83ac        3309
```

So, how do we end up with these new ID values in the left-most column of our downstream table? DM uses an algorithm to bit-shift the ID assigned by the upstream MySQL instances to generate a unique ID for the downstream TiDB instance. In our test case, the partition ID consists only of the "instance ID", because the schema and table names are the same on each of the upstream MySQL servers. We left the "schema ID" and "table ID" components of the partition id expression arguments blank:

```bash
grep arguments dm-cnf/dmtask2.yaml
```

Expected output:

```
    arguments: ["1", "", ""]
    arguments: ["2", "", ""]
    arguments: ["3", "", ""]
```

The last auto-increment ID assigned by the upstream MySQL servers was 372. The rows with the highest transformed auto-increment IDs after migration to the TiDB server are from instance 3 (identified by port number 3309 in the right-most column). The last row has the same value in the middle column as the rows with ID 372 in the MySQL instances, so we can be sure what we're looking at. The algorithm allots 44 bits of the 64 bit integer for the auto-increment ID that comes from upstream, which means that values above 2^44 (about 17.5 trillion) can't be handled by the default implementation of the partition id column mapping scheme. 1 bit is reserved for the sign, 4 for the instance ID, 7 for the schema ID, and 8 for the table ID (44 + 1 + 4 + 7 + 8 = 64 bits). Customizations of the algorithm are trivial, so please contact PingCAP if you have a use case that can't be accommodated by this implementation.

Here we can reproduce the algorithm for our use case, taking an auto-increment ID of 372 and instance ID of 3:

```bash
id=372 instance_id=3 schema_id=0 table_id=0
echo $(( instance_id << (64-1-4) | schema_id << (64-1-4-7) | table_id << 44 | id ))
```

Expected output:

```
1729382256910270836
```

Because only 44 bits correspond to the original auto-increment value, we can discard the rest of them to convert the transformed values back to what they were originally:

```bash
echo $(( 1729382256910270836 & (1<<45)-1 ))
```

Expected output:

```
372
```

And we can even use that expression in an SQL query to see the transformed IDs along the original IDs:

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select id, id&(1<<45)-1 as orig_id, c, port from t1 order by orig_id' dmtest2 | tail
```

Expected output:

```
576460752303423857      369     0c74b7f78409a4022a2c4c5a5ca3ee19        3307
576460752303423858      370     d709f38ef758b5066ef31b18039b8ce5        3307
1152921504606847346     370     d709f38ef758b5066ef31b18039b8ce5        3308
1729382256910270834     370     d709f38ef758b5066ef31b18039b8ce5        3309
576460752303423859      371     41f1f19176d383480afa65d325c06ed0        3307
1729382256910270835     371     41f1f19176d383480afa65d325c06ed0        3309
1152921504606847347     371     41f1f19176d383480afa65d325c06ed0        3308
576460752303423860      372     24b16fede9a67c9251d3e7c7161c83ac        3307
1729382256910270836     372     24b16fede9a67c9251d3e7c7161c83ac        3309
1152921504606847348     372     24b16fede9a67c9251d3e7c7161c83ac        3308
```

## Conclusion

In this tutorial, we've completed 2 exercises. The first was a shard migration from 3 upstream MySQL server instances that each assigned non-overlapping sets of auto-increment IDs, and the second was a shard migration from 3 upstream MySQL server instances that each assigned auto-increment IDs that conflicted with one another. We saw how DM not only takes care of importing an initial dump of data in the cluster, but that it can also read binary logs to keep the downstream TiDB cluster in sync with the upstream instance(s).

For additional information about DM, please consult [Data Migration Overview](/v2.1/reference/tools/data-migration/overview.md) in the TiDB documentation or join the [TiDB Community Slack](https://pingcap.com/tidbslack/) channel!
