---
title: 升级 TiFlash 节点
aliases: ['/docs-cn/v3.1/tiflash/upgrade-tiflash/','/docs-cn/v3.1/reference/tiflash/upgrade/']
---

# 升级 TiFlash 节点

> **注意：**
>
> TiFlash Pre-RC 版本升级到更高版本请联系 [PingCAP 官方](mailto:info@pingcap.com)，以获得更多资讯和帮助。

升级前请保证集群处于启动状态，升级 TiFlash 节点的步骤如下：

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
