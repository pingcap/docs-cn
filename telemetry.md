---
title: Telemetry
summary: Learn the telemetry feature, how to disable the feature and view its status.
aliases: ['/docs/dev/telemetry/']
---

# Telemetry

When the telemetry is enabled, TiDB, TiUP and TiDB Dashboard collect usage information and share the information with PingCAP to help understand how to improve the product. For example, this usage information helps prioritize new features.

> **Note:**
>
> - Starting from February 20, 2023, the telemetry feature is disabled by default in new versions of TiDB and TiDB Dashboard, including v6.6.0, and usage information is not collected and shared with PingCAP. Before upgrading to these versions, if the cluster uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. See [TiDB Release Timeline](/releases/release-timeline.md) for the specific version.
> - Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP, and usage information is not collected. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

## What is shared?

The following sections describe the shared usage information in detail for each component. The usage details that get shared might change over time. These changes (if any) will be announced in [release notes](/releases/release-notes.md).

> **Note:**
>
> In **ALL** cases, user data stored in the TiDB cluster will **NOT** be shared. You can also refer to [PingCAP Privacy Policy](https://pingcap.com/privacy-policy).

### TiDB

When the telemetry collection feature is enabled in TiDB, the TiDB cluster collects usage details on a 6-hour basis. These usage details include but are not limited to:

- A randomly generated telemetry ID.
- Deployment characteristics, such as the size of hardware (CPU, memory, disk), TiDB components versions, OS name.
- The status of query requests in the system, such as the number of query requests and the duration.
- Component usage, for example, whether the Async Commit feature is in use or not.
- Pseudonymized IP address of the TiDB telemetry data sender.

To view the full content of the usage information shared to PingCAP, execute the following SQL statement:

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB Dashboard

When the telemetry collection feature is enabled for TiDB Dashboard, usage details of the TiDB Dashboard web UI will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- User operation information, such as the name of the TiDB Dashboard web page accessed by the user.
- Browser and OS information, such as browser name, OS name, and screen resolution.

To view the full content of the usage information shared to PingCAP, use the [Network Activity Inspector of Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/network) or the [Network Monitor of Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor).

### TiUP

When the telemetry collection feature is enabled in TiUP, usage details of TiUP will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- Execution status of TiUP commands, such as whether the execution is successful and the execution duration.
- Deployment characteristics, such as the size of hardware, TiDB components versions, and deployment configuration names that have been modified.

To view the full content of the usage information shared to PingCAP, set the `TIUP_CLUSTER_DEBUG=enable` environment variable when executing the TiUP command. For example:

{{< copyable "shell-regular" >}}

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### TiSpark

> **Note:**
>
> Starting from v3.3, the telemetry collection is disabled by default in TiSpark, and usage information is not collected and shared with PingCAP.

When the telemetry collection feature is enabled for TiSpark, the Spark module will share the usage details of TiSpark, including (but not limited to):

- A randomly generated telemetry ID.
- Some configuration information of TiSpark, such as the read engine and whether streaming read is enabled.
- Cluster deployment information, such as the machine hardware information, OS information, and component version number of the node where TiSpark is located.

You can view TiSpark usage information that is collected in Spark logs. You can set the Spark log level to INFO or lower, for example:

```shell
cat {spark.log} | grep Telemetry report | tail -n 1
```

## Disable telemetry

### Disable TiDB telemetry at deployment

When the telemetry is enabled in existing TiDB clusters, you can configure [`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) on each TiDB instance to disable the TiDB telemetry collection on that instance, which does not take effect until you restart the cluster.

Detailed steps to disable telemetry in different deployment tools are listed below.

<details>
  <summary>Binary deployment</summary>

Create a configuration file `tidb_config.toml` with the following content:

{{< copyable "" >}}

```toml
enable-telemetry = false
```

Specify the `--config=tidb_config.toml` command-line parameter when starting TiDB for the configuration file above to take effect.

See [TiDB Configuration Options](/command-line-flags-for-tidb-configuration.md#--config) and [TiDB Configuration File](/tidb-configuration-file.md#enable-telemetry-new-in-v402) for details.

</details>

<details>
  <summary>Deployment using TiUP Playground</summary>

Create a configuration file `tidb_config.toml` with the following content:

{{< copyable "" >}}

```toml
enable-telemetry = false
```

When starting TiUP Playground, specify the `--db.config tidb_config.toml` command-line parameter for the configuration file above to take effect. For example:

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.config tidb_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>Deployment using TiUP Cluster</summary>

Modify the deployment topology file `topology.yaml` to add the following content:

{{< copyable "" >}}

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details>
  <summary>Deployment on Kubernetes via TiDB Operator</summary>

Configure `spec.tidb.config.enable-telemetry: false` in `tidb-cluster.yaml` or TidbCluster Custom Resource.

See [Deploy TiDB Operator on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator) for details.

> **Note:**
>
> This configuration item requires TiDB Operator v1.1.3 or later to take effect.

</details>

### Disable TiDB telemetry for deployed TiDB clusters

In existing TiDB clusters, you can also modify the system variable [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) to dynamically disable the TiDB telemetry collection:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

> **Note:**
>
> When you disable telemetry, the configuration file has a higher priority over system variable. That is, after telemetry collection is disabled by the configuration file, the value of the system variable will be ignored.

### Disable TiDB Dashboard telemetry

Configure [`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry) to disable the TiDB Dashboard telemetry collection on all PD instances. You need to restart the running clusters for the configuration to take effect.

Detailed steps to disable telemetry for different deployment tools are listed below.

<details>
  <summary>Binary deployment</summary>

Create a configuration file `pd_config.toml` with the following content:

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

Specify the `--config=pd_config.toml` command-line parameter when starting PD to take effect.

See [PD Configuration Flags](/command-line-flags-for-pd-configuration.md#--config) and [PD Configuration File](/pd-configuration-file.md#enable-telemetry) for details.

</details>

<details>
  <summary>Deployment using TiUP Playground</summary>

Create a configuration file `pd_config.toml` with the following content:

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

When starting TiUP Playground, specify the `--pd.config pd_config.toml` command-line parameter to take effect, for example:

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config pd_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>Deployment using TiUP Cluster</summary>

Modify the deployment topology file `topology.yaml` to add the following content:

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details>
  <summary>Deployment on Kubernetes via TiDB Operator</summary>

Configure `spec.pd.config.dashboard.enable-telemetry: false` in `tidb-cluster.yaml` or TidbCluster Custom Resource.

See [Deploy TiDB Operator on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator) for details.

> **Note:**
>
> This configuration item requires TiDB Operator v1.1.3 or later to take effect.

</details>

### Disable TiUP telemetry

To disable the TiUP telemetry collection, execute the following command:

{{< copyable "shell-regular" >}}

```shell
tiup telemetry disable
```

## Check telemetry status

For TiDB telemetry, execute the following SQL statement to check the telemetry status:

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

If the `DATA_PREVIEW` column in the execution result is empty, TiDB telemetry is disabled. If not, TiDB telemetry is enabled. You can also check when the usage information was shared previously according to the `LAST_STATUS` column and whether the sharing was successful or not.

For TiUP telemetry, execute the following command to check the telemetry status:

{{< copyable "shell-regular" >}}

```shell
tiup telemetry status
```

## Compliance

To meet compliance requirements in different countries or regions, the usage information is sent to servers located in different countries according to the IP address of the sender machine:

- For IP addresses from the Chinese mainland, usage information is sent to and stored on cloud servers in the Chinese mainland.
- For IP addresses from outside of the Chinese mainland, usage information is sent to and stored on cloud servers in the US.

See [PingCAP Privacy Policy](https://en.pingcap.com/privacy-policy/) for details.
