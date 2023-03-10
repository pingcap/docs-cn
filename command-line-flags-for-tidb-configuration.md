---
title: Configuration Options
summary: Learn the configuration options in TiDB.
aliases: ['/docs/dev/command-line-flags-for-tidb-configuration/','/docs/dev/reference/configuration/tidb-server/configuration/','/docs/dev/reference/configuration/tidb-server/server-command-option/']
---

# Configuration Options

When you start the TiDB cluster, you can use command-line options or environment variables to configure it. This document introduces TiDB's command options. The default TiDB ports are `4000` for client requests and `10080` for status report.

## `--advertise-address`

- The IP address through which to log into the TiDB server
- Default: `""`
- This address must be accessible by the rest of the TiDB cluster and the user.

## `--config`

- The configuration file
- Default: `""`
- If you have specified the configuration file, TiDB reads the configuration file. If the corresponding configuration also exists in the command line options, TiDB uses the configuration in the command line options to overwrite that in the configuration file. For detailed configuration information, see [TiDB Configuration File Description](/tidb-configuration-file.md).

## `--config-check`

- Checks the validity of the configuration file and exits
- Default: `false`

## `--config-strict`

- Enforces the validity of the configuration file
- Default: `false`

## `--cors`

- Specifies the `Access-Control-Allow-Origin` value for Cross-Origin Request Sharing (CORS) request of the TiDB HTTP status service
- Default: `""`

## `--enable-binlog`

+ Enables or disables TiDB binlog generation
+ Default: `false`

## `--host`

- The host address that the TiDB server monitors
- Default: `"0.0.0.0"`
- The TiDB server monitors this address.
- The `"0.0.0.0"` address monitors all network cards by default. If you have multiple network cards, specify the network card that provides service, such as `192.168.100.113`.

## `--initialize-insecure`

- Bootstraps tidb-server in insecure mode
- Default: `true`

## `--initialize-secure`

- Bootstraps tidb-server in secure mode
- Default: `false`

## `--initialize-sql-file`

- The SQL script to be executed when the TiDB cluster is started for the first time. For details, see [configuration item `initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)
- Default: `""`

## `-L`

- The log level
- Default: `"info"`
- Optional values: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`

## `--lease`

- The duration of the schema lease. It is **dangerous** to change the value unless you know what you do.
- Default: `45s`

## `--log-file`

- The log file
- Default: `""`
- If this option is not set, logs are output to "stderr". If this option is set, logs are output to the corresponding file.

## `--log-slow-query`

- The directory for the slow query log
- Default: `""`
- If this option is not set, logs are output to the file specified by `--log-file` by default.

## `--metrics-addr`

- The Prometheus Pushgateway address
- Default: `""`
- Leaving it empty stops the Prometheus client from pushing.
- The format is `--metrics-addr=192.168.100.115:9091`.

## `--metrics-interval`

- The Prometheus client push interval in seconds
- Default: `15s`
- Setting the value to 0 stops the Prometheus client from pushing.

## `-P`

- The monitoring port of TiDB services
- Default: `"4000"`
- The TiDB server accepts MySQL client requests from this port.

## `--path`

- The path to the data directory for local storage engine like "unistore"
- For `--store = tikv`, you must specify the path; for `--store = unistore`, the default value is used if you do not specify the path.
- For the distributed storage engine like TiKV, `--path` specifies the actual PD address. Assuming that you deploy the PD server on 192.168.100.113:2379, 192.168.100.114:2379 and 192.168.100.115:2379, the value of `--path` is "192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379".
- Default: `"/tmp/tidb"`
- You can use `tidb-server --store=unistore --path=""` to enable a pure in-memory TiDB.

## `--proxy-protocol-fallbackable`

- Controls whether to enable PROXY protocol fallback mode. When this parameter is set to `true`, TiDB accepts PROXY client connections and client connections without any PROXY protocol header. By default, TiDB only accepts client connections with a PROXY protocol header.
- Default value: `false`

## `--proxy-protocol-networks`

- The list of proxy server's IP addresses allowed to connect to TiDB using the [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt).
- Default: `""`
- In general cases, when you access TiDB behind a reverse proxy, TiDB takes the IP address of the reverse proxy server as the IP address of the client. By enabling the PROXY protocol, reverse proxies that support this protocol such as HAProxy can pass the real client IP address to TiDB.
- After configuring this flag, TiDB allows the configured source IP address to connect to TiDB using the PROXY protocol; if a protocol other than PROXY is used, this connection will be denied. If this flag is left empty, no IP address can connect to TiDB using the PROXY protocol. The value can be the IP address (192.168.1.50) or CIDR (192.168.1.0/24) with `,` as the separator. `*` means any IP addresses.

> **Warning:**
>
> Use `*` with caution because it might introduce security risks by allowing a client of any IP address to report its IP address. In addition, using `*` might also cause the internal component that directly connects to TiDB (such as TiDB Dashboard) to be unavailable.

> **Note:**
>
> To use an AWS Network Load Balancer (NLB) with the PROXY protocol enabled, you need to configure the `target group` property of NLB. Specifically, set `proxy_protocol_v2.client_to_server.header_place` to `on_first_ack`. At the same time, you need to submit a ticket to AWS Support. Note that after the PROXY protocol is enabled, the client will fail to obtain handshake packets from the server and the packets are blocked until the client times out. This is because NLB sends proxy packets only after the client sends data. However, before the client sends any data packets, data packets sent by the server are dropped in the internal network.

## `--proxy-protocol-header-timeout`

- Timeout for the PROXY protocol header read
- Default: `5` (seconds)

> **Warning:**
>
> Since v6.3.0, this parameter is deprecated. It is no longer used because the PROXY protocol header will be read upon the first time network data is read. Deprecating this parameter avoids affecting the timeout set when network data is read for the first time.

> **Note:**
>
> Do not set the value to `0`. Use the default value except for special situations.

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
- Default: `""`
- Use `/tmp/tidb.sock` to open the unix socket file.

## `--status`

- The status report port for TiDB server
- Default: `"10080"`
- This port is used to get server internal data. The data includes [Prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
- Prometheus metrics can be accessed by `"http://host:status_port/metrics"`.
- pprof data can be accessed by `"http://host:status_port/debug/pprof"`.

## `--status-host`

- The `HOST` used to monitor the status of TiDB service
- Default: `0.0.0.0`

## `--store`

- Specifies the storage engine used by TiDB in the bottom layer
- Default: `"unistore"`
- You can choose "unistore" or "tikv". ("unistore" is the local storage engine; "tikv" is a distributed storage engine)

## `--temp-dir`

- The temporary directory of TiDB
- Default: `"/tmp/tidb"`

## `--token-limit`

- The number of sessions allowed to run concurrently in TiDB. It is used for traffic control.
- Default: `1000`
- If the number of the concurrent sessions is larger than `token-limit`, the request is blocked and waiting for the operations which have been finished to release tokens.

## `-V`

- Outputs the version of TiDB
- Default: `""`

## `--plugin-dir`

+ The storage directory for plugins.
+ Default: `"/data/deploy/plugin"`

## `--plugin-load`

+ The names of the plugins to be loaded, each separated by a comma.
+ Default: `""`

## `--affinity-cpus`

+ Sets the CPU affinity of TiDB servers, which is separated by commas. For example, "1,2,3".
+ Default: `""`

## `--repair-mode`

+ Determines whether to enable the repair mode, which is only used in the data repair scenario.
+ Default: `false`

## `--repair-list`

+ The names of the tables to be repaired in the repair mode.
+ Default: `""`
