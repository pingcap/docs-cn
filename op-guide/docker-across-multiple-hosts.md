# Run a TiDB cluster in Docker across multiple hosts

This page shows you an example of how to manually deploy a TiDB cluster using Docker across multiple machines.


## Preparation
Assume we have 3 machines with the following details:

|Name|Host IP|
|----|-------|
|**host1**|192.168.1.100|
|**host2**|192.168.1.101|
|**host3**|192.168.1.102|

On each host, we have installed Docker with the latest version and pulled the latest Docker images of TiDB, TiKV and PD.

```bash
docker pull pingcap/tidb:latest
docker pull pingcap/tikv:latest
docker pull pingcap/pd:latest
```

## Step 1. Start the `busybox` container as the storage volume for each host

Run the following command on **host1**, **host2**, **host3** respectively:

```bash
export host1=192.168.1.100
export host2=192.168.1.101
export host3=192.168.1.102

docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

## Step 2. Start PD on each host

**host1:**
```bash
docker run -d --name pd1 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host1}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host1}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host1}:1234"
```

**host2:**
```bash
docker run -d --name pd2 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host2}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host2}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host2}:1234"
```

**host3:**
```bash
docker run -d --name pd3 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host3}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host3}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host3}:1234"
```

## Step 3. Start TiKV on each host

**host1:**
```bash
docker run -d --name tikv1 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host1}:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host2:**
```bash
docker run -d --name tikv2 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host2}:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host3:**
```bash
docker run -d --name tikv3 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host3}:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

## Step 4. Start TiDB on **host1**

```bash
docker run -d --name tidb \
  -p 4000:4000 \
  -p 10080:10080 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="${host1}:2379,${host2}:2379,${host3}:2379?cluster=1" \
  -L warn
```

## Step 5. Use the official MySQL client to connect to TiDB and enjoy it.

```bash
mysql -h 127.0.0.1 -P 4000 -u root -D test
# Welcome to the MySQL monitor.  Commands end with ; or \g.
# Your MySQL connection id is 10001
# Server version: 5.5.31-TiDB-1.0 MySQL Community Server (GPL)
```

Then run some SQL statments:

```bash
mysql> CREATE DATABASE mydb;
Query OK, 0 rows affected (0.01 sec)

mysql> USE mydb;
Database changed

mysql> CREATE TABLE mytable ( id INT, data VARCHAR(100), dt DATE, PRIMARY KEY (id) );
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO mytable VALUES (1, 'test data', '2016-08-03');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM mytable;
+----+-----------+------------+
| id | data      | dt         |
+----+-----------+------------+
|  1 | test data | 2016-08-03 |
+----+-----------+------------+
1 row in set (0.00 sec)
```
