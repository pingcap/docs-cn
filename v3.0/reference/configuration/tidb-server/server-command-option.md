---
title: The TiDB Command Options
summary: Learn about TiDB command options and configuration files.
category: user guide
aliases: ['/docs/sql/server-command-option/']
---

# The TiDB Command Options

This document describes the startup options and TiDB server configuration files.

## TiDB startup options

When you start TiDB processes, you can specify some program options.

TiDB supports a lot of startup options. Run the following command to get a brief introduction:

```
./tidb-server --help
```

Run the following command to get the version:

```
./tidb-server -V
```

The complete descriptions of startup options are as follows.

### -L

- Log level
- Default: "info"
- Optional values: debug, info, warn, error or fatal

### -P

- TiDB service monitor port
- Default: "4000"
- TiDB uses this port to accept requests from the MySQL client

### \-\-binlog-socket

- TiDB uses the unix socket file to accept the internal connection, such as the PUMP service.
- Default: ""
- For example, use "/tmp/pump.sock" to accept the PUMP unix socket file communication.

### \-\-config

- TiDB configuration files
- Default: ""
- The file path of the configuration files 

### \-\-lease

- The lease time of schema; unit: second
- Default: "10"
- The lease of schema is mainly used in online schema changes. This value affects the actual execution time of the DDL statement. In most cases, you do not need to change this value unless you clearly understand the internal implementation mechanism of TiDB DDL.

### \-\-host

- TiDB service monitor host
- Default: "0.0.0.0"
- TiDB service monitors this host.
- The 0.0.0.0 port monitors the address of all network cards. You can specify the network card that provides external service, such as 192.168.100.113.

### \-\-log-file

- Log file
- Default: ""
- If the option is not set, the log is output to "stderr"; if set, the log is output to the corresponding file. In the small hours of every day, the log automatically rotates to use a new file, renames and backups the previous file. 

### \-\-metrics-addr

- The address of Prometheus Push Gateway
- Default: ""
- If the option value is null, TiDB does not push the statistics to Push Gateway. The option format is like `--metrics-addr=192.168.100.115:9091`.

### \-\-metrics-intervel

- The time interval that the statistics are pushed to Prometheus Push Gateway
- Default: 15s
- If you set the option value to 0, the statistics are not pushed to Push Gateway. `--metrics-interval=2` means the statistics are pushed to Push Gateway every two seconds.

### \-\-path

- For the local storage engines such as "goleveldb" or "BoltDB", `path` specifies the actual data storage path.
- For the "memory" storage engine, it is not necessary to set `path`.
- For the "TiKV" storage engine, `path` specifies the actual PD address. For example, if the PD is deployed on 192.168.100.113:2379, 192.168.100.114:2379 and 192.168.100.115:2379, the `path` is "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".

### \-\-report-status

- Enable (true) or disable (false) the status monitor port
- Default: true
- The value is either true or false. The `true` value means opening the status monitor port. The `false` value means closing the status monitor port. The status monitor port is used to report some internal service information to the external.

### \-\-run-ddl

- Whether the TiDB server runs DDL statements; set the option when more than two TiDB servers are in the cluster
- Default: true
- The value is either true or false. The `true` value means the TiDB server runs DDL statements. The `false` value means the TiDB server does not run DDL statements.

### \-\-socket string

- TiDB uses the unix socket file to accept the external connection.
- Default: ""
- For example, use "/tmp/tidb.sock" to open the unix socket file.

### \-\-status

- The status monitor port of TiDB
- Default: "10080"
- This port is used to display the internal data of TiDB, including the [Prometheus statistics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
- Access the Prometheus statistics at http://host:status_port/metrics.
- Access the pprof data at http://host:status_port/debug/pprof.

### \-\-store

- To specify the storage engine used by the bottom layer of TiDB
- Default: "mocktikv"
- Optional values: "memory", "goleveldb", "boltdb", "mocktikv" or "tikv" (TiKV is a distributed storage engine, while the others are local storage engines)
- For example, use `tidb-server --store=memory` to start a TiDB server with a pure memory engine

## TiDB server configuration files

When you start the TiDB server, you can specify the server's configuration file using `--config path`. For overlapped options in configuration, the priority of command options is higher than configuration files.

See [an example of the configuration file](https://github.com/pingcap/tidb/blob/master/config/config.toml.example).

The complete descriptions of startup options are as follows.

### host

Same as the "host" startup option

### port

Same as the "P" startup option

### path

Same as the "path" startup option

### socket

Same as the "socket" startup option

### binlog-socket

Same as the "binlog-socket" startup option

### run-ddl

Same as the "run-ddl" startup option

### cross-join

- Default: true
- When you execute `join` on tables without any conditions on both sides, the statement can be run by default. But if you set the value to `false`, the server does not run such `join` statement. 

### force-priority

- The default priority for statements
- Default: `NO_PRIORITY`
- TiDB supports the priorities `NO_PRIORITY` | `LOW_PRIORITY` | `DELAYED` | `HIGH_PRIORITY` for statements. One use case for changing the priority, is you may choose to dedicate a pool of servers for OLAP queries and set the value to `LOW_PRIORITY` to ensure that TiKV servers will provide priority to OLTP workloads which are routed to a different pool of TiDB servers. This helps ensure more uniform OLTP performance at the risk of slightly slower OLAP performance.
  
TiDB will automatically set table scans to `LOW_PRIORITY` and overwriting priority on a per-statement basis is possible by using the `HIGH PRIORITY` or `LOW PRIORITY` DML modifier.

### join-concurrency

- The goroutine number when the `join-concurrency` runs `join`
- Default: 5
- To view the amount of data and data distribution; generally the more the better; a larger value indicates a larger CPU is needed

### query-log-max-len

- To record the maximum length of SQL statements in the log
- Default: 2048
- The overlong request is truncated when it is output to the log

### slow-threshold int

- To record the SQL statement that has a larger value than this option
- Default: 300
- It is required that the value is an integer (int); unit: millisecond

### slow-query-file

- The slow query log file
- Default: ""
- The value is the file name. If a non-null string is specified, the slow query log is redirected to the corresponding file. 

### retry-limit

- The maximum number of commit retries when the transaction meets a conflict
- Default: 10
- Setting a large number of retries can affect the performance of the TiDB cluster

### skip-grant-table

- Allow anyone to connect without a password, and all operations do not check privileges
- Default: false
- The value is either true or false. The machine's root privilege is required to enable this option, which is used to reset the password when forgotten.

### stats-lease

- Scan the full table incrementally, and analyze the data amount and indexes of the table
- Default: "3s"
- To use this option, you need to manually run `analyze table name`. Update the statistics automatically and store data in TiKV persistently, taking up some memory.

### tcp-keep-alive

- To Enable keepalive in the tcp layer of TiDB
- Default: false

### ssl-cert

- The file path of SSL certificate in PEM format
- Default: ""
- If this option and the `--ssl-key` option are set at the same time, the client can (not required) securely connect to TiDB using TLS.
- If the specified certificate or private key is invalid, TiDB starts as usual but does not support encrypted connections.

### ssl-key

- The file path of SSL certificate keys in PEM format, or the private keys specified by `--ssl-cert`
- Default: ""
- Currently, you cannot load a password-protected private key in TiDB.

### ssl-ca

- The file path of the trusted CA certificate in PEM format
- Default: ""
- If this option and the `--ssl-cert`, `--ssl-key` options are set at the same time, TiDB authenticates the client certificate based on the trusted CA list specified by the option when the client presents the certificate. If the authentication fails, the connection stops.
- If this option is set but the client does not present the certificate, the encrypted connection continues but the client certificate is not authenticated.
