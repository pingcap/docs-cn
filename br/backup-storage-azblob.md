---
title: 使用 BR 在 Azure Blob Storage 备份和恢复数据
summary: 介绍使用 BR 在外部存储 Azure Blob Storage 上进行备份与恢复时的方法。
aliases: ['/zh/tidb/dev/backup-and-restore-azblob']
---

# 使用 BR 在 Azure Blob Storage 备份和恢复数据

TiDB 的备份恢复功能 Backup & Restore (BR) 支持将 Azure Blob Storage 作为外部存储来进行数据备份与恢复。

## 使用场景

Azure 虚拟机可以将大规模数据快速地存放到 Azure Blob Storage 上。如果你使用 Azure 虚拟机来部署集群，可以考虑将数据备份到 Azure Blob Storage 中。

## 使用方法

使用 BR，你可以通过以下两种方法在 Azure Blob Storage 上进行备份与恢复：

- 使用 Azure AD 备份恢复
- 使用访问密钥备份恢复

在通常情况下，为了避免 `account-key` 等密钥信息记录在命令行中被泄漏，推荐使用第一种方法，即使用 Azure AD 备份恢复。

以下为使用上述两种方式在 Azure Blob Storage 上进行备份与恢复的操作示例，其中，具体操作目标如下：

- 备份：将数据库的 `test` 库备份到 Azure Blob Storage 的容器名为 `container=test` 且路径前缀为 `t1` 的空间中；
- 恢复：将 Azure Blob Storage 的容器名为 `container=test` 且路径前缀为 `t1` 的空间恢复到数据库的 `test` 库中。

> **注意：**
>
> 无论使用 Azure AD 还是使用访问密钥进行备份，都需要设置 `send-credentials-to-tikv = true`。否则，备份会失败。

### 方法一：使用 Azure AD 备份恢复（推荐）

本小节介绍如何使用 Azure AD 进行备份恢复，该方式需要先配置环境变量，然后执行备份或恢复。

#### 配置环境变量

你需要在 BR 运行环境和 TiKV 运行环境中配置环境变量 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。

- 当使用 TiUP 启动的集群时，TiKV 会使用 systemd 服务。以下示例介绍如何为 TiKV 配置上述三个环境变量：

    > **注意：**
    >
    > 该流程在第 3 步中需要重启 TiKV。如果你的集群不适合重启，请使用[方法二](#方法二使用访问密钥备份恢复简易)进行备份恢复。

    1. 假设该节点上 TiKV 端口为 24000（即 systemd 服务名为 tikv-24000）：

        ```
        systemctl edit tikv-24000
        ```

    2. 填入环境变量信息：

        ```
        [Service]
        Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ```

    3. 重新加载配置并重启 TiKV：

        ```
        systemctl daemon-reload
        systemctl restart tikv-24000
        ```

- 为命令行启动的 TiKV 和 BR 配置 Azure AD 的信息，只需要确定运行环境中存在 `$AZURE_CLIENT_ID`、`$AZURE_TENANT_ID` 和 `$AZURE_CLIENT_SECRET`。通过运行下列命令行，可以确认 BR 和 TiKV 运行环境中是否存在这三个环境变量：

    ```
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

更多关于环境变量的信息，可以参考 [Azblob 的 URL 参数](/br/backup-and-restore-storages.md#azblob-的-url-参数)。

#### 备份

本节展示了备份到 `cool tier`，即上传对象的存储类别为 `Cool` 的案例。你需要使用 URL 或命令行来指定 `account-name` 和 `access-tier`。根据指定方式的不同，备份的操作略有差异。

- 在 URL 参数中指定 `account-name` 和 `access-tier`：

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

    如果没有设置 `access-tier`（即该值为空），该值会默认设置为 `Hot`。

- 在命令行参数中指定 `account-name` 和 `access-tier` ：

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### 恢复

根据参数 `account-name` 的指定方式，你可以使用 URL 或命令行参数进行恢复。

- 在 URL 参数中指定 `account-name`：

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

- 在命令行参数中指定 `account-name`：

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### 方法二：使用访问密钥备份恢复（简易）

与使用 Azure AD 备份恢复相比，使用访问密钥备份和恢复更加简单，无需配置环境变量。其他步骤与使用 Azure AD 备份恢复相同。

#### 备份

- 在 URL 参数中指定 `account-name`、`account-key` 和 `access-tier`：

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

- 在命令行参数中指定 `account-name`、`account-key` 和 `access-tier`：

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### 恢复

- 在 URL 参数中指定 `account-name` 和 `account-key`：

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

- 在命令行参数中指定 `account-name` 和 `account-key`：

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## 兼容信息

该功能**仅兼容** TiDB v5.4.0 及后续的版本。

## 探索更多

- 如需了解 BR 支持的其他外部存储，请参阅[外部存储](/br/backup-and-restore-storages.md)。
- 有关参数的详细介绍，请参阅以下内容：

    - [URL 参数](/br/backup-and-restore-storages.md#azblob-的-url-参数)
    - [命令行参数](/br/backup-and-restore-storages.md#azblob-的命令行参数)
