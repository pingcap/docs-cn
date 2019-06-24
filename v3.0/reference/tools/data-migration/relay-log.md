---
title: Data Migration Relay Log
summary: Learn the directory structure, initial replication rules and data purge of DM relay logs.
category: reference
aliases: ['/docs/tools/dm/relay-log/'] 
---

# Data Migration Relay Log

The Data Migration (DM) relay log consists of a set of numbered files containing events that describe database changes, and an index file that contains the names of all used relay log files.

After DM-worker is started, it automatically replicates the upstream binlog to the local configuration directory (the default replication directory is `<deploy_dir>/relay_log` if DM is deployed using `DM-Ansible`). When DM-worker is running, it replicates the upstream binlog to the local file in real time. Syncer, a processing unit of DM-worker, reads the binlog events of the local relay log in real time, transforms these events to SQL statements, and then replicates these statements to the downstream database.

This document introduces the directory structure, initial replication rules and data purge of DM relay logs.

## Directory structure

An example of the directory structure of the local storage for a relay log:

```
<deploy_dir>/relay_log/
|-- 7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   |-- mysql-bin.000004
|   `-- relay.meta
|-- 842965eb-091c-11e9-9e45-9a3bff03fa39.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index
```

- `subdir`: 

    - DM-worker stores the binlog replicated from the upstream database in the same directory. Each directory is a `subdir`.

    - `subdir` is named `<Upstream database UUID>.<Local subdir serial number>`.

    - After [a switch between master and slave instances](/reference/tools/data-migration/cluster-operations.md#switch-between-master-and-slave-instances) in the upstream, DM-worker generates a new `subdir` directory with an incremental serial number.
    
        - In the above example, for the `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001` directory, `7e427cc0-091c-11e9-9e45-72b7c59d52d7` is the upstream database UUID and `000001` is the local `subdir` serial number.

- `server-uuid.index`: Records a list of names of currently available `subdir` directory.

- `relay.meta`: Stores the information of the replicated binlog in each `subdir`. For example,

    ```bash
    $ cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    binlog-name = "mysql-bin.000010"                            # The name of the currently replicated binlog.
    binlog-pos = 63083620                                       # The position of the currently replicated binlog.
    binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # GTID of the currently replicated binlog.
                                                                # There might be multiple GTIDs.
    $ cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    binlog-name = "mysql-bin.018393"
    binlog-pos = 277987307
    binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"
    ```

## Initial replication rules

For each start of DM-worker (or the relay log resuming replication after a pause), the starting position of replication includes the following conditions:

- If a valid local relay log (a valid relay log is a relay log with valid `server-uuid.index`, `subdir` and `relay.meta` files), DM-worker resumes replication from a position recorded by `relay.meta`.

- If a valid local relay log does not exist, and `relay-binlog-name` or `relay-binlog-gtid` is not specified in the DM configuration file:

    - In the non-GTID mode, DM-worker starts replication from the initial upstream binlog and replicates all the upstream binlog files to the latest successively.

    - In the GTID mode, DM-worker starts replication from the initial upstream GTID. 
    
        > **Note:**
        >
        > If the upstream relay log is purged, an error occurs. In this case, set `relay-binlog-gtid` to specify the starting position of replication.

- If a valid local relay log does not exist:

    - In the non-GTID mode, if `relay-binlog-name` is specified, DM-worker starts replication from the specified binlog file.
    - In the GTID mode, if `relay-binlog-gtid` is specified, DM-worker starts replication from the specified GTID.

## Data purge

Through the detection mechanism of reading and writing files, DM-worker does not purge the relay log that is being used or will be used later by the currently running task.

The data purge methods for the relay log include automatic purge and manual purge.

### Automatic data purge

Automatic data purge includes three configuration items in the DM-worker configuration file:

- `purge-interval`
    
    - The interval of automatic purge in the background, in seconds.
    - "3600" by default, indicating a background purge task is performed every 3600 seconds.

- `purge-expires`

    - The number of hours that a non-updated relay log can be retained for before being purged in the automatic background purge.
    - "0" by default, indicating data purge is not performed according to the update time of the relay log.

- `purge-remain-space`

    - The amount of remaining disk space in GB less than which the specified DM-worker machine tries to purge the relay log that can be purged securely in the automatic background purge. If it is set to `0`, data purge is not performed according to the remaining disk space.
    - "15" by default, indicating when the available disk space is less than 15GB, DM-master tries to purge the relay log securely.

### Manual data purge

Manual data purge means using the `purge-relay` command provided by dmctl to specify `subdir` and the binlog name thus to purge all the relay logs before the specified binlog.

Assuming that the directory structure of the current relay log is as follows:

```
$ tree .
.
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   `-- relay.meta
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
|   |-- mysql-bin.000001
|   `-- relay.meta
|-- e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index

$ cat server-uuid.index
deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
```

If you use dmctl to execute the following commands, the corresponding results are as follows:

```
# The `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001` directory is purged,
# while `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` and `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` directories are retained.

» purge-relay -w 10.128.16.223:10081 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002

# The `deb76a2b-09cc-11es9-9129-5242cf3bb246.000001、e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` directory is purged,
# while the `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` directory is retained.

» purge-relay -w 10.128.16.223:10081 --filename mysql-bin.000001
```
