---
title: Topology Configuration File for TiDB Deployment Using TiUP
---

# Topology Configuration File for TiDB Deployment Using TiUP

To deploy or scale TiDB using TiUP, you need to provide a topology file ([sample](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/topology.example.yaml)) to describe the cluster topology.

Similarly, to modify the cluster topology, you need to modify the topology file. The difference is that, after the cluster is deployed, you can only modify a part of the fields in the topology file. This document introduces each section of the topology file and each field in each section.

## File structure

A topology configuration file for TiDB deployment using TiUP might contain the following sections:

- [global](#global): The cluster's global configuration. Some of the configuration items use the default values and you can configure them separately in each instance.
- [monitored](#monitored): Configuration for monitoring services, namely, the blackbox_exporter and the `node_exporter`. On each machine, a `node_exporter` and a `blackbox_exporter` are deployed.
- [server_configs](#server_configs): Components' global configuration. You can configure each component separately. If an instance has a configuration item with the same name, the instance's configuration item will take effect.
- [pd_servers](#pd_servers): The configuration of the PD instance. This configuration specifies the machines to which the PD component is deployed.
- [tidb_servers](#tidb_servers): The configuration of the TiDB instance. This configuration specifies the machines to which the TiDB component is deployed.
- [tikv_servers](#tikv_servers): The configuration of the TiKV instance. This configuration specifies the machines to which the TiKV component is deployed.
- [tiflash_servers](#tiflash_servers): The configuration of the TiFlash instance. This configuration specifies the machines to which the TiFlash component is deployed.
- [pump_servers](#pump_servers): The configuration of the Pump instance. This configuration specifies the machines to which the Pump component is deployed.
- [drainer_servers](#drainer_servers): The configuration of the Drainer instance. This configuration specifies the machines to which the Drainer component is deployed.
- [cdc_servers](#cdc_servers): The configuration of the TiCDC instance. This configuration specifies the machines to which the TiCDC component is deployed.
- [tispark_masters](#tispark_masters): The configuration of the TiSpark master instance. This configuration specifies the machines to which the TiSpark master component is deployed. Only one node of TiSpark master can be deployed.
- [tispark_workers](#tispark_workers): The configuration of the TiSpark worker instance. This configuration specifies the machines to which the TiSpark worker component is deployed.
- [monitoring_servers](#monitoring_servers): Specifies the machines to which Prometheus is deployed. TiUP supports deploying multiple Prometheus instances but only the first instance is used.
- [grafana_servers](#grafana_servers): The configuration of the Grafana instance. This configuration specifies the machines to which Grafana is deployed.
- [alertmanager_servers](#alertmanager_servers): The configuration of the Alertmanager instance. This configuration specifies the machines to which Alertmanager is deployed.

### `global`

The `global` section corresponds to the cluster's global configuration and has the following fields:

- `user`: The user used to start the deployed cluster. The default value is `"tidb"`. If the user specified in the `<user>` field does not exist on the target machine, this user is automatically created.

- `group`: The user group to which a user belongs. It is specified when the user is created. The value defaults to that of the `<user>` field. If the specified group does not exist, it is automatically created.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. The default value is `22`.

- `enable_tls`: Specifies whether to enable TLS for the cluster. After TLS is enabled, the generated TLS certificate must be used for connections between components or between the client and the component. **Once it is enabled, it cannot be disabled**. The default value is `false`.

- `deploy_dir`: The deployment directory of each component. The default value is `"deployed"`. Its application rules are as follows:

    - If the absolute path of `deploy_dir` is configured at the instance level, the actual deployment directory is `deploy_dir` configured for the instance.

    - For each instance, if you do not configure `deploy_dir`, its default value is the relative path `<component-name>-<component-port>`.

    - If `global.deploy_dir` is an absolute path, the component is deployed to the `<global.deploy_dir>/<instance.deploy_dir>` directory.

    - If `global.deploy_dir` is a relative path, the component is deployed to the `/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>` directory.

- `data_dir`: The data directory. Default value: `"data"`. Its application rules are as follows:

    - If the absolute path of `data_dir` is configured at the instance level, the actual deployment directory is `data_dir` configured for the instance.

    - For each instance, if you do not configure `data_dir`, its default value is `<global.data_dir>`.

    - If `data_dir` is a relative path, the component data is placed in `<deploy_dir>/<data_dir>`. For the calculation rules of `<deploy_dir>`, see the application rules of the `deploy_dir` field.

- `log_dir`: The data directory. Default value: `"log"`. Its application rules are as follows:

    - If the absolute path `log_dir` is configured at the instance level, the actual log directory is the `log_dir` configured for the instance.

    - For each instance, if you not configure `log_dir`, its default value is `<global.log_dir>`.

    - If `log_dir` is a relative path, the component log is placed in `<deploy_dir>/<log_dir>`. For the calculation rules of `<deploy_dir>`, see the application rules of the `deploy_dir` field.

- `os`: The operating system of the target machine. The field controls which operating system to adapt to for the components pushed to the target machine. The default value is "linux".

- `arch`: The CPU architecture of the target machine. The field controls which platform to adapt to for the binary packages pushed to the target machine. The supported values are "amd64" and "arm64". The default value is "amd64".

- `resource_control`: Runtime resource control. All configurations in this field are written into the service file of systemd. There is no limit by default. The resources that can be controlled are as follows:

    - `memory_limit`: Limits the maximum runtime memory. For example, "2G" means that the maximum memory of 2 GB can be used.

    - `cpu_quota`: Limits the maximum CPU usage at runtime. For example, "200%".

    - `io_read_bandwidth_max`: Limits the maximum I/O bandwidth for disk reads. For example, `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"`.

    - `io_write_bandwidth_max`: Limits maximum I/O bandwidth for disk writes. For example, `/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M`.

    - `limit_core`: Controls the size of core dump.

A `global` configuration example is as follows:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

In the above configuration, the `tidb` user is used to start the cluster. At the same time, each component is restricted to a maximum of 2 GB of memory when it is running.

### `monitored`

`monitored` is used to configure the monitoring service on the target machine: [`node_exporter`](https://github.com/prometheus/node_exporter) and [`blackbox_exporter`](https://github.com/prometheus/blackbox_exporter). The following fields are included:

- `node_exporter_port`: The service port of `node_exporter`. The default value is `9100`.

- `blackbox_exporter_port`: The service port of `blackbox_exporter`. The default value is `9115`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

A `monitored` configuration example is as follows:

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

The above configuration specifies that `node_exporter` uses the `9100` port and `blackbox_exporter` uses the `9115` port.

### `server_configs`

`server_configs` is used to configure services and to generate configuration files for each component. Similar to the `global` section, the configuration of this section can be overwritten by the configurations with the same names in an instance. `server_configs` mainly includes the following fields:

- `tidb`: TiDB service-related configuration. For the complete configuration, see [TiDB configuration file](/tidb-configuration-file.md).

- `tikv`: TiKV service-related configuration. For the complete configuration, see [TiKV configuration file](/tikv-configuration-file.md).

- `pd`: PD service-related configuration. For the complete configuration, see [PD configuration file](/pd-configuration-file.md).

- `tiflash`: TiFlash service-related configuration. For the complete configuration, see [TiFlash configuration file](/tiflash/tiflash-configuration.md).

- `tiflash_learner`: Each TiFlash node has a special built-in TiKV. This configuration item is used to configure this special TiKV. It is generally not recommended to modify the content under this configuration item.

- `pump`: Pump service-related configuration. For the complete configuration, see [TiDB Binlog configuration file](/tidb-binlog/tidb-binlog-configuration-file.md#pump).

- `drainer`: Drainer service-related configuration. For the complete configuration, see [TiDB Binlog configuration file](/tidb-binlog/tidb-binlog-configuration-file.md#drainer).

- `cdc`: TiCDC service-related configuration. For the complete configuration, see [Deploy TiCDC](/ticdc/deploy-ticdc.md).

A `server_configs` configuration example is as follows:

```yaml
server_configs:
  tidb:
    run-ddl: true
    lease: "45s"
    split-table: true
    token-limit: 1000
  tikv:
    log-level: "info"
    readpool.unified.min-thread-count: 1
```

The above configuration specifies the global configuration of TiDB and TiKV.

### `pd_servers`

`pd_servers` specifies the machines to which PD services are deployed. It also specifies the service configuration on each machine. `pd_servers` is an array, and each element of the array contains the following fields:

- `host`: Specifies the machine to which the PD services are deployed. The field value is an IP address and is mandatory.

- `listen_host`: When the machine has multiple IP addresses, `listen_host` specifies the listening IP address of the service. The default value is `0.0.0.0`.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `name`: Specifies the name of the PD instance. Different instances must have unique names; otherwise, instances cannot be deployed.

- `client_port`: Specifies the port that PD uses to connect to the client. The default value is `2379`.

- `peer_port`: Specifies the port for communication between PDs. The default value is `2380`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `pd` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `pd` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `listen_host`
- `name`
- `client_port`
- `peer_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `pd_servers` configuration example is as follows:

```yaml
pd_servers:
  - host: 10.0.1.11
    config:
      schedule.max-merge-region-size: 20
      schedule.max-merge-region-keys: 200000
  - host: 10.0.1.12
```

The above configuration specifies that PD will be deployed on `10.0.1.11` and `10.0.1.12`, and makes specific configurations for the PD of `10.0.1.11`.

### `tidb_servers`

`tidb_servers` specifies the machines to which TiDB services are deployed. It also specifies the service configuration on each machine. `tidb_servers` is an array, and each element of the array contains the following fields:

- `host`: Specifies the machine to which the TiDB services are deployed. The field value is an IP address and is mandatory.

- `listen_host`: When the machine has multiple IP addresses, `listen_host` specifies the listening IP address of the service. The default value is `0.0.0.0`.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of TiDB services, which is used to provide connection to the MySQL client. The default value is `4000`.

- `status_port`: The listening port of the TiDB status service, which is used to view the status of the TiDB services from the external via HTTP requests. The default value is `10080`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `tidb` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `tidb` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `listen_host`
- `port`
- `status_port`
- `deploy_dir`
- `log_dir`
- `arch`
- `os`

A `tidb_servers` configuration example is as follows:

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### `tikv_servers`

`tikv_servers` specifies the machines to which TiKV services are deployed. It also specifies the service configuration on each machine. `tikv_servers` is an array, and each element of the array contains the following fields:

- `host`: Specifies the machine to which the TiKV services are deployed. The field value is an IP address and is mandatory.

- `listen_host`: When the machine has multiple IP addresses, `listen_host` specifies the listening IP address of the service. The default value is `0.0.0.0`.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of the TiKV services. The default value is `20160`.

- `status_port`: The listening port of the TiKV status service. The default value is `20180`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `tikv` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `tikv` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `listen_host`
- `port`
- `status_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `tikv_servers` configuration example is as follows:

```yaml
tikv_servers:
  - host: 10.0.1.14
    config:
      server.labels: { zone: "zone1", host: "host1" }
  - host: 10.0.1.15
    config:
      server.labels: { zone: "zone1", host: "host2" }
```

### `tiflash_servers`

`tiflash_servers` specifies the machines to which TiFlash services are deployed. It also specifies the service configuration on each machine. This section is an array, and each element of the array contains the following fields:

- `host`: Specifies the machine to which the TiFlash services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `tcp_port`: The port of the TiFlash TCP service. The default value is `9000`.

- `http_port`: The port of the TiFlash HTTP service. The default value is `8123`.

- `flash_service_port`: The port via which TiFlash provides services. TiDB reads data from TiFlash via this port. The default value is `3930`.

- `metrics_port`: TiFlash's status port, which is used to output metric data. The default value is `8234`.

- `flash_proxy_port`: The port of the built-in TiKV. The default value is `20170`.

- `flash_proxy_status_port`: The status port of the built-in TiKV. The default value is `20292`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`. TiFlash supports multiple `data_dir` directories separated by commas.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `tmp_path`: The storage path of TiFlash temporary files. The default value is [`path` or the first directory of `storage.latest.dir`] + "/tmp".

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `tiflash` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `tiflash` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `learner_config`: Each TiFlash node has a special built-in TiKV. This configuration item is used to configure this special TiKV. It is generally not recommended to modify the content under this configuration item.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

After the deployment, for the fields above, you can only add directories to `data_dir`; for the fields below, you cannot modified these fields:

- `host`
- `tcp_port`
- `http_port`
- `flash_service_port`
- `flash_proxy_port`
- `flash_proxy_status_port`
- `metrics_port`
- `deploy_dir`
- `log_dir`
- `tmp_path`
- `arch`
- `os`

A `tiflash_servers` configuration example is as follows:

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### `pump_servers`

`pump_servers` specifies the machines to which the Pump services of TiDB Binlog are deployed. It also specifies the service configuration on each machine. `pump_servers` is an array, and each element of the array contains the following fields:

- `host`: Specifies the machine to which the Pump services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of the Pump services. The default value is `8250`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `pump` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `pump` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `pump_servers` configuration example is as follows:

```yaml
pump_servers:
  - host: 10.0.1.21
    config:
      gc: 7
  - host: 10.0.1.22
```

### `drainer_servers`

`drainer_servers` specifies the machines to which the Drainer services of TiDB Binlog are deployed. It also specifies the service configuration on each machine. `drainer_servers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the Drainer services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of Drainer services. The default value is `8249`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `commit_ts`: When Drainer starts, it reads the checkpoint. If Drainer cannot read the checkpoint, it uses this field as the replication time point for the initial startup. This field defaults to `-1` (Drainer always gets the latest timestamp from the PD as the commit_ts).

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The configuration rule of this field is the same as the `drainer` configuration rule in `server_configs`. If this field is configured, the field content is merged with the `drainer` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `commit_ts`
- `arch`
- `os`

A `drainer_servers` configuration example is as follows:

```yaml
drainer_servers:
  - host: 10.0.1.21
    config:
      syncer.db-type: "mysql"
      syncer.to.host: "127.0.0.1"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 3306
      syncer.ignore-table:
        - db-name: test
          tbl-name: log
        - db-name: test
          tbl-name: audit
```

### `cdc_servers`

`cdc_servers` specifies the machines to which the TiCDC services are deployed. It also specifies the service configuration on each machine. `cdc_servers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the TiCDC services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of the TiCDC services. The default value is `8300`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`：Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `gc-ttl`: The Time To Live (TTL) duration of the service level GC safepoint set by TiCDC in PD, in seconds. The default value is `86400`, which is 24 hours.

- `tz`: The time zone that the TiCDC services use. TiCDC uses this time zone when internally converting time data types such as timestamp and when replicating data to the downstream. The default value is the local time zone where the process runs.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config`: The field content is merged with the `cdc` content in `server_configs` (if the two fields overlap, the content of this field takes effect). Then, a configuration file is generated and sent to the machine specified in `host`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `gc-ttl`
- `tz`
- `arch`
- `os`

A `cdc_servers` configuration example is as follows:

```yaml
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
  - host: 10.0.1.21
```

### `tispark_masters`

`tispark_masters` specifies the machines to which the master node of TiSpark is deployed. It also specifies the service configuration on each machine. `tispark_masters` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the TiSpark master is deployed. The field value is an IP address and is mandatory.

- `listen_host`: When the machine has multiple IP addresses, `listen_host` specifies the listening IP address of the service. The default value is `0.0.0.0`.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: Spark's listening port, used for communication before the node. The default value is `7077`.

- `web_port`: Spark's web port, which provides web services and the task status. The default value is `8080`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `java_home`: Specifies the path of the JRE environment to be used. This parameter corresponds to the `JAVA_HOME` system environment variable.

- `spark_config`: Configures to configure the TiSpark services. Then, a configuration file is generated and sent to the machine specified in `host`.

- `spark_env`: Configures the environment variables when Spark starts.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `listen_host`
- `port`
- `web_port`
- `deploy_dir`
- `arch`
- `os`

A `tispark_masters` configuration example is as follows:

```yaml
tispark_masters:
  - host: 10.0.1.21
    spark_config:
      spark.driver.memory: "2g"
      spark.eventLog.enabled: "False"
      spark.tispark.grpc.framesize: 2147483647
      spark.tispark.grpc.timeout_in_sec: 100
      spark.tispark.meta.reload_period_in_sec: 60
      spark.tispark.request.command.priority: "Low"
      spark.tispark.table.scan_concurrency: 256
    spark_env:
      SPARK_EXECUTOR_CORES: 5
      SPARK_EXECUTOR_MEMORY: "10g"
      SPARK_WORKER_CORES: 5
      SPARK_WORKER_MEMORY: "10g"
  - host: 10.0.1.22
```

### `tispark_workers`

`tispark_workers` specifies the machines to which the worker nodes of TiSpark are deployed. It also specifies the service configuration on each machine. `tispark_workers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the TiSpark workers are deployed. The field value is an IP address and is mandatory.

- `listen_host`: When the machine has multiple IP addresses, `listen_host` specifies the listening IP address of the service. The default value is `0.0.0.0`.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: Spark's listening port, used for communication before the node. The default value is `7077`.

- `web_port`: Spark's web port, which provides web services and the task status. The default value is `8080`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `java_home`: Specifies the path in which the JRE environment to be used is located. This parameter corresponds to the `JAVA_HOME` system environment variable.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `listen_host`
- `port`
- `web_port`
- `deploy_dir`
- `arch`
- `os`

A `tispark_workers` configuration example is as follows:

```yaml
tispark_workers:
  - host: 10.0.1.22
  - host: 10.0.1.23
```

### `monitoring_servers`

`monitoring_servers` specifies the machines to which the Prometheus services are deployed. It also specifies the service configuration on each machine. `monitoring_servers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the monitoring services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of the Prometheus services. The default value is `9090`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `storage_retention`: The retention time of the Prometheus monitoring data. The default value is `"15d"`.

- `rule_dir`: Specifies a local directory that should contain complete `*.rules.yml` files. These files are transferred to the target machine during the initialization phase of the cluster configuration as the rules for Prometheus.
- `remote_config`: Supports writing Prometheus data to the remote, or reading data from the remote. This field has two configurations:
    - `remote_write`: See the Prometheus document [`<remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write).
    - `remote_read`: See the Prometheus document [`<remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read).
- `external_alertmanagers`: If the `external_alertmanagers` field is configured, Prometheus alerts the configuration behavior to the Alertmanager that is outside the cluster. This field is an array, each element of which is an external Alertmanager and consists of the `host` and `web_port` fields.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

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
      - url: http://127.0.0.1:8003/read
      external_alertmanagers:
      - host: 10.1.1.1
        web_port: 9093
      - host: 10.1.1.2
        web_port: 9094
```

### `grafana_servers`

`grafana_servers` specifies the machines to which the Grafana services are deployed. It also specifies the service configuration on each machine. `grafana_servers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the Grafana services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `port`: The listening port of the Grafana services. The default value is `3000`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `username`: The user name on the Grafana login interface.

- `password`: The password corresponding to Grafana.

- `dashboard_dir`: Specifies a local directory that should contain complete `dashboard(*.json)` files. These files are transferred to the target machine during the initialization phase of the cluster configuration as the dashboards for Grafana.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

> **Note:**
>
> If the `dashboard_dir` field of `grafana_servers` is configured, after executing the `tiup cluster rename` command to rename the cluster, you need to perform the following operations:
>
> 1. For the `*.json` files in the local dashboards directory, update the value of the `datasource` field to the new cluster name (because `datasource` is named after the cluster name).
> 2. Execute the `tiup cluster reload -R grafana` command.

For the above fields, you cannot modify these configured fields after the deployment:

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

`alertmanager_servers` specifies the machines to which the Alertmanager services are deployed. It also specifies the service configuration on each machine. `alertmanager_servers` is an array. Each array element contains the following fields:

- `host`: Specifies the machine to which the Alertmanager services are deployed. The field value is an IP address and is mandatory.

- `ssh_port`: Specifies the SSH port to connect to the target machine for operations. If it is not specified, the `ssh_port` of the `global` section is used.

- `web_port`: Specifies the port used that Alertmanager uses to provide web services. The default value is `9093`.

- `cluster_port`: Specifies the communication port between one Alertmanger and other Alertmanager. The default value is `9094`.

- `deploy_dir`: Specifies the deployment directory. If it is not specified or specified as a relative directory, the directory is generated according to the `deploy_dir` directory configured in `global`.

- `data_dir`: Specifies the data directory. If it is not specified or specified as a relative directory, the directory is generated according to the `data_dir` directory configured in `global`.

- `log_dir`: Specifies the log directory. If it is not specified or specified as a relative directory, the log is generated according to the `log_dir` directory configured in `global`.

- `numa_node`: Allocates the NUMA policy to the instance. Before specifying this field, you need to make sure that the target machine has [numactl](https://linux.die.net/man/8/numactl) installed. If this field is specified, cpubind and membind policies are allocated using [numactl](https://linux.die.net/man/8/numactl). This field is the string type. The field value is the ID of the NUMA node, such as "0,1".

- `config_file`: Specifies a local file that is transferred to the target machine during the initialization phase of the cluster configuration as the configuration of Alertmanager.

- `os`: The operating system of the machine specified in `host`. If this field is not specified, the default value is the `os` value in `global`.

- `arch`: The architecture of the machine specified in `host`. If this field is not specified, the default value is the `arch` value in `global`.

- `resource_control`: Resource control for the service. If this field is configured, the field content is merged with the `resource_control` content in `global` (if the two fields overlap, the content of this field takes effect). Then, a systemd configuration file is generated and sent to the machine specified in `host`. The configuration rules of `resource_control` are the same as the `resource_control` content in `global`.

For the above fields, you cannot modify these configured fields after the deployment:

- `host`
- `web_port`
- `cluster_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `alertmanager_servers` configuration example is as follows:

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
