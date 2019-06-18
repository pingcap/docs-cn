---
title: tkctl 使用说明
category: reference
---

# tkctl 使用说明

tkctl(TiDB Kubernetes Controltkctl) 为 TiDB in Kubernetes 设计的命令行工具，用于运维集群和诊断集群问题。

## 安装

安装 `tkctl` 时，可以直接下载预编译的可执行文件，也可以自行从源码进行编译。

### 下载预编译的可执行文件

- [MacOS](http://download.pingcap.org/tkctl-darwin-amd64-latest.tgz)
- [Linux](http://download.pingcap.org/tkctl-linux-amd64-latest.tgz)
- [Windows](http://download.pingcap.org/tkctl-windows-amd64-latest.tgz)

下载解压后，将 `tkctl` 可执行文件加入到可执行文件路径 (`PATH`) 中即完成安装。

### 源码编译

要求：[Go](https://golang.org/) 版本 1.11 及以上

```shell
$ git clone https://github.com/pingcap/tidb-operator.git
$ GOOS=${YOUR_GOOS} make cli
$ mv tkctl /usr/local/bin/tkctl
```

## 命令自动补全

你可以配置 `tkctl` 的自动补全来简化使用：

BASH（需要预选安装 [bash-completion](https://github.com/scop/bash-completion)）

```shell
# 在当前 shell 中设置自动补全。
source <(tkctl completion bash)

# 永久设置自动补全。
echo "if hash tkctl 2>/dev/null; then source <(tkctl completion bash); fi" >> ~/.bashrc
```

ZSH

```shell
# 在当前 shell 中设置自动补全
source <(tkctl completion zsh)

# 永久设置自动补全
echo "if hash tkctl 2>/dev/null; then source <(tkctl completion zsh); fi" >> ~/.zshrc
```

## Kubernetes 配置

`tkctl` 复用了 `kubeconfig` 文件(默认位置是 `~/.kube/config`) 来连接 Kubernetes 集群。你可以通过下面的命令来验证 `kubeconfig` 是否设置正确：

```shell
$ tkctl version
```

假如上面的命令正确输出服务端的 TiDB Operator 版本，则 `kubeconfig` 配置正确。

## 所有命令

### tkctl version

该命令用于展示本地 **tkctl** 和集群中 **tidb-operator** 的版本： 

例子：

```shell
$ tkctl version
Client Version: v1.0.0-beta.1-p2-93-g6598b4d3e75705-dirty
TiDB Controller Manager Version: pingcap/tidb-operator:latest
TiDB Scheduler Version: pingcap/tidb-operator:latest
```

### tkctl list

该命令用于列出所有已安装的 TiDB 集群：

| 参数             | 缩写      | 说明                                                       |
| -----            | --------- | -----------                                                |
| --all-namespaces | -A        | 是否查询所有的 Kubernetes Namespace                        |
| --output         | -o        | 输出格式，可选值有 [default,json,yaml]，默认值为 `default` |

例子：

```shell
$ tkctl list -A
NAMESPACE NAME           PD    TIKV   TIDB   AGE
foo       demo-cluster   3/3   3/3    2/2    11m
bar       demo-cluster   3/3   3/3    1/2    11m
```

### tkctl use

该命令用于指定当前 `tkctl` 操作的 TiDB 集群，在使用该命令设置当前操作的 TiDB 集群后，所有针对集群的操作命令会自动选定该集群，从而可以略去 `--tidbcluster` 参数。

例子：

```shell
$ tkctl use --namespace=foo demo-cluster
Tidb cluster switched to foo/demo-cluster
```

### tkctl info

该命令用于展示 TiDB 集群的信息

| 参数           | 缩写      | 说明                                       |
| -----          | --------- | -----------                                |
| --tidb-cluster | -t        | 指定 TiDB 集群，默认为当前使用的 TiDB 集群 |

例子：

```shell
$ tkctl info
Name:               demo-cluster
Namespace:          foo
CreationTimestamp:  2019-04-17 17:33:41 +0800 CST
Overview:
         Phase    Ready  Desired  CPU    Memory  Storage  Version
         -----    -----  -------  ---    ------  -------  -------
  PD:    Normal   3      3        200m   1Gi     1Gi      pingcap/pd:v3.0.0-rc.1
  TiKV:  Normal   3      3        1000m  2Gi     10Gi     pingcap/tikv:v3.0.0-rc.1
  TiDB   Upgrade  1      2        500m   1Gi              pingcap/tidb:v3.0.0-rc.1
Endpoints(NodePort):
  - 172.16.4.158:31441
  - 172.16.4.155:31441
```

### tkctl get [component]

该命令用于获取 TiDB 集群中组件的详细信息。

可选的组件(`component`)有： `pd`, `tikv`, `tidb`, `volume`, `all`(用于同时查询所有组件)

| 参数 | 缩写 | 说明 |
| ----- | --------- | ----------- |
| --tidb-cluster | -t | 指定 TiDB 集群，默认为当前使用的 TiDB 集群 |
| --output | -o | 输出格式，可选值有 [default,json,yaml]，默认值为 `default` |

例子：

```shell
$ tkctl get tikv
NAME                  READY   STATUS    MEMORY          CPU   RESTARTS   AGE     NODE
demo-cluster-tikv-0   2/2     Running   2098Mi/4196Mi   2/2   0          3m19s   172.16.4.155
demo-cluster-tikv-1   2/2     Running   2098Mi/4196Mi   2/2   0          4m8s    172.16.4.160
demo-cluster-tikv-2   2/2     Running   2098Mi/4196Mi   2/2   0          4m45s   172.16.4.157
$ tkctl get volume
tkctl get volume
VOLUME              CLAIM                      STATUS   CAPACITY   NODE           LOCAL
local-pv-d5dad2cf   tikv-demo-cluster-tikv-0   Bound    1476Gi     172.16.4.155   /mnt/disks/local-pv56
local-pv-5ade8580   tikv-demo-cluster-tikv-1   Bound    1476Gi     172.16.4.160   /mnt/disks/local-pv33
local-pv-ed2ffe50   tikv-demo-cluster-tikv-2   Bound    1476Gi     172.16.4.157   /mnt/disks/local-pv13
local-pv-74ee0364   pd-demo-cluster-pd-0       Bound    1476Gi     172.16.4.155   /mnt/disks/local-pv46
local-pv-842034e6   pd-demo-cluster-pd-1       Bound    1476Gi     172.16.4.158   /mnt/disks/local-pv74
local-pv-e54c122a   pd-demo-cluster-pd-2       Bound    1476Gi     172.16.4.156   /mnt/disks/local-pv72
```

### tkctl debug [pod_name]

该命令用于诊断 TiDB 集群中的 Pod。

实际使用时，该命令会在目标 Pod 的宿主机上以指定镜像启动一个 debug 容器，该容器会与目标 Pod 中的容器共享 namespace，因此可以无缝使用 debug 容器中的各种工具对目标容器进行诊断。

| 参数            | 缩写      | 描述                                                                                                                            |
| -----           | --------- | -----------                                                                                                                     |
| --image         |           | 指定 debug 容器使用的镜像，默认为 `pingcap/tidb-debug:lastest`                                                                  |
| --container     | -c        | 选择需要诊断的容器，默认为 Pod 定义中的第一个容器                                                                               |
| --docker-socket |           | 指定目标节点上的 Docker Socket，默认为 `/var/run/docker.sock`                                                                   |
| --privileged    |           | 是否为 debug 容器开启 [privileged](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities) 模式 |

Debug 容器使用默认的镜像包含了绝大多数的诊断工具，因此体积较大，假如只需要 `pd-ctl` 和 `tidb-ctl`，可以使用 `--image=pingcap/tidb-control:latest` 来指定使用 `tidb-control` 镜像。

例子：
```
$ tkctl debug demo-cluster-tikv-0
$ ps -ef
```

由于 debug 容器和目标容器拥有不同的根文件系统，在 `tidb-debug` 容器中使用 GDB 和 perf 等工具时可能会碰到一些问题，下面将额外说明如何解决这些问题：

#### GDB

使用 GDB 调试目标容器中的进程时，需要将 `program` 参数设置为目标容器中的可执行文件，假如是在 `tidb-debug` 以外的其它 debug 容器中进行调试，或者调试的目标进行 pid 不为 1，还需要使用 `set sysroot` 命令调整动态链接库的加载位置。操作如下：

```shell
$ tkctl debug demo-cluster-tikv-0
$ gdb /proc/${pid:-1}/root/tikv-server 1

# tidb-debug 中预配置的 .gdbinit 会将 sysroot 设置为 /proc/1/root/
# 因此在 tidb-debug 中，假如目标容易的 pid 为 1，则下面的命令可以省略
(gdb) set sysroot /proc/${pid}/root/

# 开始调试 
(gdb) thread apply all bt
(gdb) info threads
```

#### Perf (以及火焰图)

使用 `perf` 命令和 `run-flamegraph.sh` 脚本时，需要将目标容器的可执行文件拷贝到 Debug 容器中：

```shell
$ tkctl debug demo-cluster-tikv-0
$ cp /proc/1/root/tikv-server /
$ ./run_flamegraph.sh 1
```

### tkctl ctop

命令的完整形式：`tkctl ctop [pod_name | node/node_name ]`。

该命令用于查看集群中 Pod 或 Node 的实时监控信息，相比于 `kubectl top`，`tkctl ctop` 还会展示网络和磁盘的使用信息。

| 参数            | 简写      | 描述                                                                         |
| -----           | --------- | -----------                                                                  |
| --image         |           | 指定 ctop 的镜像，默认为 `quay.io/vektorlab/ctop:0.7.2` |
| --docker-socket |           | 指定 ctop 使用的 Docker Socket，默认为 `/var/run/docker.sock` |

例子：

```
$ tkctl ctop demo-cluster-tikv-0
$ tkctl ctop node/172.16.4.155
```

### tkctl help [command]

该命令用于展示各个子命令的帮助信息。

例子：

```
$ tkctl help debug
```

### tkctl options

该命令用于展示 `tkctl` 的所有的全局参数。

例子：

```
$ tkctl options
The following options can be passed to any command:

      --alsologtostderr=false: log to standard error as well as files
      --as='': Username to impersonate for the operation
      --as-group=[]: Group to impersonate for the operation, this flag can be repeated to specify multiple groups.
      --cache-dir='/Users/alei/.kube/http-cache': Default HTTP cache directory
      --certificate-authority='': Path to a cert file for the certificate authority
      --client-certificate='': Path to a client certificate file for TLS
      --client-key='': Path to a client key file for TLS
      --cluster='': The name of the kubeconfig cluster to use
      --context='': The name of the kubeconfig context to use
      --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity. This will
make your HTTPS connections insecure
      --kubeconfig='': Path to the kubeconfig file to use for CLI requests.
      --log_backtrace_at=:0: when logging hits line file:N, emit a stack trace
      --log_dir='': If non-empty, write log files in this directory
      --logtostderr=true: log to standard error instead of files
  -n, --namespace='': If present, the namespace scope for this CLI request
      --request-timeout='0': The length of time to wait before giving up on a single server request. Non-zero values
should contain a corresponding time unit (e.g. 1s, 2m, 3h). A value of zero means don't timeout requests.
  -s, --server='': The address and port of the Kubernetes API server
      --stderrthreshold=2: logs at or above this threshold go to stderr
  -t, --tidbcluster='': Tidb cluster name
      --token='': Bearer token for authentication to the API server
      --user='': The name of the kubeconfig user to use
  -v, --v=0: log level for V logs
      --vmodule=: comma-separated list of pattern=N settings for file-filtered logging
```

这些参数主要用于指定如何连接 Kubernetes 集群，其中最常用的参数是： 

- `--context`：指定目标 Kubernetes 集群
- `--namespace`：指定 Namespace

