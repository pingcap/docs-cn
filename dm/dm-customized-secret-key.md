---
title: DM 自定义加解密 key
summary: 介绍如何自定义密钥，用于加密和解密 DM（Data Migration）数据源和迁移任务配置中的密码。
---

# DM 自定义加解密 key

在 v8.0.0 之前，[DM](/dm/dm-overview.md) 使用了一个[固定的 AES-256 密钥](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27)来加密和解密数据源和迁移任务配置中的密码，但固定秘钥可能产生安全风险，特别是在对安全性要求较高的环境中。为了提高安全性，从 v8.0.0 开始，DM 移除了固定密钥，并支持设置自定义密钥。

## 使用方式

1. 创建一个自定义的密钥文件，文件内容必须为长度为 64 个字符的十六进制的 AES-256 密钥。
2. 在 DM-master [启动参数](/dm/dm-command-line-flags.md)或[配置文件](/dm/dm-master-configuration-file.md) 中，设置 `secret-key-path` 为你自定义的密钥文件的路径。

## 从低于 v8.0.0 的版本升级

从 v8.0.0 开始，DM 不再使用固定密钥，因此从低于 v8.0.0 的版本升级时需要注意：

- 如果[数据源配置](/dm/dm-source-configuration-file.md)和[迁移任务配置](/dm/task-configuration-file-full.md)里使用的都是明文密码，则升级不需要做额外处理。
- 如果[数据源配置](/dm/dm-source-configuration-file.md)和[迁移任务配置](/dm/task-configuration-file-full.md)里使用了加密密码，或者后续希望使用加密密码，则需进行以下操作：
    1. 在 [DM-master 配置文件](/dm/dm-master-configuration-file.md) 中，增加 `secret-key-path` 参数，将其设置为你自定义的密钥文件的路径。该文件内容须为长度为 64 个字符的十六进制的 AES-256 密钥。如果升级前使用了[固定的 AES-256 密钥](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27) 进行加密，可拷贝该秘钥到你的秘钥文件中。请确保所有 DM-master 节点使用相同的密钥配置。
    2. 先滚动升级 DM-master，然后滚动升级 DM-worker，具体参考[滚动升级](/dm/maintain-dm-using-tiup.md#滚动升级)。

## 更新加解密 key

如需更新用于加密和解密的密钥，请按照以下顺序进行：

1. 更新 [DM-master 配置文件](/dm/dm-master-configuration-file.md) 中的 `secret-key-path`。

    > **注意：**
    >
    >  - 请确保所有 DM-master 节点更新为相同的密钥配置。
    >  - 在密钥更新期间，请不要创建新的[数据源配置文件](/dm/dm-source-configuration-file.md)和[迁移任务配置文件](/dm/task-configuration-file-full.md)。

2. 滚动重启 DM-master。
3. 使用 `tiup dmctl encrypt`（dmctl 版本需 >= v8.0.0）加密的密码用于创建[数据源配置文件](/dm/dm-source-configuration-file.md)和[迁移任务配置文件](/dm/task-configuration-file-full.md)。
