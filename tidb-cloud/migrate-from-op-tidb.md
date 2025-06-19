---
title: 从 TiDB 自建集群迁移到 TiDB Cloud
summary: 了解如何将数据从 TiDB 自建集群迁移到 TiDB Cloud。
---

# 从 TiDB 自建集群迁移到 TiDB Cloud

本文档描述了如何通过 Dumpling 和 TiCDC 将数据从 TiDB 自建集群迁移到 TiDB Cloud (AWS)。

整体流程如下：

1. 搭建环境并准备工具。
2. 迁移全量数据。过程如下：
   1. 使用 Dumpling 将数据从 TiDB 自建集群导出到 Amazon S3。
   2. 将数据从 Amazon S3 导入到 TiDB Cloud。
3. 使用 TiCDC 复制增量数据。
4. 验证迁移的数据。

## 前提条件

建议将 S3 存储桶和 TiDB Cloud 集群放在同一区域。跨区域迁移可能会产生额外的数据转换成本。

迁移前，你需要准备以下内容：

- 具有管理员访问权限的 [AWS 账户](https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-up-s3.html#sign-up-for-aws-gsg)
- [AWS S3 存储桶](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- [TiDB Cloud 账户](/tidb-cloud/tidb-cloud-quickstart.md)，至少具有目标 AWS 上 TiDB Cloud 集群的 [`Project Data Access Read-Write`](/tidb-cloud/manage-user-access.md#user-roles) 访问权限

## 准备工具

你需要准备以下工具：

- Dumpling：数据导出工具
- TiCDC：数据复制工具

### Dumpling

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) 是一个将数据从 TiDB 或 MySQL 导出到 SQL 或 CSV 文件的工具。你可以使用 Dumpling 从 TiDB 自建集群导出全量数据。

在部署 Dumpling 之前，请注意以下事项：

- 建议将 Dumpling 部署在与 TiDB Cloud 中的 TiDB 集群位于同一 VPC 的新 EC2 实例上。
- 推荐的 EC2 实例类型是 **c6g.4xlarge**（16 个 vCPU 和 32 GiB 内存）。你可以根据需要选择其他 EC2 实例类型。Amazon Machine Image (AMI) 可以是 Amazon Linux、Ubuntu 或 Red Hat。

你可以通过使用 TiUP 或使用安装包来部署 Dumpling。

#### 使用 TiUP 部署 Dumpling

使用 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview) 部署 Dumpling：

```bash
## 部署 TiUP
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source /root/.bash_profile
## 部署 Dumpling 并更新到最新版本
tiup install dumpling
tiup update --self && tiup update dumpling
```

#### 使用安装包部署 Dumpling

要使用安装包部署 Dumpling：

1. 下载[工具包](https://docs.pingcap.com/tidb/stable/download-ecosystem-tools)。

2. 将其解压到目标机器。你可以通过运行 `tiup install dumpling` 使用 TiUP 获取 Dumpling。之后，你可以使用 `tiup dumpling ...` 运行 Dumpling。更多信息，请参见 [Dumpling 简介](https://docs.pingcap.com/tidb/stable/dumpling-overview#dumpling-introduction)。

#### 配置 Dumpling 的权限

你需要以下权限才能从上游数据库导出数据：

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT
- PROCESS

### 部署 TiCDC

你需要[部署 TiCDC](https://docs.pingcap.com/tidb/dev/deploy-ticdc) 来将增量数据从上游 TiDB 集群复制到 TiDB Cloud。

1. 确认当前 TiDB 版本是否支持 TiCDC。TiDB v4.0.8.rc.1 及更高版本支持 TiCDC。你可以通过在 TiDB 集群中执行 `select tidb_version();` 来检查 TiDB 版本。如果需要升级，请参见[使用 TiUP 升级 TiDB](https://docs.pingcap.com/tidb/dev/deploy-ticdc#upgrade-ticdc-using-tiup)。

2. 向 TiDB 集群添加 TiCDC 组件。请参见[使用 TiUP 向现有 TiDB 集群添加或扩容 TiCDC](https://docs.pingcap.com/tidb/dev/deploy-ticdc#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup)。编辑 `scale-out.yml` 文件以添加 TiCDC：

    ```yaml
    cdc_servers:
    - host: 10.0.1.3
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    - host: 10.0.1.4
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    ```

3. 添加 TiCDC 组件并检查状态。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    tiup cluster display <cluster-name>
    ```

## 迁移全量数据

要将数据从 TiDB 自建集群迁移到 TiDB Cloud，请执行以下全量数据迁移：

1. 将数据从 TiDB 自建集群迁移到 Amazon S3。
2. 将数据从 Amazon S3 迁移到 TiDB Cloud。

### 将数据从 TiDB 自建集群迁移到 Amazon S3

你需要使用 Dumpling 将数据从 TiDB 自建集群迁移到 Amazon S3。

如果你的 TiDB 集群在本地 IDC 中，或者 Dumpling 服务器与 Amazon S3 之间的网络未连接，你可以先将文件导出到本地存储，然后再上传到 Amazon S3。

#### 步骤 1. 暂时禁用上游 TiDB 自建集群的 GC 机制

为确保增量迁移期间不会丢失新写入的数据，你需要在开始迁移之前禁用上游集群的垃圾回收（GC）机制，以防止系统清理历史数据。

运行以下命令验证设置是否成功。

```sql
SET GLOBAL tidb_gc_enable = FALSE;
```

以下是示例输出，其中 `0` 表示已禁用。

```sql
SELECT @@global.tidb_gc_enable;
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.01 sec)
```

#### 步骤 2. 为 Dumpling 配置 Amazon S3 存储桶的访问权限

在 AWS 控制台中创建访问密钥。详细信息请参见[创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

1. 使用你的 AWS 账户 ID 或账户别名、IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam/home#/security_credentials)。

2. 在导航栏右上角，选择你的用户名，然后点击**我的安全凭证**。

3. 要创建访问密钥，点击**创建访问密钥**。然后选择**下载 .csv 文件**将访问密钥 ID 和秘密访问密钥保存到计算机上的 CSV 文件中。将文件存储在安全位置。此对话框关闭后，你将无法再次访问秘密访问密钥。下载 CSV 文件后，选择**关闭**。创建访问密钥时，密钥对默认处于活动状态，你可以立即使用该密钥对。

    ![创建访问密钥](/media/tidb-cloud/op-to-cloud-create-access-key01.png)

    ![下载 CSV 文件](/media/tidb-cloud/op-to-cloud-create-access-key02.png)

#### 步骤 3. 使用 Dumpling 将数据从上游 TiDB 集群导出到 Amazon S3

执行以下操作，使用 Dumpling 将数据从上游 TiDB 集群导出到 Amazon S3：

1. 为 Dumpling 配置环境变量。

    ```shell
    export AWS_ACCESS_KEY_ID=${AccessKey}
    export AWS_SECRET_ACCESS_KEY=${SecretKey}
    ```

2. 从 AWS 控制台获取 S3 存储桶 URI 和区域信息。详细信息请参见[创建存储桶](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。

    以下截图显示如何获取 S3 存储桶 URI 信息：

    ![获取 S3 URI](/media/tidb-cloud/op-to-cloud-copy-s3-uri.png)

    以下截图显示如何获取区域信息：

    ![获取区域信息](/media/tidb-cloud/op-to-cloud-copy-region-info.png)

3. 运行 Dumpling 将数据导出到 Amazon S3 存储桶。

    ```shell
    dumpling \
    -u root \
    -P 4000 \
    -h 127.0.0.1 \
    -r 20000 \
    --filetype {sql|csv}  \
    -F 256MiB  \
    -t 8 \
    -o "${S3 URI}" \
    --s3.region "${s3.region}"
    ```

    `-t` 选项指定导出的线程数。增加线程数可以提高 Dumpling 的并发性和导出速度，但也会增加数据库的内存消耗。因此，不要将此参数设置得太大。

    更多信息，请参见 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-to-sql-files)。

4. 检查导出的数据。通常导出的数据包括以下内容：

    - `metadata`：此文件包含导出的开始时间和主二进制日志的位置。
    - `{schema}-schema-create.sql`：创建 schema 的 SQL 文件
    - `{schema}.{table}-schema.sql`：创建表的 SQL 文件
    - `{schema}.{table}.{0001}.{sql|csv}`：数据文件
    - `*-schema-view.sql`、`*-schema-trigger.sql`、`*-schema-post.sql`：其他导出的 SQL 文件

### 将数据从 Amazon S3 迁移到 TiDB Cloud

将数据从 TiDB 自建集群导出到 Amazon S3 后，你需要将数据迁移到 TiDB Cloud。

1. 在 TiDB Cloud 控制台中获取集群的账户 ID 和外部 ID。更多信息，请参见[步骤 2. 配置 Amazon S3 访问](/tidb-cloud/tidb-cloud-auditing.md#step-2-configure-amazon-s3-access)。

    以下截图显示如何获取账户 ID 和外部 ID：

    ![获取账户 ID 和外部 ID](/media/tidb-cloud/op-to-cloud-get-role-arn.png)

2. 配置 Amazon S3 的访问权限。通常你需要以下只读权限：

    - s3:GetObject
    - s3:GetObjectVersion
    - s3:ListBucket
    - s3:GetBucketLocation

    如果 S3 存储桶使用服务器端加密 SSE-KMS，你还需要添加 KMS 权限。

    - kms:Decrypt

3. 配置访问策略。转到 [AWS 控制台 > IAM > 访问管理 > 策略](https://console.aws.amazon.com/iamv2/home#/policies)，切换到你的区域，检查是否已存在 TiDB Cloud 的访问策略。如果不存在，请按照[在 JSON 选项卡上创建策略](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html)文档创建策略。

    以下是 json 策略的示例模板。

    ```json
    ## 创建 json 策略模板
    ##<Your customized directory>：填写 S3 存储桶中要导入的数据文件所在文件夹的路径。
    ##<Your S3 bucket ARN>：填写 S3 存储桶的 ARN。你可以在 S3 存储桶概览页面上点击复制 ARN 按钮获取。
    ##<Your AWS KMS ARN>：填写 S3 存储桶 KMS 密钥的 ARN。你可以从 S3 存储桶 > 属性 > 默认加密 > AWS KMS 密钥 ARN 获取。更多信息，请参见 https://docs.aws.amazon.com/AmazonS3/latest/userguide/viewing-bucket-key-settings.html

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<Your customized directory>"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": "<Your S3 bucket ARN>"
            }
            // 如果你为 S3 存储桶启用了 SSE-KMS，则需要添加以下权限。
            {
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "<Your AWS KMS ARN>"
            }
            ,
            {
                "Effect": "Allow",
                "Action": "kms:Decrypt",
                "Resource": "<Your AWS KMS ARN>"
            }
        ]
    }
    ```

4. 配置角色。请参见[创建 IAM 角色（控制台）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html)。在账户 ID 字段中，输入你在步骤 1 中记下的 TiDB Cloud 账户 ID 和 TiDB Cloud 外部 ID。

5. 获取 Role-ARN。转到 [AWS 控制台 > IAM > 访问管理 > 角色](https://console.aws.amazon.com/iamv2/home#/roles)。切换到你的区域。点击你创建的角色，并记下 ARN。在将数据导入 TiDB Cloud 时，你将使用它。

6. 将数据导入 TiDB Cloud。请参见[从云存储将 CSV 文件导入到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

## 复制增量数据

要复制增量数据，请执行以下操作：

1. 获取增量数据迁移的开始时间。例如，你可以从全量数据迁移的元数据文件中获取。

    ![元数据中的开始时间](/media/tidb-cloud/start_ts_in_metadata.png)

2. 授予 TiCDC 连接 TiDB Cloud 的权限。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)中，导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。
    2. 在左侧导航栏中，点击**设置** > **网络**。
    3. 在**网络**页面上，点击**添加 IP 地址**。
    4. 在显示的对话框中，选择**使用 IP 地址**，点击 **+**，在 **IP 地址**字段中填入 TiCDC 组件的公网 IP 地址，然后点击**确认**。现在 TiCDC 可以访问 TiDB Cloud。更多信息，请参见[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

3. 获取下游 TiDB Cloud 集群的连接信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)中，导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。
    2. 点击右上角的**连接**。
    3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，从**连接方式**下拉列表中选择**通用**。
    4. 从连接信息中，你可以获取集群的主机 IP 地址和端口。更多信息，请参见[通过公共连接连接](/tidb-cloud/connect-via-standard-connection.md)。

4. 创建并运行增量复制任务。在上游集群中运行以下命令：

    ```shell
    tiup cdc cli changefeed create \
    --pd=http://172.16.6.122:2379  \
    --sink-uri="tidb://root:123456@172.16.6.125:4000"  \
    --changefeed-id="upstream-to-downstream"  \
    --start-ts="431434047157698561"
    ```

    - `--pd`：上游集群的 PD 地址。格式为：`[upstream_pd_ip]:[pd_port]`
    - `--sink-uri`：复制任务的下游地址。根据以下格式配置 `--sink-uri`。目前，scheme 支持 `mysql`、`tidb`、`kafka`、`s3` 和 `local`。

        ```shell
        [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
        ```

    - `--changefeed-id`：复制任务的 ID。格式必须匹配 ^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$ 正则表达式。如果未指定此 ID，TiCDC 会自动生成一个 UUID（版本 4 格式）作为 ID。
    - `--start-ts`：指定 changefeed 的起始 TSO。从此 TSO 开始，TiCDC 集群开始拉取数据。默认值为当前时间。

    更多信息，请参见 [TiCDC Changefeeds 的 CLI 和配置参数](https://docs.pingcap.com/tidb/dev/ticdc-changefeed-config)。

5. 在上游集群中重新启用 GC 机制。如果增量复制中没有发现错误或延迟，请启用 GC 机制以恢复集群的垃圾回收。

    运行以下命令验证设置是否生效。

    ```sql
    SET GLOBAL tidb_gc_enable = TRUE;
    ```

    以下是示例输出，其中 `1` 表示 GC 已禁用。

    ```sql
    SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.01 sec)
    ```

6. 验证增量复制任务。

    - 如果输出中显示 "Create changefeed successfully!"，则复制任务创建成功。
    - 如果状态为 `normal`，则复制任务正常。

        ```shell
         tiup cdc cli changefeed list --pd=http://172.16.6.122:2379
        ```

        ![更新过滤器](/media/tidb-cloud/normal_status_in_replication_task.png)

    - 验证复制。向上游集群写入新记录，然后检查记录是否复制到下游 TiDB Cloud 集群。

7. 为上游和下游集群设置相同的时区。默认情况下，TiDB Cloud 将时区设置为 UTC。如果上游和下游集群之间的时区不同，你需要为两个集群设置相同的时区。

    1. 在上游集群中，运行以下命令检查时区：

        ```sql
        SELECT @@global.time_zone;
        ```

    2. 在下游集群中，运行以下命令设置时区：

        ```sql
        SET GLOBAL time_zone = '+08:00';
        ```

    3. 再次检查时区以验证设置：

        ```sql
        SELECT @@global.time_zone;
        ```

8. 备份上游集群中的[查询绑定](/sql-plan-management.md)并在下游集群中恢复它们。你可以使用以下查询备份查询绑定：

    ```sql
    SELECT DISTINCT(CONCAT('CREATE GLOBAL BINDING FOR ', original_sql,' USING ', bind_sql,';')) FROM mysql.bind_info WHERE status='enabled';
    ```

    如果没有得到任何输出，上游集群中可能没有使用查询绑定。在这种情况下，你可以跳过此步骤。

    获取查询绑定后，在下游集群中运行它们以恢复查询绑定。

9. 备份上游集群中的用户和权限信息，并在下游集群中恢复它们。你可以使用以下脚本备份用户和权限信息。注意需要将占位符替换为实际值。

    ```shell
    #!/bin/bash

    export MYSQL_HOST={tidb_op_host}
    export MYSQL_TCP_PORT={tidb_op_port}
    export MYSQL_USER=root
    export MYSQL_PWD={root_password}
    export MYSQL="mysql -u${MYSQL_USER} --default-character-set=utf8mb4"
    
    function backup_user_priv(){
        ret=0
        sql="SELECT CONCAT(user,':',host,':',authentication_string) FROM mysql.user WHERE user NOT IN ('root')"
        for usr in `$MYSQL -se "$sql"`;do
            u=`echo $usr | awk -F ":" '{print $1}'`
            h=`echo $usr | awk -F ":" '{print $2}'`
            p=`echo $usr | awk -F ":" '{print $3}'`
            echo "-- Grants for '${u}'@'${h}';"
            [[ ! -z "${p}" ]] && echo "CREATE USER IF NOT EXISTS '${u}'@'${h}' IDENTIFIED WITH 'mysql_native_password' AS '${p}' ;"
            $MYSQL -se "SHOW GRANTS FOR '${u}'@'${h}';" | sed 's/$/;/g'
            [ $? -ne 0 ] && ret=1 && break
        done
        return $ret
    }
    
    backup_user_priv
    ```
    
    获取用户和权限信息后，在下游集群中运行生成的 SQL 语句以恢复用户和权限信息。
