---
title: Best Practices for Read-Only Storage Nodes
summary: Learn how to configure read-only storage nodes to physically isolate important online services.
---

# Best Practices for Read-Only Storage Nodes

This document introduces how to configure read-only storage nodes and how to direct backup, analysis, testing, and other traffic to these nodes. In this way, loads with high tolerance for delay can be physically isolated from important online services.

## Procedures

### 1. Specify some TiKV nodes as read-only

To specify some TiKV nodes as read-only, you can mark these nodes with a special label (use `$` as the prefix of the label key). Unless you explicitly specify these nodes to store some data using Placement Rules, PD does not schedule any data to these nodes.

You can configure a read-only node by running the `tiup cluster edit-config` command:

```
tikv_servers:
  - host: ...
    ...
    labels:
      $mode: readonly
```

### 2. Use Placement Rules to store data on read-only nodes as learners

1. Run the `pd-ctl config placement-rules` command to export the default Placement Rules:

    ```shell
    pd-ctl config placement-rules rule-bundle load --out="rules.json"
    ```

    If you have not configured Placement Rules before, the output is as follows:

    ```json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3
          }
        ]
      }
    ]
    ```

2. Store all data on the read-only nodes as a learner. The following example is based on the default configuration:

    ```json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3
          },
          {
            "group_id": "pd",
            "id": "readonly",
            "start_key": "",
            "end_key": "",
            "role": "learner",
            "count": 1,
            "label_constraints": [
              {
                "key": "$mode",
                "op": "in",
                "values": [
                  "readonly"
                ]
              }
            ],
            "version": 1
          }
        ]
      }
    ]
    ```

3. Use the `pd-ctl config placement-rules` command to write the preceding configurations to PD:

    ```shell
    pd-ctl config placement-rules rule-bundle save --in="rules.json"
    ```

> **Note:**
>
> - If you perform the preceding operations on a cluster with a large dataset, the entire cluster might need some time to completely replicate data to read-only nodes. During this period, the read-only nodes might not be able to provide services.
> - Because of the special implementation of backup, the learner number of each label cannot exceed 1. Otherwise, it will generate duplicate data during backup.

### 3. Use Follower Read to read data from read-only nodes

#### 3.1 Use Follower Read in TiDB

To read data from read-only nodes when using TiDB, you can set the system variable [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) to `learner`:

```sql
set tidb_replica_read=learner;
```

#### 3.2 Use Follower Read in TiSpark

To read data from read-only nodes when using TiSpark, you can set the configuration item `spark.tispark.replica_read` to `learner` in the Spark configuration file:

```
spark.tispark.replica_read learner
```

#### 3.3 Use Follower Read when backing up cluster data

To read data from read-only nodes when backing up cluster data, you can specify the `--replica-read-label` option in the br command line. Note that when running the following command in shell, you need to use single quotes to wrap the label to prevent `$` from being parsed.

```shell
br backup full ... --replica-read-label '$mode:readonly'
```
