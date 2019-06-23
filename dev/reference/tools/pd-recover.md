---
title: PD Recover 使用文档
category: reference
aliases: ['/docs-cn/tools/pd-recover/']
---

# PD Recover 使用文档

PD Recover 是对 PD 进行灾难性恢复的工具，用于恢复无法正常启动或服务的 PD 集群。

## 源码编译

1. [Go](https://golang.org/) Version 1.9 以上
2. 在 PD 项目根目录使用 `make` 命令进行编译，生成 `bin/pd-recover`

## 使用方法

### 参数说明

```
  -alloc-id uint
        指定比原集群已分配过的 ID 更大的数
  -cacert string
        指定 PEM 格式的受信任 CA 的证书文件路径
  -cert string
        指定 PEM 格式的 SSL 证书文件路径
  -key string
        指定 PEM 格式的 SSL 证书密钥文件路径，即 `--cert` 所指定的证书的私钥
  -cluster-id uint
        指定原集群的 cluster ID
  -endpoints string
        指定 PD 的地址 (default "http://127.0.0.1:2379")
```

### 恢复流程

1. 从当前集群中找到集群的 Cluster ID 和 Alloc ID。一般在 PD，TiKV 或 TiDB 的日志中都可以获取 Cluster ID。已经分配过的 Alloc ID 可以从 PD 日志获得。另外也可以从 PD 的监控面板的 Metadata Information 监控项中获得。在指定 alloc-id 时需指定一个比当前最大的 Alloc ID 更大的值。如果没有途径获取 Alloc ID，可以根据集群中的 Region，Store 数预估一个较大的数，一般可取高几个数量级的数。
2. 停止整个集群，清空 PD 数据目录，重启 PD 集群。
3. 使用 PD recover 进行恢复，注意指定正确的 cluster-id 和合适的 alloc-id。
4. 提示恢复成功后，重启整个集群。
