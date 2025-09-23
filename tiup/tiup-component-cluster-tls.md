---
title: tiup cluster tls
summary: tiup cluster tls 命令用于开启、或关闭集群组件之间的 TLS。
---

# tiup cluster tls

命令 `tiup cluster tls` 用于开启集群组件之间的 TLS (Transport Layer Security)，会自签发证书下发到各个节点。

## 语法

```shell
tiup cluster tls <cluster-name> <enable/disable> [flags]
```

`<cluster-name>` 为要启用自启的集群。

## 选项

### --clean-certificate

- 当 TLS 关闭时，指定此选项可清理之前生成的证书。
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 如果不指定该选项，之后开启 TLS 时，可能沿用旧证书。

### --force

- 强制执行开启或关闭 TLS 的流程，不管当前集群是否开启 TLS。
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 如果不指定该选项，开关状态相同时跳过执行。

### --reload-certificate

- 当 TLS 开启时，指定此选项可重新生成证书。
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 如果不指定该选项，已经生成过证书后，不会再生成新证书。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。
