---
title: TiDB-Lightning Troubleshooting
summary: Learn about common errors and solutions of TiDB-Lightning.
category: tools
---

# TiDB-Lightning Troubleshooting

When Lightning encounters an unrecoverable error, it exits with nonzero exit code and leaves the reason in the log file. Errors are typically printed at the end of the log. You can also search for the string `[error]` to look for non-fatal errors.

This document summarizes some commonly encountered errors in the `tidb-lightning` log file and their solutions.

## Import speed is too slow

Normally it takes Lightning 2 minutes per thread to import a 256 MB data file. It is an error if the speed is much slower than this. The time taken for each data file can be checked from the log mentioning `restore chunk … takes`. This can also be observed from metrics on Grafana.

There are several reasons why Lightning becomes slow:

**Cause 1**: `region-concurrency` is too high, which causes thread contention and reduces performance.

1. The setting can be found from the start of the log by searching `region-concurrency`.
2. If Lightning shares the same machine with other services (e.g. Importer), `region-concurrency` must be **manually** set to 75% of the total number of CPU cores
3. If there is a quota on CPU (e.g. limited by K8s settings), Lightning may not be able to read this out. In this case, `region-concurrency` must also be **manually** reduced.

**Cause 2**: The table is too complex.

Every additional index will introduce a new KV pair for each row. If there are N indices, the actual size to be imported would be approximately (N+1) times the size of the mydumper output. If the indices are negligible, you may first remove them from the schema, and add them back via `CREATE INDEX` after import is complete.

**Cause 3**: Lightning is too old.

Try the latest version! Maybe there is new speed improvement.

## checksum failed: checksum mismatched remote vs local

**Cause**: The checksum of a table in the local data source and the remote imported database differ. This error has several deeper reasons:

1. The table might already have data before. These old data can affect the final checksum.

2. If the remote checksum is 0, which means nothing is imported, it is possible that the cluster is too hot and fails to take in any data.

3. If the data is mechanically generated, ensure it respects the constrains of the table:

    * `AUTO_INCREMENT` columns need to be positive, and do not contain the value "0".
    * The UNIQUE and PRIMARY KEYs must have no duplicated entries.

**Solutions**:

1. Delete the corrupted data with via `tidb-lightning-ctl`, and restart Lightning to import the affected tables again.

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2. Consider using an external database to store the checkpoints (change `[checkpoint] dsn`) to reduce the target database's load.

## Checkpoint for … has invalid status: 18

**Cause**: [Checkpoint](../../tools/lightning/checkpoints.md) is enabled, and Lightning or Importer has previously abnormally exited. To prevent accidental data corruption, Lightning will not start until the error is addressed.

**Solutions**:

If the error was caused by invalid data source, delete the imported data using `tidb-lightning-ctl` and start Lightning again.

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

See the [Checkpoints control](../../tools/lightning/checkpoints.md#checkpoints-control) section for other options.

## ResourceTemporarilyUnavailable("Too many open engines …: 8")

**Cause**: The number of concurrent engine files exceeds the limit imposed by `tikv-importer`. This could be caused by misconfiguration. Additionally, if `tidb-lightning` exited abnormally, an engine file might be left at a dangling open state, which could cause this error as well.

**Solutions**:

1. Increase the value of `max-open-engines` setting in `tikv-importer.toml`. This value is typically dictated by the available memory. This could be calculated as:

    Max Memory Usage ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2. Decrease the value of `table-concurrency` + `index-concurrency` so it is less than `max-open-engines`.

3. Restart `tikv-importer` to forcefully remove all engine files (default to `./data.import/`). This also removes all partially imported tables, thus it is required to clear the outdated checkpoints.

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## cannot guess encoding for input file, please convert to UTF-8 manually

**Cause**: Lightning only recognizes the UTF-8 and GB-18030 encodings for the table schemas. This error is emitted if the file isn't in any of these encodings. It is also possible that the file has mixed encoding, such as containing a string in UTF-8 and another string in GB-18030, due to historical `ALTER TABLE` executions.

**Solutions**:

1. Fix the schema so that the file is entirely in either UTF-8 or GB-18030.

2. Manually `CREATE` the affected tables in the target database, and then set `[mydumper] no-schema = true` to skip automatic table creation.

3. Set `[mydumper] character-set = "binary"` to skip the check. Note that this might introduce mojibake into the target database.

## [sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'

**Cause**: A table contains a column with the `timestamp` type, but the time value itself does not exist. This is either because of DST changes or the time value has exceeded the supported range (1970 Jan 1st to 2038 Jan 19th).

**Solutions**:

1. Ensure Lightning and the source database are using the same time zone. When deploying via TiDB-Ansible, the timezone is defined in `inventory.ini`.

    ```ini
    # inventory.ini
    [all:vars]
    timezone = Asia/Shanghai
    ```

    When executing Lightning directly, the time zone can be forced using the `$TZ` environment variable.

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2. When exporting data using mydumper, make sure to include the `--skip-tz-utc` flag.
