---
title: 升级 TiFlash 节点
category: reference
---

# 升级 TiFlash 节点

升级 TiFlash 节点的步骤如下：

1. 备份 tidb-ansible 文件夹

    {{< copyable "shell-regular" >}}

    ```shell
    mv tidb-ansible tidb-ansible-bak
    ```

2. 下载 TiDB 3.0 版本对应 tag 的 tidb-ansible

    {{< copyable "shell-regular" >}}

    ```shell
    git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

3. 编辑 inventory.ini 文件

4. 下载 binary

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml
    ```

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
