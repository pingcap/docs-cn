---
title: TiFlash 集群扩缩容
category: reference
---

# TiFlash 集群扩缩容

## 扩容 TiFlash 节点

以在节点 192.168.1.1 上部署 TiFlash 为例子，编辑 inventory.ini 文件，添加 tiflash 节点信息 (目前只支持ip，不支持域名)

```
[tiflash_servers]
192.168.1.1
```

编辑 hosts.ini 文件，添加节点信息

```
[servers]
192.168.1.1

[all:vars]
username = tidb
ntp_server = pool.ntp.org
```

初始化新增节点：

在中控机上配置部署机器 SSH 互信及 sudo 规则

```
ansible-playbook -i hosts.ini create_users.yml -l 192.168.1.1 -u root -k
```

在部署目标机器上安装 NTP 服务：

```
ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
```

在部署目标机器上初始化节点：

```
ansible-playbook bootstrap.yml -l 192.168.1.1
```

部署新增节点：

```
ansible-playbook deploy.yml -l 192.168.1.1
```

启动新节点服务：

```
ansible-playbook start.yml -l 192.168.1.1
```

更新 Prometheus 配置并重启：

```
ansible-playbook rolling_update_monitor.yml --tags=prometheus
```

打开浏览器访问监控平台，监控整个集群和新增节点的状态。

## 缩容 TiFlash 节点

请先参考 “TiFlash 下线方法” 章节，对 TiFlash 节点进行下线操作。

使用 Grafana 或者 pd-ctl 检查节点是否下线成功（下线需要一定时间）。

等待 tiflash 对应的 store 消失或者 state_name 变成 Tomestone 再关闭 tiflash 进程，以停止 192.168.1.1 节点服务为例：

```
ansible-playbook stop.yml -l 192.168.1.1
```

如只该节点仍有其他服务，只希望停止 TiFlash 则请注明 TiFlash 服务：

```
ansible-playbook stop.yml -t tiflash -l 192.168.1.1
```

然后编辑 `inventory.ini` 和 `hosts.ini` 文件，移除节点信息。
更新 Prometheus 配置并重启：

```
ansible-playbook rolling_update_monitor.yml --tags=prometheus
```

打开浏览器访问监控平台，监控整个集群的状态

注意：上述下线流程不会删除下线节点上的数据文件，如需再次上线，请先手动删除。
