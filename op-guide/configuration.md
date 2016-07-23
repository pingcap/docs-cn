# Configuration flags

TiDB/TiKV/PD are configurable through command-line flags and environment variables.


##TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### --store
+ Storage engine type
+ Human-readable name for this member.
+ default: "goleveldb"
+ You can choose from "memory", "goleveldb", "BoltDB" or "TiKV". The first three are all local storage engines. TiKV is a distributed storage engine.

### --path
+ The path to the data directory for local storage engines like goleveldb, BoltDB, or memory or the DSN for the distributed storage engine like TiKV. If you use TiKV, specify the path in the following format: $Host:$Port/pd?cluster=$ClusterID.
+ default: "/tmp/tidb"

### -L
+ The log level
+ default: "debug"
+ You can choose from debug, info, warn, error, or fatal.

### -P
+ The listening port for TiDB server.
+ default: "4000"
+ TiDB server will accept MySQL client request from this port.

### --status
+ The status report port for TiDB server
+ default: "10080"
+ This is used to get server status.

### --lease
+ The schema lease time in second.
+ default: "1"
+ This is the schema lease time that is used in online schema changes. The value will affect the DDL statement running time. You cannot change it unless you understand the internal mechanism.

### --socket
+ The socket file for connection.
+ default: ""
+ You can use the "/tmp/tidb.sock" file.

### --perfschema
+ Enable(1) or disable(0) the performance schema.
+ default: "0"
+ The value can be (1) or (0). (1) is to enable and (0) is to disable. If the value is set to be (1), the performance will be affected.

### $TIDB_PPROF environment variable
+ An environment variable that is used to enable or disable the runtime profiling data via the HTTP server. . Address is at client URL + "/debug/pprof/".
+ If set $TIDB_PPROF to 0, TiDB will disable pprof. Otherwise TiDB will enable pprof.
