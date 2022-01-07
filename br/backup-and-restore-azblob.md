---
title: 在 Azure Blob Storage 备份恢复
summary: 在 Azure Blob Storage 备份恢复方法。
aliases: ['/docs-cn/dev/br/backup-and-restore-azblob/']
---

# 在 Azure Blob Storage 备份恢复

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

本文档介绍 Azure Blob Storage 作为外部存储来进行备份恢复的使用场景、使用方法、使用限制和使用该功能的常见问题。

## 使用场景

azure 虚拟机可以将大规模数据快速地存放到 azure blob storage 上，当使用 azure 虚拟机来部署集群时，可以考虑将数据备份到 azure blob storage 中存储。

## 操作步骤

BR 提供了 2 种在 Azure Blob Storage 上备份恢复的方法，分别是 `使用 Azure AD 备份恢复` 方法和 `使用访问密钥备份恢复` 方法。

在通常情况下，为了避免 `account-key` 等密钥信息在命令行存在的泄漏风险，推荐使用 `使用 Azure AD 备份恢复` 方法。

文档使用如下演示例子：在备份过程中，将库 `test` 备份到 Azure Blob Storage 上 `container=test`，路径前缀为 `t1` 的空间中；在恢复过程中，从 Azure Blob Storage 上 `container=test`, 路径前缀为 `t1` 的空间中恢复数据到库 `test`。

### 使用 Azure AD 备份恢复

需要在 BR 运行环境和 TiKV 运行环境中存在环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。使用了 Azure AD 后访问 Azure Blob Storage 不用配置 `account-key`，这种方式更安全，也是推荐的使用。

#### 备份

该方法的备份过程中需要用到 `account-name` 这个参数, `access-tier` 可以根据需要配置，本文展示了备份到 `cool tier` 的案例。

##### 将信息放在 URL 参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
```

##### 将信息放在命令行参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
```

#### 恢复

该方法的恢复过程中用到 `account-name` 这个参数。

##### 将信息放在 URL 参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
```

##### 将信息放在命令行参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
```

### 使用访问密钥备份恢复

#### 备份

备份过程中需要用到 `account-name`, `account-key` 两个参数，`access-tier` 可以根据需要配置，本文展示了备份到 `cool tier` 的案例。

##### 将信息放在 URL 参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
```

##### 将信息放在命令行参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
```

#### 恢复

该方法的恢复过程中用到 `account-name` 和 `account-key` 两个参数。

##### 将信息放在 URL 参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
```

##### 将信息放在命令行参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
```

## 参数说明

备份和恢复过程中会用到 `account-name`, `account-key`, `access-tier` 三个参数，参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。

### URL 参数

| URL 参数 | 说明 | 默认值 | 是否必填 |
|---------:|-----|-------|---------|
| `account-name` | 存储账户名 | | 是 |
| `account-key` | 访问密钥 | | 是 |
| `access-tier` | 上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`） | `Hot` | 否 |


### 命令行参数

| 命令行参数 | 说明 | 默认值 | 是否必填 |
|----------:|-------|-------|---------|
| `--azblob.account-name` | 存储账户名 | | 是 |
| `--azblob.account-key` | 访问密钥 | | 是 |
| `--azblob.access-tier` | 上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`） | `Hot` | 否 |

## 兼容信息

仅兼容 `v5.4.0` 之后的版本

