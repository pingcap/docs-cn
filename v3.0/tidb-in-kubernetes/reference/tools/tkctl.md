---
title: TiDB Kubernetes Control User Guide
summary: Learn how to use the tkctl (TiDB Kubernetes Control) tool.
category: reference
---

# TiDB Kubernetes Control User Guide

TiDB Kubernetes Control (`tkctl`) is a command line utility that is used for TiDB Operator to maintain and diagnose the TiDB cluster in Kubernetes.

## Installation

To install `tkctl`, you can download the pre-built binary or build `tkctl` from source.

### Download the latest pre-built binary

- [MacOS](https://download.pingcap.org/tkctl-darwin-amd64-latest.tgz)
- [Linux](https://download.pingcap.org/tkctl-linux-amd64-latest.tgz)
- [Windows](https://download.pingcap.org/tkctl-windows-amd64-latest.tgz)

After unzipping the downloaded file, you can add the `tkctl` executable file to your `PATH` to finish the installation.

### Build from source

Requirement: [Go](https://golang.org/) >= the 1.11 version or later

{{< copyable "shell-regular" >}}

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator.git && \
GOOS=<YOUR_GOOS> make cli &&\
mv tkctl /usr/local/bin/tkctl
```

### Shell auto-completion

You can configure the shell auto-completion for `tkctl` to simplify its usage.

To configure the auto-completion for `BASH`, you need to first install the [bash-completion](https://github.com/scop/bash-completion) package, and configure with either of the two methods below:

- Configure auto-completion in the current shell:

    {{< copyable "shell-regular" >}}

    ```shell
    source <(tkctl completion bash)
    ```

- Add auto-completion permanently to your bash shell:

    {{< copyable "shell-regular" >}}

    ```shell
    echo "if hash tkctl 2>/dev/null; then source <(tkctl completion bash); fi" >> ~/.bashrc
    ```

To configure the auto-completion for `ZSH`, you can choose from either of the two methods below:

- Configure auto-completion in the current shell:

    {{< copyable "shell-regular" >}}

    ```shell
    source <(tkctl completion zsh)
    ```

- Add auto-completion permanently to your zsh shell:

    {{< copyable "shell-regular" >}}

    ```shell
    echo "if hash tkctl 2>/dev/null; then source <(tkctl completion zsh); fi" >> ~/.zshrc
    ```

### Kubernetes configuration

`tkctl` reuses the `kubeconfig` file (the default location is `~/.kube/config`) to connect with the Kubernetes cluster. You can verify whether `kubeconfig` is correctly configured by using the following command:

{{< copyable "shell-regular" >}}

```shell
tkctl version
```

If the above command correctly outputs the version of TiDB Operator on the server side, then `kubeconfig` is correctly configured.

## Commands

### tkctl version

This command is used to show the version of the local **tkctl** and **tidb-operator** installed in the target cluster.

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl version
```

```
Client Version: v1.0.0-beta.1-p2-93-g6598b4d3e75705-dirty
TiDB Controller Manager Version: pingcap/tidb-operator:latest
TiDB Scheduler Version: pingcap/tidb-operator:latest
```

### tkctl list

This command is used to list all installed TiDB clusters.

| Flag | Abbreviation | Description |
| ----- | --------- | ----------- |
| --all-namespaces | -A | Whether to search all Kubernetes namespaces |
| --output | -o | The output format; you can choose from [default,json,yaml], and the default format is `default` |

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl list -A
```

```
NAMESPACE NAME           PD    TIKV   TIDB   AGE
foo       demo-cluster   3/3   3/3    2/2    11m
bar       demo-cluster   3/3   3/3    1/2    11m
```

### tkctl use

This command is used to specify the TiDB cluster that the current `tkctl` command operates on. After you specify a TiDB cluster by using this command, all commands that operates on a cluster will automatically select this cluster so the `--tidbcluster` option can be omitted.

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl use --namespace=foo demo-cluster
```

```
Tidb cluster switched to foo/demo-cluster
```

### tkctl info

This command is used to display information about the TiDB cluster.

| Flag | Abbreviation | Description |
| ----- | --------- | ----------- |
| --tidb-cluster | -t | Specify a TiDB cluster; default to the TiDB cluster that is being used |

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl info
```

```
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

This is a group of commands that are used to get the details of TiDB cluster components.

You can query the following components: `pd`, `tikv`, `tidb`, `volume` and `all` (to query all components).

| Flag | Abbreviation | Description |
| ----- | --------- | ----------- |
| --tidb-cluster | -t | Specify a TiDB cluster; default to the TiDB cluster that is being used |
| --output | -o | The output format; you can choose from [default,json,yaml], and the default format is `default` |

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl get tikv
```

```
NAME                  READY   STATUS    MEMORY          CPU   RESTARTS   AGE     NODE
demo-cluster-tikv-0   2/2     Running   2098Mi/4196Mi   2/2   0          3m19s   172.16.4.155
demo-cluster-tikv-1   2/2     Running   2098Mi/4196Mi   2/2   0          4m8s    172.16.4.160
demo-cluster-tikv-2   2/2     Running   2098Mi/4196Mi   2/2   0          4m45s   172.16.4.157
```

{{< copyable "shell-regular" >}}

```shell
tkctl get volume
```

```
VOLUME              CLAIM                      STATUS   CAPACITY   NODE           LOCAL
local-pv-d5dad2cf   tikv-demo-cluster-tikv-0   Bound    1476Gi     172.16.4.155   /mnt/disks/local-pv56
local-pv-5ade8580   tikv-demo-cluster-tikv-1   Bound    1476Gi     172.16.4.160   /mnt/disks/local-pv33
local-pv-ed2ffe50   tikv-demo-cluster-tikv-2   Bound    1476Gi     172.16.4.157   /mnt/disks/local-pv13
local-pv-74ee0364   pd-demo-cluster-pd-0       Bound    1476Gi     172.16.4.155   /mnt/disks/local-pv46
local-pv-842034e6   pd-demo-cluster-pd-1       Bound    1476Gi     172.16.4.158   /mnt/disks/local-pv74
local-pv-e54c122a   pd-demo-cluster-pd-2       Bound    1476Gi     172.16.4.156   /mnt/disks/local-pv72
```

### tkctl debug [pod_name]

This command is used to diagnose the Pods in a TiDB cluster. It launches a debug container with the specified docker image on the host that holds the target Pod. The container has the necessary troubleshooting tools installed and shares the namespace with the container in the target Pod, so you can seamlessly diagnose the target container by using various tools in the debug container.

| Flag | Abbreviation | Description |
| ----- | --------- | ----------- |
| --image |    | Specify the docker image used by the debug container; default to `pingcap/tidb-debug:lastest` |
| --container | -c | Select the container to be diagnosed; default to the first container of the target Pod |
| --docker-socket |    | Specify the docker socket on the target node; default to `/var/run/docker.sock` |
| --privileged |    | Whether to enable the [privileged](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities) mode for the debug container |

> **Note:**
>
> The default image of the debug container contains various troubleshooting tools, so the image size is relatively large. If you only need `pd-ctl` and `tidb-ctl`, you can specify using the `tidb-control` image by using the `--image=pingcap/tidb-control:latest` command line option.

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl debug demo-cluster-tikv-0
```

{{< copyable "shell-regular" >}}

```shell
ps -ef
```

Using tools like `GDB` and `perf` in the debug container requires special operations because of the difference in root filesystems of the target container and the debug container.

#### GDB

When you use GDB to debug the process in the target container, make sure you set the `program` option to the binary in the **target container**. Additionally, if you use images other than `tidb-debug` as the debug container or if the `pid` of the target process is not 1, you have to configure the location of dynamic libraries via the `set sysroot` command as follows:

{{< copyable "shell-regular" >}}

```shell
tkctl debug demo-cluster-tikv-0
```

{{< copyable "shell-regular" >}}

```shell
gdb /proc/${pid:-1}/root/tikv-server 1
```

{{< copyable "shell-regular" >}}

The `.gdbinit` pre-configured in the `tidb-debug` image will set `sysroot` to `/proc/1/root/` automatically. For this reason, you can omit this following step if you are using the `tidb-debug` image and the `pid` of the target process is 1.

{{< copyable "shell-regular" >}}

```shell
(gdb) set sysroot /proc/${pid}/root/
```

Start debugging:

{{< copyable "shell-regular" >}}

```shell
(gdb) thread apply all bt
```

{{< copyable "shell-regular" >}}

```shell
(gdb) info threads
```

#### Perf and flame graphs

To use the `perf` command and the `run_flamegraph.sh` script properly, you must copy the program from the target container to the same location in the debug container:

{{< copyable "shell-regular" >}}

```shell
tkctl debug demo-cluster-tikv-0
```

{{< copyable "shell-regular" >}}

```shell
cp /proc/1/root/tikv-server /
```

{{< copyable "shell-regular" >}}

```shell
./run_flamegraph.sh 1
```

This script automatically uploads the generated flame graph (SVG format) to `transfer.sh`, and you can visit the link outputted by the script to download the flame graph.

### tkctl ctop

The complete form of the command is `tkctl ctop [pod_name | node/node_name ]`.

This command is used to view the real-time monitoring stats of the target Pod or node in the cluster. Compared with `kubectl top`, `tkctl ctop` also provides network and disk stats, which are important for diagnosing problems in the TiDB cluster.

| Flag | Abbreviation | Description |
| ----- | --------- | ----------- |
| --image |    | Specify the docker image of ctop; default to `quay.io/vektorlab/ctop:0.7.2` |
| --docker-socket |    | Specify the docker socket that ctop uses; default to `/var/run/docker.sock` |

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl ctop node/172.16.4.155
```

{{< copyable "shell-regular" >}}

```shell
tkctl ctop demo-cluster-tikv-0
```

### tkctl help [command]

This command is used to print help messages of the sub commands.

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl help debug
```

### tkctl options

This command is used to view the global flags of `tkctl`.

For example:

{{< copyable "shell-regular" >}}

```shell
tkctl options
```

```
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

These options are mainly used to connect with the Kubernetes cluster and two commonly used options among them are as follows:

- `--context`: specify the target Kubernetes cluster
- `--namespace`: specify the Kubernetes namespace
