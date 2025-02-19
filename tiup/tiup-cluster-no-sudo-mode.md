---
title: 使用 TiUP no-sudo 模式部署运维 TiDB 线上集群
summary: 了解如何使用 TiUP no-sudo 模式部署运维 TiDB 线上集群。
---

# 使用 TiUP no-sudo 模式部署运维 TiDB 线上集群

本文介绍如何使用 TiUP no-sudo 模式部署一个 TiDB 线上集群。

> **注意：**
>
> 对于 CentOS 操作系统，仅支持 CentOS 8 及更高版本。

## 准备用户并配置 SSH 互信

1. 以 `tidb` 用户为例。依次登录所有的部署目标机器，并以 `root` 用户使用如下命令创建一个普通用户 `tidb`。在 no-sudo 模式下，不需要为 `tidb` 用户配置 sudo 免密，即无需将 `tidb` 用户加入 `sudoers` 文件中。

    ```bash
    adduser tidb
    ```

2. 在每台部署目标机器上，为 `tidb` 用户启动 `systemd user` 模式。该步骤是必须的，请勿跳过。

    1. 使用 `tidb` 用户设置 `XDG_RUNTIME_DIR` 环境变量。
      
        ```bash
        mkdir -p ~/.bashrc.d
        echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" > ~/.bashrc.d/systemd
        source ~/.bashrc.d/systemd
        ```
   
    2. 使用 `root` 用户启动 user service。

        ```shell
        $ systemctl start user@1000.service # `1000` is the ID of the `tidb` user. You can get the user ID by executing the `id` command.
        $ systemctl status user@1000.service
        user@1000.service - User Manager for UID 1000
        Loaded: loaded (/usr/lib/systemd/system/user@.service; static; vendor preset>
        Active: active (running) since Mon 2024-01-29 03:30:51 EST; 1min 7s ago
        Main PID: 3328 (systemd)
        Status: "Startup finished in 420ms."
        Tasks: 6
        Memory: 6.1M
        CGroup: /user.slice/user-1000.slice/user@1000.service
                ├─dbus.service
                │ └─3442 /usr/bin/dbus-daemon --session --address=systemd: --nofork >
                ├─init.scope
                │ ├─3328 /usr/lib/systemd/systemd --user
                │ └─3335 (sd-pam)
                └─pulseaudio.service
                  └─3358 /usr/bin/pulseaudio --daemonize=no --log-target=journal
        ```

    3. 执行 `systemctl --user`。如果没有报错，说明 `systemd user` 模式已正常启动。

3. 使用 `root` 用户执行以下命令，为 systemd 用户 `tidb` 启用驻留。

    ```bash
    loginctl enable-linger tidb
    ```

    更多详情，参见 [systemd 用户实例的自动启动](https://wiki.archlinux.org/title/Systemd/User#Automatic_start-up_of_systemd_user_instances)。

4. 在中控机上使用 `ssh-keygen` 生成密钥，并将公钥复制到其他部署机器，完成 SSH 互信。

## 准备部署拓扑文件

1. 执行以下 TiUP 命令生成拓扑文件。

    ```bash
    tiup cluster template > topology.yaml
    ```
   
2. 编辑拓扑文件。

    相比以往的模式，使用 no-sudo 模式的 TiUP 时，需要在 `topology.yaml` 的 `global` 模块中新增一行 `systemd_mode: "user"`。`systemd_mode` 参数用于设置是否使用 `systemd user` 模式。如果不设置该参数，其默认值为 `system`，表示需要使用 sudo 权限。
    
    此外，由于 no-sudo 模式下，普通用户 `tidb` 没有权限使用 `/data` 目录作为 `deploy_dir` 和 `data_dir`，因此，你需要选择一个普通用户可以访问的路径。以下示例使用了相对路径，最终使用的路径为 `/home/tidb/data/tidb-deploy` 和 `/home/tidb/data/tidb-data`。拓扑文件的其余部分与旧版本一致。

    ```yaml
    global:
      user: "tidb"
      systemd_mode: "user"
      ssh_port: 22
      deploy_dir: "data/tidb-deploy"
      data_dir: "data/tidb-data"
      arch: "amd64"
      ...
    ```
   
## 手动修复检查项

执行 `tiup cluster check topology.yaml --user tidb` 会产生失败的检查项。示例如下：

```bash
Node            Check         Result  Message
----            -----         ------  -------
192.168.124.27  thp           Fail    THP is enabled, please disable it for best performance
192.168.124.27  command       Pass    numactl: policy: default
192.168.124.27  os-version    Pass    OS is CentOS Stream 8 
192.168.124.27  network       Pass    network speed of ens160 is 10000MB
192.168.124.27  disk          Warn    mount point / does not have 'noatime' option set
192.168.124.27  disk          Fail    multiple components tikv:/home/blackcat/data/tidb-deploy/tikv-20160/data/tidb-data,tikv:/home/blackcat/data/tidb-deploy/tikv-20161/data/tidb-data are using the same partition 192.168.124.27:/ as data dir
192.168.124.27  selinux       Pass    SELinux is disabled
192.168.124.27  cpu-cores     Pass    number of CPU cores / threads: 16
192.168.124.27  cpu-governor  Warn    Unable to determine current CPU frequency governor policy
192.168.124.27  swap          Warn    swap is enabled, please disable it for best performance
192.168.124.27  memory        Pass    memory size is 9681MB
192.168.124.27  service       Fail    service firewalld is running but should be stopped
```

由于在 no-sudo 模式下，`tidb` 用户没有 sudo 权限，执行 `tiup cluster check topology.yaml --apply --user tidb` 会导致无法自动修复失败的检查项。你需要使用 `root` 用户在部署机器上手动执行以下操作：

1. 安装 numactl 工具。

    ```shell
    sudo yum -y install numactl
    ```
   
2. 关闭 swap。

    ```shell
    swapoff -a || exit 0
    ```

3. 禁止透明大页。

    ```shell
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    ```

4. 开启 `irqbalance` service。

    ```shell
    systemctl start irqbalance
    ```
   
5. 关闭防火墙以及关闭防火墙自启动。

    ```shell
    systemctl stop firewalld.service
    systemctl disable firewalld.service
    ```
   
6. 修改 sysctl 参数。

    ```shell
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    echo "vm.swappiness = 0">> /etc/sysctl.conf
    sysctl -p
    ```
   
7. 配置 `tidb` 用户的 `limits.conf` 文件。

    ```shell
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack           32768
    tidb           hard    stack           32768
    tidb           soft    core            unlimited
    tidb           hard    core            unlimited
    EOF
    ```

## 部署和管理集群

为了使用上述步骤准备好的 `tidb` 用户而避免重新创建新的用户，执行 `deploy` 命令时需要加上 `--user tidb`，示例如下：

```shell
tiup cluster deploy mycluster v8.1.0 topology.yaml --user tidb
```

启动集群：

```shell
tiup cluster start mycluster
```

扩容集群：

```shell
tiup cluster scale-out mycluster scale.yaml --user tidb
```

缩容集群：

```shell
tiup cluster scale-in mycluster -N 192.168.124.27:20160
```

升级集群：

```shell
tiup cluster upgrade mycluster v8.2.0
```

## 常见问题

### 启动 user@.service 时出现报错 `Trying to run as user instance, but $XDG_RUNTIME_DIR is not set.`

该错误的原因可能是 `/etc/pam.d/system-auth.ued` 文件中缺少 `pam_systemd.so`。

要解决该问题，你可以使用以下命令检查 `/etc/pam.d/system-auth.ued` 文件是否已包含 `pam_systemd.so` 模块的配置。如果没有，则将 `session optional pam_systemd.so` 附加到文件末尾。

```shell
grep 'pam_systemd.so' /etc/pam.d/system-auth.ued || echo 'session     optional      pam_systemd.so' >> /etc/pam.d/system-auth.ued
```
