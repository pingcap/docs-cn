---
title: 在 Azure Blob Storage 备份恢复
summary: 介绍使用 BR 在外部存储 Azure Blob Storage 上进行备份与恢复时的方法。
---

# 在 Azure Blob Storage 备份恢复

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

从 TiDB v5.4.0 起，Backup & Restore (BR) 工具开始支持将 Azure Blob Storage 作为外部存储来进行数据备份与恢复。

该功能**仅兼容** TiDB v5.4.0 及后续的版本。如需了解 BR 支持的其他外部存储，请参阅[外部存储](/br/backup-and-restore-storages.md)。

## 使用场景

Azure 虚拟机可以将大规模数据快速地存放到 Azure Blob Storage 上。如果你在使用 Azure 虚拟机来部署集群，可以考虑将数据备份到 Azure Blob Storage 中。

## 使用方法

使用 BR，你可以通过以下两种方法在 Azure Blob Storage 上进行备份与恢复：

- 使用 Azure AD 备份恢复
- 使用访问密钥备份恢复

在通常情况下，为了避免 `account-key` 等密钥信息记录在命令行中可能会存在的被泄漏的风险，推荐使用第一种方法，即使用 Azure AD 备份恢复。

以下为使用上述两种方式在 Azure Blob Storage 上进行备份与恢复的操作示例，其中，具体操作目标如下：

- 备份：将数据库的 `test` 库备份到 Azure Blob Storage 的容器名为 `container=test` 且路径前缀为 `t1` 的空间中；
- 恢复：将 Azure Blob Storage 的容器名为 `container=test` 且路径前缀为 `t1` 的空间恢复到数据库的 `test`库中。

### 方法一：使用 Azure AD 备份恢复（推荐）

在 BR 运行环境和 TiKV 运行环境中，需要存在环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。当存在这三项变量时，BR 可以使用 Azure AD 访问 Azure Blob Storage 且不用配置 `account-key`。这种方式更安全，因此也推荐被使用。在这里，`$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET` 分别代表 Azure 应用程序的应用程序 ID `client_id`，租户 ID `tenant_id` 和客户端密码 `client_id`。

#### 备份

使用 Azure AD 进行备份时，需要指定参数 `account-name` 和 `access-tier`。其中，如果没有设置 `access-tier`（即该值为空），该值会默认设置为 `Hot`。

> **注意**
> 
> 使用 Azure Blob Storage 的时候必须设置 `send-credentials-to-tikv = true`（即默认情况下），否则会备份失败。

本节中展示了备份到 `cool tier`，即上传对象的存储类别为 `Cool` 的案例。你可以通过以下两种方式指定 `account-name` 和 `access-tier`：

- 将参数信息放在 URL 参数中：
    
    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

- 将参数信息放在命令行参数中
    
    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### 恢复

使用 Azure AD 进行恢复时，需要指定参数 `account-name`。你可以通过以下两种方式指定 `account-name`：

- 将参数信息放在 URL 参数中

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

- 将参数信息放在命令行参数中

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### 方法二：使用访问密钥备份恢复（简易）

#### 备份

使用访问密钥进行备份时，需要指定参数 `account-name` 和 `access-tier`。其中，如果没有设置 `access-tier`（即该值为空），该值会默认设置为 `Hot`。

> **注意**
> 
> 使用 Azure Blob Storage 的时候必须设置 `send-credentials-to-tikv = true`（即默认情况下），否则会备份失败。

本节中展示了备份到 `cool tier`，即上传对象的存储类别为 `Cool` 的案例。你可以通过以下两种方式指定 `account-name` 和 `access-tier`：

- 将参数信息放在 URL 参数中：

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

- 将参数信息放在命令行参数中

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### 恢复

使用访问密钥进行恢复时，需要指定参数 `account-name` 和 `account-key`。你可以通过以下两种方式指定这些参数：

- 将参数信息放在 URL 参数中

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

- 将参数信息放在命令行参数中

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## 参数说明

在进行备份和恢复过程中，你会用到 `account-name`, `account-key`, `access-tier` 三个参数。有关参数的详细介绍，请参阅[外部存储](/br/backup-and-restore-storages.md)。

### URL 参数

| URL 参数 | 说明 | 默认值 | 是否必填 |
|---------:|-----|-------|---------|
| `account-name` | 存储账户名 | | 是 |
| `account-key` | 访问密钥 | | 是 |
| `access-tier` | 上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`）。如果没有设置 `access-tier` 的值（该值为空），此值会默认设置为 `Hot`。 | `Hot` | 否 |

### 命令行参数

| 命令行参数 | 说明 | 默认值 | 是否必填 |
|----------:|-------|-------|---------|
| `--azblob.account-name` | 存储账户名 | | 是 |
| `--azblob.account-key` | 访问密钥 | | 是 |
| `--azblob.access-tier` | 上传对象的存储类别（例如 `Hot`、`Cool`、`Archive`）。如果没有设置 `access-tier` 的值（该值为空），此值会默认设置为 `Hot`。 | `Hot` | 否 |

### 配置环境变量作为参数

由 TiUP 启动的集群中 TiKV 是 systemd 服务，例子展示如何为 TiKV 配置参数：

> **注意**
> 
> 需要重启 TiKV

1. 假设该节点上 tikv 端口为 24000（即 systemd 服务名为 tikv-24000）

    ```
    systemctl edit tikv-24000
    ```

2. 填入环境变量信息

    ```
    [Service]
    Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ```

3. 重新加载配置并重启 TiKV

    ```
    systemctl daemon-reload
    systemctl restart tikv-24000
    ```


## 兼容信息

该功能**仅兼容** TiDB v5.4.0及后续的版本。
