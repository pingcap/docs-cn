---
title: Configuration Flags
summary: Learn some configuration flags of TiDB, TiKV and PD.
category: operations
---

# Configuration Flags

TiDB, TiKV and PD are configurable using command-line flags and environment variables.

## TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### `--advertise-address`

- The IP address on which to advertise the apiserver to the TiDB server
- Default: ""
- This address must be reachable by the rest of the TiDB cluster and the user.

### `--binlog-socket`

- The TiDB services use the unix socket file for internal connections, such as the Pump service
- Default: ""
- You can use "/tmp/pump.sock" to accept the communication of Pump unix socket file.

### `--config`

- The configuration file
- Default: ""
- If you have specified the configuration file, TiDB reads the configuration file. If the corresponding configuration also exists in the command line flags, TiDB uses the configuration in the command line flags to overwrite that in the configuration file. For detailed configuration information, see [TiDB Configuration File Description](../op-guide/tidb-config-file.md)

### `--host`

- The host address that the TiDB server monitors
- Default: "0.0.0.0"
- The TiDB server monitors this address.
- The "0.0.0.0" monitors all network cards by default. If you have multiple network cards, specify the network card that provides service, such as 192.168.100.113.

### `-L`

- The log level
- Default: "info"
- You can choose from "debug", "info", "warn", "error", or "fatal".

### `--log-file`

- The log file
- Default: ""
- If this flag is not set, logs are output to "stderr". If this flag is set, logs are output to the corresponding file, which is automatically rotated in the early morning every day, and the previous file is renamed as a backup.

### `--log-slow-query`

- The directory for the slow query log
- Default: ""
- If this flag is not set, logs are written to the file specified by `--log-file` by default.

### `--metrics-addr`

- The Prometheus Pushgateway address
- Default: ""
- Leaving it empty stops the Prometheus client from pushing.
- The format is:

    ```
    --metrics-addr=192.168.100.115:9091
    ```

### `--metrics-interval`

- The Prometheus client push interval in seconds
- Default: 15s
- Setting the value to 0 stops the Prometheus client from pushing.

### `-P`

- The monitoring port of TiDB services
- Default: "4000"
- The TiDB server accepts MySQL client requests from this port.

### `--path`

- The path to the data directory for local storage engine like "mocktikv"
- For `--store = tikv`, you must specify the path; for `--store = mocktikv`, the default value is used if you do not specify the path.
- For the distributed storage engine like TiKV, `--path` specifies the actual PD address. Assuming that you deploy the PD server on 192.168.100.113:2379, 192.168.100.114:2379 and 192.168.100.115:2379, the value of `--path` is "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
- Default: "/tmp/tidb"
- You can use `tidb-server --store=mocktikv --path=""` to enable a pure in-memory TiDB.

### `--proxy-protocol-networks`

- The list of proxy server's IP addresses allowed by PROXY Protocol; if you need to configure multiple addresses, separate them using ",".
- Default: ""
- Leaving it empty disables PROXY Protocol. The value can be the IP address (192.168.1.50) or CIDR (192.168.1.0/24). "*" means any IP addresses.

### `--proxy-protocol-header-timeout`

- Timeout for the PROXY protocol header read
- Default: 5 (seconds)
- Generally use the default value and do not set its value to 0. The unit is second.

### `--report-status`

- To enable(true) or disable(false) the status report and pprof tool
- Default: true
- The value can be (true) or (false). (true) is to enable metrics and pprof. (false) is to disable metrics and pprof.

### `--run-ddl`

- To see whether the `tidb-server` runs DDL statements, and set when the number of `tidb-server` is over two in the cluster
- Default: true
- The value can be (true) or (false). (true) indicates the `tidb-server` runs DDL itself. (false) indicates the `tidb-server` does not run DDL itself.

### `--socket string`

- The TiDB services use the unix socket file for external connections.
- Default: ""
- You can use “/tmp/tidb.sock” to open the unix socket file.

### `--status`

- The status report port for TiDB server
- Default: "10080"
- This is used to get server internal data. The data includes [Prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
- Prometheus metrics can be got through "http://host:status_port/metrics".
- Pprof data can be got through "http://host:status_port/debug/pprof".

### `--store`

- To specify the storage engine used by TiDB in the bottom layer
- Default: "mocktikv"
- You can choose "mocktikv" or "tikv". ("mocktikv" is the local storage engine; "tikv" is a distributed storage engine)

### `--token-limit`

- The number of sessions allowed to run concurrently in TiDB. It is used for traffic control.
- Default: 1000
- If the number of the concurrent sessions is larger than `token-limit`, the request is blocked and waiting for the operations which have been finished to 
release tokens.

### `-V`

- Output the version of TiDB
- Default: ""

## Placement Driver (PD)

### `--advertise-client-urls`

- The advertise URL list for client traffic from outside
- Default: ${client-urls}
- If the client cannot connect to PD through the default listening client URLs, you must manually set the advertise client URLs explicitly.
- For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 2379:2379`. In this case, you can set `--advertise-client-urls` to "http://192.168.100.113:2379". The client can find this service through "http://192.168.100.113:2379".

### `--advertise-peer-urls`

- The advertise URL list for peer traffic from outside
- Default: ${peer-urls}
- If the peer cannot connect to PD through the default listening peer URLs, you must manually set the advertise peer URLs explicitly.
- For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 2380:2380`. In this case, you can set `--advertise-peer-urls` to "http://192.168.100.113:2380". The other PD nodes can find this service through "http://192.168.100.113:2380".

### `--client-urls`

- The listening URL list for client traffic
- Default: "http://127.0.0.1:2379"
- To deploy a cluster, you must use `--client-urls` to specify the IP address of the current host, such as "http://192.168.100.113:2379". If the cluster runs on Docker, specify the IP address of Docker as "http://0.0.0.0:2379".

### `--peer-urls`

- The listening URL list for peer traffic
- Default: "http://127.0.0.1:2380"
- To deploy a cluster, you must use `--peer-urls` to specify the IP address of the current host, such as "http://192.168.100.113:2380". If the cluster runs on Docker, specify the IP address of Docker as "http://0.0.0.0:2380".

### `--config`

- The configuration file
- Default: ""
- If you set the configuration using the command line, the same setting in the configuration file will be overwritten.

### `--data-dir`

- The path to the data directory
- Default: "default.${name}"

### `--initial-cluster`

- The initial cluster configuration for bootstrapping
- Default: "{name}=http://{advertise-peer-url}"
- For example, if `name` is "pd", and `advertise-peer-urls` is "http://192.168.100.113:2380", the `initial-cluster` is "pd=http://192.168.100.113:2380".
- If you need to start three PD servers, the `initial-cluster` might be:
  
    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

### `--join`

- Join the cluster dynamically
- Default: ""
- If you want to join an existing cluster, you can use `--join="${advertise-client-urls}"`, the `advertise-client-url` is any existing PD's, multiply advertise client urls are separated by comma.

### `-L`

- The log level
- Default: "info"
- You can choose from debug, info, warn, error, or fatal.

### `--log-file`

- The log file
- Default: ""
- If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--log-rotate`

- To enable or disable log rotation
- Default: true
- When the value is true, follow the `[log.file]` in PD configuration files.

### `--name`

- The human-readable unique name for this PD member
- Default: "pd"
- If you want to start multiply PDs, you must use different name for each one.

### `--cacert`

- The file path of CA, used to enable TLS
- Default: ""

### `--cert`

- The path of the PEM file including the X509 certificate, used to enable TLS
- Default: ""

### `--key`

- The path of the PEM file including the X509 key, used to enable TLS
- Default: ""

### `--namespace-classifier`

- To specify the namespace classifier used by PD
- Default: "table"
- If you use TiKV separately, not in the entire TiDB cluster, it is recommended to configure the value to 'default'.

## TiKV

TiKV supports some readable unit conversions for command line parameters.

- File size (based on byte): KB, MB, GB, TB, PB (or lowercase)
- Time (based on ms): ms, s, m, h

### `-A, --addr`

- The address that the TiKV server monitors
- Default: "127.0.0.1:20160"
- To deploy a cluster, you must use `--addr` to specify the IP address of the current host, such as "192.168.100.113:20160". If the cluster is run on Docker, specify the IP address of Docker as "0.0.0.0:20160".

### `--advertise-addr`

- The server advertise address for client traffic from outside
- Default: ${addr}
- If the client cannot connect to TiKV through the default monitoring address because of Docker or NAT network, you must manually set the advertise address explicitly.
- For example, the internal IP address of Docker is 172.17.0.1, while the IP address of the host is 192.168.100.113 and the port mapping is set to `-p 20160:20160`. In this case, you can set `--advertise-addr` to "192.168.100.113:20160". The client can find this service through 192.168.100.113:20160.

### `-C, --config`

- The config file
- Default: ""
- If you set the configuration using the command line, the same setting in the config file will be overwritten.

### `--capacity`

- The store capacity
- Default: 0 (unlimited)
- PD uses this flag to determine how to balance the TiKV servers. (Tip: you can use 10GB instead of 1073741824)

### `--data-dir`

- The path to the data directory
- Default: "/tmp/tikv/store"

### `-L, --Log`

- The log level
- Default: "info"
- You can choose from trace, debug, info, warn, error, or off.

### `--log-file`

- The log file
- Default: ""
- If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--pd`

- The address list of PD servers
- Default: ""
- To make TiKV work, you must use the value of `--pd` to connect the TiKV server to the PD server. Separate multiple PD addresses using comma, for example "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
