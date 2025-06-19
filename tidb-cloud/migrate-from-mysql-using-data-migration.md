---
title: 使用数据迁移功能将 MySQL 兼容数据库迁移至 TiDB Cloud
summary: 了解如何使用数据迁移功能将 Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL 或自管理 MySQL 实例无缝迁移至 TiDB Cloud，并将停机时间降至最低。
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# 使用数据迁移功能将 MySQL 兼容数据库迁移至 TiDB Cloud

本文档指导你如何使用 [TiDB Cloud 控制台](https://tidbcloud.com/) 中的数据迁移功能，将 MySQL 数据库从 Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL 或自管理 MySQL 实例迁移至 TiDB Cloud。

此功能使你能够直接将现有的 MySQL 数据和持续变更（binlog）从 MySQL 兼容的源数据库复制到 TiDB Cloud，无论是在同一区域还是跨不同区域，都能保持数据一致性。这种简化的流程消除了单独的导出和导入操作的需求，减少了停机时间，简化了从 MySQL 到更具可扩展性平台的迁移过程。

如果你只想将 MySQL 兼容数据库的持续 binlog 变更复制到 TiDB Cloud，请参阅[使用数据迁移功能将增量数据从 MySQL 兼容数据库迁移至 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

## 限制

### 可用性

- 数据迁移功能仅适用于 **TiDB Cloud Dedicated** 集群。

- 如果你在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中看不到 TiDB Cloud Dedicated 集群的[数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md#步骤-1-进入数据迁移页面)入口，该功能可能在你所在的区域不可用。要请求支持你所在的区域，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

- Amazon Aurora MySQL 写入实例支持现有数据和增量数据迁移。Amazon Aurora MySQL 只读实例仅支持现有数据迁移，不支持增量数据迁移。

### 迁移任务的最大数量

每个组织最多可以创建 200 个迁移任务。如需创建更多迁移任务，你需要[提交支持工单](/tidb-cloud/tidb-cloud-support.md)。

### 被过滤和删除的数据库

- 即使你选择迁移所有数据库，系统数据库也会被过滤掉，不会迁移到 TiDB Cloud。也就是说，`mysql`、`information_schema`、`performance_schema` 和 `sys` 不会使用此功能进行迁移。

- 当你删除 TiDB Cloud 中的集群时，该集群中的所有迁移任务都会自动删除，且无法恢复。

### 现有数据迁移的限制

- 在现有数据迁移期间，如果目标数据库中已经存在要迁移的表，并且存在重复的键，具有重复键的行将被替换。

- 如果你的数据集大小小于 1 TiB，建议使用逻辑模式（默认模式）。如果你的数据集大小大于 1 TiB，或者你想更快地迁移现有数据，可以使用物理模式。更多信息，请参阅[迁移现有数据和增量数据](#迁移现有数据和增量数据)。

### 增量数据迁移的限制

- 在增量数据迁移期间，如果要迁移的表在目标数据库中已存在且有重复的键，将报告错误并中断迁移。在这种情况下，你需要确认 MySQL 源数据是否准确。如果准确，点击迁移任务的"重启"按钮，迁移任务将用 MySQL 源记录替换目标 TiDB Cloud 集群中的冲突记录。

- 在增量复制（将持续变更迁移到集群）期间，如果迁移任务从突发错误中恢复，它可能会开启 60 秒的安全模式。在安全模式期间，`INSERT` 语句将作为 `REPLACE` 迁移，`UPDATE` 语句将作为 `DELETE` 和 `REPLACE` 迁移，然后这些事务将迁移到目标 TiDB Cloud 集群，以确保突发错误期间的所有数据都已顺利迁移到目标 TiDB Cloud 集群。在这种情况下，对于没有主键或非空唯一索引的 MySQL 源表，一些数据可能在目标 TiDB Cloud 集群中重复，因为数据可能会重复插入到目标 TiDB Cloud 集群中。

- 在以下场景中，如果迁移任务耗时超过 24 小时，请不要清除源数据库中的二进制日志，以确保数据迁移可以获取连续的二进制日志进行增量复制：

    - 在现有数据迁移期间。
    - 在现有数据迁移完成后，当首次启动增量数据迁移时，延迟不为 0ms。
## 前提条件

在开始迁移之前，请检查你的数据源是否受支持，在 MySQL 兼容数据库中启用二进制日志记录，确保网络连接，并为源数据库和目标 TiDB Cloud 集群数据库授予所需权限。

### 确保你的数据源和版本受支持

数据迁移支持以下数据源和版本：

| 数据源 | 支持的版本 |
|:------------|:-------------------|
| 自管理 MySQL（本地或公有云） | 8.0、5.7、5.6 |
| Amazon Aurora MySQL | 8.0、5.7、5.6 |
| Amazon RDS MySQL | 8.0、5.7 |
| Azure Database for MySQL - Flexible Server | 8.0、5.7 |
| Google Cloud SQL for MySQL | 8.0、5.7、5.6 |

### 在源 MySQL 兼容数据库中启用二进制日志以进行复制

要使用 DM 将源 MySQL 兼容数据库的增量变更持续复制到 TiDB Cloud 目标集群，你需要在源数据库中进行以下配置以启用二进制日志：

| 配置 | 必需值 | 原因 |
|:--------------|:---------------|:----|
| `log_bin` | `ON` | 启用二进制日志记录，DM 使用它来复制变更到 TiDB |
| `binlog_format` | `ROW` | 准确捕获所有数据变更（其他格式会遗漏边缘情况） |
| `binlog_row_image` | `FULL` | 在事件中包含所有列值以进行安全的冲突解决 |
| `binlog_expire_logs_seconds` | ≥ `86400`（1 天），`604800`（7 天，推荐） | 确保 DM 在迁移期间可以访问连续的日志 |

#### 检查当前值并配置源 MySQL 实例

要检查当前配置，连接到源 MySQL 实例并执行以下语句：

```sql
SHOW VARIABLES WHERE Variable_name IN
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days');
```

如有必要，更改源 MySQL 实例配置以匹配所需值。

<details>
<summary> 配置自管理 MySQL 实例 </summary>

1. 打开 `/etc/my.cnf` 并添加以下内容：

    ```
    [mysqld]
    log_bin = mysql-bin
    binlog_format = ROW
    binlog_row_image = FULL
    binlog_expire_logs_seconds = 604800   # 7 天保留期
    ```

2. 重启 MySQL 服务以应用更改：

    ```
    sudo systemctl restart mysqld
    ```

3. 再次运行 `SHOW VARIABLES` 语句以验证设置是否生效。

有关详细说明，请参阅 MySQL 文档中的 [MySQL Server System Variables](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html) 和 [The Binary Log](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)。

</details>

<details>
<summary> 配置 AWS RDS 或 Aurora MySQL </summary>

1. 在 AWS 管理控制台中，打开 [Amazon RDS 控制台](https://console.aws.amazon.com/rds/)，在左侧导航栏中点击 **Parameter groups**，然后创建或编辑自定义参数组。
2. 将上述四个参数设置为所需值。
3. 将参数组附加到你的实例或集群，然后重启以应用更改。
4. 重启后，连接到实例并运行 `SHOW VARIABLES` 语句以验证配置。

有关详细说明，请参阅 AWS 文档中的 [Working with DB Parameter Groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html) 和 [Configuring MySQL Binary Logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。

</details>

<details>
<summary> 配置 Azure Database for MySQL - Flexible Server </summary>

1. 在 [Azure 门户](https://portal.azure.com/) 中，搜索并选择 **Azure Database for MySQL servers**，点击你的实例名称，然后在左侧导航栏中点击 **Setting** > **Server parameters**。

2. 搜索每个参数并更新其值。

    大多数更改无需重启即可生效。如果需要重启，门户会提示你。

3. 运行 `SHOW VARIABLES` 语句以验证配置。

有关详细说明，请参阅 Microsoft Azure 文档中的 [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-configure-server-parameters-portal)。

</details>

<details>
<summary> 配置 Google Cloud SQL for MySQL </summary>

1. 在 [Google Cloud 控制台](https://console.cloud.google.com/project/_/sql/instances) 中，选择包含你实例的项目，点击你的实例名称，然后点击 **Edit**。
2. 添加或修改所需的标志（`log_bin`、`binlog_format`、`binlog_row_image`、`binlog_expire_logs_seconds`）。
3. 点击 **Save**。如果需要重启，控制台会提示你。
4. 重启后，运行 `SHOW VARIABLES` 语句以确认更改。

有关详细说明，请参阅 Google Cloud 文档中的 [Configure database flags](https://cloud.google.com/sql/docs/mysql/flags) 和 [Use point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr)。

</details>

### 确保网络连接

在创建迁移任务之前，你需要规划并设置源 MySQL 实例、TiDB Cloud 数据迁移（DM）服务和目标 TiDB Cloud 集群之间的适当网络连接。

可用的连接方法如下：

| 连接方法 | 可用性 | 推荐用于 |
|:---------------------|:-------------|:----------------|
| 公共端点或 IP 地址 | TiDB Cloud 支持的所有云提供商 | 快速概念验证迁移、测试或无法使用私有连接时 |
| 私有链接或私有端点 | 仅 AWS 和 Azure | 不向公共互联网暴露数据的生产工作负载 |
| VPC 对等连接 | 仅 AWS 和 Google Cloud | 需要低延迟、区域内连接且 VPC/VNet CIDR 不重叠的生产工作负载 |

选择最适合你的云提供商、网络拓扑和安全要求的连接方法，然后按照该方法的设置说明进行操作。

#### 通过 TLS/SSL 的端到端加密

无论选择哪种连接方法，都强烈建议使用 TLS/SSL 进行端到端加密。虽然私有端点和 VPC 对等连接可以保护网络路径，但 TLS/SSL 可以保护数据本身并帮助满足合规要求。

<details>
<summary> 下载并存储云提供商的证书以进行 TLS/SSL 加密连接 </summary>

- Amazon Aurora MySQL 或 Amazon RDS MySQL：[Using SSL/TLS to encrypt a connection to a DB instance or cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
- Azure Database for MySQL - Flexible Server：[Connect with encrypted connections](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
- Google Cloud SQL for MySQL：[Manage SSL/TLS certificates](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)

</details>

#### 公共端点或 IP 地址

使用公共端点时，你可以在 DM 任务创建过程中验证网络连接和访问。TiDB Cloud 将提供特定的出口 IP 地址并在当时提示相关说明。

1. 确定并记录源 MySQL 实例的端点主机名（FQDN）或公共 IP 地址。
2. 确保你有修改数据库防火墙或安全组规则的必要权限。参考以下云提供商的文档获取指导：

    - Amazon Aurora MySQL 或 Amazon RDS MySQL：[Controlling access with security groups](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html)。
    - Azure Database for MySQL - Flexible Server：[Public Network Access](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    - Google Cloud SQL for MySQL：[Authorized Networks](https://cloud.google.com/sql/docs/mysql/configure-ip#authorized-networks)。

3. 可选：使用具有公共互联网访问权限的机器和适当的证书验证与源数据库的连接，以进行传输中加密：

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 在数据迁移任务设置期间，TiDB Cloud 将提供一个出口 IP 范围。此时，你需要按照上述相同的程序将此 IP 范围添加到数据库的防火墙或安全组规则中。
#### 私有链接或私有端点

如果你使用提供商原生的私有链接或私有端点，请为你的源 MySQL 实例（RDS、Aurora 或 Azure Database for MySQL）创建私有端点。

<details>
<summary> 为 MySQL 源数据库设置 AWS PrivateLink 和私有端点 </summary>

AWS 不支持直接通过 PrivateLink 访问 RDS 或 Aurora。因此，你需要创建一个网络负载均衡器（NLB）并将其作为与源 MySQL 实例关联的端点服务发布。

1. 在 [Amazon EC2 控制台](https://console.aws.amazon.com/ec2/) 中，在与 RDS 或 Aurora 写入器相同的子网中创建一个 NLB。配置 NLB 时，设置一个在端口 `3306` 上将流量转发到数据库端点的 TCP 监听器。

    有关详细说明，请参阅 AWS 文档中的 [Create a Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)。

2. 在 [Amazon VPC 控制台](https://console.aws.amazon.com/vpc/) 中，在左侧导航栏中点击 **Endpoint Services**，然后创建一个端点服务。在设置过程中，选择上一步创建的 NLB 作为后端负载均衡器，并启用 **Require acceptance for endpoint** 选项。端点服务创建后，复制服务名称（格式为 `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`）以供后续使用。

    有关详细说明，请参阅 AWS 文档中的 [Create an endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)。

3. 可选：在开始迁移之前，从同一 VPC 或 VNet 内的堡垒机或客户端测试连接：

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 稍后，当配置 TiDB Cloud DM 通过 PrivateLink 连接时，你需要返回 AWS 控制台并批准来自 TiDB Cloud 到此私有端点的待处理连接请求。

</details>

<details>
<summary> 为 MySQL 源数据库设置 Azure PrivateLink 和私有端点 </summary>

Azure Database for MySQL - Flexible Server 支持原生私有端点。你可以在创建 MySQL 实例时启用私有访问（VNet 集成），或者稍后添加私有端点。

要添加新的私有端点，请执行以下步骤：

1. 在 [Azure 门户](https://portal.azure.com/) 中，搜索并选择 **Azure Database for MySQL servers**，点击你的实例名称，然后在左侧导航栏中点击 **Setting** > **Networking**。
2. 在 **Networking** 页面上，滚动到 **Private endpoints** 部分，点击 **+ Create private endpoint**，然后按照屏幕上的说明设置私有端点。

    在设置过程中，在 **Virtual Network** 选项卡中选择 TiDB Cloud 可以访问的虚拟网络和子网，并在 **DNS** 选项卡中保持启用 **Private DNS integration**。私有端点创建和部署后，点击 **Go to resource**，在左侧导航栏中点击 **Settings** > **DNS configuration**，在 **Customer Visible FQDNs** 部分找到用于连接实例的主机名。通常，主机名的格式为 `<your-instance-name>.mysql.database.azure.com`。

    有关详细说明，请参阅 Azure 文档中的 [Create a private endpoint via Private Link Center](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center)。

3. 可选：在开始迁移之前，从同一 VPC 或 VNet 内的堡垒机或客户端测试连接：

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 在 [Azure 门户](https://portal.azure.com/) 中，返回到 MySQL Flexible Server 实例（不是私有端点对象）的概览页面，点击 **Essentials** 部分的 **JSON View**，然后复制资源 ID 以供后续使用。资源 ID 的格式为 `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`。你将使用此资源 ID（而不是私有端点 ID）来配置 TiDB Cloud DM。

5. 稍后，当配置 TiDB Cloud DM 通过 PrivateLink 连接时，你需要返回 Azure 门户并批准来自 TiDB Cloud 到此私有端点的待处理连接请求。

</details>

#### VPC 对等连接

如果你使用 AWS VPC 对等连接或 Google Cloud VPC 网络对等连接，请参阅以下说明配置网络。

<details>
<summary> 设置 AWS VPC 对等连接</summary>

如果你的 MySQL 服务在 AWS VPC 中，请执行以下步骤：

1. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 MySQL 服务的 VPC 和你的 TiDB 集群。

2. 修改与 MySQL 服务关联的安全组的入站规则。

    你必须将[你的 TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站规则中。这样做可以允许流量从你的 TiDB 集群流向 MySQL 实例。

3. 如果 MySQL URL 包含 DNS 主机名，你需要允许 TiDB Cloud 能够解析 MySQL 服务的主机名。

    1. 按照 [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns) 中的步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

</details>

<details>
<summary> 设置 Google Cloud VPC 网络对等连接 </summary>

如果你的 MySQL 服务在 Google Cloud VPC 中，请执行以下步骤：

1. 如果是自托管 MySQL，你可以跳过此步骤并继续下一步。如果你的 MySQL 服务是 Google Cloud SQL，你必须在 Google Cloud SQL 实例关联的 VPC 中暴露一个 MySQL 端点。你可能需要使用 Google 开发的 [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy)。

2. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接你的 MySQL 服务的 VPC 和你的 TiDB 集群。

3. 修改 MySQL 所在 VPC 的入站防火墙规则。

    你必须将[你的 TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站防火墙规则中。这样可以允许流量从你的 TiDB 集群流向 MySQL 端点。

</details>

### 授予迁移所需的权限

在开始迁移之前，你需要在源数据库和目标数据库上设置具有所需权限的适当数据库用户。这些权限使 TiDB Cloud DM 能够安全地从 MySQL 读取数据、复制变更并写入你的 TiDB Cloud 集群。由于迁移涉及现有数据的完整导出和增量变更的 binlog 复制，你的迁移用户需要基本读取访问权限之外的特定权限。

#### 在源 MySQL 数据库中为迁移用户授予所需权限

对于测试目的，你可以在源 MySQL 数据库中使用管理员用户（如 `root`）。

对于生产工作负载，建议在源 MySQL 数据库中有一个专门用于数据导出和复制的用户，并只授予必要的权限：

| 权限 | 范围 | 用途 |
|:----------|:------|:--------|
| `SELECT` | 表 | 允许从所有表读取数据 |
| `RELOAD` | 全局 | 确保完整导出期间的一致性快照 |
| `REPLICATION SLAVE` | 全局 | 启用 binlog 流式传输以进行增量复制 |
| `REPLICATION CLIENT` | 全局 | 提供对 binlog 位置和服务器状态的访问 |

例如，你可以在源 MySQL 实例中使用以下 `GRANT` 语句授予相应权限：

```sql
GRANT SELECT, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### 在目标 TiDB Cloud 集群中授予所需权限

对于测试目的，你可以使用 TiDB Cloud 集群的 `root` 账户。

对于生产工作负载，建议在目标 TiDB Cloud 集群中有一个专门用于复制的用户，并只授予必要的权限：

| 权限 | 范围 | 用途 |
|:----------|:------|:--------|
| `CREATE` | 数据库、表 | 在目标中创建架构对象 |
| `SELECT` | 表 | 在迁移期间验证数据 |
| `INSERT` | 表 | 写入迁移的数据 |
| `UPDATE` | 表 | 在增量复制期间修改现有行 |
| `DELETE` | 表 | 在复制或更新期间删除行 |
| `ALTER`  | 表 | 在架构变更时修改表定义 |
| `DROP`   | 数据库、表 | 在架构同步期间删除对象 |
| `INDEX`  | 表 | 创建和修改索引 |
| `CREATE VIEW`  | 视图 | 创建迁移使用的视图 |

例如，你可以在目标 TiDB Cloud 集群中执行以下 `GRANT` 语句授予相应权限：

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```
## 步骤 1：进入数据迁移页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/) 并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群的名称以进入其概览页面，然后在左侧导航栏中点击 **Data** > **Migration**。

3. 在**数据迁移**页面，点击右上角的**创建迁移任务**。此时会显示**创建迁移任务**页面。

## 步骤 2：配置源和目标连接

在**创建迁移任务**页面，配置源和目标连接。

1. 输入任务名称，必须以字母开头且少于 60 个字符。可以使用字母（A-Z、a-z）、数字（0-9）、下划线（_）和连字符（-）。

2. 填写源连接配置。

    - **数据源**：数据源类型。
    - **连接方式**：根据你的安全要求和云提供商选择数据源的连接方式：
        - **公共 IP**：适用于所有云提供商（推荐用于测试和概念验证迁移）。
        - **Private Link**：仅适用于 AWS 和 Azure（推荐用于需要私有连接的生产工作负载）。
        - **VPC 对等连接**：仅适用于 AWS 和 Google Cloud（推荐用于需要低延迟、区域内连接且 VPC/VNet CIDR 不重叠的生产工作负载）。
    - 根据选择的**连接方式**，执行以下操作：
        - 如果选择了**公共 IP**或 **VPC 对等连接**，在**主机名或 IP 地址**字段中填写数据源的主机名或 IP 地址。
        - 如果选择了 **Private Link**，填写以下信息：
            - **端点服务名称**（如果**数据源**来自 AWS）：输入你为 RDS 或 Aurora 实例创建的 VPC 端点服务名称（格式：`com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`）。
            - **私有端点资源 ID**（如果**数据源**来自 Azure）：输入你的 MySQL Flexible Server 实例的资源 ID（格式：`/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`）。
    - **端口**：数据源的端口。
    - **用户名**：数据源的用户名。
    - **密码**：用户名的密码。
    - **SSL/TLS**：启用 SSL/TLS 进行端到端数据加密（强烈建议用于所有迁移任务）。根据你的 MySQL 服务器的 SSL 配置上传适当的证书。

        SSL/TLS 配置选项：

        - 选项 1：仅服务器认证

            - 如果你的 MySQL 服务器仅配置了服务器认证，只需上传 **CA 证书**。
            - 在此选项中，MySQL 服务器提供其证书以证明其身份，TiDB Cloud 根据 CA 验证服务器证书。
            - 如果 MySQL 服务器以 `require_secure_transport = ON` 启动，则需要 CA 证书来防止中间人攻击。

        - 选项 2：客户端证书认证

            - 如果你的 MySQL 服务器配置了客户端证书认证，上传**客户端证书**和**客户端私钥**。
            - 在此选项中，TiDB Cloud 向 MySQL 服务器提供其证书进行认证，但 TiDB Cloud 不验证 MySQL 服务器的证书。
            - 当 MySQL 服务器配置了 `REQUIRE SUBJECT '...'` 或 `REQUIRE ISSUER '...'` 等选项而没有 `REQUIRE X509` 时，通常使用此选项，允许它检查客户端证书的特定属性而不进行完整的 CA 验证。
            - 当 MySQL 服务器在自签名或自定义 PKI 环境中接受客户端证书时，通常使用此选项。请注意，此配置容易受到中间人攻击，除非其他网络级别的控制可以保证服务器的真实性，否则不建议在生产环境中使用。

        - 选项 3：相互 TLS (mTLS) - 最高安全性

            - 如果你的 MySQL 服务器配置了相互 TLS (mTLS) 认证，上传 **CA 证书**、**客户端证书**和**客户端私钥**。
            - 在此选项中，MySQL 服务器使用客户端证书验证 TiDB Cloud 的身份，TiDB Cloud 使用 CA 证书验证 MySQL 服务器的身份。
            - 当 MySQL 服务器为迁移用户配置了 `REQUIRE X509` 或 `REQUIRE SSL` 时，需要此选项。
            - 当 MySQL 服务器需要客户端证书进行认证时，使用此选项。
            - 你可以从以下来源获取证书：
                - 从你的云提供商下载（参见 [TLS 证书链接](#通过-tlsssl-的端到端加密)）。
                - 使用你组织的内部 CA 证书。
                - 自签名证书（仅用于开发/测试）。

3. 填写目标连接配置。

    - **用户名**：输入 TiDB Cloud 中目标集群的用户名。
    - **密码**：输入 TiDB Cloud 用户名的密码。

4. 点击**验证连接并继续**以验证你输入的信息。

5. 根据你看到的消息采取行动：

    - 如果你使用**公共 IP**或 **VPC 对等连接**作为连接方式，你需要将数据迁移服务的 IP 地址添加到源数据库的 IP 访问列表和防火墙（如果有）中。
    - 如果你使用 **Private Link** 作为连接方式，系统会提示你接受端点请求：
        - 对于 AWS：转到 [AWS VPC 控制台](https://us-west-2.console.aws.amazon.com/vpc/home)，点击 **Endpoint services**，接受来自 TiDB Cloud 的端点请求。
        - 对于 Azure：转到 [Azure 门户](https://portal.azure.com)，按名称搜索你的 MySQL Flexible Server，在左侧导航栏中点击 **Setting** > **Networking**，在右侧找到 **Private endpoint** 部分，然后批准来自 TiDB Cloud 的待处理连接请求。
## 步骤 3：选择迁移任务类型

在**选择要迁移的对象**步骤中，你可以选择现有数据迁移、增量数据迁移或两者都选。

### 迁移现有数据和增量数据

要一次性将数据迁移到 TiDB Cloud，请同时选择**现有数据迁移**和**增量数据迁移**，这可以确保源数据库和目标数据库之间的数据一致性。

你可以使用**物理模式**或**逻辑模式**来迁移**现有数据**和**增量数据**。

- 默认模式是**逻辑模式**。此模式将数据从 MySQL 源数据库导出为 SQL 语句，然后在 TiDB 上执行这些语句。在此模式下，迁移前的目标表可以是空的或非空的。但性能比物理模式慢。

- 对于大型数据集，建议使用**物理模式**。此模式从 MySQL 源数据库导出数据并将其编码为 KV 对，直接写入 TiKV 以实现更快的性能。此模式要求迁移前目标表必须为空。对于 16 RCU（复制容量单位）的规格，性能约为逻辑模式的 2.5 倍。其他规格的性能可以比逻辑模式提高 20% 到 50%。请注意，性能数据仅供参考，在不同场景中可能有所不同。

> **注意：**
>
> - 当你使用物理模式时，在现有数据迁移完成之前，不能为 TiDB 集群创建第二个迁移任务或导入任务。
> - 当你使用物理模式且迁移任务已经开始时，请**不要**启用 PITR（时间点恢复）或在集群上有任何 changefeed。否则，迁移任务将会卡住。如果你需要启用 PITR 或有任何 changefeed，请改用逻辑模式迁移数据。

物理模式尽可能快地导出 MySQL 源数据，因此[不同规格](/tidb-cloud/tidb-cloud-billing-dm.md#数据迁移的规格)对 MySQL 源数据库在数据导出期间的 QPS 和 TPS 有不同的性能影响。下表显示了每个规格的性能回退。

| 迁移规格 | 最大导出速度 | MySQL 源数据库的性能回退 |
|---------|-------------|--------|
| 2 RCU   | 80.84 MiB/s  | 15.6% |
| 4 RCU   | 214.2 MiB/s  | 20.0% |
| 8 RCU   | 365.5 MiB/s  | 28.9% |
| 16 RCU  | 424.6 MiB/s  | 46.7% |

### 仅迁移现有数据

要仅将源数据库的现有数据迁移到 TiDB Cloud，请选择**现有数据迁移**。

你只能使用逻辑模式迁移现有数据。更多信息，请参见[迁移现有数据和增量数据](#迁移现有数据和增量数据)。

### 仅迁移增量数据

要仅将源数据库的增量数据迁移到 TiDB Cloud，请选择**增量数据迁移**。在这种情况下，迁移任务不会将源数据库的现有数据迁移到 TiDB Cloud，而只会迁移迁移任务明确指定的源数据库的持续变更。

有关增量数据迁移的详细说明，请参见[使用数据迁移功能仅迁移增量数据从 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

## 步骤 4：选择要迁移的对象

1. 在**选择要迁移的对象**页面，选择要迁移的对象。你可以点击**全部**选择所有对象，或点击**自定义**然后点击对象名称旁边的复选框来选择对象。

    - 如果你点击**全部**，迁移任务将从整个源数据库实例迁移现有数据到 TiDB Cloud，并在完整迁移后迁移持续变更。请注意，这仅在你在上一步中选择了**现有数据迁移**和**增量数据迁移**复选框时才会发生。
    - 如果你点击**自定义**并选择一些数据库，迁移任务将迁移所选数据库的现有数据并迁移持续变更到 TiDB Cloud。请注意，这仅在你在上一步中选择了**现有数据迁移**和**增量数据迁移**复选框时才会发生。
    - 如果你点击**自定义**并选择数据集名称下的一些表，迁移任务将只迁移所选表的现有数据并迁移持续变更。之后在同一数据库中创建的表不会被迁移。

2. 点击**下一步**。

## 步骤 5：预检查

在**预检查**页面，你可以查看预检查结果。如果预检查失败，你需要根据**失败**或**警告**详情进行操作，然后点击**重新检查**以重新检查。

如果某些检查项只有警告，你可以评估风险并考虑是否忽略警告。如果所有警告都被忽略，迁移任务将自动进入下一步。

有关错误和解决方案的更多信息，请参见[预检查错误和解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#预检查错误和解决方案)。

有关预检查项的更多信息，请参见[迁移任务预检查](https://docs.pingcap.com/tidb/stable/dm-precheck)。

如果所有检查项显示**通过**，点击**下一步**。

## 步骤 6：选择规格并开始迁移

在**选择规格并开始迁移**页面，根据你的性能要求选择适当的迁移规格。有关规格的更多信息，请参见[数据迁移的规格](/tidb-cloud/tidb-cloud-billing-dm.md#数据迁移的规格)。

选择规格后，点击**创建任务并开始**以开始迁移。

## 步骤 7：查看迁移进度

创建迁移任务后，你可以在**迁移任务详情**页面查看迁移进度。迁移进度显示在**阶段和状态**区域。

你可以在迁移任务运行时暂停或删除它。

如果迁移任务失败，你可以在解决问题后恢复它。

你可以在任何状态下删除迁移任务。

如果在迁移过程中遇到任何问题，请参见[迁移错误和解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#迁移错误和解决方案)。

## 扩缩容迁移任务规格

TiDB Cloud 支持扩大或缩小迁移任务规格，以满足不同场景下的性能和成本要求。

不同的迁移规格有不同的性能。你在不同阶段的性能要求也可能不同。例如，在现有数据迁移期间，你希望性能尽可能快，所以选择了一个大规格的迁移任务，如 8 RCU。一旦现有数据迁移完成，增量迁移不需要如此高的性能，所以你可以缩小任务规格，例如从 8 RCU 缩小到 2 RCU，以节省成本。

在扩缩容迁移任务规格时，请注意以下事项：

- 扩缩容迁移任务规格需要大约 5 到 10 分钟。
- 如果扩缩容失败，任务规格将保持与扩缩容前相同。

### 限制

- 只有当任务处于**运行中**或**已暂停**状态时，才能扩缩容迁移任务规格。
- TiDB Cloud 不支持在现有数据导出阶段扩缩容迁移任务规格。
- 扩缩容迁移任务规格将重启任务。如果任务的源表没有主键，可能会插入重复数据。
- 在扩缩容期间，不要清除源数据库的二进制日志或临时增加 MySQL 源数据库的 `expire_logs_days`。否则，由于无法获取连续的二进制日志位置，任务可能会失败。

### 扩缩容程序

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/) 并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

2. 点击目标集群的名称以进入其概览页面，然后在左侧导航栏中点击 **Data** > **Migration**。

3. 在**数据迁移**页面，找到要扩缩容的迁移任务。在**操作**列中，点击 **...** > **扩缩容**。

4. 在**扩缩容**窗口中，选择要使用的新规格，然后点击**提交**。你可以在窗口底部查看新规格的价格。
