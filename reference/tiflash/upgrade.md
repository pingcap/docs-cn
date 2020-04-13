---
title: 升级 TiFlash 节点
category: reference
---

# 升级 TiFlash 节点

升级前请保证集群处于启动状态，升级 TiFlash 节点的步骤如下：

1. 运行升级命令

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade test v4.0.0-rc
    ```

2. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

3. 打开浏览器访问监控平台，监控整个集群的状态
