---
title: TiUniManager 数据导入与导出
summary: 了解如何使用 TiUniManager 从 TiDB 集群导入和导出数据。
---

# TiUniManager 数据导入与导出

本文档介绍如何使用 TiUniManager 从 TiDB 集群导入和导出数据。

## 导入数据

DBA 管理员可从 S3 兼容存储、本地存储、或 TiUniManager 共享存储上，导入 SQL 文件、CSV 文件的数据到 TiDB 集群。

TiUniManager 共享存储是用户事先设定好、用于保存导入导出文件的文件资源池，该文件资源池是一个可挂载于 TiUniManager 中控机的 NFS 目录，你可在安装 TiUniManager 后设置该路径。

### 导入前准备

进行操作前，确保已经登录 TiUniManager 控制台。

> **注意：**
>
> - 从本地上传的源数据文件大小不能超过 2 GiB
> - TiUniManager 最多支持 3 个导入导出任务并行运行，后续任务在队列中等待

TiUniManager 默认的导入导出路径是在 TiUniManager 中控机上，细节如下：

| **配置描述**                                                 | **配置参数名**         | **参考值**                                                   |
| ------------------------------------------------------------ | ---------------------- | ------------------------------------------------------------ |
| TiUniManager 共享存储中导入文件的存储位置（建议配置为 NFS 共享存储） | `ImportShareStoragePath` | `/home/tidb/import`（备注：中控机 `tidb` 账号拥有该路径的读写权限) |
| TiUniManager 共享存储中导出文件的存储位置（建议配置为 NFS 共享存储） | `ExportShareStoragePath` | `/home/tidb/export`（备注：中控机 `tidb` 账号拥有该路径的读写权限） |

当前 TiUniManager 不支持通过前端界面修改导入路径。如需修导入路径，需要通过 OpenAPI 对配置进行修改，以修改 `ImportShareStoragePath` 为例：

1. 登录获取 user token。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X 'POST' \ 'http://172.16.6.206:4180/api/v1/user/login' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "userName": "admin", "userPassword": "admin" }'
    ```

    > **注意：**
    >
    > 你需要将以上命令中·`172.16.6.206:4180` 替换为实际环境中 TiUniManager 中控机的 IP 地址和 WebServer 服务端口。

2. 查看配置参数值。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X GET "http://172.16.6.206:4100/api/v1/config/?configKey=ImportShareStoragePath" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

3. 修改配置参数值为 `newValue`（根据实际的环境设置为新的存储路径）。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://172.16.6.206:4100/api/v1/config/update" -d "{ \"configKey\": \"ImportShareStoragePath\", \"configValue\": \"newValue\"}" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

### 导入数据操作步骤

1. 进入**集群管理** > **导入导出**页面。
2. 点击**导入数据**按钮，进入导入页面。
3. 输入目标集群信息：集群 ID、数据库用户名、数据库密码。
4. 选择源数据。存储位置可以是本地文件或 TiUniManager 共享存储或 S3 兼容存储。
5. 输入本次导入备注信息。
6. 点击**创建导入任务**开始导入。

## 导出数据

DBA 管理员可从 TiDB 集群将数据以 SQL 文件或 CSV 文件格式，导出至 S3 兼容存储、本地存储或 TiUniManager 共享存储，并可对导出数据进行筛选。数据筛选的方式包括：

* 按 SQL 语句对导出数据进行筛选
* 按指定库表对导出数据进行筛选

对于保存在 TiUniManager 共享存储上的导入数据，你可进一步下载至本地。

### 导出前准备

在导出数据前，确保已经登录 TiUniManager 控制台。

> **注意：**
>
> * TiUniManager 最多支持 3 个导入导出任务并行运行，后续任务在队列中等待。
> * 从 TiUniManager 共享存储下载的导出数据文件大小不能超过 2 GiB。

当前 TiUniManager 前端不支持修改导入导出路径，如需修改导入导出路径，需要通过 OpenAPI 对配置进行修改，以修改 `ExportShareStoragePath` 为例：

1. 登录获取 user token。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X 'POST' \ 'http://172.16.6.206:4180/api/v1/user/login' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "userName": "admin", "userPassword": "admin" }'
    ```

    > **注意：**
    >
    > 你需要将以上命令中·`172.16.6.206:4180` 替换为实际环境中 TiUniManager 中控机的 IP 地址和 WebServer 服务端口。

2. 查看配置参数值。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X GET "http://172.16.6.206:4100/api/v1/config/?configKey=ExportShareStoragePath" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

3. 修改配置参数值为 `newValue`（根据实际环境设置为新的存储路径）。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://172.16.6.206:4100/api/v1/config/update" -d "{ \"configKey\": \"ExportShareStoragePath\", \"configValue\": \"newValue\"}" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

### 导出数据操作步骤

1. 进入**集群管理** > **导入导出**页面。
2. 点击**导出数据**按钮，进入导出数据页面。
3. 输入源集群信息：集群 ID、数据库用户名、数据库密码。
4. 选择导出目标位置：TiUniManager 共享存储或 S3 兼容存储。
5. 设置导出选项：导出文件格式，是否筛选数据及筛选条件。
6. 记录本次导出备注信息。
7. 点击**创建导出任务**开始导出数据。

## 查看数据的导入导出记录

你可以通过 TiUniManager 查看、删除数据的导入导出记录，并下载记录文件至本地。

在查看数据的导入导出记录前，确保已经登录 TiUniManager 控制台。

查看数据的导入导出记录的操作步骤如下：

1. 进入**集群管理** > **导入导出**页面。
2. 查看导入导出记录列表。
3. 选择导出记录的**下载**，可下载导出记录至本地。
4. 选择记录的**删除**，可删除导入导出记录。
