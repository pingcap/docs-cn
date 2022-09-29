---
title: Maintain DM Clusters Using dmctl
summary: Learn how to maintain a DM cluster using dmctl.
aliases: ['/docs/tidb-data-migration/dev/manage-replication-tasks/']
---

# Maintain DM Clusters Using dmctl

> **Note:**
>
> For DM clusters deployed using TiUP, you are recommended to directly use [`tiup dmctl`](/dm/maintain-dm-using-tiup.md#dmctl) to maintain the clusters.

dmctl is a command line tool used to maintain DM clusters. It supports both the interactive mode and the command mode.

## Interactive mode

Enter the interactive mode to interact with DM-master:

> **Note:**
>
> The interactive mode does not support Bash features. For example, you need to directly pass string flags instead of passing them in quotes.

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261
```

```
Welcome to dmctl
Release Version: ${version}
Git Commit Hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Git Branch: release-x.x
UTC Build Time: yyyy-mm-dd hh:mm:ss
Go Version: go version gox.xx linux/amd64

» help
DM control

Usage:
  dmctl [command]

Available Commands:
  binlog          manage or show binlog operations
  binlog-schema   manage or show table schema in schema tracker
  check-task      Checks the configuration file of the task
  config          manage config operations
  decrypt         Decrypts cipher text to plain text
  encrypt         Encrypts plain text to cipher text
  help            Gets help about any command
  list-member     Lists member information
  offline-member  Offlines member which has been closed
  operate-leader  `evict`/`cancel-evict` the leader
  operate-source  `create`/`stop`/`show` upstream MySQL/MariaDB source
  pause-relay     Pauses DM-worker's relay unit
  pause-task      Pauses a specified running task or all (sub)tasks bound to a source
  purge-relay     Purges relay log files of the DM-worker according to the specified filename
  query-status    Queries task status
  resume-relay    Resumes DM-worker's relay unit
  resume-task     Resumes a specified paused task or all (sub)tasks bound to a source
  shard-ddl-lock  maintain or show shard-ddl locks information
  start-relay     Starts workers pulling relay log for a source
  start-task      Starts a task as defined in the configuration file
  stop-relay      Stops workers pulling relay log for a source
  stop-task       Stops a specified task or all (sub)tasks bound to a source
  transfer-source Transfers a upstream MySQL/MariaDB source to a free worker

Flags:
  -h, --help             Help for dmctl.
  -s, --source strings   MySQL Source ID.

Use "dmctl [command] --help" for more information about a command.
```

## Command mode

The command mode differs from the interactive mode in that you need to append the task operation right after the dmctl command. The parameters of the task operation in the command mode are the same as those in the interactive mode.

> **Note:**
>
> + A dmctl command must be followed by only one task operation.
> + Starting from v2.0.4, DM supports reading the `-master-addr` parameter from the environment variable `DM_MASTER_ADDR`.

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261 start-task task.yaml
./dmctl --master-addr 172.16.30.14:8261 stop-task task
./dmctl --master-addr 172.16.30.14:8261 query-status

export DM_MASTER_ADDR="172.16.30.14:8261"
./dmctl query-status
```

```
Available Commands:
  binlog          manage or show binlog operations
  binlog-schema   manage or show table schema in schema tracker
  check-task      Checks the configuration file of the task
  config          manage config operations
  decrypt         Decrypts cipher text to plain text
  encrypt         Encrypts plain text to cipher text
  help            Gets help about any command
  list-member     Lists member information
  offline-member  Offlines member which has been closed
  operate-leader  `evict`/`cancel-evict` the leader
  operate-source  `create`/`stop`/`show` upstream MySQL/MariaDB source
  pause-relay     Pauses DM-worker's relay unit
  pause-task      Pauses a specified running task or all (sub)tasks bound to a source
  purge-relay     Purges relay log files of the DM-worker according to the specified filename
  query-status    Queries task status
  resume-relay    Resumes DM-worker's relay unit
  resume-task     Resumes a specified paused task or all (sub)tasks bound to a source
  shard-ddl-lock  maintain or show shard-ddl locks information
  start-relay     Starts workers pulling relay log for a source
  start-task      Starts a task as defined in the configuration file
  stop-relay      Stops workers pulling relay log for a source
  stop-task       Stops a specified task or all (sub)tasks bound to a source
  transfer-source Transfers a upstream MySQL/MariaDB source to a free worker

Flags:
      --config string        Path to config file.
  -h, --help                 help for dmctl
      --master-addr string   Master API server address, this parameter is required when interacting with the dm-master
      --rpc-timeout string   RPC timeout, default is 10m. (default "10m")
  -s, --source strings       MySQL Source ID.
      --ssl-ca string        Path of file that contains list of trusted SSL CAs for connection.
      --ssl-cert string      Path of file that contains X509 certificate in PEM format for connection.
      --ssl-key string       Path of file that contains X509 key in PEM format for connection.
  -V, --version              Prints version and exit.

Use "dmctl [command] --help" for more information about a command.
```
