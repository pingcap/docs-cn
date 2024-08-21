---
title: Scheduling 配置参数
summary: Scheduling 配置参数可以通过命令行参数或环境变量配置。
---

# Scheduling 配置参数

Scheduling 节点用于提供 PD 的 `scheduling` 微服务。你可以通过命令行参数或环境变量配置 Scheduling 节点。

## `--advertise-listen-addr`

- 用于外部访问 Scheduling 节点的 URL。
- 默认：`${listen-addr}`
- 在某些情况下，例如 Docker 或者 NAT 网络环境，客户端并不能通过 Scheduling 节点自己监听的地址来访问 Scheduling 节点。此时，你可以设置 `--advertise-listen-addr` 来让客户端访问。
- 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 3379:3379`，那么可以设置 `--advertise-listen-addr="http://192.168.100.113:3379"`，然后客户端就可以通过 `http://192.168.100.113:3379` 来找到这个服务。

## `--backend-endpoints`

- Scheduling 节点监听其他 Scheduling 节点的 URL 列表。
- 默认：`http://127.0.0.1:2379`

## `--cacert`

- CA 文件路径，用于开启 TLS。
- 默认：""

## `--cert`

- 包含 X.509 证书的 PEM 文件路径，用于开启 TLS。
- 默认：""

## `--config`

- 配置文件。
- 默认：""
- 如果你指定了配置文件，Scheduling 节点会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，Scheduling 节点就会使用命令行参数的配置来覆盖配置文件里面的配置。

## `--data-dir`

- Scheduling 节点上的数据存储路径。
- 默认：`default.${name}`

## `--key`

- 包含 X.509 key 的 PEM 文件路径，用于开启 TLS。
- 默认：""

## `--listen-addr`

- Scheduling 节点监听的客户端 URL。
- 默认：`http://127.0.0.1:3379`
- 部署集群时，`--listen-addr` 必须指定当前主机的 IP 地址，例如 `http://192.168.100.113:3379`。如果运行在 Docker 中，则需要指定为 `http://0.0.0.0:3379`。

## `--log-file`

- Log 文件。
- 默认：""
- 如果未设置该参数，log 会默认输出到 "stderr"。如果设置了该参数，log 将输出到指定的文件。

## `--name` <span class="version-mark">从 v8.3.0 版本开始引入</span>

+ 当前 Scheduling 节点的名字。
+ 默认：`"scheduling-${hostname}"`
+ 如果你需要启动多个 Scheduling 节点，建议为不同 Scheduling 节点设置不同的名字，以方便区分。

## `-L`

- Log 级别。
- 默认："info"
- 可选："debug"，"info"，"warn"，"error"，"fatal"

## `-V`, `--version`

- 输出版本信息并退出。
