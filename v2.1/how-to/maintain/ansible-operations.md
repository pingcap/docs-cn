---
title:  常见运维操作
category: how-to
---

# 常见运维操作

## 启动集群

此操作会按顺序启动整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。

```
$ ansible-playbook start.yml
```

## 关闭集群

此操作会按顺序关闭整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。

```
$ ansible-playbook stop.yml
```

## 清除集群数据

此操作会关闭 TiDB、Pump、TiKV、PD 服务，并清空 Pump、TiKV、PD 数据目录。

```
$ ansible-playbook unsafe_cleanup_data.yml
```

## 销毁集群

此操作会关闭集群，并清空部署目录，若部署目录为挂载点，会报错，可忽略。

```
$ ansible-playbook unsafe_cleanup.yml
```
