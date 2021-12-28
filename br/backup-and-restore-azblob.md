---
title: 在 Azure Blob Storage 备份恢复
summary: 在 Azure Blob Storage 备份恢复方法。
aliases: ['/docs-cn/dev/br/backup-and-restore-azblob/']
---

# 使用访问密钥备份恢复

## 备份

将库 `test` 备份到 Azure Blob Storage 上，选择 `container=test`，路径前缀为 `t1` 。
以 azurite 默认账户为例，上传数据 `access-tier` 值为 `Cool`，有以下两种命令方式：

#### 将信息放在 URL 参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
```

#### 将信息放在命令行参数中

```
tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
```

## 恢复

从 Azure Blob Storage 上恢复数据到库 `test`，只需要将上述命令行中的 `backup` 子命令改成 `restore` 即可。

# 使用 Azure AD 备份恢复

需要在 BR 运行环境和 TiKV 运行环境中存在环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

## 备份

将库 `test` 备份到 Azure Blob Storage 上，选择 `container=test`，路径前缀为 `t1` 。
以 azurite 默认账户为例，上传数据 `access-tier` 值为 `Cool`，有以下三种命令方式：

#### 将 `account-name` 放在 URL 参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
```

#### 将 `account-name` 放在命令行参数中

```
tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
```

#### 将 `account-name` 放在 BR 运行环境的环境变量中

```
export AZURE_STORAGE_ACCOUNT=devstoreaccount1

tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?'
```

## 恢复

从 Azure Blob Storage 上恢复数据到库 `test`，只需要将上述命令行中的 `backup` 子命令改成 `restore` 即可。

# 使用环境变量的访问密钥备份恢复

需要 BR 运行环境中**不都**存在 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET` 这三个环境变量，否则 BR 会选择通过 Azure AD 进行备份恢复。

## 备份
将库 `test` 备份到 Azure Blob Storage 上，选择 `container=test`，路径前缀为 `t1` 。
以 azurite 默认账户为例，上传数据 `access-tier` 值为 `Cool`，有以下三种命令方式：

#### 将 `account-name` 放在 URL 参数中

```
export AZURE_STORAGE_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==

tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
```

#### 将 `account-name` 放在命令行参数中

```
export AZURE_STORAGE_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==

tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
```

#### 将 `account-name` 放在 BR 运行环境的环境变量中

```
export AZURE_STORAGE_ACCOUNT=devstoreaccount1
export AZURE_STORAGE_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==


tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?'
```

## 恢复

从 Azure Blob Storage 上恢复数据到库 `test`，只需要将上述命令行中的 `backup` 子命令改成 `restore` 即可。
