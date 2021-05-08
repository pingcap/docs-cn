---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
---

# Topology Configuration File for DM Cluster Deployment Using TiUP

To deploy or scale a TiDB Data Migration (DM) cluster, you need to provide a topology file ([sample](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/dm/topology.example.yaml)) to describe the cluster topology. 

Similarly, to modify the cluster topology, you need to modify the topology file. The difference is that, after the cluster is deployed, you can only modify a part of the fields in the topology file. This document introduces each section of the topology file and each field in each section.

## File structure

A topology configuration file for DM cluster deployment using TiUP might contain the following sections:

- [global](#global): the cluster's global configuration. Some of the configuration items use the default values of the cluster, and you can configure them separately in each instance.
- [server_configs](#server_configs): the components' global configuration. You can configure each component separately. If an instance has a configuration item with the same key, the instance's configuration item will take effect.
- [master_servers](#master_servers): the configuration of the DM-master instance. The configuration specifies the machines to which the master service of the DM component is deployed.
- [worker_servers](#worker_servers): the configuration of the DM-worker instance. The configuration specifies the machines to which the worker service of the DM component is deployed.
- [monitoring_servers](#monitoring_servers): specifies the machines to which the Prometheus instances are deployed. TiUP supports deploying multiple Prometheus instances but only the first instance is used.
- [grafana_servers](#grafana_servers): the configuration of the Grafana instances. The configuration specifies the machines to which the Grafana instances are deployed.
- [alertmanager_servers](#alertmanager_servers): the configuration of the Alertemanager instances. The configuration specifies the machines to which the Alertmanager instances are deployed.

### `global`

The `global` section corresponds to the cluster's global configuration and has the following fields:

- `user`: the user to start the deployed cluster. The default value is "tidb". If the user specified in the `<user>` field does not exist on the target machine, TiUP will automatically try to create the user.
- `group`: the user group to which a user belongs when the user is automatically created. The default value is the same as the `<user>` field. If the specified group does not exist, it will be created automatically.
- `ssh_port`: the SSH port to connect to the target machine for operations. The default value is "22".
- `deploy_dir`: the deployment directory for each component. The default value is "deploy". The construction rules are as follows:
    - If the absolute path `deploy_dir` is configured at the instance level, the actual deployment directory is the `deploy_dir` configured for the instance.
    - For each instance, if you do not configure `deploy_dir`, the default value is the relative path `<component-name>-<component-port>`.
    - If `global.deploy_dir` is set to an absolute path, the component is deployed to the `<global.deploy_dir>/<instance.deploy_dir>` directory.
    - If `global.deploy_dir` is set to a relative path, the component is deployed to the `/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>` directory.
- `data_dir`: the data directory. The default value is "data". The construction rules are as follows.
    - If the absolute path `data_dir` is configured at the instance level, the actual data directory is the `data_dir` configured for the instance.
    - For each instance, if `data_dir` is not configured, the default value is `<global.data_dir>`.
    - If `data_dir` is set to a relative path, the component data is stored in `<deploy_dir>/<data_dir>`. For the construction rules of `<deploy_dir>`, see the construction rules of the `deploy_dir` field.
- `log_dir`: the data directory. The default value is "log". The construction rules are as follows.
    - If the absolute path of `log_dir` is configured at the instance level, the actual log directory is the `log_dir` configured for the instance.
    - For each instance, if `log_dir` is not configured by the user, the default value is `<global.log_dir>`.
    - If `log_dir` is a relative path, the component logs will be stored in `<deploy_dir>/<log_dir>`. For the construction rules of `<deploy_dir>`, see the construction rules of the `deploy_dir` field.
- `os`: the operating system of the target machine. The field controls which operating system to adapt to for the components pushed to the target machine. The default value is "linux".
- `arch`: the CPU architecture of the target machine. The field controls which platform to adapt to for the binary packages pushed to the target machine. The supported values are "amd64" and "arm64". The default value is "amd64".
- `resource_control`: runtime resource control. All configurations in this field are written to the service file of systemd. There is no limit by default. The resources that can be controlled are as follows:
    - `memory_limit`: limits the maximum memory at runtime. For example, "2G" means that the maximum memory of 2 GB can be used.
    - `cpu_quota`: limits the maximum CPU usage at runtime. For example, "200%".
    - `io_read_bandwidth_max`: limits the maximum I/O bandwidth for disk reads. For example, `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"`.
    - `io_write_bandwidth_max`: limits the maximum I/O bandwidth for disk writes. For example, `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"`.
    - `limit_core`: controls the size of core dump.

A `global` configuration example:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

In the example, the configuration specifies that the `tidb` user is used to start the cluster, and that each component is limited to a maximum of 2 GB of memory when it is running.

### `server_configs`

`server_configs` is used to configure services and to generate configuration files for each component. Similar to the `global` section, the configurations in the `server_configs` section can be overwritten by the configurations with the same keys in an instance. `server_configs` mainly contains the following fields:

- `master`: the configuration related to the DM-master service. For all the supported configuration items, see [DM-master Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/dm-master-configuration-file).
- `worker`: the configuration related to the DM-worker service, For all the supported configuration items, see [DM-worker Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-configuration-file).

A `server_configs` configuration example is as follows:

```yaml
server_configs:
  master:
    log-level: info
    rpc-timeout: "30s"
    rpc-rate-limit: 10.0
    rpc-rate-burst: 40
  worker:
    log-level: info
```

## `master_servers`

`master_servers` specifies the machines to which the master node of the DM component is deployed. You can also specify the service configuration on each machine. `master_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` section is used.
- `name`: specifies the name of the DM-master instance. The name must be unique for different instances. Otherwise, the cluster cannot be deployed.
- `port`: specifies the port on which DM-master provides services. The default value is "8261".
- `peer_port`: specifies the port for communication between DM-masters. The default value is "8291".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` section.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` section.
- `log_dir`: specifies the log directory. If the field is not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` section.
- `numa_node`: allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is a string type. The field value is the ID of the NUMA node, such as "0,1".
- `config`: the configuration rules of this field are the same as that of `master` in the `server_configs` section. If `config` is specified, the configuration of `config` will be merged with the configuration of `master` in `server_configs` (if the two fields overlap, the configuration of this field takes effect), and then the configuration file is generated and distributed to the machine specified in the `host` field.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` section.
- `arch`: the architecture of the machine specified in the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` section.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` section (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` section.
- `v1_source_path`: when upgrading from v1.0.x, you can specify the directory where the configuration file of the V1 source is located in this field.

In the `master_servers` section, the following fields cannot be modified after the deployment is completed: 

- `host`
- `name`
- `port`
- `peer_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`
- `v1_source_path`

A `master_servers` configuration example is as follows:

```yaml
master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    peer_port: 8291
    deploy_dir: "/dm-deploy/dm-master-8261"
    data_dir: "/dm-data/dm-master-8261"
    log_dir: "/dm-deploy/dm-master-8261/log"
    numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      rpc-timeout: "30s"
      rpc-rate-limit: 10.0
      rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
  - host: 10.0.1.19
    name: master3
```

## `worker_servers`

`worker_servers` specifies the machines to which the master node of the DM component is deployed. You can also specify the service configuration on each machine. `worker_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` section is used.
- `name`: specifies the name of the DM-worker instance. The name must be unique for different instances. Otherwise, the cluster cannot be deployed.
- `port`: specifies the port on which DM-worker provides services. The default value is "8262".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` section.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` section.
- `log_dir`: specifies the log directory. If the field is not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` section.
- `numa_node`: allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is a string type. The field value is the ID of the NUMA node, such as "0,1".
- `config`: the configuration rules of this field are the same as that of `worker` in the `server_configs` section. If `config` is specified, the configuration of `config` will be merged with the configuration of `worker` in `server_configs` (if the two fields overlap, the configuration of this field takes effect), and then the configuration file is generated and distributed to the machine specified in the `host` field.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` section.
- `arch`: the architecture of the machine specified in the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` section.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` section (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` section.

In the `worker_servers` section, the following fields cannot be modified after the deployment is completed: 

- `host`
- `name`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `worker_servers` configuration example is as follows:

```yaml
worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    deploy_dir: "/dm-deploy/dm-worker-8262"
    log_dir: "/dm-deploy/dm-worker-8262/log"
    numa_node: "0,1"
    # config is used to overwrite the `server_configs.worker` values
    config:
      log-level: info
  - host: 10.0.1.19
```

### `monitoring_servers`

`monitoring_servers` specifies the machines to which the Prometheus service is deployed. You can also specify the service configuration on the machine. `monitoring_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` section is used.
- `port`: specifies the port on which Prometheus provides services. The default value is "9090".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` section.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` section.
- `log_dir`: specifies the log directory. If the field is not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` section.
- `numa_node`: allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is a string type. The field value is the ID of the NUMA node, such as "0,1"
- `storage_retention`: specifies the retention time of the Prometheus monitoring data. The default value is "15d".
- `rule_dir`: specifies a local directory where the complete `*.rules.yml` files are located. The files in the specified directory will be sent to the target machine as the Prometheus rules during the initialization phase of the cluster configuration.
- `remote_config`: Supports writing Prometheus data to the remote, or reading data from the remote. This field has two configurations:
    - `remote_write`: See the Prometheus document [`<remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write).
    - `remote_read`: See the Prometheus document [`<remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read).
- `external_alertmanagers`: If the `external_alertmanagers` field is configured, Prometheus alerts the configuration behavior to the Alertmanager that is outside the cluster. This field is an array, each element of which is an external Alertmanager and consists of the `host` and `web_port` fields.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` section.
- `arch`: the architecture of the machine specified in the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` section.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` section (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` section.

In the `monitoring_servers` section, the following fields cannot be modified after the deployment is completed: 

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `monitoring_servers` configuration example is as follows:

```yaml
monitoring_servers:
  - host: 10.0.1.11
    rule_dir: /local/rule/dir
    remote_config:
      remote_write:
      - queue_config:
          batch_send_deadline: 5m
          capacity: 100000
          max_samples_per_send: 10000
          max_shards: 300
        url: http://127.0.0.1:8003/write
      remote_read:
      - url: http://127.0.0.1:8003/read\
      external_alertmanagers:
      - host: 10.1.1.1
      web_port: 9093
      - host: 10.1.1.2
      web_port: 9094
```

### `grafana_servers`

`grafana_servers` specifies the machines to which the Grafana service is deployed. You can also specify the service configuration on the machine. `grafana_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` section is used.
- `port`: specifies the port on which Grafana provides services. The default value is "3000".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` section.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` section.
- `arch`: the architecture of the machine specified in the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` section.
- `username`: specifies the username of the Grafana login screen.
- `password`: specifies the corresponding password of Grafana.
- `dashboard_dir`: specifies a local directory where the complete `dashboard(*.json)` files are located. The files in the specified directory will be sent to the target machine as Grafana dashboards during the initialization phase of the cluster configuration.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` section (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` section.

> **Note:**
>
> If the `dashboard_dir` field of `grafana_servers` is configured, after executing the `tiup cluster rename` command to rename the cluster, you need to perform the following operations:
>
> 1. In the local `dashboards` directory, update the value of the `datasource` field to the new cluster name (the `datasource` is named after the cluster name).
> 2. Execute the `tiup cluster reload -R grafana` command.

In `grafana_servers`, the following fields cannot be modified after the deployment is completed:

- `host`
- `port`
- `deploy_dir`
- `arch`
- `os`

A `grafana_servers` configuration example is as follows:

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### `alertmanager_servers`

`alertmanager_servers` specifies the machines to which the Alertmanager service is deployed. You can also specify the service configuration on each machine. `alertmanager_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` section is used.
- `web_port`: specify the port on which Alertmanager provides web services. The default value is "9093".
- `cluster_port`: Specify the communication port between one Alertmanger and other Alertmanager. The default value is "9094".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` section.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` section.
- `log_dir`: specifies the log directory. If the field is not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` section.
- `numa_node`: allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is a string type. The field value is the ID of the NUMA node, such as "0,1"
- `config_file`: specifies a local file. The specified file will be sent to the target machine as the configuration for Alertmanager during the initialization phase of the cluster configuration.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` section.
- `arch`: the architecture of the machine specified in the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` section.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` section (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` section.

In `alertmanager_servers`, the following fields cannot be modified after the deployment is completed:

- `host`
- `web_port`
- `cluster_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

An `alertmanager_servers` configuration example is as follows:

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
