---
title: tiup cluster detach-grafana
summary: tiup cluster detach-grafana 命令用于将指定的 Grafana 实例移出 TiUP 管理，保留其进程和文件，交由运维人员独立维护。该命令只更新本地 metadata，不连接集群节点或 PD；执行前会校验实例登记信息和记录目录，且没有自动重新接管的命令。
---

# tiup cluster detach-grafana

当某个 Grafana 实例改由独立团队或外部流程维护，不再需要 TiUP 管理时，使用 `tiup cluster detach-grafana` 将其移出 TiUP 管理。该命令只更新本地 metadata（`meta.yaml`），不连接集群节点或 PD，也不会停止服务：现有进程、systemd service、二进制、配置文件、看板和数据都会保留，之后的 TiUP 集群操作不再管理这些实例。修改最初的部署拓扑文件不会影响已登记实例的管理状态。

> **警告：**
>
> - 本命令没有对应的重新接管（reattach）命令。执行后，TiUP 不再为这些实例保留端口、目录和 systemd 服务名。
> - 请先完成其他 TiUP 变更再执行本命令：本命令不会阻止并发的 TiUP 操作，已经读取旧拓扑的命令仍可能操作这些 Grafana，并把旧实例清单写回。
> - 本命令仅适用于 TiDB 集群，不支持 DM 集群。

## 语法

```shell
tiup cluster detach-grafana <cluster-name> [flags]
```

`<cluster-name>` 为集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### -N, --node（strings，无默认值，必须非空）

- 指定要移交的 Grafana 实例 ID，格式为 `host:port`。可重复指定，多个实例之间以逗号分割。
- 仅接受集群中已登记的 Grafana 实例；所有目标实例都校验通过后，才会更新 metadata。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 目录检查

执行 detach 前，TiUP 会基于本地 metadata 中记录的路径检查目录冲突：

- 如果目标 Grafana 的目录（包括 Grafana 配置中的 `paths.data`、`paths.logs`、`paths.plugins`、`paths.provisioning`）与同一管理主机上仍受管理组件或 exporter 的目录存在重叠（相同、包含或被包含），命令会报错退出，metadata 保持不变。
- 检查范围包括当前 cluster profile（`TIUP_HOME`）内所有集群的记录目录，以及 monitored 组件的 deploy、data、log 目录。同一台主机被多个集群管理时，任意一个集群的清理操作都可能影响目标目录。
- 记录路径必须是绝对的字面量路径。相对路径以及包含空白或 shell 元字符的路径无法在本地可靠判断，会被拒绝。注意 `tiup cluster edit-config` 只修改本地拓扑，不会修改远端配置；请先核对远端实际路径，使登记的配置与实际路径一致后再重试。本命令不提供 `--force` 绕过选项。
- 检查只基于本地 metadata，无法感知远端 symlink、挂载点、环境变量展开、修改过的启动脚本或未记录的自定义配置。检查通过不代表实际目录布局一定安全，仍需人工确认。

## 移交后的维护

- 你需要负责被移交 Grafana 的启停、版本升级、安全修复、插件、配置、数据库、备份、恢复和看板维护。Prometheus 或 VictoriaMetrics 的地址、认证、TLS 变更后，你需要相应更新 Grafana 数据源。
- 下次 Prometheus 配置刷新时，被移交 Grafana 的 `monitor_port_probe` 采集目标会被移除，你需要安排替代的健康监控方案。
- 如果某台主机在本集群中没有其他实例，本集群不再管理该主机的 exporter：后续刷新会移除相应采集目标，但 exporter 进程可能继续运行。接管或清理前，先确认该主机是否由其他集群维护。
- 被移交的实例不再出现在 `tiup cluster display` 的输出中。

### TiDB Dashboard 监控入口

detach 本身不修改 PD 中的 Grafana 发现记录。如果集群中不再有受管理的 Grafana 实例，后续拓扑刷新会保留已有记录，不补建也不校验；如果仍有其他受管理的 Grafana 实例，后续刷新会改用它们的入口。之后再新增受管理的 Grafana 会覆盖该记录；正常 scale-in 最后一个受管理的 Grafana 时会删除记录，不会自动恢复到先前移交的实例。

## 输出

tiup-cluster 的执行日志。校验失败或取消确认时，metadata 保持不变。保存沿用 TiUP 已有的备份机制；如果保存失败或被中断，请先检查 `meta.yaml` 和备份目录，确认当前状态后再重试。
