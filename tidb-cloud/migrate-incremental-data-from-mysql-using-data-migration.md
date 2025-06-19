---
title: 使用数据迁移功能从 MySQL 兼容数据库仅迁移增量数据到 TiDB Cloud
summary: 了解如何使用数据迁移功能将 Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL 或本地 MySQL 实例中的增量数据迁移到 TiDB Cloud。
---

# 使用数据迁移功能从 MySQL 兼容数据库仅迁移增量数据到 TiDB Cloud

本文档介绍如何使用 TiDB Cloud 控制台的数据迁移功能，将云服务商（Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL 或 Azure Database for MySQL）或自托管源数据库中的增量数据迁移到 TiDB Cloud。

关于如何迁移现有数据或同时迁移现有数据和增量数据的说明，请参见[使用数据迁移功能将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 限制

> **注意：**
>
> 本节仅包含增量数据迁移的限制。建议你同时阅读通用限制。参见[限制](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations)。

- 如果目标数据库中尚未创建目标表，迁移任务将报告以下错误并失败。在这种情况下，你需要手动创建目标表，然后重试迁移任务。

    ```sql
    startLocation: [position: (mysql_bin.000016, 5122), gtid-set:
    00000000-0000-0000-0000-00000000000000000], endLocation:
    [position: (mysql_bin.000016, 5162), gtid-set: 0000000-0000-0000
    0000-0000000000000:0]: cannot fetch downstream table schema of
    zm`.'table1' to initialize upstream schema 'zm'.'table1' in sschema
    tracker Raw Cause: Error 1146: Table 'zm.table1' doesn't exist
    ```

- 如果上游删除或更新了某些行，而下游没有相应的行，迁移任务在从上游复制 `DELETE` 和 `UPDATE` DML 操作时会检测到没有可供删除或更新的行。

如果你指定 GTID 作为迁移增量数据的起始位置，请注意以下限制：

- 确保源数据库已启用 GTID 模式。
- 如果源数据库是 MySQL，MySQL 版本必须是 5.6 或更高版本，存储引擎必须是 InnoDB。
- 如果迁移任务连接到上游的从库，则无法迁移 `REPLICATE CREATE TABLE ... SELECT` 事件。这是因为该语句会被拆分为两个事务（`CREATE TABLE` 和 `INSERT`），它们被分配了相同的 GTID。因此，从库会忽略 `INSERT` 语句。

## 前提条件

> **注意：**
>
> 本节仅包含增量数据迁移的前提条件。建议你同时阅读[通用前提条件](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites)。

如果你想使用 GTID 指定起始位置，请确保源数据库已启用 GTID。操作因数据库类型而异。

### 对于 Amazon RDS 和 Amazon Aurora MySQL

对于 Amazon RDS 和 Amazon Aurora MySQL，你需要创建一个新的可修改参数组（即非默认参数组），然后修改参数组中的以下参数并重启实例应用。

- `gtid_mode`
- `enforce_gtid_consistency`

你可以通过执行以下 SQL 语句来检查 GTID 模式是否已成功启用：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果是 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功启用。

更多信息，请参见 [Parameters for GTID-based replication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters)。

### 对于 Google Cloud SQL for MySQL

Google Cloud SQL for MySQL 默认启用 GTID 模式。你可以通过执行以下 SQL 语句来检查 GTID 模式是否已成功启用：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果是 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功启用。

### 对于 Azure Database for MySQL

Azure Database for MySQL（5.7 及更高版本）默认启用 GTID 模式。你可以通过执行以下 SQL 语句来检查 GTID 模式是否已成功启用：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果是 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功启用。

此外，确保 `binlog_row_image` 服务器参数设置为 `FULL`。你可以通过执行以下 SQL 语句来检查：

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

如果结果不是 `FULL`，你需要使用 [Azure 门户](https://portal.azure.com/)或 [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) 为你的 Azure Database for MySQL 实例配置此参数。

### 对于自托管 MySQL 实例

> **注意：**
>
> 具体步骤和命令可能因 MySQL 版本和配置而异。确保你了解启用 GTID 的影响，并在执行此操作之前在非生产环境中进行适当的测试和验证。

要为自托管 MySQL 实例启用 GTID 模式，请按照以下步骤操作：

1. 使用具有适当权限的 MySQL 客户端连接到 MySQL 服务器。

2. 执行以下 SQL 语句以启用 GTID 模式：

    ```sql
    -- 启用 GTID 模式
    SET GLOBAL gtid_mode = ON;

    -- 启用 `enforce_gtid_consistency`
    SET GLOBAL enforce_gtid_consistency = ON;

    -- 重新加载 GTID 配置
    RESET MASTER;
    ```

3. 重启 MySQL 服务器以确保配置更改生效。

4. 通过执行以下 SQL 语句检查 GTID 模式是否已成功启用：

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    如果结果是 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功启用。

## 步骤 1：进入数据迁移页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **迁移**。

3. 在**数据迁移**页面，点击右上角的**创建迁移任务**。此时会显示**创建迁移任务**页面。

## 步骤 2：配置源和目标连接

在**创建迁移任务**页面，配置源和目标连接。

1. 输入任务名称，必须以字母开头，且长度不超过 60 个字符。可以使用字母（A-Z、a-z）、数字（0-9）、下划线（_）和连字符（-）。

2. 填写源连接配置。

   - **数据源**：数据源类型。
   - **区域**：数据源的区域，仅云数据库需要。
   - **连接方式**：数据源的连接方式。目前，你可以根据你的连接方式选择公共 IP、VPC 对等连接或 Private Link。
   - **主机名或 IP 地址**（适用于公共 IP 和 VPC 对等连接）：数据源的主机名或 IP 地址。
   - **服务名称**（适用于 Private Link）：端点服务名称。
   - **端口**：数据源的端口。
   - **用户名**：数据源的用户名。
   - **密码**：用户名的密码。
   - **SSL/TLS**：如果启用 SSL/TLS，你需要上传数据源的证书，包括以下任意一项：
        - 仅 CA 证书
        - 客户端证书和客户端密钥
        - CA 证书、客户端证书和客户端密钥

3. 填写目标连接配置。

   - **用户名**：输入 TiDB Cloud 中目标集群的用户名。
   - **密码**：输入 TiDB Cloud 用户名的密码。

4. 点击**验证连接并继续**以验证你输入的信息。

5. 根据你看到的消息采取行动：

    - 如果使用公共 IP 或 VPC 对等连接，你需要将数据迁移服务的 IP 地址添加到源数据库的 IP 访问列表和防火墙（如果有）中。
    - 如果使用 AWS Private Link，系统会提示你接受端点请求。转到 [AWS VPC 控制台](https://us-west-2.console.aws.amazon.com/vpc/home)，点击**端点服务**以接受端点请求。

## 步骤 3：选择迁移任务类型

要仅将源数据库的增量数据迁移到 TiDB Cloud，请选择**增量数据迁移**，不要选择**现有数据迁移**。这样，迁移任务只会将源数据库的持续变更迁移到 TiDB Cloud。

在**起始位置**区域，你可以为增量数据迁移指定以下类型的起始位置之一：

- 增量迁移任务开始的时间
- GTID
- Binlog 文件名和位置

迁移任务开始后，你无法更改起始位置。

### 增量迁移任务开始的时间

如果选择此选项，迁移任务将只迁移迁移任务开始后在源数据库中生成的增量数据。

### 指定 GTID

选择此选项以指定源数据库的 GTID，例如 `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23`。迁移任务将复制不包含指定 GTID 集的事务，以将源数据库的持续变更迁移到 TiDB Cloud。

你可以运行以下命令来检查源数据库的 GTID：

```sql
SHOW MASTER STATUS;
```

有关如何启用 GTID 的信息，请参见[前提条件](#前提条件)。

### 指定 binlog 文件名和位置

选择此选项以指定源数据库的 binlog 文件名（例如 `binlog.000001`）和 binlog 位置（例如 `1307`）。迁移任务将从指定的 binlog 文件名和位置开始，将源数据库的持续变更迁移到 TiDB Cloud。

你可以运行以下命令来检查源数据库的 binlog 文件名和位置：

```sql
SHOW MASTER STATUS;
```

如果目标数据库中有数据，请确保 binlog 位置正确。否则，现有数据和增量数据之间可能会发生冲突。如果发生冲突，迁移任务将失败。如果你想用源数据库中的数据替换冲突的记录，可以恢复迁移任务。

## 步骤 4：选择要迁移的对象

1. 在**选择要迁移的对象**页面，选择要迁移的对象。你可以点击**全部**选择所有对象，或点击**自定义**，然后点击对象名称旁边的复选框选择对象。

2. 点击**下一步**。

## 步骤 5：预检查

在**预检查**页面，你可以查看预检查结果。如果预检查失败，你需要根据**失败**或**警告**详情进行操作，然后点击**重新检查**以重新检查。

如果某些检查项只有警告，你可以评估风险并考虑是否忽略警告。如果所有警告都被忽略，迁移任务将自动进入下一步。

有关错误和解决方案的更多信息，请参见[预检查错误和解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)。

有关预检查项的更多信息，请参见[迁移任务预检查](https://docs.pingcap.com/tidb/stable/dm-precheck)。

如果所有检查项都显示**通过**，点击**下一步**。

## 步骤 6：选择规格并开始迁移

在**选择规格并开始迁移**页面，根据你的性能要求选择适当的迁移规格。有关规格的更多信息，请参见[数据迁移的规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

选择规格后，点击**创建任务并开始**以开始迁移。

## 步骤 7：查看迁移进度

创建迁移任务后，你可以在**迁移任务详情**页面查看迁移进度。迁移进度显示在**阶段和状态**区域。

你可以在迁移任务运行时暂停或删除它。

如果迁移任务失败，你可以在解决问题后恢复它。

你可以在任何状态下删除迁移任务。

如果在迁移过程中遇到任何问题，请参见[迁移错误和解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)。
