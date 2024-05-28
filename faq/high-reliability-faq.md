---
title: 高可靠常见问题
summary: 介绍高可靠相关的常见问题。
aliases: ['/docs-cn/dev/faq/high-reliability-faq/']
---

# 高可靠常见问题

本文档介绍高可靠相关的常见问题。

## TiDB 是否支持数据加密？

支持。要加密传输中的数据，可以[在 TiDB 客户端和服务器之间启用 TLS](/enable-tls-between-clients-and-servers.md)。要加密存储引擎中的数据，可以启用[透明数据加密 (TDE)](/encryption-at-rest.md)。

## 我们的安全漏洞扫描工具对 MySQL version 有要求，TiDB 是否支持修改 server 版本号呢？

TiDB 在 v3.0.8 后支持通过 TiDB 配置文件中的 [`server-version`](/tidb-configuration-file.md#server-version) 配置项来修改 server 版本号。

对于 v4.0 及以上版本的集群，如果使用 TiUP 部署集群，可以通过 `tiup cluster edit-config <cluster-name>` 修改配置文件中以下部分来设置合适的版本号：

```
server_configs:
  tidb:
    server-version: 'YOUR_VERSION_STRING'
```

修改完成后，使用 `tiup cluster reload <cluster-name> -R tidb` 命令使得以上修改生效，以避免出现安全漏洞扫描不通过的问题。

## TiDB 支持哪些认证协议？过程是怎样的？

TiDB 和 MySQL 一样，在用户登录认证时使用 SASL 认证协议对密码进行处理。

客户端连接 TiDB 的时候，使用 challenge-response（挑战-应答）的认证模式，过程如下：

1. 客户端连接服务器。
2. 服务器发送随机字符串 `challenge` 给客户端。
3. 客户端发送 `username` + `response` 给服务器。
4. 服务器验证 `response`。

## 如何修改用户名密码和权限？

因为 TiDB 是分布式数据库，想要在 TiDB 中修改用户密码，建议使用 `ALTER USER` 的方法，例如 `ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';`。

不推荐使用 `UPDATE mysql.user` 的方法，因为这种方法可能会造成其它节点刷新不及时的情况。修改权限也一样，建议参考 [TiDB 用户账户管理](/user-account-management.md)文档中的方法。
