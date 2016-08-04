# Run a TiDB cluster in Docker on a single host

This page shows you how to run a TiDB cluster quickly on a single machine.


## Preparation
Before you start, make sure that:

+ Installed the latest version of [Docker](https://www.docker.com/products/docker) 
+ Pulled the TiDB/TiKV/PD docker images from PingCAP's Docker Hub repositories

```bash
docker pull pingcap/tidb:latest
docker pull pingcap/tikv:latest
docker pull pingcap/pd:latest
```

## Step 1. Create a docker bridge network

```bash
net="isolated_nw"
docker network rm ${net}
docker network create --driver bridge ${net} 
```

After creating a Docker network, add all the TiDB containers into it to make a standalone cluster.
The services in cluster can communicate with each other using the name instead of IP address.
In addition, you can replace the network name with any of your favorite names.

## Step 2. Using `Busybox` container as the storage volume

```bash
docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

## Step 3. Start the PD service

Start 3 PD servers, respectively named as **pd1**, **pd2**, **pd3**.

**pd1:** 

```bash
docker run --net ${net} -d --name pd1 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd1:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd1:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd1:1234"
```

**pd2:**

```bash
docker run --net ${net} -d --name pd2 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd2:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd2:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd2:1234"
```

**pd3:**

```bash
docker run --net ${net} -d --name pd3 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd3:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd3:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd3:1234"
```

After that, if you need to add new PD servers into the existing cluster, use the `--join` flag, and specify any one of the available **advertise-client-urls** above.

**pd4:**

```bash
docker run --net ${net} -d --name pd4 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd4" \
  --data-dir="/tidata/pd4" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd4:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd4:2380" \
  --join="http://pd1:2379" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd4:1234"
```

**pd5:**

```bash
docker run --net ${net} -d --name pd5 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd5" \
  --data-dir="/tidata/pd5" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd5:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd5:2380" \
  --join="http://pd4:2379" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd5:1234"
```

## Step 4. Start the TiKV service

Next you can run any number of TiKV instances, which is the underlying distributed storage.

**tikv1:**

```bash
docker run --net ${net} -d --name tikv1 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv1:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv2:**

```bash
docker run --net ${net} -d --name tikv2 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv2:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv3:**

```bash
docker run --net ${net} -d --name tikv3 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv3:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

## Step 5. Start the TiDB service

The **tidb-server** as the SQL Layer is stateless, and accept client connections from users.
Using `-p 4000:4000` to expose port 4000 to the host server.

```bash
docker run --net ${net} -d --name tidb \
  -p 4000:4000 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="pd1:2379,pd2:2379,pd3:2379?cluster=1" \
  -L warn
```

## Step 6. Use the official MySQL client
Once the TiDB cluster is running, you can use the official MySQL client to connect to TiDB for a quick test.

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

## Alternatively, use `docker-compose`

Note: If you are using `docker-compose`, you don't need to create a Docker network and start TiDB,TiKV,PD containers separately. 
The following `docker-compose.yml` file is enough.

```bash
version: '2'

services:
  pd1:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd1 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd1:2379
      - --advertise-peer-urls=http://pd1:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd1:1234
      
    privileged: true

  pd2:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd2 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd2:2379
      - --advertise-peer-urls=http://pd2:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd2:1234
      
    privileged: true

  pd3:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd3 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd3:2379
      - --advertise-peer-urls=http://pd3:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380 
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd3:1234
      
    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv2:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv3:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tidb:
    image: pingcap/tidb
    ports:
      - "4000"
      - "10080"

    command:
      - --store=tikv 
      - --path=pd1:2379,pd2:2379,pd3:2379?cluster=1
      - -L=warn

    depends_on:
      - "tikv1"
      - "tikv2"
      - "tikv3"

    privileged: true
```

+ Use `docker-compose up -d` to create and start the cluster. 
+ Use `docker-compose port tidb 4000` to print the TiDB public port. For example, if the output is `0.0.0.0:32966`, the TiDB public port is `32966`.
+ Use `mysql -h 127.0.0.1 -P 32966 -u root -D test` to connect to TiDB and enjoy it. 
+ Use `docker-compose down` to stop and remove the cluster.

