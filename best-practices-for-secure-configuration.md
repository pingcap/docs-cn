---
title: TiDB 安全配置最佳实践
summary: 介绍TiDB最佳安全配置，有效降低潜在的安全风险
aliases: ['/docs-cn/dev/faq/security-faq/']
---

# TiDB 安全配置最佳实践

TiDB的安全性是确保数据完整性和保护机密性的关键要素。本文档旨在为TiDB用户在部署TiDB集群时提供指导，以采取适当的安全措施。通过遵循这些安全最佳实践，您可以有效降低潜在的安全风险，防范数据泄露，并确保TiDB数据库系统能够持续稳定、可靠地运行。

## 如何为 root 账号设置初始密码？

### 问题描述

默认情况下，在创建群集时，root密码为空，这可能导致潜在的安全风险。这意味着任何人都可以尝试使用root账户登录到TiDB数据库，因为没有密码限制。这种情况下，未经授权的用户或攻击者可以轻易地访问和修改数据库中的数据，给数据库的安全性带来了严重威胁。因此，建议在部署过程中立即设置root密码，以加强数据库的安全性

### 解决方案

1. TiUP部署时， [为root账户生成随机密码](/production-deployment-using-tiup.md#第-7-步启动集群) 
2. TiDB Operator部署时， [设置root账户密码](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/initialize-a-cluster#%E5%88%9D%E5%A7%8B%E5%8C%96%E8%B4%A6%E5%8F%B7%E5%92%8C%E5%AF%86%E7%A0%81%E8%AE%BE%E7%BD%AE)

## 如何启用密码复杂性检查?

### 问题描述

默认情况下，TiDB未启用密码复杂性策略，这可能导致出现弱密码和空密码，从而增加了安全风险。为确保数据库用户创建强密码，建议配置适当的密码复杂性策略，要求密码包含大写字母、小写字母、数字和特殊字符的组合。这有助于提高数据库的安全性，防止´暴力破解攻击，减少内部威胁，遵守法规和合规性要求，降低数据泄露风险，并提高整体安全水平。

### 解决方案

配置合理的 [密码复杂度策略](/password-management.md#密码复杂度策略)，避免出现弱密码、空密码问题造成的账户安全风险

## 如何修改 Grafana 默认密码?

### 问题描述

在 TiDB 安装部署过程中，Grafana 组件是默认包含在内的。而默认情况下，Grafana 的凭据通常是 admin/admin。然而，若未及时修改这些默认凭据，可能会导致系统面临安全风险。攻击者可以利用这些默认凭据轻易地获取对系统的控制权，进而执行恶意操作，窃取敏感数据。

### 解决方案

建议在部署 TiDB 时，立即修改 Grafana 的默认凭据，采用强密码，并定期更新密码以确保系统安全。

1. 在Grafana 在首次登录后根据提示完成新密码的修改
   ![Grafana Password Reset Guide](/media/grafana-password-reset1.png)
2. 进入个人配置中心完成新密码的修改
   ![Grafana Password Reset Guide](/media/grafana-password-reset2.png)

## 如何提高 TiDB Dashboard 安全性

### 示例1 权限最小化

TiDB Dashboard 的账号体系与 TiDB SQL 用户一致，并基于 TiDB SQL 用户的权限进行 TiDB Dashboard 授权验证。TiDB Dashboard 所需的权限较少，甚至可以只有只读权限。建议为访问TiDB Dashboard创建一个最小权限的SQL用户，避免使用高权限用户，从而提高系统的安全性。

### 权限最小化解决方案

为访问 TiDB Dashboard 创建一个 [最小权限的 SQL 用户](/dashboard/dashboard-user.md)，并用该用户登录 TiDB Dashboard，避免使用高权限用户，提升安全性。 

### 示例2 访问控制限制

尽管访问 TiDB Dashboard 需要登录，但它被设计为默认供受信任的用户实体访问。默认端口将包含除 TiDB Dashboard 外的其他 API 接口。如果你希望让外部网络用户或不受信任的用户访问 TiDB Dashboard，需要采取适当的措施以避免安全漏洞的出现。

### 访问控制限制解决方案

1. 应当利用防火墙等手段将默认的2379端口放置在可信域内，禁止外部用户进行访问。 注意，TiDB、TiKV 等组件需要通过 PD Client 端口与 PD 组件进行通信，因此请勿对组件内部网络阻止访问，这将导致集群不可用。
2. 通过[配置反向代理](/dashboard/dashboard-ops-reverse-proxy.md#通过反向代理使用-tidb-dashboard)的方式将 TiDB Dashboard 服务在另一个端口上安全地提供给外部

## 如何对内部端口进行安全保护?

### 问题描述

TiDB 的默认安装中存在许多用于组件间通信的特权接口。这些端口通常不需要向用户端开放，因为它们主要设计用于内部通信。当这些端口直接暴露在公共网络上时，会增加潜在的攻击面，违反了安全最小化原则，增加了安全风险的产生，以下为TiDB集群默认监听端口的全部详细情况:

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

### 解决方案

建议只向普通用户公开数据库的 4000 端口和 Grafana 面板的 9000 端口。其他端口应该通过网络安全策略组或防火墙进行限制。此外，如果额外需要访问 TiDB Dashboard，建议通过配置[反向代理的方式](/dashboard/dashboard-ops-reverse-proxy.md#通过反向代理使用-tidb-dashboard)将 TiDB Dashboard 服务安全地提供给外部网络，并将其部署在另外的端口上。

```
# 允许来自各组件白名单IP地址范围的内部端口通讯
sudo iptables -A INPUT -s 内网IP地址范围 -j ACCEPT

# 仅对外部用户开放4000和9000端口
sudo iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

# 默认拒绝所有其他流量
sudo iptables -P INPUT DROP
```

## 如何解决三方扫描器 mysql漏洞误报问题?

### 问题描述

大多数漏洞扫描器在检测 MySQL 漏洞时，通常会根据版本信息来匹配 CVE 漏洞。然而，我们的 TiDB 产品并非 MySQL，而是仅兼容 MySQL 协议。因此，仅依赖简单的 MySQL 版本扫描可能会导致误报。我们建议漏洞扫描应以原理扫描为主。当客户的合规漏洞扫描工具要求 MySQL 版本时，TiDB 支持修改服务器版本号，以满足其要求。

### 解决方案

通过[修改服务器版本号](/faq/high-reliability-faq.md#我们的安全漏洞扫描工具对-mysql-version-有要求tidb-是否支持修改-server-版本号呢)，可避免漏洞扫描器产生误报。server-version 的值会被 TiDB 节点用于验证当前 TiDB 的版本。因此在进行 TiDB 集群升级前，请将 server-version 的值设置为空或者当前 TiDB 真实的版本值，避免出现非预期行为。

# 免责声明

本指南提供关于TiDB安全配置的一般建议。PingCAP不保证信息的完整性或准确性，对使用本指南所产生的任何问题不承担责任。用户应根据自身需求评估这些建议，并咨询专业人士以获得具体的建议。