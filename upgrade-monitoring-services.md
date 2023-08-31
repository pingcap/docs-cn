---
title: Upgrade Cluster Monitoring Services
summary: Learn how to upgrade the Prometheus, Grafana, and Alertmanager monitoring services for your TiDB cluster.
---

# Upgrade TiDB Cluster Monitoring Services

When deploying a TiDB cluster, TiUP automatically deploys monitoring services (such as Prometheus, Grafana, and Alertmanager) for the cluster. If you scale out this cluster, TiUP also automatically adds monitoring configurations for newly added nodes during the scaling. The monitoring services automatically deployed by TiUP are usually not the latest versions of these third-party monitoring services. To use the latest versions, you can follow this document to upgrade the monitoring services.

When managing a cluster, TiUP uses its own configurations to override the configurations of the monitoring services. If you directly upgrade the monitoring services by replacing their configuration files, any subsequent TiUP operations such as `deploy`, `scale-out`, `scale-in`, and `reload` on the cluster might overwrite your upgrade, leading to errors. To upgrade Prometheus, Grafana, and Alertmanager, follow the steps in this document rather than directly replacing configuration files.

> **Note:**
>
> - If your monitoring services are [deployed manually](/deploy-monitoring-services.md) instead of using TiUP, you can directly upgrade them without referring to this document.
> - The TiDB compatibility with newer versions of monitoring services has not been tested, so some features might not work as expected after the upgrade. For any issues, create an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - The upgrade steps in this document are applicable for TiUP version 1.9.0 and later. Therefore, check your TiUP version before the upgrade.
> - When you use TiUP to upgrade the TiDB cluster, TiUP will redeploy the monitoring services to the default version. You need to redo the upgrade for monitoring services after the TiDB upgrade. 

## Upgrade Prometheus

For better compatibility with TiDB, it is recommended to use the Prometheus installation package provided in the TiDB installation package. The version of Prometheus in the TiDB installation package is fixed. If you want to use a newer Prometheus version, refer to [Prometheus Release Notes](https://github.com/prometheus/prometheus/releases) for new features of each version and choose a suitable version for your production environment. You can also consult with PingCAP technical staff for a recommended version.

In the following upgrade steps, you need to download the Prometheus installation package of your desired version from the Prometheus website, and then use it to create a Prometheus package that TiUP can use.

### Step 1. Download a new Prometheus installation package from the Prometheus website

Download a new installation package from the [Prometheus download page](https://prometheus.io/download/) and extract it.

### Step 2. Download the Prometheus installation package provided by TiDB

1. Download the TiDB **Server Package** from the [TiDB download page](https://www.pingcap.com/download/) and extract it.
2. In the extracted files, locate `prometheus-v{version}-linux-amd64.tar.gz` and extract it.

    ```bash
    tar -xzf prometheus-v{version}-linux-amd64.tar.gz
    ```

### Step 3. Create a new Prometheus package that TiUP can use

1. Copy the files extracted in [Step 1](#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website), and then use the copied files to replace the files in the `./prometheus-v{version}-linux-amd64/prometheus` directory extracted in [Step 2](#step-2-download-the-prometheus-installation-package-provided-by-tidb).
2. Recompress the `./prometheus-v{version}-linux-amd64` directory and name the new compressed package as `prometheus-v{new-version}.tar.gz`, where `{new-version}` can be specified according to your need.

    ```bash
    cd prometheus-v{version}-linux-amd64.tar.gz
    tar -zcvf ../prometheus-v{new-version}.tar.gz ./
    ```

### Step 4. Upgrade Prometheus using the newly created Prometheus package

Execute the following command to upgrade Prometheus:

```bash
tiup cluster patch <cluster-name> prometheus-v{new-version}.tar.gz -R prometheus
```

After the upgrade, you can go to the home page of the Prometheus server (usually at `http://<Prometheus-server-host-name>:9090`), click **Status** in the top navigation menu, and then open the **Runtime & Build Information** page to check the Prometheus version and confirm whether the upgrade is successful.

## Upgrade Grafana

For better compatibility with TiDB, it is recommended to use the Grafana installation package provided in the TiDB installation package. The version of Grafana in the TiDB installation package is fixed. If you want to use a newer Grafana version, refer to [Grafana Release Notes](https://grafana.com/docs/grafana/latest/whatsnew/) for new features of each version and choose a suitable version for your production environment. You can also consult with PingCAP technical staff for a recommended version.

In the following upgrade steps, you need to download the Grafana installation package of your desired version from the Grafana website, and then use it to create a Grafana package that TiUP can use.

### Step 1. Download a new Grafana installation package from the Grafana website

1. Download a new installation package from the [Grafana download page](https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1). You can choose either the `OSS` or `Enterprise` edition according to your needs.
2. Extract the downloaded package. 

### Step 2. Download the Grafana installation package provided by TiDB

1. Download the TiDB **Server Package** package from the [TiDB download page](https://www.pingcap.com/download) and extract it.
2. In the extracted files, locate `grafana-v{version}-linux-amd64.tar.gz` and extract it.

    ```bash
    tar -xzf grafana-v{version}-linux-amd64.tar.gz
    ```

### Step 3. Create a new Grafana package that TiUP can use

1. Copy the files extracted in [Step 1](#step-1-download-a-new-grafana-installation-package-from-the-grafana-website), and then use the copied files to replace the files in the `./grafana-v{version}-linux-amd64/` directory extracted in [Step 2](#step-2-download-the-grafana-installation-package-provided-by-tidb).
2. Recompress the `./grafana-v{version}-linux-amd64` directory and name the new compressed package as `grafana-v{new-version}.tar.gz`, where `{new-version}` can be specified according to your need.

    ```bash
    cd grafana-v{version}-linux-amd64.tar.gz
    tar -zcvf ../grafana-v{new-version}.tar.gz ./
    ```

### Step 4. Upgrade Grafana using the newly created Grafana package

Execute the following command to upgrade Grafana:

```bash
tiup cluster patch <cluster-name> grafana-v{new-version}.tar.gz -R grafana

```

After the upgrade, you can go to the home page of the Grafana server (usually at `http://<Grafana-server-host-name>:3000`), and then check the Grafana version on the page to confirm whether the upgrade is successful.

## Upgrade Alertmanager

The Alertmanager package in the TiDB installation package is directly from the Prometheus website. Therefore, when upgrading Alertmanager, you only need to download and install a new version of Alertmanager from the Prometheus website.

### Step 1. Download a new Alertmanager installation package from the Prometheus website

Download the `alertmanager` installation package from the [Prometheus download page](https://prometheus.io/download/#alertmanager).

### Step 2. Upgrade Alertmanager using the downloaded installation package

Execute the following command to upgrade Alertmanager:

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager
```

After the upgrade, you can go to the home page of the Alertmanager server (usually at `http://<Alertmanager-server-host-name>:9093`), click **Status** in the top navigation menu, and then check the Alertmanager version to confirm whether the upgrade is successful.