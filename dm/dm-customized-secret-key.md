---
title: DM 自定义加解密 key
summary: DM 自定义加解密 key
---

# DM 自定义加解密 key

在 DM v8.0.0 之前，DM 内部使用了[固定的 AES-256 key](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27) 来加解密 source 和 task 配置中的密码，但固定秘钥会产生安全风险，特别是在安全要求较高的环境下，自 v8.0.0 版本开始，DM 移除了固定秘钥，并支持设置自定义秘钥。

## 使用方式

在 dm-master 启动参数或者配置文件中设置 [`secret-key-path`](/dm/dm-master-configuration-file.md)，该参数指向秘钥文件路径，文件内容必须是长度为 64 的 hex AES-256 key。

## 从 < v8.0.0 版本升级

由于从 v8.0.0 版本开始 DM 移除了固定秘钥，不在向后兼容，因此从 < v8.0.0 版本升级时需要做一些额外操作

- 如果所有的 source/task 配置都使用的明文密码，则升级不需要做额外处理。
- 如果存在 source/task 配置使用了加密密码，或者后续希望使用加密密码，则需要：
    - 修改 dm-master 配置文件，增加 [`secret-key-path`](/dm/dm-master-configuration-file.md)，如果之前使用了 [固定的 AES-256 key](https://github.com/pingcap/tiflow/blob/1252979421fc83ffa2a1548d981e505f7fc0b909/dm/pkg/encrypt/encrypt.go#L27) 做加密，可拷贝该秘钥到秘钥文件中。注意，所有 dm-master 配置的秘钥需要一致。
    - 先滚动升级 dm-master，然后滚动升级 dm-worker，具体参考[滚动升级](/dm/maintain-dm-using-tiup.md#滚动升级)。

## 更新加密 key

- 更新期间请不要创建 source/task。
- 更改 [`secret-key-path`](/dm/dm-master-configuration-file.md) 中的秘钥。注意，所有 dm-master 配置的秘钥需要一致。
- 滚动重启 dm-master
- 使用 `dmctl encrypt`(dmctl 版本需 >= v8.0.0) 加密的密码来创建 source/task。
