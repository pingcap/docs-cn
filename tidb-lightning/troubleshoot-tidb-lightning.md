---
title: Troubleshoot TiDB Lightning
summary: Learn the common problems you might encounter when you use TiDB Lightning and their solutions.
aliases: ['/docs/dev/troubleshoot-tidb-lightning/','/docs/dev/how-to/troubleshoot/tidb-lightning/','/docs/dev/tidb-lightning/tidb-lightning-misuse-handling/','/docs/dev/reference/tools/error-case-handling/lightning-misuse-handling/','/tidb/dev/tidb-lightning-misuse-handling','/tidb/dev/troubleshoot-tidb-lightning']
---

# Troubleshoot TiDB Lightning

This document summarizes the common problems you might encounter when you use TiDB Lightning and their solutions.

## Import speed is too slow

Normally it takes 2 minutes per thread for TiDB Lightning to import a 256 MB data file. If the speed is much slower than this, there is an error. You can check the time taken for each data file from the log mentioning `restore chunk … takes`. This can also be observed from metrics on Grafana.

There are several reasons why TiDB Lightning becomes slow:

**Cause 1**: `region-concurrency` is set too high, which causes thread contention and reduces performance.

1. The setting can be found from the start of the log by searching `region-concurrency`.
2. If TiDB Lightning shares the same machine with other services (for example, TiKV Importer), `region-concurrency` must be **manually** set to 75% of the total number of CPU cores.
3. If there is a quota on CPU (for example, limited by Kubernetes settings), TiDB Lightning may not be able to read this out. In this case, `region-concurrency` must also be **manually** reduced.

**Cause 2**: The table schema is too complex.

Every additional index introduces a new KV pair for each row. If there are N indices, the actual size to be imported would be approximately (N+1) times the size of the Dumpling output. If the indices are negligible, you may first remove them from the schema, and add them back using `CREATE INDEX` after the import is complete.

**Cause 3**: Each file is too large.

TiDB Lightning works the best when the data source is broken down into multiple files of size around 256 MB so that the data can be processed in parallel. If each file is too large, TiDB Lightning might not respond.

If the data source is CSV, and all CSV files have no fields containing newline control characters (U+000A and U+000D), you can turn on "strict format" to let TiDB Lightning automatically split the large files.

```toml
[mydumper]
strict-format = true
```

**Cause 4**: TiDB Lightning is too old.

Try the latest version. Maybe there is new speed improvement.

## The `tidb-lightning` process suddenly quits while running in background

It is potentially caused by starting `tidb-lightning` incorrectly, which causes the system to send a SIGHUP signal to stop the `tidb-lightning` process. In this situation, `tidb-lightning.log` usually outputs the following log:

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

It is not recommended to directly use `nohup` in the command line to start `tidb-lightning`. You can [start `tidb-lightning`](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning) by executing a script.

In addition, if the last log of TiDB Lightning shows that the error is "Context canceled", you need to search for the first "ERROR" level log. This "ERROR" level log is usually followed by "got signal to exit", which indicates that TiDB Lightning received an interrupt signal and then exited.

## The TiDB cluster uses lots of CPU resources and runs very slowly after using TiDB Lightning

If `tidb-lightning` abnormally exited, the cluster might be stuck in the "import mode", which is not suitable for production. The current mode can be retrieved using the following command:

{{< copyable "shell-regular" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

You can force the cluster back to "normal mode" using the following command:

{{< copyable "shell-regular" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightning reports an error

### `could not find first pair, this shouldn't happen`

This error occurs possibly because the number of files opened by TiDB Lightning exceeds the system limit when TiDB Lightning reads the sorted local files. In the Linux system, you can use the `ulimit -n` command to confirm whether the value of this system limit is too small. It is recommended that you adjust this value to `1000000` (`ulimit -n 1000000`) during the import.

### `checksum failed: checksum mismatched remote vs local`

**Cause**: The checksum of a table in the local data source and the remote imported database differ. This error has several deeper reasons. You can further locate the reason by checking the log that contains `checksum mismatched`.

The lines that contain `checksum mismatched` provide the information `total_kvs: x vs y`, where `x` indicates the number of key-value pairs (KV pairs) calculated by the target cluster after the import is completed, and `y` indicates the number of key-value pairs generated by the local data source.

- If `x` is greater, it means that there are more KV pairs in the target cluster.
    - It is possible that this table is not empty before the import and therefore affects the data checksum. It is also possible that TiDB Lightning has previously failed and shut down, but did not restart correctly.
- If `y` is greater, it means that there are more KV pairs in the local data source.
    - If the checksum of the target database is all 0, it means that no import has occurred. It is possible that the cluster is too busy to receive any data.
    - It is possible that the exported data contains duplicate data, such as the UNIQUE and PRIMARY KEYs with duplicate values, or that the downstream table structure is case-insensitive while the data is case-sensitive.
- Other possible reasons
    - If the data source is machine-generated and not backed up by Dumpling, make sure the data conforms to the table limits. For example, the AUTO_INCREMENT column needs to be positive and not 0.

**Solutions**:

1. Delete the corrupted data using `tidb-lightning-ctl`, check the table structure and the data, and restart TiDB Lightning to import the affected tables again.

    {{< copyable "shell-regular" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2. Consider using an external database to store the checkpoints (change `[checkpoint] dsn`) to reduce the target database's load.

3. If TiDB Lightning was improperly restarted, see also the "[How to properly restart TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)" section in the FAQ.

### `Checkpoint for … has invalid status:` (error code)

**Cause**: [Checkpoint](/tidb-lightning/tidb-lightning-checkpoints.md) is enabled, and TiDB Lightning or TiKV Importer has previously abnormally exited. To prevent accidental data corruption, TiDB Lightning will not start until the error is addressed.

The error code is an integer smaller than 25, with possible values of 0, 3, 6, 9, 12, 14, 15, 17, 18, 20, and 21. The integer indicates the step where the unexpected exit occurs in the import process. The larger the integer is, the later step the exit occurs at.

**Solutions**:

If the error was caused by invalid data source, delete the imported data using `tidb-lightning-ctl` and start Lightning again.

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

See the [Checkpoints control](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control) section for other options.

### `cannot guess encoding for input file, please convert to UTF-8 manually`

**Cause**: TiDB Lightning only recognizes the UTF-8 and GB-18030 encodings for the table schemas. This error is emitted if the file isn't in any of these encodings. It is also possible that the file has mixed encoding, such as containing a string in UTF-8 and another string in GB-18030, due to historical `ALTER TABLE` executions.

**Solutions**:

1. Fix the schema so that the file is entirely in either UTF-8 or GB-18030.

2. Manually `CREATE` the affected tables in the target database.

3. Set `[mydumper] character-set = "binary"` to skip the check. Note that this might introduce mojibake into the target database.

### `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'`

**Cause**: A table contains a column with the `timestamp` type, but the time value itself does not exist. This is either because of DST changes or the time value has exceeded the supported range (Jan 1, 1970 to Jan 19, 2038).

**Solutions**:

1. Ensure TiDB Lightning and the source database are using the same time zone.

    When executing TiDB Lightning directly, the time zone can be forced using the `$TZ` environment variable.

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2. Ensure the entire cluster is using the same and latest version of `tzdata` (version 2018i or above).

    On CentOS, run `yum info tzdata` to check the installed version and whether there is an update. Run `yum upgrade tzdata` to upgrade the package.

### `[Error 8025: entry too large, the max entry size is 6291456]`

**Cause**: A single row of key-value pairs generated by TiDB Lightning exceeds the limit set by TiDB.

**Solution**:

Currently, the limitation of TiDB cannot be bypassed. You can only ignore this table to ensure the successful import of other tables.

### Encounter `rpc error: code = Unimplemented ...` when TiDB Lightning switches the mode

**Cause**: Some node(s) in the cluster does not support `switch-mode`. For example, if the TiFlash version is earlier than `v4.0.0-rc.2`, [`switch-mode` is not supported](https://github.com/pingcap/tidb-lightning/issues/273).

**Solutions**:

- If there are TiFlash nodes in the cluster, you can update the cluster to `v4.0.0-rc.2` or higher versions.
- Temporarily disable TiFlash if you do not want to upgrade the cluster.

### `tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'`

TiDB Lightning Local-backend only supports importing data to TiDB clusters of v4.0.0 and later versions. If you try to use Local-backend to import data to a v2.x or v3.x cluster, the above error is reported. At this time, you can modify the configuration to use Importer-backend or TiDB-backend for data import.

Some `nightly` versions might be similar to v4.0.0-beta.2. These `nightly` versions of TiDB Lightning actually support Local-backend. If you encounter this error when using a `nightly` version, you can skip the version check by setting the configuration `check-requirements = false`. Before setting this parameter, make sure that the configuration of TiDB Lightning supports the corresponding version; otherwise, the import might fail.

### `restore table test.district failed: unknown columns in header [...]`

This error occurs usually because the CSV data file does not contain a header (the first row is not column names but data). Therefore, you need to add the following configuration to the TiDB Lightning configuration file:

```
[mydumper.csv]
header = false
```

### `Unknown character set`

TiDB does not support all MySQL character sets. Therefore, TiDB Lightning reports this error if an unsupported character set is used when creating the table schema during an import. To bypass this error, you can create the table schema in the downstream in advance using the [character sets supported by TiDB](/character-set-and-collation.md) according to the specific data.

### `invalid compression type ...`

- TiDB Lightning v6.4.0 and later versions only support the following compressed data files: `gzip`, `snappy`, and `zstd`. Other types of compressed files cause errors. If an unsupported compressed file exists in the directory where the source data file is stored, this will cause the task to report an error. You can move those unsupported files out of the import data directory to avoid such errors. For more details, see [Compressed files](/tidb-lightning/tidb-lightning-data-source.md#compressed-files).

> **Note:**
>
> The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
