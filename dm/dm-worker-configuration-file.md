---
title: DM-worker Configuration File
summary: Learn the configuration file of DM-worker.
aliases: ['/docs/tidb-data-migration/dev/dm-worker-configuration-file/','/docs/tidb-data-migration/dev/dm-worker-configuration-file-full/']
---

# DM-worker Configuration File

This document introduces the configuration of DM worker, including a configuration file template and a description of each configuration parameter in this file.

## Configuration file template

The following is a configuration file template of the DM-worker:

```toml
# Worker Configuration.
name = "worker1"

# Log configuration.
log-level = "info"
log-file = "dm-worker.log"

# DM-worker listen address.
worker-addr = ":8262"
advertise-addr = "127.0.0.1:8262"
join = "http://127.0.0.1:8261,http://127.0.0.1:8361,http://127.0.0.1:8461"

keepalive-ttl = 60
relay-keepalive-ttl = 1800 # New in DM v2.0.2.
# relay-dir = "relay_log" # New in 5.4.0. When you use a relative path, check the deployment and start method of DM-worker to determine the full path.

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"]
```

## Configuration parameters

### Global

| Parameter        | Description                           |
| :------------ | :--------------------------------------- |
| `name` | The name of the DM-worker. |
| `log-level` | Specifies a log level from `debug`, `info`, `warn`, `error`, and `fatal`. The default log level is `info`. |
| `log-file` | Specifies the log file directory. If this parameter is not specified, the logs are printed onto the standard output. |
| `worker-addr` | Specifies the address of DM-worker which provides services. You can omit the IP address and specify the port number only, such as ":8262". |
| `advertise-addr` | Specifies the address that DM-worker advertises to the outside world. |
| `join` | Corresponds to one or more [`master-addr`s](/dm/dm-master-configuration-file.md#global-configuration) in the DM-master configuration file. |
| `keepalive-ttl` | The keepalive time (in seconds) of a DM-worker node to the DM-master node if the upstream data source of the DM-worker node does not enable the relay log. The default value is 60s.|
| `relay-keepalive-ttl` | The keepalive time (in seconds) of a DM-worker node to the DM-master node if the upstream data source of the DM-worker node enables the relay log. The default value is 1800s. This parameter is added since DM v2.0.2.|
| `relay-dir` | When relay log is enabled in the bound upstream data source, DM-worker stores the relay log in this directory. This parameter is new in v5.4.0 and takes precedence over the configuration of the upstream data source. |
| `ssl-ca` | The path of the file that contains list of trusted SSL CAs for DM-worker to connect with other components. |
| `ssl-cert` | The path of the file that contains X509 certificate in PEM format for DM-worker to connect with other components. |
| `ssl-key` | The path of the file that contains X509 key in PEM format for DM-worker to connect with other components. |
| `cert-allowed-cn` | Common Name list. |
