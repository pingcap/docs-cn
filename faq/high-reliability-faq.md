---
title: 高可靠常见问题
summary: 介绍高可靠相关的常见问题。
---

# 高可靠常见问题

本文档介绍高可靠相关的常见问题。

## 我们的安全漏洞扫描工具对 MySQL version 有要求，TiDB 是否支持修改 server 版本号呢？

TiDB 在 v3.0.8 后支持修改 server 版本号，可以通过配置文件中的 [`server-version`](/tidb-configuration-file.md#server-version) 配置项进行修改。在使用 TiUP 部署集群时，可以通过 `tiup cluster edit-config <cluster-name>` 修改配置文件中以下部分来设置合适的版本号：

```
server_configs:
  tidb:
    server-version: 'YOUR_VERSION_STRING'
```

并通过 `tiup cluster reload <cluster-name> -R tidb` 命令使得以上修改生效，以避免出现安全漏洞扫描不通过的问题。

## TiDB 支持哪些认证协议，过程是怎样的？

这一层跟 MySQL 一样，走的 SASL 认证协议，用于用户登录认证，对密码的处理流程。

客户端连接 TiDB 的时候，走的是 challenge-response（挑战-应答）的认证模式，过程如下：

1. 客户端连接服务器；
2. 服务器发送随机字符串 `challenge` 给客户端；
3. 客户端发送 `username` + `response` 给服务器；
4. 服务器验证 `response`。

## 如何修改用户名密码和权限？

TiDB 作为分布式数据库，在 TiDB 中修改用户密码建议使用 `set password for 'root'@'%' = '0101001';` 或 `alter` 方法，不推荐使用 `update mysql.user` 的方法进行，这种方法可能会造成其它节点刷新不及时的情况。修改权限也一样，都建议采用官方的标准语法。详情可参考 [TiDB 用户账户管理](/user-account-management.md)。
