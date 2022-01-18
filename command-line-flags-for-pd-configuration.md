---
title: PD Configuration Flags
summary: Learn some configuration flags of PD.
aliases: ['/docs/dev/command-line-flags-for-pd-configuration/','/docs/dev/reference/configuration/pd-server/configuration/']
---

# PD Configuration Flags

PD is configurable using command-line flags and environment variables.

## `--advertise-client-urls`

- The list of advertise URLs for the client to access PD
- Default: `"${client-urls}"`
- In some situations such as in the Docker or NAT network environment, if a client cannot access PD through the default client URLs listened to by PD, you must manually set the advertise client URLs.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 2379:2379`. In this case, you can set `--advertise-client-urls` to `"http://192.168.100.113:2379"`. The client can find this service through `"http://192.168.100.113:2379"`.

## `--advertise-peer-urls`

- The list of advertise URLs for other PD nodes (peers) to access a PD node
- Default: `"${peer-urls}"`
- In some situations such as in the Docker or NAT network environment, if the other nodes (peers) cannot access the PD node through the default peer URLs listened to by this PD node, you must manually set the advertise peer URLs.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 2380:2380`. In this case, you can set `--advertise-peer-urls` to `"http://192.168.100.113:2380"`. The other PD nodes can find this service through `"http://192.168.100.113:2380"`.

## `--client-urls`

- The list of client URLs to be listened to by PD
- Default: `"http://127.0.0.1:2379"`
- When you deploy a cluster, you must specify the IP address of the current host as `--client-urls` (for example, `"http://192.168.100.113:2379"`). If the cluster runs on Docker, specify the IP address of Docker as `"http://0.0.0.0:2379"`.

## `--peer-urls`

- The list of peer URLs to be listened to by a PD node
- Default: `"http://127.0.0.1:2380"`
- When you deploy a cluster, you must specify `--peer-urls` as the IP address of the current host, such as `"http://192.168.100.113:2380"`. If the cluster runs on Docker, specify the IP address of Docker as `"http://0.0.0.0:2380"`.

## `--config`

- The configuration file
- Default: `""`
- If you set the configuration using the command line, the same setting in the configuration file will be overwritten.

## `--data-dir`

- The path to the data directory
- Default: `"default.${name}"`

## `--initial-cluster`

- The initial cluster configuration for bootstrapping
- Default: `"{name}=http://{advertise-peer-url}"`
- For example, if `name` is "pd", and `advertise-peer-urls` is `"http://192.168.100.113:2380"`, the `initial-cluster` is `"pd=http://192.168.100.113:2380"`.
- If you need to start three PD servers, the `initial-cluster` might be:

    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

## `--join`

- Join the cluster dynamically
- Default: `""`
- If you want to join an existing cluster, you can use `--join="${advertise-client-urls}"`, the `advertise-client-url` is any existing PD's, multiply advertise client urls are separated by comma.

## `-L`

- The log level
- Default: `"info"`
- Optional values: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`

## `--log-file`

- The log file
- Default: `""`
- If this flag is not set, logs will be written to "stderr". If this flag is set, logs are output to the corresponding file.

## `--log-rotate`

- To enable or disable log rotation
- Default: `true`
- When the value is true, follow the `[log.file]` in PD configuration files.

## `--name`

- The human-readable unique name for this PD member
- Default: `"pd"`
- If you want to start multiply PDs, you must use different name for each one.

## `--cacert`

- The file path of CA, used to enable TLS
- Default: `""`

## `--cert`

- The path of the PEM file including the X509 certificate, used to enable TLS
- Default: `""`

## `--key`

- The path of the PEM file including the X509 key, used to enable TLS
- Default: `""`

## `--metrics-addr`

- The address of Prometheus Pushgateway, which does not push data to Prometheus by default.
- Default: `""`
