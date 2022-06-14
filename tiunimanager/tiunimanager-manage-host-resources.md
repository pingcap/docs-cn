---
title: TiUniManager 主机资源管理
summary: 如何通过 TiUniManager 管理主机资源。
---

# TiUniManager 主机资源管理

本文档介绍如何通过 TiUniManager 管理主机资源，包括导入、查看、删除主机资源。

## 导入主机

系统初始化或者扩容机器时，系统管理员需将机器信息导入 TiUniManager 平台，TiUniManager 将导入的机器加入到集群中，由平台统一管理。

### 前置条件

将主机节点加入 TiDB 集群前，需要保证：

- 已经登录 TiUniManager 控制台
- 已安装主机的操作系统和所依赖的软件，并通过测试

> **注意：**
>
> - 你需要按照主机模板完整、正确地填写字段信息。详情参见本节中[主机模板字段说明](#主机模板字段说明)。
> - 导入主机时，TiDB 会对主机进行检查，参见 [TiDB 环境与系统配置检查](/check-before-deployment.md)。

TiUniManager 中控机通过 SSH 连接主机，默认连接端口为 `22`。如果环境中 SSH 端口不为默认的 `22`，可通过 OpenAPI 修改 `config_default_ssh_port` 参数来配置主机的默认登陆端口，该参数默认值为 `22`。以下示例通过 OpenAPI 修改 `config_default_ssh_port` 参数的值，从而修改主机的默认登陆端口：

1. 登录 TiUniManager 获取用户 Token。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X 'POST' \ 'http://172.16.6.206:4180/api/v1/user/login' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "userName": "admin", "userPassword": "admin" }'
    ```

    > **注意：**
    >
    > 你需要将以上命令中 `172.16.6.206:4180` 替换为实际环境中 TiUniManager 中控机的 IP 地址和 WebServer 服务端口。

2. 查看 `config_default_ssh_port` 的参数值。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X GET "http://172.16.6.206:4100/api/v1/config/?configKey=config_default_ssh_port" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

3. 将 `config_default_ssh_port` 的值修改为 `newValue`。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://172.16.6.206:4100/api/v1/config/update" -d "{ \"configKey\": \"config_default_ssh_port\", \"configValue\": \"newValue\"}" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

### 操作步骤

1. 进入资源管理页面。
2. 点击**导入主机**按钮。
3. 点击**下载主机模板**按钮。
4. 双击打开模板，并按照模板填入相应信息并保存。
5. 点击**上传**按钮，选择步骤 5 中编辑的文件，并上传该文件。
6. 点击**确认**按钮，确认导入主机信息。

### 主机模板字段说明

| Hostname        | 主机名                                                       |
| :--------------- | :------------------------------------------------------------ |
| IP              | 主机 IP 地址                                                 |
| Login username  | 主机用户名（选填， 当通过用户名密码方式导入主机时，才需要填写） |
| Login password  | 主机密码（选填， 当通过用户名密码方式导入主机时，才需要填写） |
| Region          | 区域 ID  (产品初始化时设定的 Region ID）                     |
| Zone            | 可用区 ID (产品初始化时设定的 Zone ID）                      |
| Rack            | 机架 ID （产品初始化时设定的 Rack ID）                       |
| Arch            | 体系架构                                                     |
| OS Version      | 操作系统版本                                                 |
| Kernel          | 内核版本                                                     |
| vCPU            | CPU 核数                                                     |
| Memory          | 内存大小                                                     |
| NIC             | 网卡规格                                                     |
| Cluster Purpose | 区分主机用来部署什么类型的集群，包括 TiDB、DM、TiUniManager          |
| Host Purpose    | 主机用途：用来区分部署的组件类型，包括：Compute、Storage、Schedule 三种用途。多种用途以逗号 “,” 连接，例如 ‘Compute,Storage,Schedule’ |
| Disk Type       | 磁盘类型，包括：NVMe SSD、SSD、SATA 三种类型                 |
| Disks           | 磁盘信息，包括磁盘名称、容量、状态、路径，示例：{"name": "sda","capacity": 256,"status": "Available", "path": "/mnt/sda"} |

如果通过用户名密钥方式导入主机，需要在 TiUniManager 安装前配置用户名和密钥路径，参见[指定 TiUniManager 中控机登录 TiDB 资源机的账户和密钥](/tiunimanager/tiunimanager-install-and-maintain.md#指定-tiunimanager-中控机登录-tidb-资源机的帐户和密钥)。

## 查看主机列表

查看 TiUniManager 当前管理的所有主机信息列表。

操作步骤如下：

1. 登录控制台。
2. 进入主机管理页面，在该页面即可看到主机列表。

## 删除主机

从 TiUniManager 主机资源池中删除主机。

操作步骤如下：

1. 登录控制台。
2. 进入资源管理页面。
3. 点击主机条目的**删除**。
4. 输入 "delete" 以确认删除操作。
5. 点击**确认删除**按钮。
