---
title: ALTER INSTANCE
summary: TiDB 数据库中 ALTER INSTANCE 的使用概况。
category: reference
---

# ALTER INSTANCE

`ALTER INSTANCE` 语句用于对单个 TiDB 实例进行变更操作， 目前 TiDB 仅支持 `RELOAD TLS` 子句。

# RELOAD TLS

`ALTER INSTACE RELOAD TLS` 语句用于从原配置的证书([`ssl-cert`](/reference/configuration/tidb-server/configuration-file.md#ssl-cert)), 密钥([`ssl-key`](/reference/configuration/tidb-server/configuration-file.md#ssl-key)) 和 CA([`ssl-ca`](/reference/configuration/tidb-server/configuration-file.md#ssl-ca))路径重新加证书，密钥和 CA。

新加载的证书密钥和 CA 将在语句执行成功后对新建立的连接生效，不会影响语句执行前已建立的连接。

在重加载遇到错误时默认会报错且继续使用变更前的密钥和证书，而在添加可选的 `NO ROLLBACK ON ERROR` 后重加载遇到错误将不报错并关闭 TLS 安全连接功能继续工作。 

## 语法图

![AlterInstanceStmt](/media/sqlgram/AlterInstanceStmt.png)


## 示例

{{< copyable "sql" >}}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL 兼容性

- 仅支持从原配置路径重加载， 不支持动态修改加载路径，也不支持动态启用启动时未开启的 TLS 加密连接功能。

## 另请参阅

* [Enable Client TLS](/how-to/secure/enable-tls-clients.md) 