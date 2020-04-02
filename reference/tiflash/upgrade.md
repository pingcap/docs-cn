---
title: 升级 TiFlash 节点
category: reference
---

# 升级 TiFlash 节点

升级 TiFlash 节点的步骤如下：

1. 下载新版 TiFlash binary 到中控机，方式有如下两种：

    - 下载最新版 TiDB Ansible 或者通过 `git pull` 命令更新 TiDB Ansible git repo，然后执行 `ansible-playbook local_prepare.yml` 命令。
    - 或者手动下载 TiFlash binary 并覆盖到 `resource/bin/tiflash`。

2. 滚动升级 TiFlash：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update.yml --tags tiflash
    ```

3. 滚动升级 TiDB 监控组件：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml
    ```
