---
title: Export and Import Data Sources and Task Configuration of Clusters
summary: Learn how to export and import data sources and task configuration of clusters when you use DM.
---

# Export and Import Data Sources and Task Configuration of Clusters

`config` command is used to export and import data sources and task configuration of clusters.

> **Note:**
>
> For clusters earlier than v2.0.5, you can use dmctl v2.0.5 or later to export and import the data source and task configuration files.

{{< copyable "" >}}

```bash
» help config
Commands to import/export config
Usage:
  dmctl config [command]
Available Commands:
  export      Export the configurations of sources and tasks.
  import      Import the configurations of sources and tasks.
Flags:
  -h, --help   help for config
Global Flags:
  -s, --source strings   MySQL Source ID.
Use "dmctl config [command] --help" for more information about a command.
```

## Export the data source and task configuration of clusters

You can use `export` command to export the data source and task configuration of clusters to specified files.

{{< copyable "" >}}

```bash
config export [--dir directory]
```

### Parameter explanation

- `dir`:
    - optional
    - specifies the file path for exporting
    - the default value is `./configs`

### Returned results

{{< copyable "" >}}

```bash
config export -d /tmp/configs
```

```
export configs to directory `/tmp/configs` succeed
```

## import the data source and task configuration of clusters

You can use `import` command to import the data source and task configuration of clusters from specified files.

{{< copyable "" >}}

```bash
config import [--dir directory]
```

> **Note:**
>
> For clusters later than v2.0.2, currently, it is not supported to automatically import the configuration related to relay worker. You can use `start-relay` command to manually [start relay log](/dm/relay-log.md#enable-and-disable-relay-log).

### Parameter explanation

- `dir`:
    - optional
    - specifies the file path for importing
    - the default value is `./configs`

### Returned results

{{< copyable "" >}}

```bash
config import -d /tmp/configs
```

```
start creating sources
start creating tasks
import configs from directory `/tmp/configs` succeed
```
