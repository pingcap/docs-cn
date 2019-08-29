---
title: 使用 TiDB-Ansible 升级 TiDB 集群
category: how-to
aliases: ['/docs-cn/op-guide/ansible-deployment-rolling-update/']

---

# 使用 TiDB-Ansible 升级 TiDB 集群

滚动升级 TiDB 集群时，会串行关闭服务，更新服务 binary 和配置文件，再启动服务。在前端配置负载均衡的情况下，滚动升级期间不影响业务运行（最小环境 ：pd \* 3、tidb \* 2、tikv \* 3）。

> **注意：**
>
> 如果 TiDB 集群开启了 binlog，部署了 Pump 和 Drainer 服务，升级 TiDB 服务时会升级 Pump，请先停止 Drainer 服务再执行滚动升级操作。

## 升级组件版本

跨大版本升级，必须更新 `tidb-ansible`，小版本升级，也建议更新 `tidb-ansible`，以获取最新的配置文件模板、特性及 bug 修复。

- 从 TiDB 1.0 升级到 TiDB 2.1，参考 [TiDB 2.1 升级操作指南](/how-to/upgrade/to-tidb-2.1.md)。
- 从 TiDB 2.1 升级到 TiDB 3.0，参考 [TiDB 3.0 升级操作指南](/how-to/upgrade/from-previous-version.md)。

### 自动下载 binary

1. 修改 `/home/tidb/tidb-ansible/inventory.ini` 中的 `tidb_version` 参数值，指定需要升级的版本号，如从 `v2.0.6` 升级到 `v2.0.7`

    ```
    tidb_version = v2.0.7
    ```

    > **注意：**
    >
    > 如果使用 master 分支的 tidb-ansible，`tidb_version = latest` 保持不变即可，latest 版本的 TiDB 安装包会每日更新。

2. 删除原有的 downloads 目录 `/home/tidb/tidb-ansible/downloads/`

    {{< copyable "shell-regular" >}}

    ```bash
    cd /home/tidb/tidb-ansible &&
    rm -rf downloads
    ```

3. 使用 playbook 下载 TiDB binary，自动替换 binary 到 `/home/tidb/tidb-ansible/resource/bin/`

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook local_prepare.yml
    ```

### 手动下载 binary

除 “自动下载 binary” 中描述的方法之外，也可以手动下载 binary，解压后手动替换 binary 到 `/home/tidb/tidb-ansible/resource/bin/`，需注意替换链接中的版本号。

{{< copyable "shell-regular" >}}

```bash
wget http://download.pingcap.org/tidb-v2.0.7-linux-amd64.tar.gz
```

如果使用 master 分支的 tidb-ansible，使用以下命令下载 binary：

{{< copyable "shell-regular" >}}

```bash
wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
```

### 使用 Ansible 滚动升级

- 滚动升级 PD 节点（只升级单独 PD 服务）

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=pd
    ```

    如果 PD 实例数大于等于 3，滚动升级 PD leader 实例时，Ansible 会先迁移 PD leader 到其他节点再关闭该实例。

- 滚动升级 TiKV 节点（只升级 TiKV 服务）

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=tikv
    ```

    滚动升级 TiKV 实例时，Ansible 会迁移 region leader 到其他节点。具体逻辑为：调用 PD API 添加 evict leader scheduler，每 10 秒探测一次该 TiKV 实例 leader_count， 等待 leader_count 降到 1 以下或探测超 18 次后，即三分钟超时后，开始关闭 TiKV 升级，启动成功后再去除 evict leader scheduler，串行操作。

    如中途升级失败，请登录 pd-ctl 执行 `scheduler show`，查看是否有 evict-leader-scheduler, 如有需手工清除。`{PD_IP}` 和 `{STORE_ID}` 请替换为你的 PD IP 及 TiKV 实例的 store_id。

    {{< copyable "shell-regular" >}}

    ```bash
    /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://{PD_IP}:2379"
    » scheduler show
    [
      "label-scheduler",
      "evict-leader-scheduler-{STORE_ID}",
      "balance-region-scheduler",
      "balance-leader-scheduler",
      "balance-hot-region-scheduler"
    ]
    » scheduler remove evict-leader-scheduler-{STORE_ID}
    ```

- 滚动升级 TiDB 节点（只升级单独 TiDB 服务，如果 TiDB 集群开启了 binlog，升级 TiDB 服务时会升级 pump）

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=tidb
    ```

- 滚动升级所有服务（依次升级 PD，TiKV，TiDB 服务，如果 TiDB 集群开启了 binlog，升级 TiDB 服务时会升级 pump）

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml
    ```

- 滚动升级监控组件

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml
    ```

## 变更组件配置

1. 更新组件配置模板

    TiDB 集群组件配置模板存储在 `/home/tidb/tidb-ansible/conf` 文件夹下。

    | 组件       | 配置文件模板名     |
    | :-------- | :----------: |
    | TiDB | tidb.yml  |
    | TiKV | tikv.yml  |
    | PD | pd.yml  |

    默认配置项是注释状态，使用默认值。如果需要修改，需取消注释，即去除 `#`，修改对应参数值。配置模板使用 yaml 格式，注意参数名及参数值之间使用 `:` 分隔，缩进为两个空格。

    如修改 TiKV 配置中  `high-concurrency`、`normal-concurrency` 和 `low-concurrency` 三个参数为 16：

    ```
    readpool:
      coprocessor:
        # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        high-concurrency: 16
        normal-concurrency: 16
        low-concurrency: 16
    ```

2. 修改服务配置后，需使用 Ansible 滚动升级，参考[使用 Ansible 滚动升级](#使用-ansible-滚动升级)。
