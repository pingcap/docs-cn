---
title: TiDB Docker Compose Deployment
summary: Use Docker Compose to quickly deploy a TiDB testing cluster.
category: how-to
---

# TiDB Docker Compose Deployment

This document describes how to quickly deploy a TiDB testing cluster with a single command using [Docker Compose](https://docs.docker.com/compose/overview).

With Docker Compose, you can use a YAML file to configure application services in multiple containers. Then, with a single command, you can create and start all the services from your configuration.

> **Warning:**
>
> This is for testing only. DO NOT USE in production! Please deploy TiDB with [our Ansible solution](/how-to/deploy/orchestrated/ansible.md) or [TiDB Operator in Kubernetes](/tidb-in-kubernetes/deploy/tidb-operator.md) in production.

## Prerequisites

Make sure you have installed the following items on your machine:

- [Git](https://git-scm.com/downloads)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL Client](https://dev.mysql.com/downloads/mysql/)

## Deploy TiDB using Docker Compose

1. Download `tidb-docker-compose`.

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. Change the directory to tidb-docker-compose and get the latest TiDB Docker Images:

    ```bash
    cd tidb-docker-compose && docker-compose pull
    ```

3. Start the TiDB cluster:

    ```bash
    docker-compose up -d
    ```

4. Use the MySQL client to connect to TiDB to read and write data:

    ```
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

## Monitor the cluster 

After you have successfully deployed a TiDB cluster, you can now monitor the TiDB cluster using one of the following methods:

- Use Grafana to view the status of the cluster via [http://localhost:3000](http://localhost:3000) with the default account name and password:  `admin` and `admin`.
- Use [TiDB-Vision](https://github.com/pingcap/tidb-vision), a cluster visualization tool, to see data transfer and load-balancing inside your cluster via [http://localhost:8010](http://localhost:8010).

## Customize the cluster

After the deployment is completed, the following components are deployed by default:

- 3 PD instances, 3 TiKV instances, 1 TiDB instance
- Monitoring components: Prometheus, Pushgateway, Grafana
- Data visualization component: tidb-vision

To customize the cluster, you can edit the `docker-compose.yml` file directly. It is recommended to generate `docker-compose.yml` using the [Helm](https://helm.sh) template engine, because manual editing is tedious and error-prone.

1. Install Helm.

    [Helm](https://helm.sh) can be used as a template rendering engine. To use Helm, you only need to download its binary file:

    ```bash
    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
    ```

    For macOS, you can also install Helm using the following command in Homebrew:

    ```bash
    brew install kubernetes-helm
    ```

2. Download `tidb-docker-compose`.

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

3. Customize the cluster.

    ```bash
    cd tidb-docker-compose
    vim compose/values.yaml # custom the cluster size, docker image, port mapping and so on
    ```

    You can modify the configuration in `values.yaml`, such as the cluster size, TiDB image version, and so on.

    [tidb-vision](https://github.com/pingcap/tidb-vision) is the data visualization interface of the TiDB cluster, used to visually display the PD scheduling on TiKV data. If you do not need this component, comment out the `tidbVision` section.

    For PD, TiKV, TiDB and tidb-vision, you can build Docker images from GitHub source code or local files for development and testing.

    - To build PD, TiKV or TiDB images from the locally compiled binary file, you need to comment out the `image` field and copy the compiled binary file to the corresponding `pd/bin/pd-server`, `tikv/bin/tikv-server`, `tidb/bin/tidb-server`.
    - To build the tidb-vision image from local, you need to comment out the `image` field and copy the tidb-vision project to `tidb-vision/tidb-vision`.

4. Generate the `docker-compose.yml` file.

    ```bash
    helm template compose > generated-docker-compose.yml
    ```

5. Create and start the cluster using the generated `docker-compose.yml` file.

    ```bash
    docker-compose -f generated-docker-compose.yml pull # Get the latest Docker images
    docker-compose -f generated-docker-compose.yml up -d
    ```

6. Access the cluster.

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

    Access the Grafana monitoring interface:

    - Default address: <http://localhost:3000>
    - Default account name: admin
    - Default password: admin

    If tidb-vision is enabled, you can access the cluster data visualization interface: <http://localhost:8010>.

## Access the Spark shell and load TiSpark

Insert some sample data to the TiDB cluster:

```bash
$ docker-compose exec tispark-master bash
$ cd /opt/spark/data/tispark-sample-data
$ mysql -h tidb -P 4000 -u root < dss.ddl
```

After the sample data is loaded into the TiDB cluster, you can access the Spark shell using `docker-compose exec tispark-master /opt/spark/bin/spark-shell`.

```bash
$ docker-compose exec tispark-master /opt/spark/bin/spark-shell
...
Spark context available as 'sc' (master = local[*], app id = local-1527045927617).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.1.1
      /_/

Using Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_172)
Type in expressions to have them evaluated.
Type :help for more information.

scala> import org.apache.spark.sql.TiContext
...
scala> val ti = new TiContext(spark)
...
scala> ti.tidbMapDatabase("TPCH_001")
...
scala> spark.sql("select count(*) from lineitem").show
+--------+
|count(1)|
+--------+
|   60175|
+--------+
```

You can also access Spark with Python or R using the following commands:

```
docker-compose exec tispark-master /opt/spark/bin/pyspark
docker-compose exec tispark-master /opt/spark/bin/sparkR
```

For more details about TiSpark, see [here](/how-to/deploy/tispark.md).

Here is [a 5-minute tutorial](https://www.pingcap.com/blog/how_to_spin_up_an_htap_database_in_5_minutes_with_tidb_tispark/) for macOS users that shows how to spin up a standard TiDB cluster using Docker Compose on your local computer.
