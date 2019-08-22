---
title: Monitor a TiDB Cluster in Kubernetes
summary: Learn how to monitor a TiDB cluster in kubernetes.
category: how-to
aliases: ['/docs/v3.0/how-to/monitor/tidb-in-kubernetes/']
---

# Monitor a TiDB Cluster in Kubernetes

Monitoring a TiDB cluster deployed in Kubernetes can be roughly divided into two parts:

- Monitoring the TiDB cluster itself
- Monitoring the Kubernetes cluster and TiDB Operator

This document gives a brief introduction to the two monitoring tasks.

## Monitor the TiDB cluster

You can monitor the TiDB cluster with Prometheus and Grafana. A separate monitoring system is created and configured for each TiDB cluster created by TiDB Operator. The monitoring system runs in the same Namespace as the TiDB cluster, and includes two components - Prometheus and Grafana.

The monitoring data is not persisted by default. If the monitoring container restarts for some reason, the existing monitoring data gets lost. To persist the monitoring data, you can set `monitor.persistent` to `true` in the `values.yaml` file. When you enable this option, you need to set `storageClass` to an existing storage in the current cluster, and this storage is required to support persisting data, otherwise there is still a risk of data loss.

For configuration details on the monitoring system, refer to [TiDB Cluster Monitoring](/how-to/monitor/monitor-a-cluster.md).

### View the monitoring dashboard

You can run the `kubectl port-forward` command to view the monitoring dashboard:

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward -n <namespace> svc/<release-name>-grafana 3000:3000 &>/tmp/portforward-grafana.log &
```

Then open [http://localhost:3000](http://localhost:3000) in your browser and log on with the default username and password `admin`.

The Grafana service is exposed by `NodePort` by default. If the Kubernetes cluster supports load balancer, you can change `monitor.grafana.service.type` to `LoadBalancer` in `values.yaml`. Then, after executing `helm upgrade`, access the dashboard through the load balancer.

If there is no need to use Grafana, you can save resources by setting `monitor.grafana.create` to `false` in `values.yaml` during deployment. In this case, you need to use other existing or newly deployed data visualization tools to directly access the monitoring data.

### Access the monitoring data

To access the monitoring data directly, run the `kubectl port-forward` command to access Prometheus:

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward -n <namespace> svc/<release-name>-prometheus 9090:9090 &>/tmp/portforward-prometheus.log &
```

Then open [http://localhost:9090](http://localhost:9090) in your browser or access this address via a client tool.

The Prometheus service is exposed by `NodePort` by default. If the Kubernetes cluster supports load balancer, you can change `monitor.prometheus.service.type` to `LoadBalancer` in `values.yaml`. Then, after executing `helm upgrade`, access the monitoring data through the load balancer.

## Monitor the Kubernetes cluster

The TiDB monitoring system deployed with the cluster only focuses on the operation of the TiDB components themselves, and does not include the monitoring of container resources, hosts, Kubernetes components, and TiDB Operator. Monitoring of these components or resources requires the deployment of a monitoring system across the entire Kubernetes cluster dimension.

### Monitor the host

Monitoring the host and its resources works in the same way as monitoring physical resources of a traditional server.

If you already have a monitoring system for your physical server in your existing infrastructure, you only need to add the host that holds Kubernetes to the existing monitoring system by conventional means; if there is no monitoring system available, or you want to deploy a separate monitoring system to monitor the host that holds Kubernetes, then you can use any monitoring system that you are familiar with.

The newly deployed monitoring system can run on a separate server, directly on the host that holds Kubernetes, or in a Kubernetes cluster. Different deployment methods might mean differences in the deployment configuration and resource utilization, but there are no major differences in usage.

Some common open source monitoring systems that can be used to monitor server resources are:

- [CollectD](https://collectd.org/)
- [Nagios](https://www.nagios.org/)
- [Prometheus](http://prometheus.io/) & [node_exporter](https://github.com/prometheus/node_exporter)
- [Zabbix](https://www.zabbix.com/)

Some cloud service providers or specialized performance monitoring service providers also have their own free or chargeable monitoring solutions that you can choose from.

It is recommended to deploy a host monitoring system in the Kubernetes cluster via [Prometheus Operator](https://github.com/coreos/prometheus-operator) based on [Node Exporter](https://github.com/prometheus/node_exporter) and Prometheus. This solution can also be compatible with and used for monitoring the Kubernetes' own components.

### Monitor Kubernetes components

For monitoring Kubernetes components, you can refer to the solutions provided in the [Kubernetes official documentation](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/) or use other Kubernetes-compatible monitoring systems.

Some cloud service providers may provide their own solutions for monitoring Kubernetes components, and some specialized performance monitoring service providers have their own Kubernetes integration solutions that you can choose from.

TiDB Operator is actually a container running in Kubernetes. For this reason, you can monitor TiDB Operator by choosing any monitoring system that can monitor the status and resources of a Kubernetes container without deploying additional monitoring components.

It is recommended to deploy a host monitoring system via [Prometheus Operator](https://github.com/coreos/prometheus-operator) based on [Node Exporter](https://github.com/prometheus/node_exporter) and Prometheus. This solution can also be compatible with and used for monitoring host resources.

## Alert configuration

### Alerts in the TiDB Cluster

When Prometheus is deployed with a TiDB cluster, some default alert rules are automatically imported. You can view all alert rules and statuses in the current system by accessing the Alerts page of Prometheus through a browser.

Currently, the custom configuration of alert rules is not supported. If you do need to modify the alert rules, you can manually download charts to modify them.

The default Prometheus and alert configuration do not support sending alert messages. To send an alert message, you can integrate Prometheus with any tool that supports Prometheus alerts. It is recommended to manage and send alert messages via [AlertManager](https://prometheus.io/docs/alerting/alertmanager/).

If you already have an available AlertManager service in your existing infrastructure, you can modify `monitor.prometheus.alertmanagerURL` in the `values.yaml` file and configure its address for use by Prometheus; if there is no AlertManager service available, or if you want to deploy a separate set of services, you can refer to [Prometheus official document](https://github.com/prometheus/alertmanager).

### Alerts in Kubernetes

If you deploy a monitoring system for Kubernetes hosts and services by Prometheus Operator, some alert rules are configured by default, and an AlertManager service is deployed. For details, see [kube-prometheus](https://github.com/coreos/).

If you monitor Kubernetes hosts and services by using other tools or services, you can consult the corresponding information provided by the tool or service provider.
