---
title: TiDB Lightning Command Line Flags
summary: Learn how to configure TiDB Lightning using command line flags.
---

# TiDB Lightning Command Line Flags

You can configure TiDB Lightning either using the configuration file or in command line. This document describes the command line flags of TiDB Lightning.

## Command line flags

### `tidb-lightning`

You can configure the following parameters using `tidb-lightning`:

| Parameter | Description | Corresponding configuration item |
| :---- | :---- | :---- |
| `--config <file>` | Read the global configuration from the file. If this parameter is not specified, TiDB Lightning uses the default configuration. | |
| `-V` | Print the program version. | |
| `-d <directory>` | Local directory or [external storage URL](/br/backup-and-restore-storages.md#url-format) of data files. | `mydumper.data-source-dir` |
| `-L <level>` | Log level: `debug`, `info`, `warn`, `error`, or `fatal`. `info` by default.| `lightning.level` |
| `-f <rule>` | [Table filter rules](/table-filter.md). Can be specified multiple times. | `mydumper.filter` |
| `--backend <backend>` | Select an import mode. `local` refers to [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md); `tidb` refers to [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md). | `tikv-importer.backend` |
| `--log-file <file>` | Log file path. By default, it is `/tmp/lightning.log.{timestamp}`. If set to '-', it means that the log files will be output to stdout. | `lightning.log-file` |
| `--status-addr <ip:port>` | Listening address of the TiDB Lightning server | `lightning.status-port` |
| `--importer <host:port>` | Address of TiKV Importer | `tikv-importer.addr` |
| `--pd-urls <host:port>` | PD endpoint address | `tidb.pd-addr` |
| `--tidb-host <host>` | TiDB server host | `tidb.host` |
| `--tidb-port <port>` | TiDB server port (default = 4000) | `tidb.port` |
| `--tidb-status <port>` | TiDB status port (default = 10080) | `tidb.status-port` |
| `--tidb-user <user>` | User name to connect to TiDB | `tidb.user` |
| `--tidb-password <password>` | Password to connect to TiDB. The password can either be plaintext or Base64 encoded. | `tidb.password` |
| `--enable-checkpoint <bool>` | Whether to enable checkpoints (default = true) | `checkpoint.enable` |
| `--analyze <level>` | Analyze tables after importing. Available values are "required", "optional" (default value), and "off". | `post-restore.analyze` |
| `--checksum <level>` | Compare checksum after importing. Available values are "required" (default value), "optional", and "off". | `post-restore.checksum` |
| `--check-requirements <bool>` | Check cluster version compatibility before starting (default = true) | `lightning.check-requirements` |
| `--ca <file>` | CA certificate path for TLS connection | `security.ca-path` |
| `--cert <file>` | Certificate path for TLS connection | `security.cert-path` |
| `--key <file>` | Private key path for TLS connection | `security.key-path` |
| `--server-mode` | Start TiDB Lightning in server mode | `lightning.server-mode` |

If you specify both a command line parameter and the corresponding setting in the configuration file, the command line parameter takes precedence. For example, running `./tidb-lightning -L debug --config cfg.toml` would always set the log level to "debug" regardless of the content of `cfg.toml`.

## `tidb-lightning-ctl`

All parameters of `tidb-lightning` apply to `tidb-lightning-ctl`. In addition, you can also configure the following parameters using `tidb-lightning-ctl`:

| Parameter | Description |
|:----|:----|
| `--compact` | Perform a full compaction. |
| `--switch-mode <mode>` | Switch every TiKV store to the given mode: normal or import. |
| `--fetch-mode` | Print the current mode of every TiKV store. |
| `--import-engine <uuid>` | Import the closed engine file from TiKV Importer into the TiKV cluster. |
| `--cleanup-engine <uuid>` | Delete the engine file from TiKV Importer. |
| `--checkpoint-dump <folder>` | Dump current checkpoint as CSVs into the folder. |
| `--checkpoint-error-destroy <table_name>` | Remove the checkpoint. If it causes an error, drop the table. |
| `--checkpoint-error-ignore <table_name>` | Ignore any error recorded in the checkpoint involving the given table. |
|`--checkpoint-remove <table_name>` | Unconditionally remove the checkpoint of the table. |

The `<table_name>` must either be a qualified table name in the form `` `db`.`tbl` `` (including the backquotes), or the keyword `all`.
