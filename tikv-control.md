---
title: TiKV Control User Guide
summary: Use TiKV Control to manage a TiKV cluster.
aliases: ['/docs/dev/tikv-control/','/docs/dev/reference/tools/tikv-control/']
---

# TiKV Control User Guide

TiKV Control (`tikv-ctl`) is a command line tool of TiKV, used to manage the cluster. Its installation directory is as follows:

* If the cluster is deployed using TiUP, `tikv-ctl` directory is in the in `~/.tiup/components/ctl/{VERSION}/` directory.

## Use TiKV Control in TiUP

> **Note:**
>
> It is recommended that the version of the Control tool you use is consistent with the version of the cluster.

`tikv-ctl` is also integrated in the `tiup` command. Execute the following command to call the `tikv-ctl` tool:

```shell
tiup ctl:v<CLUSTER_VERSION> tikv
```

```
Starting component `ctl`: /home/tidb/.tiup/components/ctl/v4.0.8/ctl tikv
TiKV Control (tikv-ctl)
Release Version:   4.0.8
Edition:           Community
Git Commit Hash:   83091173e960e5a0f5f417e921a0801d2f6635ae
Git Commit Branch: heads/refs/tags/v4.0.8
UTC Build Time:    2020-10-30 08:40:33
Rust Version:      rustc 1.42.0-nightly (0de96d37f 2019-12-19)
Enable Features:   jemalloc mem-profiling portable sse protobuf-codec
Profile:           dist_release

A tool for interacting with TiKV deployments.
USAGE:
    TiKV Control (tikv-ctl) [FLAGS] [OPTIONS] [SUBCOMMAND]
FLAGS:
    -h, --help                    Prints help information
        --skip-paranoid-checks    Skip paranoid checks when open rocksdb
    -V, --version                 Prints version information
OPTIONS:
        --ca-path <ca-path>              Set the CA certificate path
        --cert-path <cert-path>          Set the certificate path
        --config <config>                TiKV config path, by default it's <deploy-dir>/conf/tikv.toml
        --data-dir <data-dir>            TiKV data directory path, check <deploy-dir>/scripts/run.sh to get it
        --decode <decode>                Decode a key in escaped format
        --encode <encode>                Encode a key in escaped format
        --to-hex <escaped-to-hex>        Convert an escaped key to hex key
        --to-escaped <hex-to-escaped>    Convert a hex key to escaped key
        --host <host>                    Set the remote host
        --key-path <key-path>            Set the private key path
        --log-level <log-level>          Set the log level [default: warn]
        --pd <pd>                        Set the address of pd
SUBCOMMANDS:
    bad-regions           Get all regions with corrupt raft
    cluster               Print the cluster id
    compact               Compact a column family in a specified range
    compact-cluster       Compact the whole cluster in a specified range in one or more column families
    consistency-check     Force a consistency-check for a specified region
    decrypt-file          Decrypt an encrypted file
    diff                  Calculate difference of region keys from different dbs
    dump-snap-meta        Dump snapshot meta file
    encryption-meta       Dump encryption metadata
    fail                  Inject failures to TiKV and recovery
    help                  Prints this message or the help of the given subcommand(s)
    metrics               Print the metrics
    modify-tikv-config    Modify tikv config, eg. tikv-ctl --host ip:port modify-tikv-config -n
                          rocksdb.defaultcf.disable-auto-compactions -v true
    mvcc                  Print the mvcc value
    print                 Print the raw value
    raft                  Print a raft log entry
    raw-scan              Print all raw keys in the range
    recover-mvcc          Recover mvcc data on one node by deleting corrupted keys
    recreate-region       Recreate a region with given metadata, but alloc new id for it
    region-properties     Show region properties
    scan                  Print the range db range
    size                  Print region size
    split-region          Split the region
    store                 Print the store id
    tombstone             Set some regions on the node to tombstone by manual
    unsafe-recover        Unsafely recover the cluster when the majority replicas are failed
```

You can add corresponding parameters and subcommands after `tiup ctl:v<CLUSTER_VERSION> tikv`.

## General options

`tikv-ctl` provides two operation modes:

- Remote mode: use the `--host` option to accept the service address of TiKV as the argument

    For this mode, if SSL is enabled in TiKV, `tikv-ctl` also needs to specify the related certificate file. For example:

    ```shell
    tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
    ```

    However, sometimes `tikv-ctl` communicates with PD instead of TiKV. In this case, you need to use the `--pd` option instead of `--host`. Here is an example:

    ```shell
    tikv-ctl --pd 127.0.0.1:2379 compact-cluster
    ```

    ```
    store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!
    ```

- Local mode:

    * Use the `--data-dir` option to specify the local TiKV data directory path.
    * Use the `--config` option to specify the local TiKV configuration file path.

  In this mode, you need to stop the running TiKV instance.

Unless otherwise noted, all commands support both the remote mode and the local mode.

Additionally, `tikv-ctl` has two simple commands `--to-hex` and `--to-escaped`, which are used to make simple changes to the form of the key.

Generally, use the `escaped` form of the key. For example:

```shell
tikv-ctl --to-escaped 0xaaff
\252\377
tikv-ctl --to-hex "\252\377"
AAFF
```

> **Note:**
>
> When you specify the `escaped` form of the key in a command line, it is required to enclose it in double quotes. Otherwise, bash eats the backslash and a wrong result is returned.

## Subcommands, some options and flags

This section describes the subcommands that `tikv-ctl` supports in detail. Some subcommands support a lot of options. For all details, run `tikv-ctl --help <subcommand>`.

### View information of the Raft state machine

Use the `raft` subcommand to view the status of the Raft state machine at a specific moment. The status information includes two parts: three structs (**RegionLocalState**, **RaftLocalState**, and **RegionApplyState**) and the corresponding Entries of a certain piece of log.

Use the `region` and `log` subcommands to obtain the above information respectively. The two subcommands both support the remote mode and the local mode at the same time.

For the `region` subcommand:

- To specify the Regions to be viewed, use the `-r` option. Multiple Regions are separated by `,`. You can also use the `--all-regions` option to view all Regions. Note that `-r` and `--all-regions` cannot be used at the same time.
- To limit the number of Regions to be printed, use the `--limit` option (default: `16`).
- To query which Regions are included in a certain key range, use the `--start` and `--end` options (default: no range limit, in Hex format).

For example, to print the Region with the ID `1239`, use the following command:

```shell
tikv-ctl --host 127.0.0.1:20160 raft region -r 1239
```

The output is as follows:

```
"region id": 1239
"region state": {
    id: 1239,
    start_key: 7480000000000000FF4E5F728000000000FF1443770000000000FA,
    end_key: 7480000000000000FF4E5F728000000000FF21C4420000000000FA,
    region_epoch: {conf_ver: 1 version: 43},
    peers: [ {id: 1240 store_id: 1 role: Voter} ]
}
"raft state": {
    hard_state {term: 8 vote: 5 commit: 7}
    last_index: 8)
}
"apply state": {
    applied_index: 8 commit_index: 8 commit_term: 8
    truncated_state {index: 5 term: 5}
}
```

To query which Regions are included in a certain key range, use the following command:

- If the key range is in a Region range, the Region information is output.
- If the key range is the same as a Region range, for example, when the given key range is the same as the Region `1239`, because the Region range is a left-closed and right-open interval, and Region `1009` takes the `end_key` of Region `1239` as the `start_key`, the Region `1009` information is also output.

```shell
tikv-ctl --host 127.0.0.1:20160 raft region --start 7480000000000000FF4E5F728000000000FF1443770000000000FA --end 7480000000000000FF4E5F728000000000FF21C4420000000000FA
```

The output is as follows:

```
"region state": {
    id: 1009
    start_key: 7480000000000000FF4E5F728000000000FF21C4420000000000FA,
    end_key: 7480000000000000FF5000000000000000F8,
    ...
}
"region state": {
    id: 1239
    start_key: 7480000000000000FF4E5F728000000000FF06C6D60000000000FA,
    end_key: 7480000000000000FF4E5F728000000000FF1443770000000000FA,
    ...
}
```

### View the Region size

Use the `size` command to view the Region size:

```shell
tikv-ctl --data-dir /path/to/tikv size -r 2
```

The output is as follows:

```
region id: 2
cf default region size: 799.703 MB
cf write region size: 41.250 MB
cf lock region size: 27616
```

### Scan to view MVCC of a specific range

The `--from` and `--to` options of the `scan` command accept two escaped forms of raw key, and use the `--show-cf` flag to specify the column families that you need to view.

```shell
tikv-ctl --data-dir /path/to/tikv scan --from 'zm' --limit 2 --show-cf lock,default,write
```

```
key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
         write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

### View MVCC of a given key

Similar to the `scan` command, the `mvcc` command can be used to view MVCC of a given key.

```shell
tikv-ctl --data-dir /path/to/tikv mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
```

```
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

In this command, the key is also the escaped form of raw key.

### Scan raw keys

The `raw-scan` command scans directly from the RocksDB. Note that to scan data keys you need to add a `'z'` prefix to keys.

Use `--from` and `--to` options to specify the range to scan (unbounded by default). Use `--limit` to limit at most how many keys to print out (30 by default). Use `--cf` to specify which cf to scan (can be `default`, `write` or `lock`).

```shell
tikv-ctl --data-dir /var/lib/tikv raw-scan --from 'zt' --limit 2 --cf default
```

```
key: "zt\200\000\000\000\000\000\000\377\005_r\200\000\000\000\000\377\000\000\001\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002\002%\010\004\002\010root\010\006\002\000\010\010\t\002\010\n\t\002\010\014\t\002\010\016\t\002\010\020\t\002\010\022\t\002\010\024\t\002\010\026\t\002\010\030\t\002\010\032\t\002\010\034\t\002\010\036\t\002\010 \t\002\010\"\t\002\010s\t\002\010&\t\002\010(\t\002\010*\t\002\010,\t\002\010.\t\002\0100\t\002\0102\t\002\0104\t\002"
key: "zt\200\000\000\000\000\000\000\377\025_r\200\000\000\000\000\377\000\000\023\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002&slow_query_log_file\010\004\002P/usr/local/mysql/data/localhost-slow.log"

Total scanned keys: 2
```

### Print a specific key value

To print the value of a key, use the `print` command.

### Print some properties about Region

In order to record Region state details, TiKV writes some statistics into the SST files of Regions. To view these properties, run `tikv-ctl` with the `region-properties` sub-command:

```shell
tikv-ctl --host localhost:20160 region-properties -r 2
```

```
num_files: 0
num_entries: 0
num_deletes: 0
mvcc.min_ts: 18446744073709551615
mvcc.max_ts: 0
mvcc.num_rows: 0
mvcc.num_puts: 0
mvcc.num_versions: 0
mvcc.max_row_versions: 0
middle_key_by_approximate_size:
```

The properties can be used to check whether the Region is healthy or not. If not, you can use them to fix the Region. For example, splitting the Region manually by `middle_key_approximate_size`.

### Compact data of each TiKV manually

Use the `compact` command to manually compact data of each TiKV.

- Use the `--from` and `--to` options to specify the compaction range in the form of escaped raw key. If not set, the whole range will be compacted.
- Use the `--region` option to compact the range of a specific region. If set, `--from` and `--to` will be ignored.
- Use the `--db` option to specify the RocksDB that performs compaction. The optional values are `kv` and `raft`.
- Use the `--threads` option allows you to specify the concurrency for the TiKV compaction and its default value is `8`. Generally, a higher concurrency comes with a faster compaction speed, which might yet affect the service. You need to choose an appropriate concurrency count based on your scenario.
- Use the `--bottommost` option to include or exclude the bottommost files when TiKV performs compaction. The value options are `default`, `skip`, and `force`. The default value is `default`.
    - `default` means that the bottommost files are included only when the Compaction Filter feature is enabled.
    - `skip` means that the bottommost files are excluded when TiKV performs compaction.
    - `force` means that the bottommost files are always included when TiKV performs compaction.

- To compact data in the local mode, use the following command:

    ```shell
    tikv-ctl --data-dir /path/to/tikv compact --db kv
    ```

- To compact data in the remote mode, use the following command:

    ```shell
    tikv-ctl --host ip:port compact --db kv
    ```

### Compact data of the whole TiKV cluster manually

Use the `compact-cluster` command to manually compact data of the whole TiKV cluster. The flags of this command have the same meanings and usage as those of the `compact` command.

### Set a Region to tombstone

The `tombstone` command is usually used in circumstances where the sync-log is not enabled, and some data written in the Raft state machine is lost caused by power down.

In a TiKV instance, you can use this command to set the status of some Regions to tombstone. Then when you restart the instance, those Regions are skipped to avoid the restart failure caused by damaged Raft state machines of those Regions. Those Regions need to have enough healthy replicas in other TiKV instances to be able to continue the reads and writes through the Raft mechanism.

In general cases, you can remove the corresponding Peer of this Region using the `remove-peer` command:

```shell
pd-ctl operator add remove-peer <region_id> <store_id>
```

Then use the `tikv-ctl` tool to set a Region to tombstone on the corresponding TiKV instance to skip the health check for this Region at startup:

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>
```

```
success!
```

However, in some cases, you cannot easily remove this Peer of this Region from PD, so you can specify the `--force` option in `tikv-ctl` to forcibly set the Peer to tombstone:

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>,<region_id> --force
```

```
success!
```

> **Note:**
>
> - The `tombstone` command only supports the local mode.
> - The argument of the `-p` option specifies the PD endpoints without the `http` prefix. Specifying the PD endpoints is to query whether PD can safely switch to Tombstone.

### Send a `consistency-check` request to TiKV

Use the `consistency-check` command to execute a consistency check among replicas in the corresponding Raft of a specific Region. If the check fails, TiKV itself panics. If the TiKV instance specified by `--host` is not the Region leader, an error is reported.

```shell
tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
tikv-ctl --host 127.0.0.1:20161 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **Note:**
>
> - It is **NOT** recommended to use the `consistency-check` command, because it is incompatible with the garbage collection in TiDB and might mistakenly report an error.
> - This command only supports the remote mode.
> - Even if this command returns `success!`, you need to check whether TiKV panics. This is because this command is only a proposal that requests a consistency check for the leader, and you cannot know from the client whether the whole check process is successful or not.

### Dump snapshot meta

This sub-command is used to parse a snapshot meta file at given path and print the result.

### Print the Regions where the Raft state machine corrupts

To avoid checking the Regions while TiKV is started, you can use the `tombstone` command to set the Regions where the Raft state machine reports an error to Tombstone. Before running this command, use the `bad-regions` command to find out the Regions with errors, so as to combine multiple tools for automated processing.

```shell
tikv-ctl --data-dir /path/to/tikv bad-regions
```

```
all regions are healthy
```

If the command is successfully executed, it prints the above information. If the command fails, it prints the list of bad Regions. Currently, the errors that can be detected include the mismatches between `last index`, `commit index` and `apply index`, and the loss of Raft log. Other conditions like the damage of snapshot files still need further support.

### View Region properties

- To view in local the properties of Region 2 on the TiKV instance that is deployed in `/path/to/tikv`:

    ```shell
    tikv-ctl --data-dir /path/to/tikv/data region-properties -r 2
    ```

- To view online the properties of Region 2 on the TiKV instance that is running on `127.0.0.1:20160`:

    ```shell
    tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
    ```

### Modify the TiKV configuration dynamically

You can use the `modify-tikv-config` command to dynamically modify the configuration arguments. Currently, the TiKV configuration items that can be dynamically modified and the detailed modification are consistent with modifying configuration using SQL statements. For details, see [Modify TiKV configuration dynamically](/dynamic-config.md#modify-tikv-configuration-dynamically).

- `-n` is used to specify the full name of the configuration item. For the list of configuration items that can be modified dynamically, see [Modify TiKV configuration dynamically](/dynamic-config.md#modify-tikv-configuration-dynamically).
- `-v` is used to specify the configuration value.

Set the size of `shared block cache`:

```shell
tikv-ctl --host ip:port modify-tikv-config -n storage.block-cache.capacity -v 10GB
```

```
success
```

When `shared block cache` is disabled, set `block cache size` for the `write` CF:

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.writecf.block-cache-size -v 256MB
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftdb.defaultcf.disable-auto-compactions -v true
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftstore.sync-log -v false
```

```
success
```

When the compaction rate limit causes accumulated compaction pending bytes, disable the `rate-limiter-auto-tuned` mode or set a higher limit for the compaction flow:

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-limiter-auto-tuned -v false
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-bytes-per-sec -v "1GB"
```

```
success
```

### Force Regions to recover services from failure of multiple replicas (deprecated)

> **Warning:**
>
> It is not recommended to use this feature. Instead, you can use Online Unsafe Recovery in `pd-ctl` which provides one-stop automatic recovery capabilities. Extra operations such as stopping services are not needed. For detailed introduction, see [Online Unsafe Recovery](/online-unsafe-recovery.md).

You can use the `unsafe-recover remove-fail-stores` command to remove the failed machines from the peer list of Regions. Before running this command, you need to stop the service of the target TiKV store to release file locks.

The `-s` option accepts multiple `store_id` separated by comma and uses the `-r` flag to specify involved Regions. If you need to perform this operation on all Regions in a specific store, you can simply specify `--all-regions`.

> **Warning:**
>
> - If any misoperation is performed, it might be hard to recover the cluster. Be aware of the potential risks and avoid using this feature in a production environment.
> - If the `--all-regions` option is used, you are expected to run this command on all the remaining stores connected to the cluster. You need to ensure that these healthy stores stop providing services before recovering the damaged stores. Otherwise, the inconsistent peer lists in Region replicas will cause errors when you run `split-region` or `remove-peer`. This further causes inconsistency between other metadata, and finally, the Regions will become unavailable.
> - Once you have run `remove-fail-stores`, you cannot restart the removed nodes or add these nodes to the cluster. Otherwise, the metadata will be inconsistent, and finally, the Regions will be unavailable.

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 3 -r 1001,1002
```

```
success!
```

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

Then, after you restart TiKV, the Regions can continue providing services with the remaining healthy replicas. This command is commonly used when multiple TiKV stores are damaged or deleted.

> **Note:**
>
> - You are expected to run this command for all stores where the specified Regions' peers are located.
> - This command only supports the local mode. It prints `success!` when successfully run.

### Recover from MVCC data corruption

Use the `recover-mvcc` command in circumstances where TiKV cannot run normally caused by MVCC data corruption. It cross-checks 3 CFs ("default", "write", "lock") to recover from various kinds of inconsistency.

- Use the `-r` option to specify involved Regions by `region_id`.
- Use the `-p` option to specify PD endpoints.

```shell
tikv-ctl --data-dir /path/to/tikv recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **Note:**
>
> - This command only supports the local mode. It prints `success!` when successfully run.
> - The argument of the `-p` option specifies the PD endpoints without the `http` prefix. Specifying the PD endpoints is to query whether the specified `region_id` is validated or not.
> - You need to run this command for all stores where specified Regions' peers are located.

### Ldb Command

The `ldb` command line tool offers multiple data access and database administration commands. Some examples are listed below. For more information, refer to the help message displayed when running `tikv-ctl ldb` or check the documents from RocksDB.

Examples of data access sequence:

To dump an existing RocksDB in HEX:

```shell
tikv-ctl ldb --hex --db=/tmp/db dump
```

To dump the manifest of an existing RocksDB:

```shell
tikv-ctl ldb --hex manifest_dump --path=/tmp/db/MANIFEST-000001
```

You can specify the column family that your query is against using the `--column_family=<string>` command line.

`--try_load_options` loads the database options file to open the database. It is recommended to always keep this option on when the database is running. If you open the database with default options, the LSM-tree might be messed up, which cannot be recovered automatically.

### Dump encryption metadata

Use the `encryption-meta` subcommand to dump encryption metadata. The subcommand can dump two types of metadata: encryption info for data files, and the list of data encryption keys used.

To dump encryption info for data files, use the `encryption-meta dump-file` subcommand. You need to create a TiKV config file to specify `data-dir` for the TiKV deployment:

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"
```

The `--path` option can be used to specify an absolute or relative path to the data file of interest. The command might give empty output if the data file is not encrypted. If `--path` is not provided, encryption info for all data files will be printed.

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-file --path=/path/to/tikv/data/db/CURRENT
```

```
/path/to/tikv/data/db/CURRENT: key_id: 9291156302549018620 iv: E3C2FDBF63FC03BFC28F265D7E78283F method: Aes128Ctr
```

To dump data encryption keys, use the `encryption-meta dump-key` subcommand. In additional to `data-dir`, you also need to specify the current master key used in the config file. For how to config master key, refer to [Encryption-At-Rest](/encryption-at-rest.md). Also with this command, the `security.encryption.previous-master-key` config will be ignored, and the master key rotation will not be triggered.

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"

[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

Note if the master key is a AWS KMS key, `tikv-ctl` needs to have access to the KMS key. Access to a AWS KMS key can be granted to `tikv-ctl` via environment variable, AWS default config file, or IAM role, whichever is suitable. Refer to AWS document for usage.

The `--ids` option can be used to specified a list of comma-separated data encryption key ids to print. If `--ids` is not provided, all data encryption keys will be printed, along with current key id, which is the id of the latest active data encryption key.

When using the command, you will see a prompt warning that the action will expose sensitive information. Type "I consent" to continue.

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key
```

```
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
current key id: 9291156302549018620
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key --ids=9291156302549018620
```

```
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

> **Note:**
>
> The command will expose data encryption keys as plaintext. In production, DO NOT redirect the output to a file. Even deleting the output file afterward may not cleanly wipe out the content from disk.

### Print information related to damaged SST files

Damaged SST files in TiKV might cause TiKV processes to panic. Before TiDB v6.1.0, these files cause TiKV to panic immediately. Since TiDB v6.1.0, TiKV processes panic 1 hour after SST files are damaged.

To clean up the damaged SST files, you can run the `bad-ssts` command in TiKV Control to show the needed information. The following is an example command and output.

> **Note:**
>
> Before running this command, stop the running TiKV instance.

```shell
tikv-ctl --data-dir </path/to/tikv> bad-ssts --pd <endpoint>
```

```
--------------------------------------------------------
corruption info:
data/tikv-21107/db/000014.sst: Corruption: Bad table magic number: expected 9863518390377041911, found 759105309091689679 in data/tikv-21107/db/000014.sst

sst meta:
14:552997[1 .. 5520]['0101' seq:1, type:1 .. '7A7480000000000000FF0F5F728000000000FF0002160000000000FAFA13AB33020BFFFA' seq:2032, type:1] at level 0 for Column family "default"  (ID 0)
it isn't easy to handle local data, start key:0101

overlap region:
RegionInfo { region: id: 4 end_key: 7480000000000000FF0500000000000000F8 region_epoch { conf_ver: 1 version: 2 } peers { id: 5 store_id: 1 }, leader: Some(id: 5 store_id: 1) }

suggested operations:
tikv-ctl ldb --db=data/tikv-21107/db unsafe_remove_sst_file "data/tikv-21107/db/000014.sst"
tikv-ctl --db=data/tikv-21107/db tombstone -r 4 --pd <endpoint>
--------------------------------------------------------
corruption analysis has completed
```

From the output above, you can see that the information of the damaged SST file is printed first and then the meta-information is printed.

+ In the `sst meta` part, `14` means the SST file number; `552997` means the file size, followed by the smallest and largest sequence numbers and other meta-information.
+ The `overlap region` part shows the information of the Region involved. This information is obtained through the PD server.
+ The `suggested operations` part provides you suggestion to clean up the damaged SST file. You can take the suggestion to clean up files and restart the TiKV instance.
