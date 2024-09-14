---
title: TiDB 安全配置最佳实践
summary: 介绍 TiDB 安全配置的最佳实践，帮助你降低潜在的安全风险。
---

# TiDB 安全配置最佳实践

TiDB 的安全性对于保护数据完整性和机密性至关重要。本文提供了 TiDB 集群部署时的安全配置指南。遵循这些最佳实践可以有效降低潜在安全风险、防范数据泄露，并确保 TiDB 数据库系统能够持续稳定、可靠地运行。

> **注意：**
>
> 本文提供关于 TiDB 安全配置的一般建议。PingCAP 不保证信息的完整性或准确性，对使用本指南所产生的任何问题不承担责任。用户应根据自身需求评估这些建议，并咨询专业人士以获得具体的建议。

## 设置 root 用户初始密码

默认情况下，新创建的 TiDB 集群中 root 用户的密码为空，这可能导致潜在的安全风险。任何人都可以尝试使用 root 用户登录 TiDB 数据库，从而可能访问和修改数据。

为避免此风险，建议在部署过程中设置 root 密码：

- 使用 TiUP 部署时，参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md#第-7-步启动集群)为 root 用户生成随机密码。
- 使用 TiDB Operator 部署时，参考[初始化账号和密码设置](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/initialize-a-cluster#初始化账号和密码设置)为 root 用户设置密码。

## 启用密码复杂性检查

默认情况下，TiDB 未启用密码复杂性策略，这可能导致使用弱密码或空密码，增加安全风险。

为确保数据库用户创建强密码，建议配置合理的[密码复杂度策略](/password-management.md#密码复杂度策略)。例如，要求密码包含大写字母、小写字母、数字和特殊字符的组合。启用密码复杂性检查可以提高数据库的安全性、防止暴力破解攻击、减少内部威胁、遵守法规和合规性要求、降低数据泄露风险，并提高整体安全水平。

## 修改 Grafana 默认密码

TiDB 安装时默认包含 Grafana 组件，其默认的用户名密码通常为 `admin/admin`。如不及时修改，可能被攻击者利用获取系统控制权。

建议在部署 TiDB 时立即修改 Grafana 的密码为强密码，并定期更新密码以确保系统安全。修改 Grafana 密码的方式如下：

- 首次登录 Grafana 时，根据提示完成新密码的修改。

    ![Grafana Password Reset Guide](/media/grafana-password-reset1.png)

- 进入 Grafana 个人配置中心完成新密码的修改。

    ![Grafana Password Reset Guide](/media/grafana-password-reset2.png)

## 提高 TiDB Dashboard 安全性

### 使用最小权限用户

TiDB Dashboard 的账号体系与 TiDB SQL 用户一致，并基于 TiDB SQL 用户的权限进行 TiDB Dashboard 授权验证。TiDB Dashboard 所需的权限较少，甚至可以只有只读权限。

为提高系统安全性，建议为访问 TiDB Dashboard 创建一个[最小权限的 SQL 用户](/dashboard/dashboard-user.md)，并用该用户登录 TiDB Dashboard，避免使用高权限用户，提升安全性。

### 限制访问控制

默认情况下，TiDB Dashboard 设计为供受信任的用户访问。默认端口将包含除 TiDB Dashboard 外的其他 API 接口。如果你希望让外部网络用户或不受信任的用户访问 TiDB Dashboard，需要采取以下的措施以避免安全漏洞的出现：

- 使用防火墙等手段将默认的 `2379` 端口限制在可信域内，禁止外部用户进行访问。

    > **注意：**
    >
    > TiDB、TiKV 等组件需要通过 PD Client 端口与 PD 组件进行通信。请勿对组件内部网络阻止访问，这将导致集群不可用。

- [配置反向代理](/dashboard/dashboard-ops-reverse-proxy.md#通过反向代理使用-tidb-dashboard)，将 TiDB Dashboard 服务在另一个端口上安全地提供给外部。

## 保护内部端口

TiDB 的默认安装中存在许多用于组件间通信的特权接口。这些端口通常不需要向用户端开放，因为它们主要用于内部通信。当这些端口直接暴露在公共网络上时，会增加潜在的攻击面，违反了安全最小化原则，增加了安全风险的产生。下表列出了 TiDB 集群默认监听端口的详细情况：

| 组件                | 默认监听端口  | 协议       |
|-------------------|--------------|------------|
| TiDB              | 4000         | MySQL      |
| TiDB              | 10080        | HTTP       |
| TiKV              | 20160        | Protocol   |
| TiKV              | 20180        | HTTP       |
| PD                | 2379         | HTTP/Protocol|
| PD                | 2380         | Protocol   |
| TiFlash           | 3930         | Protocol   |
| TiFlash           | 20170        | Protocol   |
| TiFlash           | 20292        | HTTP       |
| TiFlash           | 8234         | HTTP       |
| TiFlow            |  8261/8291 | HTTP  |
| TiFlow            |  8262      | HTTP  |
| TiFlow            |  8300     | HTTP       |
| TiDB Lightning    | 8289         | HTTP       |
| TiDB Operator     | 6060         | HTTP       |
| TiDB Dashboard    | 2379         | HTTP       |
| TiDB Binlog       |  8250   | HTTP       |
| TiDB Binlog       |  8249 | HTTP      |
| TMS               | 8082         | HTTP       |
| TEM               | 8080         | HTTP       |
| TEM               | 8000         | HTTP       |
| TEM               | 4110         | HTTP       |
| TEM               | 4111         | HTTP       |
| TEM               | 4112         | HTTP       |
| TEM               | 4113         | HTTP       |
| TEM               | 4124         | HTTP       |
| Prometheus        | 9090         | HTTP       |
| Grafana           | 3000         | HTTP       |
| AlertManager      | 9093         | HTTP       |
| AlertManager      | 9094         | Protocol   |
| Node Exporter     | 9100         | HTTP       |
| Blackbox Exporter | 9115        | HTTP       |
| NG Monitoring     | 12020        | HTTP       |

建议只向普通用户公开数据库的 `4000` 端口和 Grafana 面板的 `9000` 端口，并通过网络安全策略组或防火墙限制其他端口。以下是使用 `iptables` 限制端口访问的示例：

```shell
# 允许来自各组件白名单 IP 地址范围的内部端口通讯
sudo iptables -A INPUT -s 内网 IP 地址范围 -j ACCEPT

# 仅对外部用户开放 4000 和 9000 端口
sudo iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

# 默认拒绝所有其他流量
sudo iptables -P INPUT DROP
```

如果需要访问 TiDB Dashboard，建议通过[配置反向代理](/dashboard/dashboard-ops-reverse-proxy.md#通过反向代理使用-tidb-dashboard)的方式将 TiDB Dashboard 服务安全地提供给外部网络，并将其部署在另外的端口上。

## 解决第三方扫描器 MySQL 漏洞误报

大多数漏洞扫描器在检测 MySQL 漏洞时，会根据版本信息来匹配 CVE 漏洞。由于 TiDB 仅兼容 MySQL 协议而非 MySQL 本身，基于版本信息的漏洞扫描可能导致误报。建议漏洞扫描应以原理扫描为主。当合规漏洞扫描工具要求 MySQL 版本时，你可以[修改服务器版本号](/faq/high-reliability-faq.md#我们的安全漏洞扫描工具对-mysql-version-有要求tidb-是否支持修改-server-版本号呢)，以满足其要求。

通过修改服务器版本号，可避免漏洞扫描器产生误报。[`server-version`](/tidb-configuration-file.md#server-version) 的值会被 TiDB 节点用于验证当前 TiDB 的版本。在进行 TiDB 集群升级前，请将 `server-version` 的值设置为空或者当前 TiDB 真实的版本值，避免出现非预期行为。
