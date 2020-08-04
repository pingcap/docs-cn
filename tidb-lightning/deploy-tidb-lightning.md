---
title: TiDB Lightning 部署与执行
aliases: ['/docs-cn/v3.0/tidb-lightning/deploy-tidb-lightning/','/docs-cn/v3.0/reference/tools/tidb-lightning/deployment/','/docs-cn/tools/lightning/deployment/']
---

# TiDB Lightning 部署与执行

本文主要介绍 TiDB Lightning 使用 Importer-backend（默认）进行数据导入的硬件需求，以及使用 TiDB Ansible 部署与手动部署 TiDB Lightning 这两种部署方式。

如果你不希望影响 TiDB 集群的对外服务，可以参考 [TiDB Lightning TiDB-backend](/tidb-lightning/tidb-lightning-tidb-backend.md) 中的硬件需求与部署方式进行数据导入。

## 注意事项

在使用 TiDB Lightning 前，需注意以下事项：

- TiDB Lightning 运行后，TiDB 集群将无法正常对外提供服务。
- 若 `tidb-lightning` 崩溃，集群会留在“导入模式”。若忘记转回“普通模式”，集群会产生大量未压缩的文件，继而消耗 CPU 并导致延迟。此时，需要使用 `tidb-lightning-ctl` 手动将集群转回“普通模式”：

    {{< copyable "shell-regular" >}}

    ```sh
    bin/tidb-lightning-ctl -switch-mode=normal
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

`tidb-lightning` 和 `tikv-importer` 这两个组件皆为资源密集程序，建议各自单独部署。

为了优化效能，建议硬件配置如下：

- `tidb-lightning`

    - 32+ 逻辑核 CPU
    - 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程默认会占满 CPU，建议单独部署。条件不允许的情况下可以和其他组件（比如 `tidb-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 使用 CPU 资源。

- `tikv-importer`

    - 32+ 逻辑核 CPU
    - 40 GB+ 内存
    - 1 TB+ SSD 硬盘，IOPS 越高越好（要求 ≥8000）
        * 硬盘必须大于最大的 N 个表的大小总和，其中 N = max(index-concurrency, table-concurrency)。
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程中 CPU、I/O 和网络带宽都可能占满，建议单独部署。

如果机器充裕的话，可以部署多套 `tidb-lightning` + `tikv-importer`，然后将源数据以表为粒度进行切分，并发导入。

> **注意：**
>
> - `tidb-lightning` 是 CPU 密集型程序，如果和其它程序混合部署，需要通过 `region-concurrency` 限制 `tidb-lightning` 的 CPU 实际占用核数，否则会影响其他程序的正常运行。建议将混合部署机器上 75% 的 CPU 资源分配给 `tidb-lightning`。例如，机器为 32 核，则 `tidb-lightning` 的 `region-concurrency` 可设为 “24”。
>
> - `tikv-importer` 将中间数据存储缓存到内存上以加速导入过程。占用内存大小可以通过 **(`max-open-engines` × `write-buffer-size` × 2) + (`num-import-jobs` × `region-split-size` × 2)** 计算得来。如果磁盘写入速度慢，缓存可能会带来更大的内存占用。

此外，目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/tidb-faq.md#326-每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。

## 导出数据

使用 [`mydumper`](/mydumper-overview.md) 从 MySQL 导出数据，如下：

{{< copyable "shell-regular" >}}

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-T t1,t2`：只导出 `t1` 和 `t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256`：将每张表切分成多个文件，每个文件大小约为 256 MB。
- `--skip-tz-utc`：添加这个参数则会忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

如果数据源是 CSV 文件，请参考 [CSV 支持](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)获取配置信息。

## 部署 TiDB Lightning

本节介绍 TiDB Lightning 的两种部署方式：[使用 TiDB Ansible 部署](#使用-tidb-ansible-部署-tidb-lightning)和[手动部署](#手动部署-tidb-lightning)。

### 使用 TiDB Ansible 部署 TiDB Lightning

TiDB Lightning 可随 TiDB 集群一起用 [TiDB Ansible 部署](/online-deployment-using-ansible.md)。

1. 编辑 `inventory.ini`，分别配置一个 IP 来部署 `tidb-lightning` 和 `tikv-importer`。

    ```ini
    ...

    [importer_server]
    192.168.20.9

    [lightning_server]
    192.168.20.10

    ...
    ```

2. 修改 `group_vars/*.yml` 的变量配置这两个工具。

    - `group_vars/all.yml`

        ```yaml
        ...
        # tikv-importer 的监听端口。需对 tidb-lightning 服务器开放。
        tikv_importer_port: 8287
        ...
        ```

    - `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # 提供监控告警的端口。需对监控服务器 (monitoring_server) 开放。
        tidb_lightning_pprof_port: 8289

        # 获取数据源（Mydumper SQL dump 或 CSV）的路径。
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

    - `group_vars/importer_server.yml`

        ```yaml
        ---
        dummy:

        # 储存引擎文件的路径。需存放在空间足够大的分区。
        import_dir: "{{ deploy_dir }}/data.import"
        ```

3. 开始部署。

    {{< copyable "shell-regular" >}}

    ```sh
    ansible-playbook bootstrap.yml &&
    ansible-playbook deploy.yml
    ```

4. 将数据源写入 `data_source_dir` 指定的路径。

5. 登录 `tikv-importer` 的服务器，并执行以下命令来启动 Importer。

    {{< copyable "shell-regular" >}}

    ```sh
    scripts/start_importer.sh
    ```

6. 登录 `tidb-lightning` 的服务器，并执行以下命令来启动 Lightning，开始导入过程。

    {{< copyable "shell-regular" >}}

    ```sh
    scripts/start_lightning.sh
    ```

7. 完成后，在 `tikv-importer` 的服务器执行 `scripts/stop_importer.sh` 来关闭 Importer。

### 手动部署 TiDB Lightning

#### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考 [TiDB 快速入门指南](/overview.md#部署方式)。

#### 第 2 步：下载 TiDB Lightning 安装包

在[工具下载](/download-ecosystem-tools.md#tidb-lightning)页面下载 TiDB Lightning 安装包（需选择与 TiDB 集群相同的版本）。

#### 第 3 步：启动 `tikv-importer`

1. 从安装包上传 `bin/tikv-importer`。

2. 配置 `tikv-importer.toml`。

    ```toml
    # TiKV Importer 配置文件模版

    # 日志文件。
    log-file = "tikv-importer.log"
    # 日志等级：trace、debug、info、warn、error、off。
    log-level = "info"

    [server]
    # tikv-importer 监听的地址，tidb-lightning 需要连到这个地址进行数据写入。
    addr = "192.168.20.10:8287"

    [metric]
    # 给 Prometheus 客户端的推送任务名称。
    job = "tikv-importer"
    # 给 Prometheus 客户端的推送间隔。
    interval = "15s"
    # Prometheus Pushgateway 地址。
    address = ""

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/mnt/ssd/data.import/"
    ```

    上面仅列出了 `tikv-importer` 的基本配置。完整配置请参考[`tikv-importer` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)。

3. 运行 `tikv-importer`。

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### 第 4 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。对于没有出现在下述模版中的配置，TiDB Lightning 给出配置错误的提醒并退出。

    ```toml
    [lightning]

    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    # region-concurrency =

    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # tikv-importer 的监听地址，需改成 tikv-importer 服务器的实际地址。
    addr = "172.16.31.10:8287"

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
    ```

    上面仅列出了 `tidb-lightning` 的基本配置。完整配置请参考[`tidb-lightning` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)。

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## 升级 TiDB Lightning

你可以通过替换二进制文件升级 TiDB Lightning，无需其他配置。重启 TiDB Lightning 的具体操作参见 [FAQ](/tidb-lightning/tidb-lightning-faq.md#如何正确重启-tidb-lightning)。

如果当前有运行的导入任务，推荐任务完成后再升级 TiDB Lightning。否则，你可能需要从头重新导入，因为无法保证断点可以跨版本工作。
