---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy a local TiDB cluster using the playground component of TiUP.
aliases: ['/docs/dev/tiup/tiup-playground/','/docs/dev/reference/tools/tiup/playground/']
---

# Quickly Deploy a Local TiDB Cluster

The TiDB cluster is a distributed system that consists of multiple components. A typical TiDB cluster consists of at least three PD nodes, three TiKV nodes, and two TiDB nodes. If you want to have a quick experience on TiDB, you might find it time-consuming and complicated to manually deploy so many components. This document introduces the playground component of TiUP and how to use it to quickly build a local TiDB test environment.

## TiUP playground overview

The basic usage of the playground component is shown as follows:

```bash
tiup playground [version] [flags]
```

If you directly execute the `tiup playground` command, TiUP uses the locally installed TiDB, TiKV, and PD components or installs the stable version of these components to start a TiDB cluster that consists of one TiKV instance, one TiDB instance, and one PD instance.

This command actually performs the following operations:

- Because this command does not specify the version of the playground component, TiUP first checks the latest version of the installed playground component. Assume that the latest version is v1.5.0, then this command works the same as `tiup playground:v1.5.0`.
- If you have not used TiUP playground to install the TiDB, TiKV, and PD components, the playground component installs the latest stable version of these components, and then start these instances.
- Because this command does not specify the version of the TiDB, PD, and TiKV component, TiUP playground uses the latest version of each component by default. Assume that the latest version is v5.0.0, then this command works the same as `tiup playground:v1.5.0 v5.1.0`.
- Because this command does not specify the number of each component, TiUP playground, by default, starts a smallest cluster that consists of one TiDB instance, one TiKV instance, and one PD instance.
- After starting each TiDB component, TiUP playground reminds you that the cluster is successfully started and provides you some useful information, such as how to connect to the TiDB cluster through the MySQL client and how to access the [TiDB Dashboard](/dashboard/dashboard-intro.md).

The command-line flags of the playground component are described as follows:

```bash
Flags:
      --db int                   TiDB instance number (default 1)
      --db.binpath string        TiDB instance binary path
      --db.config string         TiDB instance configuration file
      --db.host host             Set the listening address of TiDB
      --drainer int              Set the Drainer data of the cluster
      --drainer.binpath string   Specify the location of the Drainer binary files (optional, for debugging)
      --drainer.config string    Specify the Drainer configuration file
  -h, --help                     help for tiup
      --host string              Playground cluster host (default "127.0.0.1")
      --kv int                   TiKV instance number (default 1)
      --kv.binpath string        TiKV instance binary path
      --kv.config string         TiKV instance configuration file
      --monitor                  Start prometheus component
      --pd int                   PD instance number (default 1)
      --pd.binpath string        PD instance binary path
      --pd.config string         PD instance configuration file
      --pump int                 Specify the number of Pump nodes in the cluster. If the value is not "0", TiDB Binlog is enabled.
      --pump.binpath string      Specify the location of the Pump binary files (optional, for debugging)
      --pump.config string       Specify the Pump configuration file (optional, for debugging)
      --tiflash int              TiFlash instance number
      --tiflash.binpath string   TiFlash instance binary path
      --tiflash.config string    TiFlash instance configuration file
```

## Examples

### Use the nightly version to start a TiDB cluster

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly
```

In the command above, `nightly` is the version number of the cluster. Similarly, you can replace `nightly` with `v5.1.0`, and the command is `tiup playground v5.1.0`.

### Start a cluster with monitor

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly --monitor
```

This command starts Prometheus on port 9090 to display the time series data in the cluster.

### Override PD's default configuration

First, you need to copy the [PD configuration template](https://github.com/pingcap/pd/blob/master/conf/config.toml). Assume you place the copied file to `~/config/pd.toml` and make some changes according to your need, then you can execute the following command to override PD's default configuration:

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config ~/config/pd.toml
```

### Replace the default binary files

By default, when playground is started, each component is started using the binary files from the official mirror. If you want to put a temporarily compiled local binary file into the cluster for testing, you can use the `--{comp}.binpath` flag for replacement. For example, execute the following command to replace the binary file of TiDB:

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.binpath /xx/tidb-server
```

### Start multiple component instances

By default, only one instance is started for each TiDB, TiKV, and PD component. To start multiple instances for each component, add the following flag:

{{< copyable "shell-regular" >}}

```shell
tiup playground v3.0.10 --db 3 --pd 3 --kv 3
```

## Quickly connect to the TiDB cluster started by playground

TiUP provides the `client` component, which is used to automatically find and connect to a local TiDB cluster started by playground. The usage is as follows:

{{< copyable "shell-regular" >}}

```shell
tiup client
```

This command provides a list of TiDB clusters that are started by playground on the current machine on the console. Select the TiDB cluster to be connected. After clicking <kbd>Enter</kbd>, a built-in MySQL client is opened to connect to TiDB.

## View information of the started cluster

{{< copyable "shell-regular" >}}

```shell
tiup playground display
```

The command above returns the following results:

```
Pid    Role     Uptime
---    ----     ------
84518  pd       35m22.929404512s
84519  tikv     35m22.927757153s
84520  pump     35m22.92618275s
86189  tidb     exited
86526  tidb     34m28.293148663s
86190  drainer  35m19.91349249s
```

## Scale out a cluster

The command-line parameter for scaling out a cluster is similar to that for starting a cluster. You can scale out two TiDB instances by executing the following command:

{{< copyable "shell-regular" >}}

```shell
tiup playground scale-out --db 2
```

## Scale in clusters

You can specify a `pid` in the `tiup playground scale-in` command to scale in the corresponding instance. To view the `pid`, execute `tiup playground display`.

{{< copyable "shell-regular" >}}

```shell
tiup playground scale-in --pid 86526
```
