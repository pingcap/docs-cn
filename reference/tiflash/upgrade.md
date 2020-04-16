---
title: 升级 TiFlash 节点
category: reference
---

# 升级 TiFlash 节点

<<<<<<< HEAD
升级 TiFlash 节点的步骤如下：
=======
> **注意：**
>
> TiFlash Pre-RC 版本升级到更高版本请联系 [PingCAP 官方](mailto:info@pingcap.com)，以获得更多资讯和帮助。

目前 TiFlash 暂时还不支持通过 `tiup cluster upgrade` 进行升级。 推荐使用下面的步骤进行升级：
>>>>>>> cb0e766... tiflash: add warning to upgrade from pre-rc version (#2778)

1. 备份 tidb-ansible 文件夹

    {{< copyable "shell-regular" >}}

    ```shell
    mv tidb-ansible tidb-ansible-bak
    ```

2. 下载 TiDB 3.1 版本对应 tag 的 tidb-ansible

    {{< copyable "shell-regular" >}}

    ```shell
    git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

3. 下载 binary

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml
    ```

4. 编辑 inventory.ini 文件

5. 滚动升级 TiFlash：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update.yml --tags tiflash
    ```

6. 滚动升级 TiDB 监控组件：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml
    ```
