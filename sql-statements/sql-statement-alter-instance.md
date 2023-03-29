---
title: ALTER INSTANCE
summary: TiDB 数据库中 ALTER INSTANCE 的使用概况。
---

# ALTER INSTANCE

`ALTER INSTANCE` 语句用于对单个 TiDB 实例进行变更操作。目前 TiDB 仅支持 `RELOAD TLS` 子句。

## RELOAD TLS

`ALTER INSTANCE RELOAD TLS` 语句用于从原配置的证书 ([`ssl-cert`](/tidb-configuration-file.md#ssl-cert))、密钥 ([`ssl-key`](/tidb-configuration-file.md#ssl-key)) 和 CA ([`ssl-ca`](/tidb-configuration-file.md#ssl-ca)) 的路径重新加证书、密钥和 CA。

新加载的证书密钥和 CA 将在语句执行成功后对新建立的连接生效，不会影响语句执行前已建立的连接。

在重加载遇到错误时默认会报错返回且继续使用变更前的密钥和证书，但在添加可选的 `NO ROLLBACK ON ERROR` 后遇到错误将不报错并以关闭 TLS 安全连接功能的方式处理后续请求。

## 语法图

```ebnf+diagram
AlterInstanceStmt ::=
    'ALTER' 'INSTANCE' InstanceOption

InstanceOption ::=
    'RELOAD' 'TLS' ('NO' 'ROLLBACK' 'ON' 'ERROR')?
```

## 示例

{{< copyable "sql" >}}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL 兼容性

仅支持从原配置路径重加载，不支持动态修改加载路径，也不支持动态启用启动 TiDB 时未开启的 TLS 加密连接功能。

## 另请参阅

[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)
