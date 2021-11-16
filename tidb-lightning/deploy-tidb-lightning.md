---
title: TiDB Lightning 部署与执行
aliases: ['/docs-cn/stable/tidb-lightning/deploy-tidb-lightning/','/docs-cn/v4.0/tidb-lightning/deploy-tidb-lightning/','/docs-cn/stable/reference/tools/tidb-lightning/deployment/']
---

# TiDB Lightning 部署与执行

本文主要介绍 TiDB Lightning 使用 Local-backend 进行数据导入的硬件需求，以及使用 TiDB Ansible 部署与手动部署 TiDB Lightning 这两种部署方式。

如果使用 Local-backend 进行数据导入，TiDB Lightning 运行后，**TiDB 集群将无法正常对外提供服务**。如果你不希望 TiDB 集群的对外服务受到影响，可以参考 [TiDB Lightning TiDB-backend](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-tidb-backend) 中的硬件需求与部署方式进行数据导入。

## 注意事项

在使用 TiDB Lightning 前，需注意以下事项：

- 若 `tidb-lightning` 崩溃，集群会留在“导入模式”。若忘记转回“普通模式”，集群会产生大量未压缩的文件，继而消耗 CPU 并导致延迟。此时，需要使用 `tidb-lightning-ctl` 手动将集群转回“普通模式”：

    {{< copyable "shell-regular" >}}

    ```sh
    bin/tidb-lightning-ctl --switch-mode=normal
    ```

- TiDB Lightning 需要下游 TiDB 有如下权限：

    | 权限 | 作用域 |
    |:----|:------|
    | SELECT | Tables |
    | INSERT | Tables |
    | UPDATE | Tables |
    | DELETE | Tables |
    | CREATE | Databases, tables |
    | DROP | Databases, tables |
    | ALTER | Tables |

  如果配置项 `checksum = true`，则 TiDB Lightning 需要有下游 TiDB admin 用户权限。

## 硬件需求

`tidb-lightning`为资源密集程序，为了优化效能，建议硬件配置如下：

- 32+ 逻辑核 CPU
- 20GB+ 内存
- 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
- 使用万兆网卡，带宽需要 1GB/s 以上
- 运行过程默认会占满 CPU，建议单独部署。条件不允许的情况下可以和其他组件（比如 `tikv-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 使用 CPU 资源。

> **注意：**
>
> - `tidb-lightning` 是 CPU 密集型程序，如果和其它程序混合部署，需要通过 `region-concurrency` 限制 `tidb-lightning` 的 CPU 实际占用核数，否则会影响其他程序的正常运行。建议将混合部署机器上 75% 的 CPU 资源分配给 `tidb-lightning`。例如，机器为 32 核，则 `tidb-lightning` 的 `region-concurrency` 可设为 “24”。

此外，目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/deploy-and-maintain-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。

## 导出数据

使用 [`dumpling`](/dumpling-overview.md) 从 MySQL 导出数据，如下：

{{< copyable "shell-regular" >}}

```sh
./bin/dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-f test.t[12]`：只导出 `test.t1` 和 `test.t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256MB`：将每张表切分成多个文件，每个文件大小约为 256 MB。

如果数据源是 CSV 文件，请参考 [CSV 支持](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)获取配置信息。

## 部署 TiDB Lightning

本节介绍 TiDB Lightning 的两种部署方式：[使用 TiDB Ansible 部署](#使用-tidb-ansible-部署-tidb-lightning)和[手动部署](#手动部署-tidb-lightning)。

### 使用 TiDB Ansible 部署 TiDB Lightning

TiDB Lightning 可随 TiDB 集群一起用 [TiDB Ansible 部署](/online-deployment-using-ansible.md)。

1. 编辑 `inventory.ini`，为 `tidb-lightning` 配置一个 IP。

    ```ini
    ...
    [lightning_server]
    192.168.20.10

    ...
    ```

2. 修改 `group_vars/*.yml` 的变量配置 `tidb-lightning`。

    - `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # 提供监控告警的端口。需对监控服务器 (monitoring_server) 开放。
        tidb_lightning_pprof_port: 8289

        # 获取数据源（Dumpling SQL dump 或 CSV）的路径。
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

3. 开始部署。

    {{< copyable "shell-regular" >}}

    ```sh
    ansible-playbook bootstrap.yml &&
    ansible-playbook deploy.yml
    ```

4. 将数据源写入 `data_source_dir` 指定的路径。

5. 登录 `tidb-lightning` 的服务器，编辑 `conf/tidb-lighting.toml` 如下配置项：

    ```
    [tikv-importer]
    # 选择使用 local 模式
    backend = "local"
    # 设置排序的键值对的临时存放地址，目标路径需要是一个空目录
    "sorted-kv-dir" = "/mnt/ssd/sorted-kv-dir"
    
    [tidb]
    # pd-server 的地址，填一个即可
    pd-addr = "172.16.31.4:2379"
    ```

6. 登录 `tidb-lightning` 的服务器，并执行以下命令来启动 Lightning，开始导入过程。

    {{< copyable "shell-regular" >}}

    ```sh
    scripts/start_lightning.sh
    ```

### 手动部署 TiDB Lightning

#### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

#### 第 2 步：下载 TiDB Lightning 安装包

在[工具下载](/download-ecosystem-tools.md#tidb-lightning)页面下载 TiDB Lightning 安装包（需选择与 TiDB 集群相同的版本）。

#### 第 3 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。对于没有出现在下述模版中的配置，TiDB Lightning 给出配置错误的提醒并退出。`sorted-kv-dir`需要设置为一个空的目录，并且确保所在的磁盘有较多空闲的空间。

    ```toml
    [lightning]

    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    # region-concurrency =

    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # backend 设置为 local 模式
    backend = "local"
    # 设置本地临时存储路径
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Mydumper 源数据目录。
    data-source-dir = "/data/my_database"

    [tidb]
    # 目标集群的信息。tidb-server 的监听地址，填一个即可。
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    # pd-server 的地址，填一个即可
    pd-addr = "172.16.31.4:2379"
    ```

    上面仅列出了 `tidb-lightning` 的基本配置信息。完整配置信息请参考[`tidb-lightning` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)。

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## 升级 TiDB Lightning

你可以通过替换二进制文件升级 TiDB Lightning，无需其他配置。重启 TiDB Lightning 的具体操作参见 [FAQ](/tidb-lightning/tidb-lightning-faq.md#如何正确重启-tidb-lightning)。

如果当前有运行的导入任务，推荐任务完成后再升级 TiDB Lightning。否则，你可能需要从头重新导入，因为无法保证断点可以跨版本工作。
