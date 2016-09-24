# Configuration flags

TiDB/TiKV/PD are configurable through command-line flags and environment variables.


## TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### --store
+ the storage engine type
+ Human-readable name for this member.
+ default: "goleveldb"
+ You can choose from "memory", "goleveldb", "BoltDB" or "TiKV". The first three are all local storage engines. TiKV is a distributed storage engine.

### --path
+ the path to the data directory for local storage engines like goleveldb, BoltDB, or memory or the DSN for the distributed storage engine like TiKV. If you use TiKV, specify the path in the following format: $Host:$Port?cluster=$ClusterID.
+ default: "/tmp/tidb"

### -L
+ the log level
+ default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### --log-file
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### --host
+ the listening address for TiDB server
+ default: "0.0.0.0"
+ TiDB server will listen on this address.

### -P
+ the listening port for TiDB server
+ default: "4000"
+ TiDB server will accept MySQL client request from this port.

### --status
+ the status report port for TiDB server
+ default: "10080"
+ This is used to get server internal data. The data includes [prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
+ Prometheus metrics can be got through "http://host:status_port/metrics".
+ Pprof data can be got through "http://host:status_port/debug/pprof".

### --lease
+ the schema lease time in seconds
+ default: "1"
+ This is the schema lease time that is used in online schema changes. The value will affect the DDL statement running time. Do not change it unless you understand the internal mechanism.

### --socket
+ the socket file for connection
+ default: ""
+ You can use the "/tmp/tidb.sock" file.

### --perfschema
+ enable(true) or disable(false) the performance schema
+ default: false
+ The value can be (true) or (false). (true) is to enable and (false) is to disable. The Performance Schema provides a way to inspect internal execution of the server at runtime. See [performance schema](http://dev.mysql.com/doc/refman/5.7/en/performance-schema.html) for more information. If you enable the performance schema, the performance will be affected.

### --report-status
+ enable(true) or disable(false) the status report and pprof tool.
+ default: true
+ The value can be (true) or (false). (true) is to enable metrics and pprof. (false) is to disable metrics and pprof.

### --metrics-addr
+ the Prometheus pushgateway address
+ default: ""
+ Leaving it empty stops the Prometheus client from pushing.

### --metrics-intervel
+ the Prometheus client push interval in seconds
+ default: 0
+ Setting the value to 0 stops the Prometheus client from pushing.

## Placement Driver (PD)

### -L

+ the log level
+ default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### --log-file
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### --config

+ the config file
+ default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### --cluster-id

+ the cluster ID to identify unique cluster
+ default: 0
+ You must use a unique ID to distinguish different clusters.

### --name

+ the human-readable unique name for this PD member
+ default: "pd"
+ If you want to start multiply PDs, you must use different name for each one.

### --data-dir

+ the path to the data directory
+ default: "default.${name}"

### --client-urls

+ the listening URL list for client traffic
+ default: "http://127.0.0.1:2379"

###  --advertise-client-urls

+ the advertise URL list for client traffic from outside
+ default: ${client-urls}
+ If the client cannot connect to PD through the default listening client URLs, you must manually set the advertise client URLs explicitly.

### --peer-urls

+ the listening URL list for peer traffic
+ default: "http://127.0.0.1:2380"

### --advertise-peer-urls

+ the advertise URL list for peer traffic from outside
+ default: ${peer-urls}
+ If the peer cannot connect to PD through the default listening peer URLs, you must manually set the advertise peer URLs explicitly.

### --initial-cluster

+ the initial cluster configuration for bootstrapping
+ default: "{name}=http://{advertise-peer-url}"
+ For example, if `name` is "pd", and `advertise-peer-urls` is "http://127.0.0.1:2380,http://127.0.0.1:2381", the `initial-cluster` is "pd=http://127.0.0.1:2380,pd=http://127.0.0.1:2381".

### --join

+ join the cluster dynamically
+ default: ""
+ If you want to join an existing cluster, you can use `--join="${advertise-client-urls}"`, the `advertise-client-url` is any existing PD's, multiply advertise client urls are separated by comma.

## TiKV

TiKV supports some human readable conversion.

 - File size (based on byte): KB, MB, GB, TB, PB (or lowercase)
 - Time (based on ms): ms, s, m, h

### -A, --addr

+ the server listening address
+ default: "127.0.0.1:20160"

### --advertise-addr

+ the server advertise address for client traffic.
+ default: ${addr}
+ + If the client cannot connect to TiKV through the default listening address, you must manually set the advertise address explicitly.

### -L, --Log

+ the log level
+ default: "info"
+ You can choose from trace, debug, info, warn, error, or off.

### --log-file
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### -C, --config

+ the config file
+ default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### -s, --store

+ the path to the data directory
+ default: "/tmp/tikv/store"

### --capacity

+ the store capacity
+ default: 0 (unlimited)
+ PD uses this flag to determine how to balance the TiKV servers. (Tip: you can use 10GB instead of 1073741824)

### -S, --dsn

+ the DSN to use, "rocksdb" or "raftkv"
+ default: "rocksdb"
+ You must set the value to "raftkv" in production, because "rocksdb" is for local test only.

### -I, --cluster-id

+ the unique ID to distinguish cluster
+ default: 0
+ The cluster ID must be the same as PD's.

### --pd

+ the pd endpoints
+ default: ""
+ You must set this flag to let TiKV connect to PD. Multiple endpoints are separated by comma, for example, "pd1:2379,pd2:2379".
