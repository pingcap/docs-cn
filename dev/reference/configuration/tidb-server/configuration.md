---
title: Configuration Flags
summary: Learn some configuration flags for TiDB
category: reference
---

# Configuration Flags

TiDB is configurable using command-line flags and environment variables. The default TiDB ports are 4000 for client requests and 10080 for status report.

## `--advertise-address`

- The IP address on which to advertise the apiserver to the TiDB server
- Default: ""
- This address must be reachable by the rest of the TiDB cluster and the user.

## `--binlog-socket`

- The TiDB services use the unix socket file for internal connections, such as the Pump service
- Default: ""
- You can use "/tmp/pump.sock" to accept the communication of Pump unix socket file.

## `--config`

- The configuration file
- Default: ""
- If you have specified the configuration file, TiDB reads the configuration file. If the corresponding configuration also exists in the command line flags, TiDB uses the configuration in the command line flags to overwrite that in the configuration file. For detailed configuration information, see [TiDB Configuration File Description](/dev/reference/configuration/tidb-server/configuration-file.md).

## `--host`

- The host address that the TiDB server monitors
- Default: "0.0.0.0"
- The TiDB server monitors this address.
- The "0.0.0.0" monitors all network cards by default. If you have multiple network cards, specify the network card that provides service, such as 192.168.100.113.

## `-L`

- The log level
- Default: "info"
- You can choose from "debug", "info", "warn", "error", or "fatal".

## `--log-file`

- The log file
- Default: ""
- If this flag is not set, logs are output to "stderr". If this flag is set, logs are output to the corresponding file, which is automatically rotated in the early morning every day, and the previous file is renamed as a backup.

## `--log-slow-query`

- The directory for the slow query log
- Default: ""
- If this flag is not set, logs are written to the file specified by `--log-file` by default.

## `--status-host`

- The `HOST` used to monitor the status of TiDB service
- Default: `0.0.0.0`

## `--metrics-addr`

- The Prometheus Pushgateway address
- Default: ""
- Leaving it empty stops the Prometheus client from pushing.
- The format is `--metrics-addr=192.168.100.115:9091`.

## `--metrics-interval`

- The Prometheus client push interval in seconds
- Default: 15s
- Setting the value to 0 stops the Prometheus client from pushing.

## `-P`

- The monitoring port of TiDB services
- Default: "4000"
- The TiDB server accepts MySQL client requests from this port.

## `--path`

- The path to the data directory for local storage engine like "mocktikv"
- For `--store = tikv`, you must specify the path; for `--store = mocktikv`, the default value is used if you do not specify the path.
- For the distributed storage engine like TiKV, `--path` specifies the actual PD address. Assuming that you deploy the PD server on 192.168.100.113:2379, 192.168.100.114:2379 and 192.168.100.115:2379, the value of `--path` is "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
- Default: "/tmp/tidb"
- You can use `tidb-server --store=mocktikv --path=""` to enable a pure in-memory TiDB.

## `--proxy-protocol-networks`

- The list of proxy server's IP addresses allowed by PROXY Protocol; if you need to configure multiple addresses, separate them using ",".
- Default: ""
- Leaving it empty disables PROXY Protocol. The value can be the IP address (192.168.1.50) or CIDR (192.168.1.0/24). "\*" means any IP addresses.

## `--proxy-protocol-header-timeout`

- Timeout for the PROXY protocol header read
- Default: 5 (seconds)

    > **Note:**
    >
    > Do not set the value to `0`. Use the default value except for special situations.

## `--cors`

- Specifies the `Access-Control-Allow-Origin` value for Cross-Origin Request Sharing (CORS) request of the TiDB HTTP status service
- Default: ""

## `--report-status`

- Enables (`true`) or disables (`false`) the status report and pprof tool
- Default: `true`
- When set to `true`, this parameter enables metrics and pprof. When set to `false`, this parameter disables metrics and pprof.

## `--run-ddl`

- To see whether the `tidb-server` runs DDL statements, and set when the number of `tidb-server` is over two in the cluster
- Default: `true`
- The value can be (true) or (false). (true) indicates the `tidb-server` runs DDL itself. (false) indicates the `tidb-server` does not run DDL itself.

## `--socket string`

- The TiDB services use the unix socket file for external connections.
- Default: ""
- Use `/tmp/tidb.sock` to open the unix socket file.

## `--status`

- The status report port for TiDB server
- Default: "10080"
- This is used to get server internal data. The data includes [Prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
- Prometheus metrics can be got through `"http://host:status_port/metrics"`.
- Pprof data can be got through `"http://host:status_port/debug/pprof"`.

## `--store`

- Specifies the storage engine used by TiDB in the bottom layer
- Default: "mocktikv"
- You can choose "mocktikv" or "tikv". ("mocktikv" is the local storage engine; "tikv" is a distributed storage engine)

## `--token-limit`

- The number of sessions allowed to run concurrently in TiDB. It is used for traffic control.
- Default: 1000
- If the number of the concurrent sessions is larger than `token-limit`, the request is blocked and waiting for the operations which have been finished to release tokens.

## `-V`

- Outputs the version of TiDB
- Default: ""
