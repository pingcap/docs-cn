---
title: 将 TiDB Cloud 与 Prometheus 和 Grafana 集成（Beta）
summary: 了解如何通过 Prometheus 和 Grafana 集成监控你的 TiDB 集群。
---

# 将 TiDB Cloud 与 Prometheus 和 Grafana 集成（Beta）

TiDB Cloud 提供了一个 [Prometheus](https://prometheus.io/) API 端点（beta）。如果你有 Prometheus 服务，可以轻松地从该端点监控 TiDB Cloud 的关键指标。

本文档描述如何配置你的 Prometheus 服务以从 TiDB Cloud 端点读取关键指标，以及如何使用 [Grafana](https://grafana.com/) 查看这些指标。

## 前提条件

- 要将 TiDB Cloud 与 Prometheus 集成，你必须有一个自托管或托管的 Prometheus 服务。

- 要编辑 TiDB Cloud 的第三方集成设置，你必须在 TiDB Cloud 中拥有组织的 `Organization Owner` 访问权限或目标项目的 `Project Member` 访问权限。

## 限制

- 你不能在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群中使用 Prometheus 和 Grafana 集成。

- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，Prometheus 和 Grafana 集成不可用。

## 步骤

### 步骤 1. 获取 Prometheus 的 scrape_config 文件

在配置 Prometheus 服务以读取 TiDB Cloud 的指标之前，你需要先在 TiDB Cloud 中生成一个 `scrape_config` YAML 文件。`scrape_config` 文件包含一个唯一的持有者令牌，允许 Prometheus 服务监控当前项目中的任何数据库集群。

要获取 Prometheus 的 `scrape_config` 文件，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击 **Project Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Prometheus (BETA)**。
4. 点击 **Add File** 为当前项目生成并显示 scrape_config 文件。

5. 复制 `scrape_config` 文件内容以供后续使用。

    > **注意：**
    >
    > 出于安全考虑，TiDB Cloud 只会显示一次新生成的 `scrape_config` 文件。确保在关闭文件窗口之前复制内容。如果忘记复制，你需要在 TiDB Cloud 中删除 `scrape_config` 文件并生成一个新文件。要删除 `scrape_config` 文件，选择该文件，点击 **...**，然后点击 **Delete**。

### 步骤 2. 与 Prometheus 集成

1. 在 Prometheus 服务指定的监控目录中，找到 Prometheus 配置文件。

    例如，`/etc/prometheus/prometheus.yml`。

2. 在 Prometheus 配置文件中，找到 `scrape_configs` 部分，然后将从 TiDB Cloud 获取的 `scrape_config` 文件内容复制到该部分。

3. 在你的 Prometheus 服务中，检查 **Status** > **Targets** 以确认新的 `scrape_config` 文件已被读取。如果没有，你可能需要重启 Prometheus 服务。

### 步骤 3. 使用 Grafana GUI 仪表板可视化指标

在你的 Prometheus 服务从 TiDB Cloud 读取指标后，你可以按照以下步骤使用 Grafana GUI 仪表板来可视化指标：

1. 在[这里](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)下载 TiDB Cloud 的 Grafana 仪表板 JSON。

2. [将此 JSON 导入到你自己的 Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) 以可视化指标。
    
    > **注意：**
    >
    > 如果你已经在使用 Prometheus 和 Grafana 监控 TiDB Cloud，并想要整合新可用的指标，建议你创建一个新的仪表板，而不是直接更新现有仪表板的 JSON。

3. （可选）根据需要自定义仪表板，例如添加或删除面板、更改数据源和修改显示选项。

有关如何使用 Grafana 的更多信息，请参见 [Grafana 文档](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)。

## 轮换 scrape_config 的最佳实践

为了提高数据安全性，定期轮换 `scrape_config` 文件持有者令牌是一般的最佳实践。

1. 按照[步骤 1](#步骤-1-获取-prometheus-的-scrape_config-文件)为 Prometheus 创建一个新的 `scrape_config` 文件。
2. 将新文件的内容添加到你的 Prometheus 配置文件中。
3. 一旦确认你的 Prometheus 服务仍然能够从 TiDB Cloud 读取数据，从你的 Prometheus 配置文件中删除旧的 `scrape_config` 文件内容。
4. 在你项目的 **Integrations** 页面上，删除相应的旧 `scrape_config` 文件，以阻止其他人使用它从 TiDB Cloud Prometheus 端点读取数据。

## Prometheus 可用的指标

Prometheus 跟踪你的 TiDB 集群的以下指标数据。

| 指标名称 | 指标类型 | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| tidbcloud_db_queries_total| count | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行的语句总数 |
| tidbcloud_db_failed_queries_total | count | type: `planner:xxx\|executor:2345\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行错误的总数 |
| tidbcloud_db_connections | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | TiDB 服务器中的当前连接数 |
| tidbcloud_db_query_duration_seconds | histogram | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 语句的持续时间直方图 |
| tidbcloud_changefeed_latency | gauge | changefeed_id | 变更数据捕获上游和下游之间的数据复制延迟 |
| tidbcloud_changefeed_checkpoint_ts | gauge | changefeed_id | 变更数据捕获的检查点时间戳，表示成功写入下游的最大 TSO（时间戳预言机） |
| tidbcloud_changefeed_replica_rows | gauge | changefeed_id | 变更数据捕获每秒写入下游的复制行数 |
| tidbcloud_node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘使用字节数 |
| tidbcloud_node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘容量字节数 |
| tidbcloud_node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 使用率 |
| tidbcloud_node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 限制核心数 |
| tidbcloud_node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的已用内存字节数 |
| tidbcloud_node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的内存容量字节数 |
| tidbcloud_node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiKV/TiFlash 节点的可用磁盘空间字节数 |
| tidbcloud_disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的读取延迟（秒） |
| tidbcloud_disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的写入延迟（秒） |
| tidbcloud_kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | 按类型划分的 TiKV 请求持续时间（秒） |
| tidbcloud_component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|pd\|...`<br/>cluster_name: `<cluster name>` | TiDB 组件的运行时间（秒） |
| tidbcloud_ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | 变更数据捕获所有者的已解析时间戳延迟（秒） |
| tidbcloud_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | 变更数据捕获状态：<br/>`-1`: 未知<br/>`0`: 正常<br/>`1`: 警告<br/>`2`: 失败<br/>`3`: 已停止<br/>`4`: 已完成<br/>`6`: 警告<br/>`7`: 其他 |
| tidbcloud_resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | 资源管理器消耗的读请求单位 |
| tidbcloud_resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | 资源管理器消耗的写请求单位 |

## 常见问题

- 为什么同一指标在同一时间在 Grafana 和 TiDB Cloud 控制台上显示的值不同？

    Grafana 和 TiDB Cloud 之间的聚合计算逻辑不同，因此显示的聚合值可能会有所不同。你可以调整 Grafana 中的 `mini step` 配置以获取更细粒度的指标值。
