---
title: 使用 WebUI 管理 DM 迁移任务
summary: 学习如何使用 WebUI 来方便的管理数据迁移任务
---

# 使用 WebUI 管理 DM 迁移任务

DM WebUI 是为了方便大量迁移任务的管理、简化操作步骤的目的开发，其主要特性包含运行状态监控，上游数据源配置，以及迁移任务管理等。DM WebUI 可以从任意 master 节点访问，其端口与 OpenAPI 保持一致，默认为 8261。访问地址示例：`http://{master_ip}:{master_port}/dashboard/`。

> **注意：**
>
> - DM WebUI 当前为实验特性，尚不建议用于生产环境。
> 
> - DM WebUI 中 task 的生命周期有所改变，不建议与 dmctl 同时使用。

## 实验特性开关

若要使用 DM WebUI，需要在 master 配置中开启`openapi`配置：

```
openapi = true
```

## Dashboard

Dashboard 是内嵌了 DM 的 Grafana Dashboard，包含两个视图`Standard`和`Professional`分别展示了不同角度的监控信息。

如果要在 DM WebUI 中正确显示 Dashboard，首次部署必须确认以下两个步骤正确完成：

1. 部署时正确安装监控相关组件：`monitoring_servers`和`grafana_servers` ，其中`grafana_servers`的配置必须如下所示：

    ```
    grafana_servers:
      - host: 10.0.1.14
        # port: 3000
        # deploy_dir: /tidb-deploy/grafana-3000
        config:
          auth.anonymous.enabled: true
          security.allow_embedding: true
    ```

2. 若`grafana_servers`使用了非默认的 IP 和端口，则需要在 WebUI 的 Dashboard 界面填写正确的 IP 和端口。

若 DM 是从旧版本升级，则需要手动修改 Grafana 的配置，首先编辑`/{deploy-dir}/grafana-{port}/conf/grafana.ini`，修改以下两项配置：

```ini
[auth.anonymous]
enabled = true

[security]
allow_embedding = true
```

然后执行`tiup dm reload`使新的配置生效即可。

## 任务列表

任务列表用于管理所有的迁移任务。与 v6.0 以下版本不同，WebUI 首先使用了新的生命周期管理（dmctl 预计将在 v6.1 版本同步修改）。这将导致操作方式与之前版本有所不同，可能需要一些适应。

原有 task 生命周期

![dm-task-state-old](/media/dm/dm-task-state-old.jpg)

新的 task 生命周期

![dm-task-state-new](/media/dm/dm-task-state-new.jpg)

创建新的任务前，需要在侧边栏-上游配置页面中添加上游数据库信息。

## 上游配置

创建迁移任务之前，需要先行创建所需要同步的上游数据源信息。请注意：

1. GTID。如果存在主从切换，请务必在上游 MySQL 开启 GTID，并在创建上游配置时将 GTID 设为 True，否则数据迁移任务将在主从切换时中断（AWS Aurora 除外）；
2. 停用。若某个上游数据库需要临时下线，可将其“停用”，但停用期间其他正在同步的 MySQL 实例不可执行 DDL 操作，否则停用的实例被启用后将无法正常同步。
3. relay log。当多个迁移任务使用同一个上游时，可能对其造成额外压力。建议开启 relay log 可降低对上游的影响。

## 同步详情

如果需要查看迁移任务中所配置的迁移规则的运行情况，同步详情页面支持根据任务、数据源、表库名称进行查询。查询结果中将包含上游表至下游表的对应信息，因此请慎重使用`*`等通配符，以防止查询结果过多导致页面反应迟缓。
