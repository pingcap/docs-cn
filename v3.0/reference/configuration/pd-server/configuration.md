---
title: PD 配置参数
category: reference
aliases: ['/docs-cn/op-guide/pd-configuration/']
---

# PD 配置参数

PD 可以通过命令行参数或环境变量配置。

## `--advertise-client-urls`

+ 对外客户端访问 URL 列表。
+ 默认：`${client-urls}`
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，客户端并不能通过 PD 自己监听的 client URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让客户端访问
+ 例如，docker 内部 IP 地址为 172.17.0.1，而宿主机的 IP 地址为 192.168.100.113 并且设置了端口映射 `-p 2379:2379`，那么可以设置为 `--advertise-client-urls="http://192.168.100.113:2379"`，客户端可以通过 `http://192.168.100.113:2379` 来找到这个服务。

## `--advertise-peer-urls`

+ 对外其他 PD 节点访问 URL 列表。
+ 默认：`${peer-urls}`
+ 在某些情况下，譬如 docker，或者 NAT 网络环境，其他节点并不能通过 PD 自己监听的 peer URLs 来访问到 PD，这时候，你就可以设置 advertise urls 来让其他节点访问
+ 例如，docker 内部 IP 地址为 172.17.0.1，而宿主机的 IP 地址为 192.168.100.113 并且设置了端口映射 `-p 2380:2380`，那么可以设置为 `--advertise-peer-urls="http://192.168.100.113:2380"`，其他 PD 节点可以通过 `http://192.168.100.113:2380` 来找到这个服务。

## `--client-urls`

+ 处理客户端请求监听 URL 列表。
+ 默认：`http://127.0.0.1:2379`
+ 如果部署一个集群，\-\-client-urls 必须指定当前主机的 IP 地址，例如 `http://192.168.100.113:2379"`，如果是运行在 docker 则需要指定为 `http://0.0.0.0:2379`。

## `--peer-urls`

+ 处理其他 PD 节点请求监听 URL 列表。
+ default: `http://127.0.0.1:2380`
+ 如果部署一个集群，\-\-peer-urls 必须指定当前主机的 IP 地址，例如 `http://192.168.100.113:2380`，如果是运行在 docker 则需要指定为 `http://0.0.0.0:2380`。

## `--config`

+ 配置文件。
+ 默认：""
+ 如果你指定了配置文件，PD 会首先读取配置文件的配置。然后如果对应的配置在命令行参数里面也存在，PD 就会使用命令行参数的配置来覆盖配置文件里面的。

## `--data-dir`

+ PD 存储数据路径。
+ 默认：`default.${name}`

## `--initial-cluster`

+ 初始化 PD 集群配置。
+ 默认："{name}=http://{advertise-peer-url}"
+ 例如，如果 name 是 "pd", 并且 `advertise-peer-urls` 是 `http://192.168.100.113:2380`, 那么 `initial-cluster` 就是 `pd=http://192.168.100.113:2380`。
+ 如果你需要启动三台 PD，那么 `initial-cluster` 可能就是
  `pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380`。

## `--join`

+ 动态加入 PD 集群。
+ 默认：""
+ 如果你想动态将一台 PD 加入集群，你可以使用 `--join="${advertise-client-urls}"`， `advertise-client-url` 是当前集群里面任意 PD 的 `advertise-client-url`，你也可以使用多个 PD 的，需要用逗号分隔。

## `-L`

+ Log 级别。
+ 默认："info"
+ 我们能选择 debug, info, warn, error 或者 fatal。

## `--log-file`

+ Log 文件。
+ 默认：""
+ 如果没设置这个参数，log 会默认输出到 "stderr"，如果设置了，log 就会输出到对应的文件里面，在每天凌晨，log 会自动轮转使用一个新的文件，并且将以前的文件改名备份。

## `--log-rotate`

+ 是否开启日志切割。
+ 默认：true
+ 当值为 true 时,按照 PD 配置文件中 `[log.file]` 信息执行。

## `--name`

+ 当前 PD 的名字。
+ 默认："pd"
+ 如果你需要启动多个 PD，一定要给 PD 使用不同的名字

## `--cacert`

+ CA 文件路径，用于开启 TLS。
+ 默认：""

## `--cert`

+ 包含 X509 证书的 PEM 文件路径，用户开启 TLS。
+ 默认：""

## `--key`

+ 包含 X509 key 的 PEM 文件路径，用于开启 TLS。
+ 默认：""

## `--namespace-classifier`

+ 指定 PD 使用的 namespace 分类器。
+ 默认："table"
+ 如果 TiKV 不与 TiDB 集群配合运行，建议配置为 'default'。

## `--metrics-addr`

+ Prometheus Pushgateway 的地址，默认不向 Promethus 推送数据.
+ 默认：""
