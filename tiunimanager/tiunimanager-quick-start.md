---
title: TiUniManager 快速操作指南
summary: 了解如何快速使用 TiUniManager 进行集群操作。
---

# TiUniManager 快速操作指南

本文档介绍 TiUniManager 的常见操作场景以及基本的集群操作，包括将主机节点加入 TiDB 集群、创建 TiDB 集群、删除集群、接管集群。

在阅读本文档前，你需要先阅读 [TiUniManager 安装和运维手册](/tiunimanager/tiunimanager-install-and-maintain.md)完成 TiUniManager 的安装。

## 将主机节点加入 TiDB 集群

系统初始化或者扩容机器时，系统管理员需将主机信息导入 TiUniManager 平台，TiUniManager 将导入的机器加入到集群中，由平台统一管理。

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

## 创建集群

TiUniManager 部署完成后，你可以通过 TiUniManager 创建 TiDB 集群，并自定义集群配置。

### 前置条件

- 已登录 TiUniManager 控制台
- 已完成主机资源导入

### 操作步骤

1. 进入**集群管理** > **集群**页面。
2. 点击创建集群按钮，跳转至创建实例的页面。
3. 选择集群创建模式。
4. 选择集群主机所在厂商、区域。
5. 输入以下数据库基本信息：
    - 数据库类型
    - CPU 体系架构
    - 数据库版本
    - 参数组
6. 设置数据库产品各组件的以下配置：
    - 所在可用区
    - 实例规格
    - 实例数量
7. 输入集群的以下基本信息：
    - 集群名称 。集群名称必须是 4 - 64 个字符，可包含大小写字母、数字和连字符，并以字母或数字开头。
    - 集群标签
    - 数据库管理员 Root 的密码。密码必须是 8-64 个字符，可包含大小写字母、数字和可见的特殊字符（包括 `!@#$%^&*()_+=)`）
    - 是否独占部署
8. 点击**提交**按钮，确认主机资源库存满足集群要求后，点击**确认创建**按钮。

## 删除集群

由于业务或其他原因，如果你不再需要某个已创建的实例，可以将此集群删除。

### 前置条件

- 已登录 TiUniManager 控制台。
- 待删除的 TiDB 集群已存在。

> **注意：**
>
> 删除集群同时将删除集群上自动备份的数据。如果需要某个备份数据，应在删除实例之前将该备份恢复到新实例上，数据恢复操作可参见[备份管理 - 数据恢复](/tiunimanager/tiunimanager-manage-clusters.md#备份管理---数据恢复) 。

### 操作步骤

1. 进入**集群管理** > **集群页面**。
2. 选择待删除的集群，点击集群 ID 进入**集群详情**页面。
3. 点击**删除**按钮。
4. 选择是否在删除集群前完成一次数据备份。
5. 选择是否保留手动备份数据。
6. 输入 "delete" 以确认删除，点击**确认删除**按钮。

## 接管集群

通过 TiUniManager 接管已经存在的 TiDB 集群，统一管理新老集群，提高集群管理效率。

### 前置条件

已经登录 TiUniManager 控制台。

### 操作步骤

1. 进入**集群管理** > **集群**页面。
2. 点击接管集群按钮，进入**接管集群**页面。
3. 输入接管集群的基本信息：集群名称、数据库用户名 root、数据库密码。
4. 输入接管集群中控配配置信息：
    - 接管集群中控机主机 IP 地址
    - 接管集群中控机 SSH 端口号
    - 接管集群中控机 SSH 用户名
    - 接管集群中控机 SSH 密码
    - 接管集群中控机 TiUP 路径（即 `.tiup` 目录所在路径，不含路径结尾的 `/`，例如 `/root/.tiup` 不能填写为 `/root/.tiup/`）
5. 导入接管集群的主机（导入主机流程参见[将主机节点加入 TiDB 集群](#将主机节点加入-tidb-集群)）。