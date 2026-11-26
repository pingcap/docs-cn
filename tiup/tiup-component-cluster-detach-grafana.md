---
title: tiup cluster detach-grafana
summary: tiup cluster detach-grafana 命令用于将指定的 Grafana 实例移出 TiUP 管理，保留其进程和文件，交由运维人员独立维护。该命令只更新本地 metadata，不连接集群节点或 PD；执行前会校验实例登记信息和记录目录，且没有自动重新接管的命令。
---

# tiup cluster detach-grafana

当某个 Grafana 实例改由独立团队或外部流程维护，不再需要 TiUP 管理时，使用 `tiup cluster detach-grafana` 将其移出 TiUP 管理。该命令只更新本地 metadata（`meta.yaml`），不连接集群节点或 PD，也不会停止服务：现有进程、systemd service、二进制、配置文件、看板和数据都会保留，之后的 TiUP 集群操作不再管理这些实例。修改最初的部署拓扑文件不会影响已登记实例的管理状态。

> **警告：**
>
> - 本命令没有对应的重新接管（reattach）命令。执行后，TiUP 不再为这些实例保留端口、目录和 systemd 服务名。
> - 请先完成其他进行中的 TiUP 变更再执行本命令：若存在未完成的两阶段扩容（two-phase scale-out），本命令会拒绝执行；除此之外，本命令不会阻止并发的 TiUP 操作，已经读取旧拓扑的命令仍可能操作这些 Grafana，并把旧实例清单写回。
> - 本命令仅适用于 TiDB 集群，不支持 DM 集群。

## 语法

```shell
tiup cluster detach-grafana <cluster-name> [flags]
```

`<cluster-name>` 为集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### -N, --node（strings，无默认值，必须非空）

- 指定要移出 TiUP 管理的 Grafana 实例 ID，格式为 `host:port`。可重复指定，多个实例之间以逗号分割。
- 仅接受集群中已登记的 Grafana 实例；所有目标实例都校验通过后，才会更新 metadata。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 目录检查

执行 detach 前，TiUP 会基于本地 metadata 中记录的路径检查目录冲突，避免移交出去的 Grafana 目录在后续缩容、销毁、升级等 TiUP 操作中被删除或覆盖：

- 如果目标 Grafana 的位置（包括其 deploy、data、log 目录，Grafana 配置中的 `paths.data`、`paths.logs`、`paths.plugins`、`paths.provisioning`，以及 `database.url`、`database.path` 配置指向的本地数据库文件）与同一管理主机上仍受管理的组件或 exporter 的目录存在重叠（相同、包含或被包含），命令会报错退出，metadata 保持不变。`database.url` 指向外部数据库（如 MySQL、PostgreSQL）时不参与该检查。检查按 metadata 中记录的管理主机匹配主机：记录为 IP 地址的主机按地址值比较，同一台机器的不同 IPv6 写法（例如压缩形式和完整形式）视为同一主机；如果同一台机器在不同集群中记录为不同的主机名（例如域名和 IP，或两个不同的域名），两边记录的目录不会被互相比较。
- 检查范围包括当前 cluster profile（`TIUP_HOME`）内所有集群的记录目录，以及 monitored 组件的 deploy、data、log 目录。同一台主机被多个集群管理时，任意一个集群的清理操作都可能影响目标目录。
- 路径检查基于记录值本身：所有被检查的目录都必须是绝对路径，且不能包含空白或 shell 元字符，否则命令会报错拒绝，并提示先用 `tiup cluster edit-config` 修正。这同样适用于 Grafana 配置中的 `paths.*` 和 `database.*`（实例配置优先，其次 `server_configs`）、TiFlash 实例配置中的 `storage.remote.cache.dir` 和 monitored 组件的目录。正常部署和扩容写入的 metadata 已满足该要求，通常只有之后通过 edit-config 引入相对路径或特殊字符时才会触发。注意 `tiup cluster edit-config` 只修改本地拓扑，不会修改远端配置；请先核对远端实际路径，使登记的配置与实际路径一致后再重试。本命令不提供 `--force` 绕过选项。
- 检查只基于本地 metadata，无法感知远端 symlink、挂载点、环境变量展开、修改过的启动脚本或未记录的自定义配置。检查通过不代表实际目录布局一定安全，仍需人工确认。

## 移交后的维护

- 你需要负责被移出实例的启停、版本升级、安全修复、插件、配置、数据库、备份、恢复和看板维护。Prometheus 或 VictoriaMetrics 的地址、认证、TLS 变更后，你需要相应更新 Grafana 数据源。
- 下次 Prometheus 配置刷新时，被移出实例的 `monitor_port_probe` 采集目标会被移除，你需要安排替代的健康监控方案。
- 如果某台主机在本集群中没有其他实例，本集群不再管理该主机的 exporter：后续刷新会移除相应采集目标，但 exporter 进程可能继续运行。接管或清理前，先确认该主机是否由其他集群维护。
- 被移出的实例不再出现在 `tiup cluster display` 的输出中。

### TiDB Dashboard 监控入口

detach 本身不修改 PD 中的 Grafana 发现记录（discovery record）。只要集群中没有受管的 Grafana 实例，TiUP 就不再维护这条记录：既不改写，也不补建。如果被移出的 Grafana 迁移到新地址，你可以自行更新这条记录。

唯一的例外是 TiUP 自己通过缩容移除最后一个受管 Grafana 实例（`tiup cluster scale-in`）。此时如果发现记录仍指向被移除的实例，TiUP 会删除这条记录；删除失败时，之后的拓扑刷新会重试。之后如果新增受管的 Grafana 实例，发现记录会改为指向受管实例。TiUP v1.17.1 及之前的版本不遵循以上规则，拓扑刷新时会删除这条记录。

## 输出

tiup-cluster 的执行日志。命令会列出要移出的实例及其影响，确认后才会保存；校验失败或取消确认时，metadata 保持不变。metadata 的保存沿用 TiUP 已有的备份机制；如果保存失败或被中断，请先检查 `meta.yaml` 和备份目录，确认当前状态后再重试。
