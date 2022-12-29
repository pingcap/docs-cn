---
title: 为 TiDB 组件间通信开启加密传输
aliases: ['/docs-cn/dev/enable-tls-between-components/','/docs-cn/dev/how-to/secure/enable-tls-between-components/']
---

# 为 TiDB 组件间通信开启加密传输

本部分介绍如何为 TiDB 集群内各部组件间开启加密传输，一旦开启以下组件间均将使用加密传输：

- TiDB 与 TiKV、PD
- TiKV 与 PD
- TiDB Control 与 TiDB，TiKV Control 与 TiKV，PD Control 与 PD
- TiKV、PD、TiDB 各自集群内内部通讯

目前暂不支持只开启其中部分组件的加密传输。

## 配置开启加密传输

1. 准备证书。

    推荐为 TiDB、TiKV、PD 分别准备一个 Server 证书，并保证可以相互验证，而它们的 Control 工具则可选择共用 Client 证书。

    有多种工具可以生成自签名证书，如 `openssl`，`easy-rsa`，`cfssl`。

    这里提供一个使用 `openssl` 生成证书的示例：[生成自签名证书](/generate-self-signed-certificates.md)。

2. 配置证书。

    - TiDB

        在 `config` 文件或命令行参数中设置：

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

    - TiKV

        在 `config` 文件或命令行参数中设置，并设置相应的 URL 为 https：

        ```toml
        [security]
        # set the path for certificates. Empty string means disabling secure connectoins.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tikv-server.pem"
        key-path = "/path/to/tikv-server-key.pem"
        ```

    - PD

        在 `config` 文件或命令行参数中设置，并设置相应的 URL 为 https：

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
        cacert-path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    - TiFlash（从 v4.0.5 版本开始引入）

        在 `tiflash.toml` 文件中设置，将 `http_port` 项改为 `https_port`:

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
        ca_path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert_path = "/path/to/tiflash-server.pem"
        # Path of file that contains X509 key in PEM format.
        key_path = "/path/to/tiflash-server-key.pem"
        ```

        在 `tiflash-learner.toml` 文件中设置，

        ```toml
        [security]
        # Sets the path for certificates. The empty string means that secure connections are disabled.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tiflash-server.pem"
        key-path = "/path/to/tiflash-server-key.pem"
        ```

    - TiCDC

        在 `config` 文件中设置

        ```toml
        [security]
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/cdc-server.pem"
        key-path = "/path/to/cdc-server-key.pem"
        ```

        或者在启动命令行中设置，并设置相应的 URL 为 `https`：

        {{< copyable "shell-regular" >}}

        ```bash
        cdc server --pd=https://127.0.0.1:2379 --log-file=ticdc.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301 --ca=/path/to/ca.pem --cert=/path/to/ticdc-cert.pem --key=/path/to/ticdc-key.pem
        ```

    此时 TiDB 集群各个组件间已开启加密传输。

    > **注意：**
    >
    > 若 TiDB 集群各个组件间开启加密传输后，在使用 tidb-ctl、tikv-ctl 或 pd-ctl 工具连接集群时，需要指定 client 证书，示例：

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    tiup ctl:<cluster-version> pd -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

## 认证组件调用者身份

通常被调用者除了校验调用者提供的密钥、证书和 CA 有效性外，还需要校验调用方身份以防止拥有有效证书的非法访问者进行访问（例如：TiKV 只能被 TiDB 访问，需阻止拥有合法证书但非 TiDB 的其他访问者访问 TiKV）。

如希望进行组件调用者身份认证，需要在生证书时通过 `Common Name` 标识证书使用者身份，并在被调用者配置检查证书 `Common Name` 列表来检查调用者身份。

- TiDB

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cluster-verify-cn = [
      "TiDB-Server",
      "TiKV-Control",
    ]
    ```

- TiKV

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cert-allowed-cn = [
        "TiDB-Server", "PD-Server", "TiKV-Control", "RawKvClient1",
    ]
    ```

- PD

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cert-allowed-cn = ["TiKV-Server", "TiDB-Server", "PD-Control"]
    ```

- TiFlash（从 v4.0.5 版本开始引入）

    在 `tiflash.toml` 文件中设置：

    ```toml
    [security]
    cert_allowed_cn = ["TiKV-Server", "TiDB-Server"]
    ```

    在 `tiflash-learner.toml` 文件中设置：

    ```toml
    [security]
    cert-allowed-cn = ["PD-Server", "TiKV-Server", "TiFlash-Server"]
    ```

## TiUP 开启组件加密

该步骤以为已存在但并未开启组件加密的集群为例，为其开启组件加密，步骤及说明如下：

1. tiup v1.9.0 版本开始支持通过 tiup cluster tls 命令方式对已部署的 TiDB 集群开启或关闭 TLS 加密。该操作不支持在线进行，需要重启集群。并通过 `tiup cluster tls ${cluster_name} enable/disable` 命令开启或关闭 TLS 组件加密。首先，查看集群初始状态如下：

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ssl-test]# tiup cluster display tidb-prod
    tiup is checking updates for component cluster ...
    Starting component `cluster`: /root/.tiup/components/cluster/v1.9.4/tiup-cluster /root/.tiup/components/cluster/v1.9.4/tiup-cluster display tidb-prod
    Cluster type:       tidb
    Cluster name:       tidb-prod
    Cluster version:    v5.4.0
    Deploy user:        root
    SSH type:           builtin
    Dashboard URL:      http://10.0.2.29:2379/dashboard
    ID                Role          Host        Ports        OS/Arch       Status  Data Dir                    Deploy Dir
    --                ----          ----        -----        -------       ------  --------                    ----------
    10.0.0.83:9093    alertmanager  10.0.0.83   9093/9094    linux/x86_64  Up      /data1/alertmanager-9093    /tidb-deploy/alertmanager-9093
    10.0.0.88:2379    pd            10.0.0.88   2379/2380    linux/x86_64  Up      /data1/pd-2379              /tidb-deploy/pd-2379
    10.0.1.185:2379   pd            10.0.1.185  2379/2380    linux/x86_64  Up|L    /data1/pd-2379              /tidb-deploy/pd-2379
    10.0.2.29:2379    pd            10.0.2.29   2379/2380    linux/x86_64  Up|UI   /data1/pd-2379              /tidb-deploy/pd-2379
    10.0.0.83:9090    prometheus    10.0.0.83   9090/12020   linux/x86_64  Up      /data1/prometheus-9090      /tidb-deploy/prometheus-9090
    10.0.0.85:8250    pump          10.0.0.85   8250         linux/x86_64  Up      /data1/tidb-data/pump-8250  /data1/tidb-deploy/pump-8250
    10.0.1.183:8250   pump          10.0.1.183  8250         linux/x86_64  Up      /data1/tidb-data/pump-8250  /data1/tidb-deploy/pump-8250
    10.0.0.86:4000    tidb          10.0.0.86   4000/10080   linux/x86_64  Up      -                           /tidb-deploy/tidb-4000
    10.0.1.184:4000   tidb          10.0.1.184  4000/10080   linux/x86_64  Up      -                           /tidb-deploy/tidb-4000
    10.0.2.28:4000    tidb          10.0.2.28   4000/10080   linux/x86_64  Up      -                           /tidb-deploy/tidb-4000
    10.0.0.85:20160   tikv          10.0.0.85   20160/20180  linux/x86_64  Up      /data1/tikv-20160           /tidb-deploy/tikv-20160
    10.0.1.183:20160  tikv          10.0.1.183  20160/20180  linux/x86_64  Up      /data1/tikv-20160           /tidb-deploy/tikv-20160
    10.0.2.27:20160   tikv          10.0.2.27   20160/20180  linux/x86_64  Up      /data1/tikv-20160           /tidb-deploy/tikv-20160
    Total nodes: 13
    ```

2. 通过 tiup cluster edit-config tidb-prod 将要缩容的 pd 节点信息保存到单独文件，方便后续扩容。 因为通过 `tiup cluster tls ${cluster_name} enable/disable` 开启或关闭 TLS 都需要先将 PD 节点缩容到 1 个节点，然后执行 enable/disable 操作，等待操作完成之后将 PD 节点重新扩容回之前状态。这是由于 ETCD 机制限制。  
注意：`tiup cluster tls ${cluster_name} enable/disable` 方式开启或关闭 TLS 时会重启 TiDB 集群，行为类似于 tiup cluster restart ，并不会滚动重启节点。

    ```yaml
    pd_servers:
    - host: 10.0.2.29
      ssh_port: 22
      name: pd-10.0.2.29-2379
      client_port: 2379
      peer_port: 2380
      deploy_dir: /tidb-deploy/pd-2379
      data_dir: /data1/pd-2379
      log_dir: /tidb-deploy/pd-2379/log
      arch: amd64
      os: linux
    - host: 10.0.0.88
      ssh_port: 22
      name: pd-10.0.0.88-2379
      client_port: 2379
      peer_port: 2380
      deploy_dir: /tidb-deploy/pd-2379
      data_dir: /data1/pd-2379
      log_dir: /tidb-deploy/pd-2379/log
      arch: amd64
      os: linux
    ```

3. 将 PD 节点缩容至 1 个节点

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ssl-test]# tiup cluster scale-in tidb-prod -N 10.0.0.88:2379,10.0.2.29:2379
    ......
    Do you want to continue? [y/N]:(default=N) y
    Scale-in nodes...
    + [ Serial ] - SSHKeySet: privateKey=/root/.tiup/storage/cluster/clusters/tidb-prod/ssh/id_rsa, publicKey=/root/.tiup/storage/cluster/clusters/
    ......
    + Reload prometheus and grafana
      - Reload prometheus -> 10.0.0.83:9090 ... Done
    Scaled cluster `tidb-prod` in successfully
    
    [root@iZuf6d7xln13sovvijl68rZ ssl-test]# tiup cluster display tidb-prod
    tiup is checking updates for component cluster ...
    Starting component `cluster`: /root/.tiup/components/cluster/v1.9.4/tiup-cluster /root/.tiup/components/cluster/v1.9.4/tiup-cluster display tidb-prod
    Cluster type:       tidb
    Cluster name:       tidb-prod
    Cluster version:    v5.4.0
    Deploy user:        root
    SSH type:           builtin
    Dashboard URL:      http://10.0.1.185:2379/dashboard
    ID                Role          Host        Ports        OS/Arch       Status   Data Dir                    Deploy Dir
    --                ----          ----        -----        -------       ------   --------                    ----------
    10.0.0.83:9093    alertmanager  10.0.0.83   9093/9094    linux/x86_64  Up       /data1/alertmanager-9093    /tidb-deploy/alertmanager-9093
    10.0.1.185:2379   pd            10.0.1.185  2379/2380    linux/x86_64  Up|L|UI  /data1/pd-2379              /tidb-deploy/pd-2379
    10.0.0.83:9090    prometheus    10.0.0.83   9090/12020   linux/x86_64  Up       /data1/prometheus-9090      /tidb-deploy/prometheus-9090
    10.0.0.85:8250    pump          10.0.0.85   8250         linux/x86_64  Up       /data1/tidb-data/pump-8250  /data1/tidb-deploy/pump-8250
    10.0.1.183:8250   pump          10.0.1.183  8250         linux/x86_64  Up       /data1/tidb-data/pump-8250  /data1/tidb-deploy/pump-8250
    10.0.0.86:4000    tidb          10.0.0.86   4000/10080   linux/x86_64  Up       -                           /tidb-deploy/tidb-4000
    10.0.1.184:4000   tidb          10.0.1.184  4000/10080   linux/x86_64  Up       -                           /tidb-deploy/tidb-4000
    10.0.2.28:4000    tidb          10.0.2.28   4000/10080   linux/x86_64  Up       -                           /tidb-deploy/tidb-4000
    10.0.0.85:20160   tikv          10.0.0.85   20160/20180  linux/x86_64  Up       /data1/tikv-20160           /tidb-deploy/tikv-20160
    10.0.1.183:20160  tikv          10.0.1.183  20160/20180  linux/x86_64  Up       /data1/tikv-20160           /tidb-deploy/tikv-20160
    10.0.2.27:20160   tikv          10.0.2.27   20160/20180  linux/x86_64  Up       /data1/tikv-20160           /tidb-deploy/tikv-20160
    Total nodes: 11
    ```

4. 通过 tiup cluster tls tidb-prod enable 开启 TLS

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ssl-test]# tiup cluster tls tidb-prod enable
    ......
    Enable/Disable TLS will stop and restart the cluster `tidb-prod`
    Do you want to continue? [y/N]:(default=N) y
    Generate certificate: /root/.tiup/storage/cluster/clusters/tidb-prod/tls
    + [ Serial ] - SSHKeySet: privateKey=/root/.tiup/storage/cluster/clusters/tidb-prod/ssh/id_rsa, publicKey=/root/.tiup/storage/cluster/clusters/tidb-prod/ssh/id_rsa.pub
    ......
            Start 10.0.2.28 success
            Start 10.0.1.185 success
    + [ Serial ] - Reload PD Members
            Update pd-10.0.1.185-2379 peerURLs: [https://10.0.1.185:2380]
    Enabled TLS between TiDB components for cluster `tidb-prod` successfully
    ```

5. 查看集群状态  

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ~]# tiup cluster display tidb-prod
    tiup is checking updates for component cluster ...
    Starting component `cluster`: /root/.tiup/components/cluster/v1.9.4/tiup-cluster /root/.tiup/components/cluster/v1.9.4/tiup-cluster display tidb-prod
    Cluster type:       tidb
    Cluster name:       tidb-prod
    Cluster version:    v5.4.0
    Deploy user:        root
    SSH type:           builtin
    TLS encryption:     enabled
    CA certificate:     /root/.tiup/storage/cluster/clusters/tidb-prod/tls/ca.crt
    Client private key: /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.pem
    Client certificate: /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.crt
    Dashboard URL:      https://10.0.1.185:2379/dashboard
    ID                Role          Host        Ports        OS/Arch       Status   Data Dir                       Deploy Dir
    --                ----          ----        -----        -------       ------   --------                       ----------
    10.0.0.83:9093    alertmanager  10.0.0.83   9093/9094    linux/x86_64  Up       /data1/alertmanager-9093       /tidb-deploy/alertmanager-9093
    10.0.2.27:8249    drainer       10.0.2.27   8249         linux/x86_64  Up       /data1/tidb-data/drainer-8249  /data1/tidb-deploy/drainer-8249
    10.0.1.185:2379   pd            10.0.1.185  2379/2380    linux/x86_64  Up|L|UI  /data1/pd-2379                 /tidb-deploy/pd-2379
    10.0.0.83:9090    prometheus    10.0.0.83   9090/12020   linux/x86_64  Up       /data1/prometheus-9090         /tidb-deploy/prometheus-9090
    10.0.0.85:8250    pump          10.0.0.85   8250         linux/x86_64  Up       /data1/tidb-data/pump-8250     /data1/tidb-deploy/pump-8250
    10.0.1.183:8250   pump          10.0.1.183  8250         linux/x86_64  Up       /data1/tidb-data/pump-8250     /data1/tidb-deploy/pump-8250
    10.0.0.86:4000    tidb          10.0.0.86   4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.1.184:4000   tidb          10.0.1.184  4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.2.28:4000    tidb          10.0.2.28   4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.0.85:20160   tikv          10.0.0.85   20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    10.0.1.183:20160  tikv          10.0.1.183  20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    10.0.2.27:20160   tikv          10.0.2.27   20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    Total nodes: 12
    ```

6. 验证  TLS 开启情况

    注意：在 -u 指定 pd 地址时，需要使用 https 协议
    检查 pd-ctl 执行 member 命令，输出的结果中对应的 peer_urls 以及 client_urls 都变为了 https 协议。若不为 https 协议，则需要检查环境，执行 tiup cluster tls ${cluster_name} disable 回退操作；如果都是 https 协议，则 可以进行下一步骤。

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ~]# export PDTLS="--cacert /root/.tiup/storage/cluster/clusters/tidb-prod/tls/ca.crt --cert /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.crt --key /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.pem"
    [root@iZuf6d7xln13sovvijl68rZ ~]# tiup ctl:v5.4.0 pd -u https://10.0.1.185:2379 $PDTLS -i
    ......
    » member
    {
      "header": {
        "cluster_id": 7094548242622134819
      },
      "members": [
        {
          "name": "pd-10.0.1.185-2379",
          "member_id": 6720685150051887399,
          "peer_urls": [
            "https://10.0.1.185:2380"
          ],
          "client_urls": [
            "https://10.0.1.185:2379"
          ],
          "deploy_path": "/tidb-deploy/pd-2379/bin",
          "binary_version": "v5.4.0",
          "git_hash": "e3807695b6fc524f9cb84402937e56e733cabd64"
        }
      ],
      "leader": {
        "name": "pd-10.0.1.185-2379",
        "member_id": 6720685150051887399,
        "peer_urls": [
          "https://10.0.1.185:2380"
        ],
        "client_urls": [
          "https://10.0.1.185:2379"
        ],
        "deploy_path": "/tidb-deploy/pd-2379/bin",
        "binary_version": "v5.4.0",
        "git_hash": "e3807695b6fc524f9cb84402937e56e733cabd64"
      },
      "etcd_leader": {
        "name": "pd-10.0.1.185-2379",
        "member_id": 6720685150051887399,
        "peer_urls": [
          "https://10.0.1.185:2380"
        ],
        "client_urls": [
          "https://10.0.1.185:2379"
        ],
        "deploy_path": "/tidb-deploy/pd-2379/bin",
        "binary_version": "v5.4.0",
        "git_hash": "e3807695b6fc524f9cb84402937e56e733cabd64"
      }
    }
    ```

7. 根据之前缩容前保存的拓扑信息，扩容 pd 节点  

    ```shell
    tiup cluster scale-out ${cluster_name} ./scale-pd.yaml
    ```

8. 检查集群，并且尝试连接验证集群

    ```shell
    [root@iZuf6d7xln13sovvijl68rZ ~]# tiup cluster display tidb-prod
    tiup is checking updates for component cluster ...
    Starting component `cluster`: /root/.tiup/components/cluster/v1.9.4/tiup-cluster /root/.tiup/components/cluster/v1.9.4/tiup-cluster display tidb-prod
    Cluster type:       tidb
    Cluster name:       tidb-prod
    Cluster version:    v5.4.0
    Deploy user:        root
    SSH type:           builtin
    TLS encryption:     enabled
    CA certificate:     /root/.tiup/storage/cluster/clusters/tidb-prod/tls/ca.crt
    Client private key: /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.pem
    Client certificate: /root/.tiup/storage/cluster/clusters/tidb-prod/tls/client.crt
    Dashboard URL:      https://10.0.1.185:2379/dashboard
    ID                Role          Host        Ports        OS/Arch       Status   Data Dir                       Deploy Dir
    --                ----          ----        -----        -------       ------   --------                       ----------
    10.0.0.83:9093    alertmanager  10.0.0.83   9093/9094    linux/x86_64  Up       /data1/alertmanager-9093       /tidb-deploy/alertmanager-9093
    10.0.2.27:8249    drainer       10.0.2.27   8249         linux/x86_64  Up       /data1/tidb-data/drainer-8249  /data1/tidb-deploy/drainer-8249
    10.0.0.88:2379    pd            10.0.0.88   2379/2380    linux/x86_64  Up       /data1/pd-2379                 /tidb-deploy/pd-2379
    10.0.1.185:2379   pd            10.0.1.185  2379/2380    linux/x86_64  Up|L|UI  /data1/pd-2379                 /tidb-deploy/pd-2379
    10.0.2.29:2379    pd            10.0.2.29   2379/2380    linux/x86_64  Up       /data1/pd-2379                 /tidb-deploy/pd-2379
    10.0.0.83:9090    prometheus    10.0.0.83   9090/12020   linux/x86_64  Up       /data1/prometheus-9090         /tidb-deploy/prometheus-9090
    10.0.0.85:8250    pump          10.0.0.85   8250         linux/x86_64  Up       /data1/tidb-data/pump-8250     /data1/tidb-deploy/pump-8250
    10.0.1.183:8250   pump          10.0.1.183  8250         linux/x86_64  Up       /data1/tidb-data/pump-8250     /data1/tidb-deploy/pump-8250
    10.0.0.86:4000    tidb          10.0.0.86   4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.1.184:4000   tidb          10.0.1.184  4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.2.28:4000    tidb          10.0.2.28   4000/10080   linux/x86_64  Up       -                              /tidb-deploy/tidb-4000
    10.0.0.85:20160   tikv          10.0.0.85   20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    10.0.1.183:20160  tikv          10.0.1.183  20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    10.0.2.27:20160   tikv          10.0.2.27   20160/20180  linux/x86_64  Up       /data1/tikv-20160              /tidb-deploy/tikv-20160
    Total nodes: 14
    ```
    
## 证书重加载

TiDB、PD 和 TiKV 和各种 Client 都会在每次新建相互通讯的连接时重新读取当前的证书和密钥文件内容，实现证书和密钥的重加载。目前暂不支持 CA 的重加载。

## 另请参阅

- [为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)
