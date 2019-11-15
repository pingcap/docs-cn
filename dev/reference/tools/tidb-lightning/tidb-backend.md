---
title: TiDB Lightning "TiDB" Back End
summary: Choose how to write data into the TiDB cluster.
category: reference
---

# TiDB Lightning "TiDB" Back End

TiDB Lightning supports two back ends: "Importer" and "TiDB". It determines how `tidb-lightning` delivers data into the target cluster.

The "Importer" back end (default) requires `tidb-lightning` to first encode the SQL or CSV data into KV pairs, and relies on the external `tikv-importer` program to sort these KV pairs and ingest directly into the TiKV nodes.

The "TiDB" back end requires `tidb-lightning` to encode these data into SQL `INSERT` statements, and has these statements executed directly on the TiDB node.

| Back end | "Importer" | "TiDB" |
|:---|:---|:---|
| Speed | Fast (~300 GB/hr) | Slow (~50 GB/hr) |
| Resource usage | High | Low |
| ACID respected while importing | No | Yes |
| Target tables | Must be empty | Can be populated |

## Deployment for "TiDB" back end

When using the "TiDB" back end, you no longer need `tikv-importer`. Compared with the [standard deployment procedure](/dev/reference/tools/tidb-lightning/deployment.md), the "TiDB" back end deployment has the following two differences:

* Steps involving `tikv-importer` can all be skipped.
* The configuration must be changed to indicate the "TiDB" back end is used.

### Ansible deployment

1. The `[importer_server]` section in `inventory.ini` can be left blank.

    ```ini
    ...

    [importer_server]
    # keep empty

    [lightning_server]
    192.168.20.10

    ...
    ```

2. The `tikv_importer_port` setting in `group_vars/all.yml` is ignored, and the file `group_vars/importer_server.yml` does not need to be changed. But you need to edit `conf/tidb-lightning.yml` and change the `backend` setting to `tidb`.

    ```yaml
    ...
    tikv_importer:
        backend: "tidb"   # <-- change this
    ...
    ```

3. Bootstrap and deploy the cluster as usual.

4. Mount the data source for TiDB Lightning as usual.

5. Start `tidb-lightning` as usual.

### Manual deployment

You do not need to download and configure `tikv-importer`.

Before running `tidb-lightning`, add the following lines into the configuration file:

```toml
[tikv-importer]
backend = "tidb"
```

or supplying the `--backend tidb` arguments when executing `tidb-lightning`.

## Conflict resolution

The "TiDB" back end supports importing to an already-populated table. However, the new data might cause a unique key conflict with the old data. You can control how to resolve the conflict by using this task configuration.

```toml
[tikv-importer]
backend = "tidb"
on-duplicate = "replace" # or "error" or "ignore"
```

| Setting | Behavior on conflict | Equivalent SQL statement |
|:---|:---|:---|
| replace | New entries replace old ones | `REPLACE INTO ...` |
| ignore | Keep old entries and ignore new ones | `INSERT IGNORE INTO ...` |
| error | Abort import | `INSERT INTO ...` |

## Migrating from Loader to TiDB Lightning "TiDB" back end

TiDB Lightning using the "TiDB" back end can completely replace functions of [Loader](/dev/reference/tools/loader.md). The following list shows how to translate Loader configurations into [TiDB Lightning configurations](/dev/reference/tools/tidb-lightning/config.md).

<table>
<thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thread>
<tbody>
<tr><td>

```toml

# logging
log-level = "info"
log-file = "loader.log"

# Prometheus
status-addr = ":8272"

# concurrency
pool-size = 16
```

</td><td>

```toml
[lightning]
# logging
level = "info"
file = "tidb-lightning.log"

# Prometheus
pprof-port = 8289

# concurrency (better left as default)
#region-concurrency = 16
```

</td></tr>
<tr><td>

```toml

# checkpoint database

checkpoint-schema = "tidb_loader"






```

</td><td>

```toml
[checkpoint]
# checkpoint storage
enable = true
schema = "tidb_lightning_checkpoint"
# by default the checkpoint is stored in
# a local file, which is more efficient.
# but you could still choose to store the
# checkpoints in the target database with
# this setting:
#driver = "mysql"
```

</td></tr>
<tr><td>

```toml



```

</td><td>

```toml
[tikv-importer]
# use the "TiDB" back end
backend = "tidb"
```

</td></tr>
<tr><td>

```toml

# data source directory
dir = "/data/export/"
```

</td><td>

```toml
[mydumper]
# data source directory
data-source-dir = "/data/export"
```

</td></tr>

<tr><td>

```toml
[db]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000

user = "root"
password = ""

#sql-mode = ""
```

</td><td>

```toml
[tidb]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000
status-port = 10080  # <- this is required
user = "root"
password = ""

#sql-mode = ""
```

</td></tr>
</tbody>
</table>
