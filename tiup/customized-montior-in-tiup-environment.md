---
title: 自定义监控组件的配置
summary: 了解如何自定义 TiUP 管理的监控组件的配置。
---

# 自定义监控组件的配置

使用 TiUP 部署 TiDB 集群时，TiUP 会同时自动部署 Prometheus、Grafana 和 Alertmanager 等监控组件，并且在集群扩容中自动为新增节点添加监控配置。

如果需要自定义 Prometheus、Grafana 和 Alertmanager 等监控组件的配置，请参考本文在 TiDB 集群的拓扑配置 topology.yaml 文件中添加对应的配置项。

> **注意：**
> 
> - 在自定义监控组件的配置时，请勿直接修改监控组件的配置文件。因为在对集群进行 deploy/scale-out/scale-in/reload 等操作时，TiUP 会使用自己的配置参数覆盖监控组件的配置。
>
> - 如果监控组件不是由 TiUP 部署和管理，可以直接修改监控组件的配置文件，无需参考本文档。
>
> - 本文所述功能在 TiUP v1.9.0 及后续版本支持，使用本功能前请检查 TiUP 版本号。

## 自定义 Prometheus 配置

目前，TiUP 支持自定义 Prometheus 的 rule 配置和 scrape 配置。

### 自定义 Prometheus rule

1. 将自定义的 rule 配置文件放到 TiUP 所在机器的某个目录下。

2. 在 TiDB 集群的拓扑配置 topology.yaml 文件中，将自定义规则文件目录 rule_dir 设置为实际 rule 配置文件的目录。

以下为 topology.yaml 文件中的 monitoring_servers 配置示例:

```
# # Server configs are used to specify the configuration of Prometheus Server.
monitoring_servers:
  # # The ip address of the Monitoring Server.
  - host: 127.0.0.1
    rule_dir: /home/tidb/prometheus_rule   # prometheus rule dir on TiUP machine
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 将读取**本机** /home/tidb/prometheus_rule 路径下的自定义 rule，然后将该配置发送到 Prometheus Server， 替换默认配置规则。

### 自定义 Prometheus scrape 配置

1. 打开 TiDB 集群的拓扑配置文件 topology.yaml。

2. 在 monitoring_servers 的配置部分添加 additional_scrape_conf 字段。

以下为 topology.yaml 文件中的 monitoring_servers 配置示例:

```
monitoring_servers:
- host: xxxxxxx
  ssh_port: 22
  port: 9090
  deploy_dir: /tidb-deploy/prometheus-9090
  data_dir: /tidb-data/prometheus-9090
  log_dir: /tidb-deploy/prometheus-9090/log
  external_alertmanagers: []
  arch: amd64
  os: linux
  additional_scrape_conf:
    metric_relabel_configs:
      - source_labels: [__name__]
        separator: ;
        regex: tikv_thread_nonvoluntary_context_switches|tikv_thread_voluntary_context_switches|tikv_threads_io_bytes_total
        action: drop
      - source_labels: [__name__,name]
        separator: ;
        regex: tikv_thread_cpu_seconds_total;(tokio|rocksdb).+
        action: drop
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 会将 additional_scrape_conf 字段的内容会添加到 Prometheus 配置文件的对应参数中。

## 自定义 Grafana 配置

目前，TiUP 支持自定义 Grafana Dashboard 和其他配置。

### 自定义 Grafana Dashboard

1. 将自定义的 Dashboard 配置文件放到 TiUP 所在机器的某个目录下。

2. 在 TiDB 集群的拓扑配置 topology.yaml 文件中，将自定义规则文件目录 dashboard_dir 设置为实际放置 Dashboard 配置文件的目录。

以下为 topology.yaml 文件中的 monitoring_servers 配置示例：

```
# # Server configs are used to specify the configuration of Grafana Servers.
grafana_servers:
  # # The ip address of the Grafana Server.
  - host: 127.0.0.1
    dashboard_dir: /home/tidb/dashboards   # grafana dashboard dir on TiUP machine
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 将读取**本机** /home/tidb/dashboards 路径下的自定义 Dashboard ，然后将该配置发送到 Grafana Server， 替换默认配置规则。

### 自定义 Grafana 其他配置

1. 打开集群配置文件 topology.yaml。

2. 在 grafana_servers 的配置部分添加其他配置。

以下为 topology.yaml 文件中的 [log.file] level 字段以及 smtp 配置示例：

```
# # Server configs are used to specify the configuration of Grafana Servers.
grafana_servers:
  # # The ip address of the Grafana Server.
  - host: 127.0.0.1
    config:
      log.file.level: warning
      smtp.enabled: true
      smtp.host: {IP}:{port}
      smtp.user: example@pingcap.com
      smtp.password: {password}
      smtp.skip_verify: true
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 会将 config 字段的内容会添加到 grafana 的配置文件 grafana.ini 中。

## 自定义 Alertmanager 配置

目前，TiUP 支持自定义配置 Alertmanager 的监听地址。

TiUP 部署的 Alertmanager 默认监听 alertmanager_servers.host，如果你使用代理，则无法访问 Alertmanager。此时，你可以在集群配置文件 topology.yaml 中添加 listen_host 指定监听地址，使得 Alertmanager 可以通过代理访问。 推荐配置为 0.0.0.0。

以下示例将 listen_host 字段设置为 `0.0.0.0`。

```
alertmanager_servers:
  # # The ip address of the Alertmanager Server.
  - host: 172.16.7.147
    listen_host: 0.0.0.0
    # # SSH port of the server.
    ssh_port: 22
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 会将 listen_host 字段的内容会添加到 Alertmanager 启动参数的 '--web.listen-address' 中。
