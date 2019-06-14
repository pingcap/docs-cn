---
title: TiSpark Quick Start Guide
summary: Learn how to use TiSpark quickly.
category: User Guide
---

# TiSpark Quick Start Guide

To make it easy to [try TiSpark](/dev/tispark/tispark-user-guide.md), the TiDB cluster installed using TiDB-Ansible integrates Spark, TiSpark jar package and TiSpark sample data by default.

## Deployment information

- Spark is deployed by default in the `spark` folder in the TiDB instance deployment directory.
- The TiSpark jar package is deployed by default in the `jars` folder in the Spark deployment directory.

    ```
    spark/jars/tispark-SNAPSHOT-jar-with-dependencies.jar
    ```

- TiSpark sample data and import scripts are deployed by default in the TiDB-Ansible directory.

    ```
    tidb-ansible/resources/bin/tispark-sample-data
    ```

## Prepare the environment

### Install JDK on the TiDB instance

Download the latest version of JDK 1.8 from [Oracle JDK official download page](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase8-2177648.html). The version used in the following example is `jdk-8u141-linux-x64.tar.gz`.

Extract the package and set the environment variables based on your JDK deployment directory.  

Edit the `~/.bashrc` file. For example:

```bashrc
export JAVA_HOME=/home/pingcap/jdk1.8.0_144
export PATH=$JAVA_HOME/bin:$PATH
```

Verify the validity of JDK:

```
$ java -version
java version "1.8.0_144"
Java(TM) SE Runtime Environment (build 1.8.0_144-b01)
Java HotSpot(TM) 64-Bit Server VM (build 25.144-b01, mixed mode)
```

### Import the sample data

Assume that the TiDB cluster is started. The service IP of one TiDB instance is `192.168.0.2`, the port is `4000`, the user name is `root`, and the password is null.

```
cd tidb-ansible/resources/bin/tispark-sample-data
```

Edit the TiDB login information in `sample_data.sh`. For example:

```
mysql --local-infile=1 -h 192.168.0.2 -P 4000 -u root < dss.ddl
```

Run the script:

```
./sample_data.sh
```

> **Note:**
>
> You need to install the MySQL client on the machine that runs the script. If you are a CentOS user, you can install it through the command `yum -y install mysql`.

Log into TiDB and verify that the `TPCH_001` database and the following tables are included.

```
$ mysql -uroot -P4000 -h192.168.0.2
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| TPCH_001           |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)

MySQL [(none)]> use TPCH_001
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MySQL [TPCH_001]> show tables;
+--------------------+
| Tables_in_TPCH_001 |
+--------------------+
| CUSTOMER           |
| LINEITEM           |
| NATION             |
| ORDERS             |
| PART               |
| PARTSUPP           |
| REGION             |
| SUPPLIER           |
+--------------------+
8 rows in set (0.00 sec)
```

## Use example

First start the spark-shell in the spark deployment directory:

```
$ cd spark
$ bin/spark-shell
```

```scala
import org.apache.spark.sql.TiContext
val ti = new TiContext(spark)

// Mapping all TiDB tables from `TPCH_001` database as Spark SQL tables
ti.tidbMapDatabase("TPCH_001")
```

Then you can call Spark SQL directly:

```scala
scala> spark.sql("select count(*) from lineitem").show
```

The result is:

```
+--------+
|count(1)|
+--------+
|   60175|
+--------+
```

Now run a more complex Spark SQL:

```scala
scala> spark.sql(
      """select
        |   l_returnflag,
        |   l_linestatus,
        |   sum(l_quantity) as sum_qty,
        |   sum(l_extendedprice) as sum_base_price,
        |   sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
        |   sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
        |   avg(l_quantity) as avg_qty,
        |   avg(l_extendedprice) as avg_price,
        |   avg(l_discount) as avg_disc,
        |   count(*) as count_order
        |from
        |   lineitem
        |where
        |   l_shipdate <= date '1998-12-01' - interval '90' day
        |group by
        |   l_returnflag,
        |   l_linestatus
        |order by
        |   l_returnflag,
        |   l_linestatus
      """.stripMargin).show
```

The result is:

```
+------------+------------+---------+--------------+--------------+
|l_returnflag|l_linestatus|  sum_qty|sum_base_price|sum_disc_price|
+------------+------------+---------+--------------+--------------+
|           A|           F|380456.00|  532348211.65|505822441.4861|
|           N|           F|  8971.00|   12384801.37| 11798257.2080|
|           N|           O|742802.00| 1041502841.45|989737518.6346|
|           R|           F|381449.00|  534594445.35|507996454.4067|
+------------+------------+---------+--------------+--------------+
(Continued)
-----------------+---------+------------+--------+-----------+
       sum_charge|  avg_qty|   avg_price|avg_disc|count_order|
-----------------+---------+------------+--------+-----------+
 526165934.000839|25.575155|35785.709307|0.050081|      14876|
  12282485.056933|25.778736|35588.509684|0.047759|        348|
1029418531.523350|25.454988|35691.129209|0.049931|      29181|
 528524219.358903|25.597168|35874.006533|0.049828|      14902|
-----------------+---------+------------+--------+-----------+
```

See [more examples](https://github.com/ilovesoup/tpch/tree/master/sparksql).
