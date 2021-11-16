---
title: TiDB Ansible 常见运维操作
aliases: ['/docs-cn/stable/maintain-tidb-using-ansible/','/docs-cn/v4.0/maintain-tidb-using-ansible/','/docs-cn/stable/how-to/maintain/ansible-operations/','/zh/tidb/dev/maintain-tidb-using-ansible/','/docs-cn/dev/maintain-tidb-using-ansible/','/docs-cn/dev/how-to/maintain/ansible-operations/','/zh/tidb/stable/maintain-tidb-using-ansible/']
---

# TiDB Ansible 常见运维操作

> **警告：**
>
> 对于生产环境，推荐[使用 TiUP 进行集群运维操作](/maintain-tidb-using-tiup.md)。自 v4.0 版本起，PingCAP 不再提供 TiDB Ansible 的运维支持（废弃）。继续使用 TiDB Ansible 运维 TiDB 集群可能存在风险，因此不推荐该运维方式。

## 启动集群

此操作会按顺序启动整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。

{{< copyable "shell-regular" >}}

```bash
ansible-playbook start.yml
```

## 关闭集群

此操作会按顺序关闭整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。

{{< copyable "shell-regular" >}}

```bash
ansible-playbook stop.yml
```

## 清除集群数据

此操作会关闭 TiDB、Pump、TiKV、PD 服务，并清空 Pump、TiKV、PD 数据目录。

{{< copyable "shell-regular" >}}

```bash
ansible-playbook unsafe_cleanup_data.yml
```

## 销毁集群

此操作会关闭集群，并清空部署目录，若部署目录为挂载点，会报错，可忽略。

{{< copyable "shell-regular" >}}

```bash
ansible-playbook unsafe_cleanup.yml
```
