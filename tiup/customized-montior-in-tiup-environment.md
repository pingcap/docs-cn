---
title: TiUP 管理下的监控组件的自定义配置
summary: 如何自定义 TiUP 管理的监控组件的配置
---

# TiUP 管理下的监控组件的自定义配置

使用 TiUP 部署的 TiDB 集群，集群中的监控组件（Promethues 和 Grafana）也由 TiUP 进行部署和管理，本文介绍如何对这些 TiUP 管理下的监控组件进行自定义配置。 
> **注意：**
> 对于非 TiUP 部署和管理监控组件的场景，可以直接修改监控组件的配置文件进行配置，无需参考本文档。

## 场景说明

 TiDB 使用开源时序数据库 Prometheus 作为监控和性能指标信息存储方案，使用 Grafana 作为可视化组件进行展示。
 TiUP 部署方式，会同时自动部署监控组件，并且在集群扩容中自动为新增节点添加监控配置。在 TiUP 部署方式中，TiUP 会使用自己的配置参数覆盖监控组件的配置，用户若直接修改监控组件的配置文件，修改的配置文件可能在集群的 deploy/scale-out/scale-in/reload 等操作中被覆盖，导致配置不生效。
 
 在TiUP 部署方式中，如果需要对 Promethues 和 Grafana 进行自定义配置，请参考本文的配置规则。

## 自定义 Prometheus 配置

目前 TiUP 可以支持自定义 Prometheus 的 rule 配置和 scrape 配置。

## 1. 自定义 Prometheus rule
TiUP 支持自定义 prometheus rule ，需要将自定义的 rule 配置文件放到 TiUP 所在机器的某个目录下， 并在 TiDB 集群的拓扑配置 topology.yaml 文件中设置自定义规则文件目录 rule_dir 为放置 rule 配置文件的目录。 

topology.yaml 文件中 monitoring_servers 的配置示例：

```
...
# # Server configs are used to specify the configuration of Prometheus Server.
monitoring_servers:
  # # The ip address of the Monitoring Server.
  - host: 127.0.0.1
    rule_dir: /home/tidb/prometheus_rule   # prometheus rule dir on TiUP machine
...
```

上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 将读取**本机** /home/tidb/prometheus_rule 路径下的自定义 rule ，然后将该配置发送到 Prometheus Server， 替换默认配置规则。


## 2. 自定义 Prometheus scrape 配置

在 TiDB 集群的拓扑配置 topology.yaml 文件中的 monitoring_servers 的配置部分添加 additional_scrape_conf 字段。

topology.yaml 文件中 monitoring_servers 的配置示例:
```
...
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
...
```
上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 会将 additional_scrape_conf 字段的内容会添加到 Prometheus 配置文件的对应参数中。

# 自定义 Grafana 配置

目前 TiUP 可以支持自定义 Grafana Dashboard 和其他配置。

## 1. 自定义 Grafana Dashboard

TiUP 支持自定义 Grafana Dashboard ，需要将自定义的 Dashboard 配置文件放到 TiUP 所在机器的某个目录下， 并在 TiDB 集群的拓扑配置 topology.yaml 文件中设置自定义规则文件目录 dashboard_dir 为放置 Dashboard 配置文件的目录。 

topology.yaml 文件中 monitoring_servers 的配置示例：

```
...
# # Server configs are used to specify the configuration of Grafana Servers.  
grafana_servers:
  # # The ip address of the Grafana Server.
  - host: 127.0.0.1
    dashboard_dir: /home/tidb/dashboards   # grafana dashboard dir on TiUP machine
...
```
上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 将读取**本机** /home/tidb/dashboards 路径下的自定义 Dashboard ，然后将该配置发送到 Grafana Server， 替换默认配置规则。

## 2. 自定义 Grafana 其他配置

当需要自定义 Grafana 的其他配置，不能直接修改 Grafana server 的配置文件（/usr/local/etc/grafana/grafana.ini）该文件会在集群进行 deploy/scale-out/scale-in/reload 操作时被 TiUP 重置。 需要将相关自定义配置写入集群配置文件 topology.yaml 中的 grafana_servers 的配置部分。

以下例子配置了 [log.file] level 字段以及 smtp 的相关配置项。

```
...
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
...
```
上述配置后，在集群进行 deploy/scale-out/scale-in/reload 操作时， TiUP 会将 config 字段的内容会添加到 grafana 的配置文件 grafana.ini 中。
