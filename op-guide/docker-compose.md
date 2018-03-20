---
title: 使用 Docker Compose 构建集群
category: deployment
---

# 使用 Docker Compose 快速构建集群

本文档介绍如何通过 Docker Compose 快速部署 TiDB 集群。

[Docker Compose](https://docs.docker.com/compose/overview) 可以通过一个 YAML 文件定义多个容器的应用服务，然后一键启动或停止。可以用来在单机上一键部署一套 TiDB 测试集群，使用 Docker Compose 部署 TiDB 集群要求 Docker 是 17.06.0 及以上版本。

## 快速部署

1. 下载 `tidb-docker-compose`

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. 创建并启动集群

    ```bash
    cd tidb-docker-compose && docker-compose up -d
    ```

3. 访问集群

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

    访问集群 Grafana 监控页面：<http://localhost:3000> 默认用户名和密码均为 admin。

    [集群数据可视化](https://github.com/pingcap/tidb-vision)：<http://localhost:8010>

## 自定义集群

在完成快速部署后，以下组件已默认部署：3 个 PD，3 个 TiKV，1 个 TiDB 和监控组件 Prometheus，Pushgateway，Grafana 以及 tidb-vision。

如果想自定义集群，可以直接修改 `docker-compose.yml`，但是手动修改比较繁琐而且容易出错，强烈建议使用 [Helm](https://helm.sh) 模板引擎生成 `docker-compose.yml` 文件。

1. 安装 Helm

    [Helm](https://helm.sh) 可以用作模板渲染引擎，只需要下载其 binary 文件即可以使用。

    ```bash
    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
    ```

    如果是 Mac 系统，也可以通过 Homebrew 安装：`brew install kubernetes-helm`

2. 下载 `tidb-docker-compose`

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

3. 自定义集群

    ```bash
    cd tidb-docker-compose
    cp compose/values.yaml values.yaml
    vim values.yaml
    ```

    修改 `values.yaml` 里面的配置，例如集群规模，TiDB 镜像版本等。

    [tidb-vision](https://github.com/pingcap/tidb-vision) 是 TiDB 集群可视化页面，可以可视化地显示 PD 对 TiKV 数据的调度。如果不想部署该组件，可以将 `tidbVision` 项留空。

    PD，TiKV，TiDB 和 tidb-vision 支持从 GitHub 源码或本地文件构建 Docker 镜像，供开发测试使用。

    - 如果希望从 GitHub 源码构建某个组件的镜像，需要将其 `image` 字段留空，然后设置其 `buildFrom` 为 `remote`。

    - 如果希望从本地已编译好的 binary 文件构建 PD，TiKV 或 TiDB 镜像，需要将其 `image` 字段留空，然后设置其 `buildFrom` 为 `local`，并将已编译好的 binary 拷贝到对应的 `pd/bin/pd-server`，`tikv/bin/tikv-server`，`tidb/bin/tidb-server`。

    - 如果希望从本地构建 tidb-vision 镜像，需要将其 `image` 字段留空，然后设置其 `buildFrom` 为 `local`，并将 tidb-vision 项目拷贝到 `tidb-vision/tidb-vision`。

4. 生成 `docker-compose.yml` 文件

    ```bash
    helm template -f values.yaml compose > generated-docker-compose.yml
    ```

5. 使用生成的 `docker-compose.yml` 创建并启动集群

    ```bash
    docker-compose -f generated-docker-compose.yml up -d
    ```

6. 访问集群

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

    访问集群 Grafana 监控页面：<http://localhost:3000> 默认用户名和密码都是 admin。

    如果启用了 tidb-vision，可以通过 <http://localhost:8010> 查看。
