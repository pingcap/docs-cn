---
title: 升级 TiFlash 节点
category: reference
aliases: ['/docs-cn/dev/reference/tiflash/upgrade/']
---

# 升级 TiFlash 节点

> **注意：**
>
> TiFlash Pre-RC 版本升级到更高版本请联系 [PingCAP 官方](mailto:info@pingcap.com)，以获得更多资讯和帮助。

目前 TiFlash 暂时还不支持通过 `tiup cluster upgrade` 进行升级。 推荐使用下面的步骤进行升级：

1. 参考[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#4-缩容-tiflash-节点)章节，对所有的 TiFlash 节点进行缩容操作

2. 运行升级命令

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade test v4.0.0-rc
    ```

3. 运行扩容 TiFlash 的命令

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out test scale-out.yaml
    ```

4. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

5. 打开浏览器访问监控平台，监控整个集群的状态
