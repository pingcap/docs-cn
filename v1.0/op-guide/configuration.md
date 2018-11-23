---
title: Configuration Flags
category: operations
---

# Configuration Flags

TiDB, TiKV and PD are configurable using command-line flags and environment variables.

## TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### `--binlog-socket`

- The TiDB services use the unix socket file for internal connections, such as the PUMP service
- Default: ``
- You can use "/tmp/pump.sock" to accept the communication of PUMP unix socket file.

### `--cross-join`

- To enable (true) or disable (false) the cross join without any equal conditions
- Default: true
- The value can be `true` or `false`. By default, `true` is to enable `join` without any equal conditions (the `Where` field). If you set the value to `false`, the server refuses to run the `join` statement.

### `--host`

- The host address that the TiDB server monitors
- Default: "0.0.0.0"
- The TiDB server monitors this address.
- The "0.0.0.0" monitors all network cards. If you have multiple network cards, specify the network card that provides service, such as 192.168.100.113.

### `--join-concurrency int`

- The number of goroutine when `join-concurrency` executes `join` concurrently
- Default: 5
- The number depends on the amount of data and data distribution, usually the larger the better, and a larger number means a larger CPU overhead.

### `-L`

+ The log level
+ Default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### `--lease`

+ The schema lease time in seconds
+ Default: "10"
+ This is the schema lease time that is used in online schema changes. The value will affect the DDL statement running time. Do not change it unless you understand the internal mechanism.

### `--log-file`

+ The log file
+ Default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--metrics-addr`

+ The Prometheus pushgateway address
+ Default: ""
+ Leaving it empty stops the Prometheus client from pushing.
+ The format is:
    
    ```
    --metrics-addr=192.168.100.115:9091
    ```

### `--metrics-interval`

+ The Prometheus client push interval in seconds
+ Default: 0
+ Setting the value to 0 stops the Prometheus client from pushing.

### `-P`

+ The monitoring port of TiDB services
+ Default: "4000"
+ The TiDB server accepts MySQL client requests from this port.

### `--path`

- The path to the data directory for local storage engines like "goleveldb" and "BoltDB"
- Do not set `--path` for the "memory" storage engine.
- For the distributed storage engine like TiKV, `--path` specifies the actual PD address. Assuming that you deploy the PD server on 192.168.100.113:2379, 192.168.100.114:2379 and 192.168.100.115:2379, the value of `--path` is "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
- Default: "/tmp/tidb"

### `--perfschema`

+ To enable(true) or disable(false) the performance schema
+ Default: false
+ The value can be (true) or (false). (true) is to enable and (false) is to disable. The Performance Schema provides a way to inspect internal execution of the server at runtime. See [performance schema](http://dev.mysql.com/doc/refman/5.7/en/performance-schema.html) for more information. If you enable the performance schema, the performance is affected.

### `--privilege`

+ To enable(true) or disable(false) the privilege check(for debugging)
+ Default: true
+ The value can be (true) or (false). (true) is to enable and (false) is to disable. This option is deprecated and will be removed.

### `--proxy-protocol-networks`

+ The list of proxy server's IP addresses allowed by PROXY Protocol; if you need to configure multiple addresses, separate them using `,`
+ Default: "" (empty string)
+ Leaving it empty disables PROXY Protocol. The value can be the IP address (192.168.1.50) or CIDR (192.168.1.0/24). `*` means any IP addresses.

### `--proxy-protocol-header-timeout`

+ Timeout for the PROXY protocol header read
+ Default: 5 (seconds)
+ Generally use the default value and do not set its value to 0. The unit is second.

### `--query-log-max-len int`

- The maximum length of SQL statements recorded in the log
- Default: 2048
- Overlong requests are truncated when output to the log.

### `--report-status`

+ To enable(true) or disable(false) the status report and pprof tool
+ Default: true
+ The value can be (true) or (false). (true) is to enable metrics and pprof. (false) is to disable metrics and pprof.

### `--retry-limit int`

- The maximum number of retries when a transaction meets conflicts
- Default: 10
- A large number of retries affects the TiDB cluster performance.

### `--run-ddl`

- To see whether the `tidb-server` runs DDL statements, and set when the number of `tidb-server` is over two in the cluster
- Default: true
- The value can be (true) or (false). (true) indicates the `tidb-server` runs DDL itself. (false) indicates the `tidb-server` does not run DDL itself.

### `--skip-grant-table`

+ To enable anyone to connect without a password and with all privileges
+ Default: false
+ The value can be (true) or (false). This option is usually used to reset password, and enabling it requires the root privileges.

### `--slow-threshold int`

- The SQL statements with a larger value of this parameter are recorded.
- Default: 300
- The value can only be an integer (int), and the unit is millisecond.

### `--socket string`

+ The TiDB services use the unix socket file for external connections.
+ Default: ""
+ You can use "/tmp/tidb.sock" to open the unix socket file.

### `--ssl-ca`

+ The path to a file in PEM format that contains a list of trusted SSL certificate authorities.
+ Default: ""
+ When this option is specified along with `--ssl-cert` and `--ssl-key`, the server verifies the client's certificate via this CA list if the client provides its certificate accordingly.
+ The secure connection will be established without client verification if the client does not provide a certificate even when this option is set.

### `--ssl-cert`

+ The path to an SSL certificate file in PEM format to use for establishing a secure connection.
+ Default: ""
+ When this option is specified along with `--ssl-key`, the server permits but does not require secure connections.
+ If the specified certificate or key is not valid, the server still starts normally but does not permit secure connections.

### `--ssl-key`

+ The path to an SSL key file in PEM format to use for establishing a secure connection, namely the private key of the certificate you specified by `--ssl-cert`.
+ Default: ""
+ Currently TiDB does not support keys protected by a passphrase.

### `--status`

+ The status report port for TiDB server
+ Default: "10080"
+ This is used to get server internal data. The data includes [prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
+ Prometheus metrics can be got through "http://host:status_port/metrics".
+ Pprof data can be got through "http://host:status_port/debug/pprof".

### `--statsLease string`

- Scan the full table incrementally, and analyze information like the data amount and index of the table
- Default: 3s
- Before you use `--statsLease string`, run `analyze table name` manually. The statistics are updated automatically and stored in TiKV, taking up some memory.

### `--store` 

+ The storage engine type
+ Human-readable name for this member.
+ Default: "goleveldb"
+ You can choose from "memory", "goleveldb", "BoltDB" or "TiKV". The first three are all local storage engines. TiKV is a distributed storage engine.

### `--tcp-keep-alive`

- `keepalive` is enabled in the tcp layer of TiDB.
- Default: false

## Placement Driver (PD)

### `--advertise-client-urls`

+ The advertise URL list for client traffic from outside
+ Default: ${client-urls}
+ If the client cannot connect to PD through the default listening client URLs, you must manually set the advertise client URLs explicitly.
+ For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 2379:2379`. In this case, you can set `--advertise-client-urls` to "http://192.168.100.113:2379". The client can find this service through "http://192.168.100.113:2379".

### `--advertise-peer-urls`

+ The advertise URL list for peer traffic from outside
+ Default: ${peer-urls}
+ If the peer cannot connect to PD through the default listening peer URLs, you must manually set the advertise peer URLs explicitly.
+ For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 2380:2380`. In this case, you can set `--advertise-peer-urls` to "http://192.168.100.113:2380". The other PD nodes can find this service through "http://192.168.100.113:2380".

### `--client-urls`

+ The listening URL list for client traffic
+ Default: "http://127.0.0.1:2379"
+ To deploy a cluster, you must use `--client-urls` to specify the IP address of the current host, such as "http://192.168.100.113:2379". If the cluster is run on Docker, specify the IP address of Docker as "http://0.0.0.0:2379".

### `--config`

+ The config file
+ Default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### `--data-dir`

+ The path to the data directory
+ Default: "default.${name}"

### `--initial-cluster`

+ The initial cluster configuration for bootstrapping
+ Default: "{name}=http://{advertise-peer-url}"
+ For example, if `name` is "pd", and `advertise-peer-urls` is "http://192.168.100.113:2380", the `initial-cluster` is "pd=http://192.168.100.113:2380".
+ If you need to start three PD servers, the `initial-cluster` might be:
  
    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

### `--join`

+ Join the cluster dynamically
+ Default: ""
+ If you want to join an existing cluster, you can use `--join="${advertise-client-urls}"`, the `advertise-client-url` is any existing PD's, multiply advertise client urls are separated by comma.

### `-L`

+ The log level
+ Default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### `--log-file`

+ The log file
+ Default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--log-rotate`

- To enable or disable log rotation
- Default: true
- When the value is true, follow the `[log.file]` in PD configuration files.

### `--name`

+ The human-readable unique name for this PD member
+ Default: "pd"
+ If you want to start multiply PDs, you must use different name for each one.

### `--peer-urls`

+ The listening URL list for peer traffic
+ Default: "http://127.0.0.1:2380"
+ To deploy a cluster, you must use `--peer-urls` to specify the IP address of the current host, such as "http://192.168.100.113:2380". If the cluster is run on Docker, specify the IP address of Docker as "http://0.0.0.0:2380".

## TiKV

TiKV supports some readable unit conversions for command line parameters.

- File size (based on byte): KB, MB, GB, TB, PB (or lowercase)
- Time (based on ms): ms, s, m, h

### `-A, --addr`

+ The address that the TiKV server monitors
+ Default: "127.0.0.1:20160"
+ To deploy a cluster, you must use `--addr` to specify the IP address of the current host, such as "192.168.100.113:20160". If the cluster is run on Docker, specify the IP address of Docker as "0.0.0.0:20160".

### `--advertise-addr`

+ The server advertise address for client traffic from outside
+ Default: ${addr}
+ If the client cannot connect to TiKV through the default monitoring address because of Docker or NAT network, you must manually set the advertise address explicitly.
+ For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 20160:20160`. In this case, you can set `--advertise-addr` to "192.168.100.113:20160". The client can find this service through 192.168.100.113:20160.

### `-C, --config`

+ The config file
+ Default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### `--capacity`

+ The store capacity
+ Default: 0 (unlimited)
+ PD uses this flag to determine how to balance the TiKV servers. (Tip: you can use 10GB instead of 1073741824)

### `--data-dir`

+ The path to the data directory
+ Default: "/tmp/tikv/store"

### `-L, --Log`

+ The log level
+ Default: "info"
+ You can choose from trace, debug, info, warn, error, or off.

### `--log-file`

+ The log file
+ Default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--pd`

- The address list of PD servers
- Default: ""
- To make TiKV work, you must use the value of `--pd` to connect the TiKV server to the PD server. Separate multiple PD addresses using comma, for example "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
