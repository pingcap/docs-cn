---
title: 将大规模 MySQL 分片数据迁移和合并到 TiDB Cloud
summary: 了解如何将大规模 MySQL 分片数据迁移和合并到 TiDB Cloud。
---

# 将大规模 MySQL 分片数据迁移和合并到 TiDB Cloud

本文档介绍如何将大规模 MySQL 数据集（例如，超过 1 TiB）从不同分区迁移到 TiDB Cloud。完成全量数据迁移后，你可以根据业务需求使用 [TiDB Data Migration (DM)](https://docs.pingcap.com/tidb/stable/dm-overview) 执行增量迁移。

本文档中的示例使用了跨多个 MySQL 实例的复杂分片迁移任务，并涉及处理自增主键的冲突。本示例中的场景也适用于合并单个 MySQL 实例中不同分片表的数据。

## 示例环境信息

本节描述示例中使用的上游集群、DM 和下游集群的基本信息。

### 上游集群

上游集群的环境信息如下：

- MySQL 版本：MySQL v5.7.18
- MySQL 实例 1：
    - schema `store_01` 和表 `[sale_01, sale_02]`
    - schema `store_02` 和表 `[sale_01, sale_02]`
- MySQL 实例 2：
    - schema `store_01` 和表 `[sale_01, sale_02]`
    - schema `store_02` 和表 `[sale_01, sale_02]`
- 表结构：

  ```sql
  CREATE TABLE sale_01 (
  id bigint(20) NOT NULL auto_increment,
  uid varchar(40) NOT NULL,
  sale_num bigint DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY ind_uid (uid)
  );
  ```

### DM

DM 的版本是 v5.3.0。你需要手动部署 TiDB DM。详细步骤，请参见[使用 TiUP 部署 DM 集群](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

### 外部存储

本文档以 Amazon S3 为例。

### 下游集群

分片的 schema 和表被合并到表 `store.sales` 中。
## 从 MySQL 到 TiDB Cloud 执行全量数据迁移

以下是将 MySQL 分片的全量数据迁移和合并到 TiDB Cloud 的步骤。

在以下示例中，你只需要将表中的数据导出为 **CSV** 格式。

### 步骤 1. 在 Amazon S3 存储桶中创建目录

在 Amazon S3 存储桶中创建一个一级目录 `store`（对应数据库级别）和一个二级目录 `sales`（对应表级别）。在 `sales` 中，为每个 MySQL 实例创建一个三级目录（对应 MySQL 实例级别）。例如：

- 将 MySQL 实例 1 中的数据迁移到 `s3://dumpling-s3/store/sales/instance01/`
- 将 MySQL 实例 2 中的数据迁移到 `s3://dumpling-s3/store/sales/instance02/`

如果有跨多个实例的分片，你可以为每个数据库创建一个一级目录，为每个分片表创建一个二级目录。然后为每个 MySQL 实例创建一个三级目录，以便于管理。例如，如果你想将 MySQL 实例 1 和 MySQL 实例 2 中的表 `stock_N.product_N` 迁移和合并到 TiDB Cloud 中的表 `stock.products`，你可以创建以下目录：

- `s3://dumpling-s3/stock/products/instance01/`
- `s3://dumpling-s3/stock/products/instance02/`

### 步骤 2. 使用 Dumpling 将数据导出到 Amazon S3

有关如何安装 Dumpling 的信息，请参见 [Dumpling 简介](https://docs.pingcap.com/tidb/stable/dumpling-overview)。

使用 Dumpling 将数据导出到 Amazon S3 时，请注意以下事项：

- 为上游集群启用 binlog。
- 选择正确的 Amazon S3 目录和区域。
- 通过配置 `-t` 选项选择适当的并发度，以最小化对上游集群的影响，或直接从备份数据库导出。有关如何使用此参数的更多信息，请参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。
- 为 `--filetype csv` 和 `--no-schemas` 设置适当的值。有关如何使用这些参数的更多信息，请参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。

CSV 文件的命名规则如下：

- 如果一个表的数据被分成多个 CSV 文件，在这些 CSV 文件后面添加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续但必须按升序排列。你还需要在数字前添加额外的零，以确保所有后缀的长度相同。

> **注意：**
>
> 如果在某些情况下无法按照上述规则更新 CSV 文件名（例如，CSV 文件链接也被其他程序使用），你可以保持文件名不变，并在[步骤 5](#步骤-5-执行数据导入任务) 中使用**映射设置**将源数据导入到单个目标表。

要将数据导出到 Amazon S3，请执行以下操作：

1. 获取 Amazon S3 存储桶的 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`。

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2. 将数据从 MySQL 实例 1 导出到 Amazon S3 存储桶中的 `s3://dumpling-s3/store/sales/instance01/` 目录。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    有关参数的更多信息，请参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。

3. 将数据从 MySQL 实例 2 导出到 Amazon S3 存储桶中的 `s3://dumpling-s3/store/sales/instance02/` 目录。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

详细步骤，请参见[导出数据到 Amazon S3 云存储](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage)。

### 步骤 3. 在 TiDB Cloud 集群中创建 schema

按照以下步骤在 TiDB Cloud 集群中创建 schema：

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

在本示例中，上游表 `sale_01` 和 `sale_02` 的列 ID 是自增主键。在下游数据库中合并分片表时可能会发生冲突。执行以下 SQL 语句将 ID 列设置为普通索引而不是主键：

```sql
mysql> CREATE TABLE `sales` (
         `id` bigint(20) NOT NULL ,
         `uid` varchar(40) NOT NULL,
         `sale_num` bigint DEFAULT NULL,
         INDEX (`id`),
         UNIQUE KEY `ind_uid` (`uid`)
        );
Query OK, 0 rows affected (0.17 sec)
```

有关解决此类冲突的解决方案，请参见[移除列的 PRIMARY KEY 属性](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column)。
### 步骤 4. 配置 Amazon S3 访问

按照[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)中的说明获取访问源数据的角色 ARN。

以下示例仅列出关键策略配置。请将 Amazon S3 路径替换为你自己的值。

```yaml
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Sid": "VisualEditor0",
           "Effect": "Allow",
           "Action": [
               "s3:GetObject",
               "s3:GetObjectVersion"
           ],
           "Resource": [
               "arn:aws:s3:::dumpling-s3/*"
           ]
       },
       {
           "Sid": "VisualEditor1",
           "Effect": "Allow",
           "Action": [
               "s3:ListBucket",
               "s3:GetBucketLocation"
           ],

           "Resource": "arn:aws:s3:::dumpling-s3"
       }
   ]
}
```

### 步骤 5. 执行数据导入任务

配置 Amazon S3 访问后，你可以在 TiDB Cloud 控制台中执行数据导入任务，步骤如下：

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**，然后点击 **Amazon S3**。

3. 在**从 Amazon S3 导入数据**页面，填写以下信息：

    - **导入文件数量**：对于 TiDB Cloud Serverless，选择**多个文件**。TiDB Cloud Dedicated 中不提供此字段。
    - **包含 Schema 文件**：选择**否**。
    - **数据格式**：选择 **CSV**。
    - **文件夹 URI**：填写源数据的存储桶 URI。你可以使用对应表的二级目录，本例中为 `s3://dumpling-s3/store/sales/`，这样 TiDB Cloud 可以一次性将所有 MySQL 实例中的数据导入并合并到 `store.sales` 中。
    - **存储桶访问** > **AWS Role ARN**：输入你获取的 Role-ARN。

    如果存储桶的位置与你的集群不同，请确认跨区域合规性。

    TiDB Cloud 开始验证是否可以访问指定存储桶 URI 中的数据。验证后，TiDB Cloud 会使用默认的文件命名模式尝试扫描数据源中的所有文件，并在下一页的左侧返回扫描摘要结果。如果遇到 `AccessDenied` 错误，请参见[排查从 S3 导入数据时的访问被拒绝错误](/tidb-cloud/troubleshoot-import-access-denied-error.md)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，数据源文件将使用提供的自定义映射规则重新扫描。

    在**源文件 URI 和名称**中输入源文件 URI 和名称时，确保其格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://sampledata/ingest/TableName.01.csv`。

    你也可以使用通配符来匹配源文件。例如：

    - `s3://[bucket_name]/[data_source_folder]/my-data?.csv`：该文件夹中以 `my-data` 开头后跟一个字符的所有 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）将被导入到同一个目标表中。

    - `s3://[bucket_name]/[data_source_folder]/my-data*.csv`：该文件夹中以 `my-data` 开头的所有 CSV 文件将被导入到同一个目标表中。

    注意，仅支持 `?` 和 `*` 通配符。

    > **注意：**
    >
    > URI 必须包含数据源文件夹。

6. 如果需要，编辑 CSV 配置。

    你也可以点击**编辑 CSV 配置**来配置反斜杠转义、分隔符和定界符，以实现更精细的控制。

    > **注意：**
    >
    > 对于分隔符、定界符和空值的配置，你可以使用字母数字字符和某些特殊字符。支持的特殊字符包括 `\t`、`\b`、`\n`、`\r`、`\f` 和 `\u0001`。

7. 点击**开始导入**。

8. 当导入进度显示**已完成**时，检查导入的表。

数据导入后，如果你想移除 TiDB Cloud 的 Amazon S3 访问权限，只需删除你添加的策略即可。
## 从 MySQL 到 TiDB Cloud 执行增量数据复制

要基于 binlog 从上游集群的指定位置复制数据变更到 TiDB Cloud，你可以使用 TiDB Data Migration (DM) 执行增量复制。

### 开始之前

如果你想迁移增量数据并合并 MySQL 分片到 TiDB Cloud，你需要手动部署 TiDB DM，因为 TiDB Cloud 目前不支持迁移和合并 MySQL 分片。详细步骤，请参见[使用 TiUP 部署 DM 集群](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

### 步骤 1. 添加数据源

1. 创建一个新的数据源文件 `dm-source1.yaml` 以将上游数据源配置到 DM 中。添加以下内容：

    ```yaml
    # MySQL 配置。
    source-id: "mysql-replica-01"
    # 指定 DM-worker 是否使用 GTID（全局事务标识符）拉取 binlog。
    # 前提是你已经在上游 MySQL 中启用了 GTID。
    # 如果你已经配置上游数据库服务在不同节点之间自动切换主节点，则必须启用 GTID。
    enable-gtid: true
    from:
     host: "${host}"           # 例如：192.168.10.101
     user: "user01"
     password: "${password}"   # 支持明文密码，但不推荐。建议使用 dmctl encrypt 加密明文密码。
     port: ${port}             # 例如：3307
    ```

2. 创建另一个新的数据源文件 `dm-source2.yaml`，并添加以下内容：

    ```yaml
    # MySQL 配置。
    source-id: "mysql-replica-02"
    # 指定 DM-worker 是否使用 GTID（全局事务标识符）拉取 binlog。
    # 前提是你已经在上游 MySQL 中启用了 GTID。
    # 如果你已经配置上游数据库服务在不同节点之间自动切换主节点，则必须启用 GTID。
    enable-gtid: true
    from:
     host: "192.168.10.102"
     user: "user02"
     password: "${password}"
     port: 3308
    ```

3. 在终端中运行以下命令。使用 `tiup dmctl` 将第一个数据源配置加载到 DM 集群中：

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    上述命令中使用的参数说明如下：

    |参数              |说明    |
    |-                      |-              |
    |`--master-addr`        |要连接的 DM 集群中任一 DM-master 节点的 `{advertise-addr}`。例如：192.168.11.110:9261|
    |`operate-source create`|将数据源加载到 DM 集群。|

    以下是示例输出：

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source1.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262"
           }
       ]
    }

    ```

4. 在终端中运行以下命令。使用 `tiup dmctl` 将第二个数据源配置加载到 DM 集群中：

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    以下是示例输出：

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262"
           }
       ]
    }
    ```
### 步骤 2. 创建复制任务

1. 为复制任务创建一个 `test-task1.yaml` 文件。

2. 在 Dumpling 导出的 MySQL 实例 1 的元数据文件中找到起始点。例如：

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3. 在 Dumpling 导出的 MySQL 实例 2 的元数据文件中找到起始点。例如：

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4. 编辑任务配置文件 `test-task1`，为每个数据源配置增量复制模式和复制起始点。

    ```yaml
    ## ********* 任务配置 *********
    name: test-task1
    shard-mode: "pessimistic"
    # 任务模式。"incremental" 模式仅执行增量数据迁移。
    task-mode: incremental
    # timezone: "UTC"

    ## ******** 数据源配置 **********
    ## （可选）如果你需要增量复制已经在全量数据迁移中迁移的数据，则需要启用安全模式以避免增量数据迁移错误。
    ##  这种情况在以下场景中很常见：全量迁移数据不属于数据源的一致性快照，之后 DM 从早于全量迁移的位置开始复制增量数据。
    syncers:           # 同步处理单元的运行配置。
     global:           # 配置名称。
       safe-mode: false # # 如果此字段设置为 true，DM 会将数据源的 INSERT 更改为目标数据库的 REPLACE，
                        # # 并将数据源的 UPDATE 更改为目标数据库的 DELETE 和 REPLACE。
                        # # 这是为了确保当表结构包含主键或唯一索引时，DML 语句可以重复导入。
                        # # 在启动或恢复增量迁移任务的第一分钟，DM 会自动启用安全模式。
    mysql-instances:
    - source-id: "mysql-replica-01"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000002"
         binlog-pos: 246546174
         binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801"
    - source-id: "mysql-replica-02"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000001"
         binlog-pos: 1312659
         binlog-gtid: "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036"

    ## ******** TiDB Cloud 上目标 TiDB 集群的配置 **********
    target-database:       # TiDB Cloud 上的目标 TiDB 集群
     host: "tidb.xxxxxxx.xxxxxxxxx.ap-northeast-1.prod.aws.tidbcloud.com"
     port: 4000
     user: "root"
     password: "${password}"  # 如果密码不为空，建议使用 dmctl 加密的密文。

    ## ******** 功能配置 **********
    routes:
     store-route-rule:
       schema-pattern: "store_*"
       target-schema: "store"
     sale-route-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       target-schema: "store"
       target-table:  "sales"
    filters:
     sale-filter-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       events: ["truncate table", "drop table", "delete"]
       action: Ignore
     store-filter-rule:
       schema-pattern: "store_*"
       events: ["drop database"]
       action: Ignore
    block-allow-list:
     bw-rule-1:
       do-dbs: ["store_*"]

    ## ******** 忽略检查项 **********
    ignore-checking-items: ["table_schema","auto_increment_ID"]
    ```

有关详细的任务配置，请参见 [DM 任务配置](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)。

为了使数据复制任务顺利运行，DM 会在任务开始时自动触发预检查并返回检查结果。DM 仅在预检查通过后才开始复制。要手动触发预检查，请运行 check-task 命令：

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

以下是示例输出：

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### 步骤 3. 启动复制任务

使用 `tiup dmctl` 运行以下命令来启动数据复制任务：

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

上述命令中使用的参数说明如下：

|参数              |说明    |
|-                      |-              |
|`--master-addr`        |要连接的 DM 集群中任一 DM-master 节点的 `{advertise-addr}`。例如：192.168.11.110:9261|
|`start-task`           |启动迁移任务。|

以下是示例输出：

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 start-task dm-task.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-192.168.11.111-9262"
       },

       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-192.168.11.112-9262"
       }
   ],
   "checkResult": ""
}
```

如果任务启动失败，请检查提示消息并修复配置。之后，你可以重新运行上述命令来启动任务。

如果遇到任何问题，请参考 [DM 错误处理](https://docs.pingcap.com/tidb/stable/dm-error-handling) 和 [DM 常见问题](https://docs.pingcap.com/tidb/stable/dm-faq)。

### 步骤 4. 检查复制任务状态

要了解 DM 集群是否有正在进行的复制任务并查看任务状态，请使用 `tiup dmctl` 运行 `query-status` 命令：

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

以下是示例输出：

```shell
{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262",
               "result": null,
               "relayStatus": null
           },

           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "4048",
                       "totalTps": "3",
                       "recentTps": "3",
                       "masterBinlog": "(mysql-bin.000002, 246550002)",
                       "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "syncerBinlog": "(mysql-bin.000002, 246550002)",
                       "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       },
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262",
               "result": null,
               "relayStatus": null
           },
           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "33",
                       "totalTps": "0",
                       "recentTps": "0",
                       "masterBinlog": "(mysql-bin.000001, 1316487)",
                       "masterBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "syncerBinlog": "(mysql-bin.000001, 1316487)",
                       "syncerBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       }
   ]
}
```

有关结果的详细解释，请参见[查询状态](https://docs.pingcap.com/tidb/stable/dm-query-status)。
