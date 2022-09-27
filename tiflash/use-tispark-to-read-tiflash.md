---
title: Use TiSpark to Read TiFlash Replicas
summary: Learn how to use TiSpark to read TiFlash replicas.
---

# Use TiSpark to Read TiFlash Replicas

This document introduces how to use TiSpark to read TiFlash replicas.

Currently, you can use TiSpark to read TiFlash replicas in a method similar to the engine isolation in TiDB. This method is to configure the `spark.tispark.isolation_read_engines` parameter. The parameter value defaults to `tikv,tiflash`, which means that TiDB reads data from TiFlash or from TiKV according to CBO's selection. If you set the parameter value to `tiflash`, it means that TiDB forcibly reads data from TiFlash.

> **Note:**
>
> When this parameter is set to `tiflash`, only the TiFlash replicas of all tables involved in the query are read and these tables must have TiFlash replicas; for tables that do not have TiFlash replicas, an error is reported. When this parameter is set to `tikv`, only the TiKV replica is read.

You can configure this parameter in one of the following ways:

* Add the following item in the `spark-defaults.conf` file:

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

* Add `--conf spark.tispark.isolation_read_engines=tiflash` in the initialization command when initializing Spark shell or Thrift server.

* Set `spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")` in Spark shell in a real-time manner.

* Set `set spark.tispark.isolation_read_engines=tiflash` in Thrift server after the server is connected via beeline.
