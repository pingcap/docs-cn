# Configuration flags

TiDB is configurable through command-line flags and environment variables.

The official TiDB ports are 4000 for client requests and 10080 for status report.

### --store
+ Storage type
+ Human-readable name for this member.
+ default: "goleveldb"
+ You can choose from memory, goleveldb, boltdb and tikv. The first three are all local storage. TiKV is a distributed storage.

### --path
+ Path to the data directory for local storage (goleveldb, boltdb, memory). DSN to the distributed storage (TiKV).
+ default: "/tmp/tidb"
+ If use TiKV, the path should be in this format: $Host:$Port/pd?cluster=$ClusterID

### -L
+ Log level
+ default: "debug"
+ You can choose from debug, info, warn, error, fatal.

### -P
+ TiDB server listening port.
+ default: "4000"
+ TiDB server will accept MySQL client request from this port.

### --status
+ TiDB server status report port.
+ default: "10080"
+ This is used for get server status.

### --lease
+ Schema lease time in second.
+ default: "1"
+ It is schema lease time used in online schema change. Its value will affact DDL statement running time. It is very dangerous to change it if you don't understand the internal mechanism.

### --socket
+ The socket file to use for connection.
+ default: ""
+ example: "/tmp/tidb.sock"

### --perfschema
+ Enable(1) or disable(0) performance schema.
+ default: "0"
+ If set this to 1, it will affect performance.

### TIDB_PPROF environment variable
+ Enable runtime profiling data via HTTP server. Address is at client URL + "/debug/pprof/"
+ If set $TIDB_PPROF to 0, TiDB will disable pprof. Otherwise TiDB will enable pprof.
