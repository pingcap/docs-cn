---
title: 为 TiDB 开启数据加密存储
summary: 介绍如何为 TiDB 开启数据加密存储。
category: how-to
---

# 为 TiDB 开启数据加密存储

在 TiDB 集群中，用户的数据都存储在 TiKV 中，配置了 TiKV 数据加密存储功能，就代表 TiDB 集群已经加密存储了用户的数据。本部分主要介绍如何配置 TiKV 的加密存储功能。

## 操作流程

1. 生成 token 文件。

    token 文件存储的是密钥，用于对用户数据进行加密，以及对已加密的数据进行解密。

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl random-hex --len 256 > cipher-file-256
    ```

    > **注意：**
    >
    > TiKV 只接受 hex 格式的 token 文件，文件的长度必须是 2<sup>n</sup>，并且小于等于 1024。

2. 配置 TiKV。

    ```toml
    [security]
    # Cipher file 的存储路径
    cipher-file = "/path/to/cipher-file-256"
    ```

> **注意：**
>
> 若使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 向集群导入数据，如果目标集群开启了加密功能，Lightning 生成的 SST 文件也必须是加密的格式。

## 使用限制

目前 TiKV 数据加密存储存在以下限制：

- 对之前没有开启加密存储的集群，不支持开启该功能。
- 已经开启加密功能的集群，不允许关闭加密存储功能。
- 同一集群内部，不允许部分 TiKV 实例开启该功能，部分 TiKV 实例不开启该功能。对于加密存储功能，所有 TiKV 实例要么都开启该功能，要么都不开启该功能。这是由于 TiKV 实例之间会有数据迁移，如果开启了加密存储功能，迁移过程中数据也是加密的。
