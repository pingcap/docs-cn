---
title: Scheduling 配置参数
summary: Scheduling 配置参数可以通过命令行参数或环境变量配置。
---

# Scheduling 配置参数

Scheduling 可以通过命令行参数或环境变量配置。

## `--advertise-listen-addr`

- 用于外部访问 Scheduling 的 URL。
- 默认：`${listen-addr}`
- 在某些情况下，例如 Docker 或者 NAT 网络环境，客户端并不能通过 Scheduling 自己监听的地址来访问到 Scheduling，这时候，你就可以设置 advertise URL 来让客户端访问。
- 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 3379:3379`，那么可以设置为 `--advertise-client-urls="http://192.168.100.113:3379"`，客户端可以通过 `http://192.168.100.113:3379` 来找到这个服务。

## `--listen-addr`

- Scheduling 监听的客户端 URL。
- 默认：`http://127.0.0.1:3379`
- 如果部署一个集群，`--listen-addr` 必须指定当前主机的 IP 地址，例如 `http://192.168.100.113:3379"`，如果是运行在 Docker 则需要指定为 `http://0.0.0.0:3379`。

## `--backend-endpoints`

- Scheduling 节点监听其他 PD 节点的 URL 列表。
- 默认：`http://127.0.0.1:2379`

## `--config`

- 配置文件。
- 默认：""

## `--data-dir`

- Scheduling 存储数据路径。
- 默认：`default.${name}`

## `-L`

- Log 级别。
- 默认："info"
- 可选："debug"，"info"，"warn"，"error"，"fatal"

## `--log-file`

- Log 文件。
- 默认：""
- 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面。

## `--cacert`

- CA 文件路径，用于开启 TLS。
- 默认：""

## `--cert`

- 包含 X509 证书的 PEM 文件路径，用户开启 TLS。
- 默认：""

## `--key`

- 包含 X509 key 的 PEM 文件路径，用于开启 TLS。
- 默认：""

## `-V`, `--version`

- 输出版本信息并退出。
