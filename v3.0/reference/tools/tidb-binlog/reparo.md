---
title: Reparo User Guide
summary: Learn to use Reparo.
category: reference
aliases: ['/docs/tools/binlog/reparo/']
---

# Reparo User Guide

Reparo is a TiDB-Binlog tool, used to recover the incremental data. To back up the incremental data, you can use Drainer of TiDB-Binlog to output the binlog data in the protobuf format to files. To restore the incremental data, you can use Reparo to parse the binlog data in the files and apply the binlog in TiDB/MySQL.

Download Reparo via [tidb-binlog-cluster-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-binlog-cluster-latest-linux-amd64.tar.gz)

## Reparo usage

### Description of command line parameters

```
Usage of Reparo:
-L string
    The level of the output information of logs
    Value: "debug"/"info"/"warn"/"error"/"fatal" ("info" by default)
-V Prints the version.
-config string
    The path of the configuration file
    If the configuration file is specified, Reparo reads the configuration data in this file.
    If the configuration data also exists in the command line parameters, Reparo uses the configuration data in the command line parameters to cover that in the configuration file.
-data-dir string
    The storage directory for the binlog file in the protobuf format that Drainer outputs ("data.drainer" by default)
-dest-type string
    The downstream service type
    Value: "print"/"mysql" ("print" by default)
    If it is set to "print", the data is parsed and printed to standard output while the SQL statement is not executed.
    If it is set to "mysql", you need to configure the "host", "port", "user" and "password" information in the configuration file.
-log-file string
    The path of the log file
-log-rotate string
    The switch frequency of log files
    Value: "hour"/"day"
-start-datetime string
    Specifies the time point for starting recovery.
    Format: "2006-01-02 15:04:05"
    If it is not set, the recovery process starts from the earliest binlog file.
-stop-datetime string
    Specifies the time point of finishing the recovery process.
    Format: "2006-01-02 15:04:05"
    If it is not set, the recovery process ends up with the last binlog file.
```

### Description of the configuration file

```toml
# The storage directory for the binlog file in the protobuf format that Drainer outputs
data-dir = "./data.drainer"

# Uses the index file to locate `ts`. Set this parameter if `start-ts` is set. The file
# directory is {data-dir}/{index-name}.
# index-name = "binlog.index"
# log-file = ""
# log-rotate = "hour"

# The level of the output information of logs
# Value: "debug"/"info"/"warn"/"error"/"fatal" ("info" by default)
log-level = "info"

# Uses `start-datetime` and `stop-datetime` to specify the time range in which
# the binlog files are to be recovered.
# Format: "2006-01-02 15:04:05"
# start-datetime = ""
# stop-datetime = ""

# Correspond to `start-datetime` and `stop-datetime` respectively.
# They are used to specify the time range in which the binlog files are to be recovered.
# If `start-datetime` and `stop-datetime` are set, there is no need to set `start-tso` and `stop-tso`.
# start-tso = 0
# stop-tso = 0

# The downstream service type
# Value: "print"/"mysql" ("print" by default)
# If it is set to "print", the data is parsed and printed to standard output
# while the SQL statement is not executed.
# If it is set to "mysql", you need to configure `host`, `port`, `user` and `password` in [dest-db].
dest-type = "mysql"

# `replicate-do-db` and `replicate-do-table` specify the database and table to be recovered.
# `replicate-do-db` has priority over `replicate-do-table`.
# You can use a regular expression for configuration. The regular expression should start with "~".
# The configuration method for `replicate-do-db` and `replicate-do-table` is
# the same with that for `replicate-do-db` and `replicate-do-table` of Drainer.
# replicate-do-db = ["~^b.*","s1"]
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "log"
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# If `dest-type` is set to `mysql`, `dest-db` needs to be configured.
[dest-db]
host = "127.0.0.1"
port = 3309
user = "root"
password = ""
```

### Start example

```
./bin/reparo -config reparo.toml
```

> **Note:**
>
> * `data-dir` specifies the directory for the binlog file that Drainer outputs.
> * Both `start-datatime` and `start-tso` are used to specify the time point for starting recovery, but they are different in the time format. If they are not set, the recovery process starts from the earliest binlog file by default.
> * Both `stop-datetime` and `stop-tso` are used to specify the time point for finishing recovery, but they are different in the time format. If they are not set, the recovery process ends up with the last binlog file by default.
> * `dest-type` specifies the destination type. Its value can be "mysql" and "print."
>
>     * When it is set to `mysql`, the data can be recovered to MySQL or TiDB that uses or is compatible with the MySQL protocol. In this case, you need to specify the database information in `[dest-db]` of the configuration information.
>     * When it is set to `print`, only the binlog information is printed. It is generally used for debugging and checking the binlog information. In this case, there is no need to specify `[dest-db]`.
>
> * `replicate-do-db` specifies the database for recovery. If it is not set, all the databases are to be recovered.
> * `replicate-do-table` specifies the table for recovery. If it is not set, all the tables are to be recovered.
