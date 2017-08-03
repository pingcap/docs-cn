---
title: 其他
category: faq-operations
---

# 其他

## TiDB是如何进行权限管理的？

TiDB 遵循 MySQL 的权限管理体系，可以创建用户并授予权限。

在创建用户时，可以使用 MySQL 语法，如 `CREATE USER 'test'@'localhost' identified by '123';`，这样就添加了一个用户名为 test，密码为 123 的用户，这个用户只能从 localhost 登录。

修改用户密码时，可以使用 Set Password 语句，例如给 TiDB 的默认 root 用户增加密码：`SET PASSWORD FOR 'root'@'%' = '123';`。

在进行授权时，也可以使用 MySQL 语法，如 `GRANT SELECT ON *.* TO  'test'@'localhost';`，将读权限授予 test 用户。

更多细节可以参考[权限管理](https://github.com/pingcap/docs-cn/blob/master/sql/privilege.md)。


## TiDB 高可用的特性是怎么样的？

高可用是 TiDB 的另一大特点，TiDB/TiKV/PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](README.md#高可用)。

## 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。我们提供了一个[检查工具](https://github.com/pingcap/tidb-tools/tree/master/checker)，用于检查 MySQL 中的 Schema 是否和 TiDB 兼容。

## TiDB/PD/TiKV 的日志在哪里

这三个组件默认情况下会将日志输出到标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

## 如何安全停止 TiDB?
如果是 ansible 部署的， 参考 https://github.com/pingcap/docs-cn/blob/master/op-guide/ansible-deployment.md。如果不是 ansible 部署，直接 kill 掉所有服务即可。其实大部分关闭脚本本身逻辑就是 kill，原理是一样的。并且发kill的信号，TiDB 的组件会做 graceful 的 shutdown，这点放心。

## TiDB 里面不能执行 kill 吗？
目前只能 kill 非 ddl 语句，ddl语句执行以后，除非出错，是无法 kill 的。进行 kill 操作的方法是，首先使用 `show processlist`，找到对应 session 的 id，然后执行 `kill tidb connection id`。



