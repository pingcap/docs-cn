---
title: 在 Azure Blob Storage 备份恢复
summary: 在 Azure Blob Storage 备份恢复方法。
aliases: ['/docs-cn/dev/br/backup-and-restore-azblob/']
---

# 在 Azure Blob Storage 备份恢复

文档将介绍如何使用 Azure Blob Storage 作为外部存储来进行备份恢复。在备份过程中，介绍如何将库 `test` 备份到 Azure Blob Storage 上 `container=test`，路径前缀为 `t1` 的空间中；在恢复过程中，介绍如何从 Azure Blob Storage 上 `container=test`, 路径前缀为 `t1` 的空间中恢复数据到库 `test`。

文档以 azurite 默认账户为例，上传数据的 `access-tier` 值为 `Cool`。参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。

## 使用访问密钥备份恢复

### 备份

备份过程中需要用到 `account-name`, `account-key`, `access-tier` 三个参数，参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。有以下两种命令方式。

#### 将信息放在 URL 参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
```

#### 将信息放在命令行参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
```

### 恢复

恢复过程中用到 `account-name` 和 `account-key` 两个参数，参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。恢复的命令与备份相似，只需要将上述命令行中的 `backup` 子命令改成 `restore` 即可。其中 `access-tier` 参数对于恢复命令来说没有影响。

## 使用 Azure AD 备份恢复

需要在 BR 运行环境和 TiKV 运行环境中存在环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

### 备份

备份过程中需要用到 `account-name`, `account-key`, `access-tier` 三个参数，参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。

#### 将 `account-name` 放在 URL 参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
```

#### 将 `account-name` 放在命令行参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
```

### 恢复

恢复过程中用到 `account-name` 和 `account-key` 两个参数，参数的详细介绍请参考[外部存储](/br/backup-and-restore-storages.md)。恢复的命令与备份相似，只需要将上述命令行中的 `backup` 子命令改成 `restore` 即可。其中 `access-tier` 参数对于恢复命令来说没有影响。
