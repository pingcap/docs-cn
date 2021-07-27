---
title: TiDB Binlog Cluster Deployment
summary: Learn how to deploy TiDB Binlog cluster.
aliases: ['/docs/dev/tidb-binlog/deploy-tidb-binlog/','/docs/dev/reference/tidb-binlog/deploy/','/docs/dev/how-to/deploy/tidb-binlog/']
---

# TiDB Binlog Cluster Deployment

This document describes how to [deploy TiDB Binlog using a Binary package](#deploy-tidb-binlog-using-a-binary-package).

## Hardware requirements

Pump and Drainer are deployed and operate on 64-bit universal hardware server platforms with Intel x86-64 architecture.

In environments of development, testing and production, the requirements on server hardware are as follows:

| Service     | The Number of Servers       | CPU   | Disk          | Memory   |
| :-------- | :-------- | :-------- | :--------------- | :------ |
| Pump | 3 | 8 core+    | SSD, 200 GB+ | 16G |
| Drainer | 1 | 8 core+ | SAS, 100 GB+ (If binlogs are output as local files, the disk size depends on how long these files are retained.) | 16G |

## Deploy TiDB Binlog using a Binary package

### Download the official Binary package

Run the following commands to download the packages:

{{< copyable "shell-regular" >}}

```bash
version="latest" for nightly builds &&
wget https://download.pingcap.org/tidb-latest-linux-amd64.{tar.gz,sha256}
```

Check the file integrity. If the result is OK, the file is correct.

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-latest-linux-amd64.sha256
```

For TiDB v2.1.0 GA or later versions, Pump and Drainer are already included in the TiDB download package. For other TiDB versions, you need to download Pump and Drainer separately using the following command:

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-binlog-$version-linux-amd64.{tar.gz,sha256}
```

Check the file integrity. If the result is OK, the file is correct.

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-binlog-$version-linux-amd64.sha256
```

### The usage example

Assuming that you have three PD nodes, one TiDB node, two Pump nodes, and one Drainer node, the information of each node is as follows:

| Node     | IP           |
| :---------|:------------ |
| TiDB     | 192.168.0.10 |
| PD1      | 192.168.0.16 |
| PD2      | 192.168.0.15 |
| PD3      | 192.168.0.14 |
| Pump     | 192.168.0.11 |
| Pump     | 192.168.0.12 |
| Drainer  | 192.168.0.13 |

The following part shows how to use Pump and Drainer based on the nodes above.

1. Deploy Pump using the binary.

    - To view the command line parameters of Pump, execute `./bin/pump -help`:

        ```bash
        Usage of Pump:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the RPC address through which Pump provides the service (-addr="192.168.0.11:8250")
        -advertise-addr string
            the RPC address through which Pump provides the external service (-advertise-addr="192.168.0.11:8250")
        -config string
            the path of the configuration file. If you specify the configuration file, Pump reads the configuration in the configuration file first. If the corresponding configuration also exits in the command line parameters, Pump uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the path where the Pump data is stored
        -gc int
            the number of days to retain the data in Pump ("7" by default)
        -heartbeat-interval int
            the interval of the heartbeats Pump sends to PD (in seconds)
        -log-file string
            the file path of logs
        -log-rotate string
            the switch frequency of logs (hour/day)
        -metrics-addr string
            the Prometheus Pushgateway address. If not set, it is forbidden to report the monitoring metrics.
        -metrics-interval int
            the report frequency of the monitoring metrics ("15" by default, in seconds)
        -node-id string
            the unique ID of a Pump node. If you do not specify this ID, the system automatically generates an ID based on the host name and listening port.
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -fake-binlog-interval int
            the frequency at which a Pump node generates fake binlog ("3" by default, in seconds)
        ```

    - Taking deploying Pump on "192.168.0.11" as an example, the Pump configuration file is as follows:

        ```toml
        # Pump Configuration

        # the bound address of Pump
        addr = "192.168.0.11:8250"

        # the address through which Pump provides the service
        advertise-addr = "192.168.0.11:8250"

        # the number of days to retain the data in Pump ("7" by default)
        gc = 7

        # the directory where the Pump data is stored
        data-dir = "data.pump"

        # the interval of the heartbeats Pump sends to PD (in seconds)
        heartbeat-interval = 2

        # the address of the PD cluster nodes (each separated by a comma with no whitespace)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # [security]
        # This section is generally commented out if no special security settings are required.
        # The file path containing a list of trusted SSL CAs connected to the cluster.
        # ssl-ca = "/path/to/ca.pem"
        # The path to the X509 certificate in PEM format that is connected to the cluster.
        # ssl-cert = "/path/to/drainer.pem"
        # The path to the X509 key in PEM format that is connected to the cluster.
        # ssl-key = "/path/to/drainer-key.pem"

        # [storage]
        # Set to true (by default) to guarantee reliability by ensuring binlog data is flushed to the disk
        # sync-log = true

        # When the available disk capacity is less than the set value, Pump stops writing data.
        # 42 MB -> 42000000, 42 mib -> 44040192
        # default: 10 gib
        # stop-write-at-available-space = "10 gib"
        # The LSM DB settings embedded in Pump. Unless you know this part well, it is usually commented out.
        # [storage.kv]
        # block-cache-capacity = 8388608
        # block-restart-interval = 16
        # block-size = 4096
        # compaction-L0-trigger = 8
        # compaction-table-size = 67108864
        # compaction-total-size = 536870912
        # compaction-total-size-multiplier = 8.0
        # write-buffer = 67108864
        # write-L0-pause-trigger = 24
        # write-L0-slowdown-trigger = 17
        ```

    - The example of starting Pump:

        {{< copyable "shell-regular" >}}

        ```bash
        ./bin/pump -config pump.toml
        ```

        If the command line parameters is the same with the configuration file parameters, the values of command line parameters are used.

2. Deploy Drainer using binary.

    - To view the command line parameters of Drainer, execute `./bin/drainer -help`:

        ```bash
        Usage of Drainer:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the address through which Drainer provides the service (-addr="192.168.0.13:8249")
        -c int
            the number of the concurrency of the downstream for replication. The bigger the value, the better throughput performance of the concurrency ("1" by default).
        -cache-binlog-count int
            the limit on the number of binlog items in the cache ("8" by default)
            If a large single binlog item in the upstream causes OOM in Drainer, try to lower the value of this parameter to reduce memory usage.
        -config string
            the directory of the configuration file. Drainer reads the configuration file first.
            If the corresponding configuration exists in the command line parameters, Drainer uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the directory where the Drainer data is stored ("data.drainer" by default)
        -dest-db-type string
            the downstream service type of Drainer
            The value can be "mysql", "tidb", "kafka", and "file". ("mysql" by default)
        -detect-interval int
            the interval of checking the online Pump in PD ("10" by default, in seconds)
        -disable-detect
            whether to disable the conflict monitoring
        -disable-dispatch
            whether to disable the SQL feature of splitting a single binlog file. If it is set to "true", each binlog file is restored to a single transaction for replication based on the order of binlogs.
            It is set to "False", when the downstream is MySQL.
        -ignore-schemas string
            the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
            It does not support the Rename DDL operation on tables of `ignore schemas`.
        -initial-commit-ts
            If Drainer does not have the related breakpoint information, you can configure the related breakpoint information using this parameter. ("-1" by default)
            If the value of this parameter is `-1`, Drainer automatically obtains the latest timestamp from PD.
        -log-file string
            the path of the log file
        -log-rotate string
            the switch frequency of log files, hour/day
        -metrics-addr string
            the Prometheus Pushgateway address
            It it is not set, the monitoring metrics are not reported.
        -metrics-interval int
            the report frequency of the monitoring metrics ("15" by default, in seconds)
        -node-id string
            the unique ID of a Drainer node. If you do not specify this ID, the system automatically generates an ID based on the host name and listening port.
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -safe-mode
            Whether to enable safe mode so that data can be written into the downstream MySQL/TiDB repeatedly.
            This mode replaces the `INSERT` statement with the `REPLACE` statement and splits the `UPDATE` statement into `DELETE` plus `REPLACE`.
        -txn-batch int
            the number of SQL statements of a transaction which are output to the downstream database ("1" by default)
        ```

    - Taking deploying Drainer on "192.168.0.13" as an example, the Drainer configuration file is as follows:

        ```toml
        # Drainer Configuration.

        # the address through which Drainer provides the service ("192.168.0.13:8249")
        addr = "192.168.0.13:8249"

        # the address through which Drainer provides the external service
        advertise-addr = "192.168.0.13:8249"

        # the interval of checking the online Pump in PD ("10" by default, in seconds)
        detect-interval = 10

        # the directory where the Drainer data is stored "data.drainer" by default)
        data-dir = "data.drainer"

        # the address of the PD cluster nodes (each separated by a comma with no whitespace)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # the directory of the log file
        log-file = "drainer.log"

        # Drainer compresses the data when it gets the binlog from Pump. The value can be "gzip". If it is not configured, it will not be compressed
        # compressor = "gzip"

        # [security]
        # This section is generally commented out if no special security settings are required.
        # The file path containing a list of trusted SSL CAs connected to the cluster.
        # ssl-ca = "/path/to/ca.pem"
        # The path to the X509 certificate in PEM format that is connected to the cluster.
        # ssl-cert = "/path/to/pump.pem"
        # The path to the X509 key in PEM format that is connected to the cluster.
        # ssl-key = "/path/to/pump-key.pem"

        # Syncer Configuration
        [syncer]
        # If the item is set, the sql-mode will be used to parse the DDL statement.
        # If the downstream database is MySQL or TiDB, then the downstream sql-mode
        # is also set to this value.
        # sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

        # the number of SQL statements of a transaction that are output to the downstream database ("20" by default)
        txn-batch = 20

        # the number of the concurrency of the downstream for replication. The bigger the value,
        # the better throughput performance of the concurrency ("16" by default)
        worker-count = 16

        # whether to disable the SQL feature of splitting a single binlog file. If it is set to "true",
        # each binlog file is restored to a single transaction for replication based on the order of binlogs.
        # If the downstream service is MySQL, set it to "False".
        disable-dispatch = false

        # In safe mode, data can be written into the downstream MySQL/TiDB repeatedly.
        # This mode replaces the `INSERT` statement with the `REPLACE` statement and replaces the `UPDATE` statement with `DELETE` plus `REPLACE` statements.
        safe-mode = false

        # the downstream service type of Drainer ("mysql" by default)
        # Valid value: "mysql", "tidb", "file", and "kafka".
        db-type = "mysql"

        # If `commit ts` of the transaction is in the list, the transaction is filtered and not replicated to the downstream.
        ignore-txn-commit-ts = []

        # the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
        # Does not support the Rename DDL operation on tables of `ignore schemas`.
        ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

        # `replicate-do-db` has priority over `replicate-do-table`. When they have the same `db` name,
        # regular expressions are supported for configuration.
        # The regular expression should start with "~".

        # replicate-do-db = ["~^b.*","s1"]

        # [syncer.relay]
        # It saves the directory of the relay log. The relay log is not enabled if the value is empty.
        # The configuration only comes to effect if the downstream is TiDB or MySQL.
        # log-dir = ""
        # the maximum size of each file
        # max-file-size = 10485760

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "log"

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "~^a.*"

        # Ignore the replication of some tables
        # [[syncer.ignore-table]]
        # db-name = "test"
        # tbl-name = "log"

        # the server parameters of the downstream database when `db-type` is set to "mysql"
        [syncer.to]
        host = "192.168.0.13"
        user = "root"
        # If you do not want to set a cleartext `password` in the configuration file, you can create `encrypted_password` using `./binlogctl -cmd encrypt -text string`.
        # When you have created an `encrypted_password` that is not empty, the `password` above will be ignored, because `encrypted_password` and `password` cannot take effect at the same time.
        password = ""
        encrypted_password = ""
        port = 3306

        [syncer.to.checkpoint]
        # When the checkpoint type is "mysql" or "tidb", this option can be
        # enabled to change the database that saves the checkpoint
        # schema = "tidb_binlog"
        # Currently only the "mysql" and "tidb" checkpoint types are supported
        # You can remove the comment tag to control where to save the checkpoint
        # The default method of saving the checkpoint for the downstream db-type:
        # mysql/tidb -> in the downstream MySQL or TiDB database
        # file/kafka -> file in `data-dir`
        # type = "mysql"
        # host = "127.0.0.1"
        # user = "root"
        # password = ""
        # `encrypted_password` is encrypted using `./binlogctl -cmd encrypt -text string`.
        # When `encrypted_password` is not empty, the `password` above will be ignored.
        # encrypted_password = ""
        # port = 3306

        # the directory where the binlog file is stored when `db-type` is set to `file`
        # [syncer.to]
        # dir = "data.drainer"

        # the Kafka configuration when `db-type` is set to "kafka"
        # [syncer.to]
        # only one of kafka-addrs and zookeeper-addrs is needed. If both are present, the program gives priority
        # to the kafka address in zookeeper
        # zookeeper-addrs = "127.0.0.1:2181"
        # kafka-addrs = "127.0.0.1:9092"
        # kafka-version = "0.8.2.0"
        # kafka-max-messages = 1024

        # the topic name of the Kafka cluster that saves the binlog data. The default value is <cluster-id>_obinlog
        # To run multiple Drainers to replicate data to the same Kafka cluster, you need to set different `topic-name`s for each Drainer.
        # topic-name = ""
        ```

    - Starting Drainer:

        > **Note:**
        >
        > If the downstream is MySQL/TiDB, to guarantee the data integrity, you need to obtain the `initial-commit-ts` value and make a full backup of the data and restore the data before the initial start of Drainer.

        When Drainer is started for the first time, use the `initial-commit-ts` parameter.

        {{< copyable "shell-regular" >}}

        ```bash
        ./bin/drainer -config drainer.toml -initial-commit-ts {initial-commit-ts}
        ```

        If the command line parameter and the configuration file parameter are the same, the parameter value in the command line is used.

3. Starting TiDB server:

    - After starting Pump and Drainer, start TiDB server with binlog enabled by adding this section to your config file for TiDB server:

        ```
        [binlog]
        enable=true
        ```

    - TiDB server will obtain the addresses of registered Pumps from PD and will stream data to all of them. If there are no registered Pump instances, TiDB server will refuse to start or will block starting until a Pump instance comes online.

> **Note:**
>
> - When TiDB is running, you need to guarantee that at least one Pump is running normally.
> - To enable the TiDB Binlog service in TiDB server, use the `-enable-binlog` startup parameter in TiDB, or add enable=true to the [binlog] section of the TiDB server configuration file.
> - Make sure that the TiDB Binlog service is enabled in all TiDB instances in a same cluster, otherwise upstream and downstream data inconsistency might occur during data replication. If you want to temporarily run a TiDB instance where the TiDB Binlog service is not enabled, set `run_ddl=false` in the TiDB configuration file.
> - Drainer does not support the `rename` DDL operation on the table of `ignore schemas` (the schemas in the filter list).
> - If you want to start Drainer in an existing TiDB cluster, generally you need to make a full backup of the cluster data, obtain **snapshot timestamp**, import the data to the target database, and then start Drainer to replicate the incremental data from the corresponding **snapshot timestamp**.
> - When the downstream database is TiDB or MySQL, ensure that the `sql_mode` in the upstream and downstream databases are consistent. In other words, the `sql_mode` should be the same when each SQL statement is executed in the upstream and replicated to the downstream. You can execute the `select @@sql_mode;` statement in the upstream and downstream respectively to compare `sql_mode`.
> - When a DDL statement is supported in the upstream but incompatible with the downstream, Drainer fails to replicate data. An example is to replicate the `CREATE TABLE t1(a INT) ROW_FORMAT=FIXED;` statement when the downstream database MySQL uses the InnoDB engine. In this case, you can configure [skipping transactions](/tidb-binlog/tidb-binlog-faq.md#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database) in Drainer, and manually execute compatible statements in the downstream database.
