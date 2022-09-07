---
title: TiUniManager 系统管理
summary: 了解如何通过 TiUniManager 管理系统。
---

# TiUniManager 系统管理

本文档介绍如何通过 TiUniManager 管理系统。

## 查看系统监控

你可能需要查看 TiUniManager 系统监控，了解 TiUniManager 系统运行情况、TiUniManager 所在主机运行情况。

操作步骤如下：

1. 登录 TiUniManager 控制台。
2. 进入**系统管理** > **系统监控**页面。
3. 选择 **EM Server**，查看 TiUniManager 系统运行情况的 Dashboard。
4. 选择 **Node Exporter**，查看 TiUniManager 所在主机运行情况的 Dashboard。

## 查看系统日志

查看 TiUniManager 系统日志的步骤如下：

1. 登录 TiUniManager 控制台。
2. 进入**系统管理** > **系统日志**页面查看系统日志。

## TiUniManager 告警规则

TiUniManager 默认包含以下告警规则，以便接受相应的告警通知。

### work flow error alert

* 报警规则：`sum(increase(em_work_flow_total{flow_status="Error"}[5m])) by(service, biz_type, flow_name, flow_status) > 3`
* 规则描述：错误状态工作流数量超过 3 时告警。
* 处理方法：可能是逻辑问题。查看失败工作流，或者联系 TiUniManager 开发人员。

### work flow node error alert

* 报警规则：`sum(increase(em_work_flow_node_total{flow_node_status="Error"}[5m])) by(service, biz_type, flow_name, flow_node, flow_node_status) > 3`
* 规则描述：错误状态工作流节点超过 3 时告警。
* 处理方法：可能是逻辑问题。查看失败工作流，或者联系 TiUniManager 开发人员。

### cluster-server request error rate

* 报警规则： `sum(increase(em_micro_requests_total{service="cluster-server", code!="0"}[1m]) / increase(em_micro_requests_total{service="cluster-server"}[1m])) by(service, method) > 0.05`
* 规则描述： 接口失败率超过 5% 时告警。
* 处理方法：可以查看系统日志或系统追踪，或者联系 TiUniManager 开发人员。

### openapi-server request error rate

* 报警规则： `sum(increase(em_http_requests_total{service="openapi-server", code!="200"}[1m]) / increase(em_http_requests_total{service="openapi-server"}[1m])) by(service, handler, method) > 0.05`
* 规则描述： 接口失败率超过 5% 时告警。
* 处理方法：可以查看系统日志或系统追踪，或者联系 TiUniManager 开发人员。

## TiUniManager 告警设置

TiUniManager 告警设置支持钉钉、Email 等告警通道，具体见 [List of notifiers supported by Grafana](https://grafana.com/docs/grafana/latest/alerting/unified-alerting/contact-points/#list-of-notifiers-supported-by-grafana)。在设置 TiUniManager 告警前，确保已登录 TiUniManager 控制台。

以下示例基于 Grafana v7.5.15，展示如何在 Grafana 上配置钉钉的告警通道。

1. 打开 **Notification channels** 配置页面，点击 **New channel** 创建通道。

    ![Notification channels - New channel](/media/tiunimanager/tiunimanager-notification-channels-new-channel.png)

2. 配置消息接收方，示例如下：

    ![Notification channels - Edit config](/media/tiunimanager/tiunimanager-notification-channels-edit-config.png)

    若要接入钉钉自定义机器人，参考[钉钉文档 - 自定义机器人接入](https://open.dingtalk.com/document/group/custom-robot-access)。
