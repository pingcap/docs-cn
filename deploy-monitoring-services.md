---
title: Deploy Monitoring Services for the TiDB Cluster
summary: Learn how to deploy monitoring services for the TiDB cluster.
aliases: ['/docs/dev/deploy-monitoring-services/','/docs/dev/how-to/monitor/monitor-a-cluster/','/docs/dev/monitor-a-tidb-cluster/']
---

# Deploy Monitoring Services for the TiDB Cluster

This document is intended for users who want to manually deploy TiDB monitoring and alert services.

If you deploy the TiDB cluster using TiUP, the monitoring and alert services are automatically deployed, and no manual deployment is needed.

## Deploy Prometheus and Grafana

Assume that the TiDB cluster topology is as follows:

| Name  | Host IP | Services |
| :-- | :-- | :-------------- |
| Node1 | 192.168.199.113| PD1, TiDB, node_export, Prometheus, Grafana |
| Node2 | 192.168.199.114| PD2, node_export  |
| Node3 | 192.168.199.115| PD3, node_export |
| Node4 | 192.168.199.116| TiKV1, node_export |
| Node5 | 192.168.199.117| TiKV2, node_export |
| Node6 | 192.168.199.118| TiKV3, node_export |

### Step 1: Download the binary package

{{< copyable "shell-regular" >}}

```bash
# Downloads the package.
wget https://download.pingcap.org/prometheus-2.27.1.linux-amd64.tar.gz
wget https://download.pingcap.org/node_exporter-v1.3.1-linux-amd64.tar.gz
wget https://download.pingcap.org/grafana-7.5.11.linux-amd64.tar.gz
```

{{< copyable "shell-regular" >}}

```bash
# Extracts the package.
tar -xzf prometheus-2.27.1.linux-amd64.tar.gz
tar -xzf node_exporter-v1.3.1-linux-amd64.tar.gz
tar -xzf grafana-7.5.11.linux-amd64.tar.gz
```

### Step 2: Start `node_exporter` on Node1, Node2, Node3, and Node4

{{< copyable "shell-regular" >}}

```bash
cd node_exporter-v1.3.1-linux-amd64

# Starts the node_exporter service.
$ ./node_exporter --web.listen-address=":9100" \
    --log.level="info" &
```

### Step 3: Start Prometheus on Node1

Edit the Prometheus configuration file:

{{< copyable "shell-regular" >}}

```bash
cd prometheus-2.27.1.linux-amd64 &&
vi prometheus.yml
```

```ini
...

global:
  scrape_interval:     15s  # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s  # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default value (10s).
  external_labels:
    cluster: 'test-cluster'
    monitor: "prometheus"

scrape_configs:
  - job_name: 'overwritten-nodes'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:9100'
      - '192.168.199.114:9100'
      - '192.168.199.115:9100'
      - '192.168.199.116:9100'
      - '192.168.199.117:9100'
      - '192.168.199.118:9100'

  - job_name: 'tidb'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:10080'

  - job_name: 'pd'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:2379'
      - '192.168.199.114:2379'
      - '192.168.199.115:2379'

  - job_name: 'tikv'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.116:20180'
      - '192.168.199.117:20180'
      - '192.168.199.118:20180'

...

```

Start the Prometheus service:

```bash
$ ./prometheus \
    --config.file="./prometheus.yml" \
    --web.listen-address=":9090" \
    --web.external-url="http://192.168.199.113:9090/" \
    --web.enable-admin-api \
    --log.level="info" \
    --storage.tsdb.path="./data.metrics" \
    --storage.tsdb.retention="15d" &
```

### Step 4: Start Grafana on Node1

Edit the Grafana configuration file:

{{< copyable "shell-regular" >}}

```ini
cd grafana-7.5.11 &&
vi conf/grafana.ini

...

[paths]
data = ./data
logs = ./data/log
plugins = ./data/plugins
[server]
http_port = 3000
domain = 192.168.199.113
[database]
[session]
[analytics]
check_for_updates = true
[security]
admin_user = admin
admin_password = admin
[snapshots]
[users]
[auth.anonymous]
[auth.basic]
[auth.ldap]
[smtp]
[emails]
[log]
mode = file
[log.console]
[log.file]
level = info
format = text
[log.syslog]
[event_publisher]
[dashboards.json]
enabled = false
path = ./data/dashboards
[metrics]
[grafana_net]
url = https://grafana.net

...

```

Start the Grafana service:

{{< copyable "shell-regular" >}}

```bash
./bin/grafana-server \
    --config="./conf/grafana.ini" &
```

## Configure Grafana

This section describes how to configure Grafana.

### Step 1: Add a Prometheus data source

1. Log in to the Grafana Web interface.

    - Default address: [http://localhost:3000](http://localhost:3000)
    - Default account: admin
    - Default password: admin

    > **Note:**
    >
    > For the **Change Password** step, you can choose **Skip**.

2. In the Grafana sidebar menu, click **Data Source** within the **Configuration**.

3. Click **Add data source**.

4. Specify the data source information.

    - Specify a **Name** for the data source.
    - For **Type**, select **Prometheus**.
    - For **URL**, specify the Prometheus address.
    - Specify other fields as needed.

5. Click **Add** to save the new data source.

### Step 2: Import a Grafana dashboard

To import a Grafana dashboard for the PD server, the TiKV server, and the TiDB server, take the following steps respectively:

1. Click the Grafana logo to open the sidebar menu.

2. In the sidebar menu, click **Dashboards** -> **Import** to open the **Import Dashboard** window.

3. Click **Upload .json File** to upload a JSON file (Download TiDB Grafana configuration files from [pingcap/tidb](https://github.com/pingcap/tidb/tree/master/metrics/grafana), [tikv/tikv](https://github.com/tikv/tikv/tree/master/metrics/grafana), and [tikv/pd](https://github.com/tikv/pd/tree/master/metrics/grafana)).

    > **Note:**
    >
    > For the TiKV, PD, and TiDB dashboards, the corresponding JSON files are `tikv_summary.json`, `tikv_details.json`, `tikv_trouble_shooting.json`, `pd.json`, `tidb.json`, and `tidb_summary.json`.

4. Click **Load**.

5. Select a Prometheus data source.

6. Click **Import**. A Prometheus dashboard is imported.

## View component metrics

Click **New dashboard** in the top menu and choose the dashboard you want to view.

![view dashboard](/media/view-dashboard.png)

You can get the following metrics for cluster components:

+ **TiDB server:**

    - Query processing time to monitor the latency and throughput
    - The DDL process monitoring
    - TiKV client related monitoring
    - PD client related monitoring

+ **PD server:**

    - The total number of times that the command executes
    - The total number of times that a certain command fails
    - The duration that a command succeeds
    - The duration that a command fails
    - The duration that a command finishes and returns result

+ **TiKV server:**

    - Garbage Collection (GC) monitoring
    - The total number of times that the TiKV command executes
    - The duration that Scheduler executes commands
    - The total number of times of the Raft propose command
    - The duration that Raft executes commands
    - The total number of times that Raft commands fail
    - The total number of times that Raft processes the ready state
