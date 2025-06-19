---
title: 配置 TiDB Cloud Serverless 外部存储访问
summary: 了解如何配置 Amazon Simple Storage Service (Amazon S3) 访问。
---

# 配置 TiDB Cloud Serverless 的外部存储访问

如果你想在 TiDB Cloud Serverless 集群中从外部存储导入数据或将数据导出到外部存储，你需要配置跨账户访问。本文档描述了如何为 TiDB Cloud Serverless 集群配置外部存储访问。

如果你需要为 TiDB Cloud Dedicated 集群配置这些外部存储，请参见[配置 TiDB Cloud Dedicated 的外部存储访问](/tidb-cloud/dedicated-external-storage.md)。

## 配置 Amazon S3 访问

要允许 TiDB Cloud Serverless 集群访问你的 Amazon S3 存储桶中的源数据，请使用以下任一方法为集群配置存储桶访问：

- [使用角色 ARN](#使用角色-arn-配置-amazon-s3-访问)：使用角色 ARN 访问你的 Amazon S3 存储桶。
- [使用 AWS 访问密钥](#使用-aws-访问密钥配置-amazon-s3-访问)：使用 IAM 用户的访问密钥访问你的 Amazon S3 存储桶。

### 使用角色 ARN 配置 Amazon S3 访问

建议你使用 [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) 创建角色 ARN。按照以下步骤创建：

> **注意：**
>
> 角色 ARN 访问 Amazon S3 仅支持云提供商为 AWS 的集群。如果你使用其他云提供商，请改用 AWS 访问密钥。更多信息，请参见[使用 AWS 访问密钥配置 Amazon S3 访问](#使用-aws-访问密钥配置-amazon-s3-访问)。

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/) 并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    2. 点击目标集群的名称以进入其概览页面，然后在左侧导航栏中点击 **Data** > **Import**。

2. 打开**添加新 ARN**对话框。

    - 如果你想从 Amazon S3 导入数据，按以下步骤打开**添加新 ARN**对话框：

        1. 点击**从 S3 导入**。
        2. 填写**文件 URI**字段。
        3. 选择 **AWS Role ARN** 并点击**点击此处使用 AWS CloudFormation 创建新的**。

    - 如果你想将数据导出到 Amazon S3，按以下步骤打开**添加新 ARN**对话框：

        1. 点击**导出数据到...** > **Amazon S3**。如果你的集群之前从未导入或导出过任何数据，请点击页面底部的**点击此处导出数据到...** > **Amazon S3**。
        2. 填写**文件夹 URI**字段。
        3. 选择 **AWS Role ARN** 并点击**点击此处使用 AWS CloudFormation 创建新的**。

3. 使用 AWS CloudFormation 模板创建角色 ARN。

    1. 在**添加新 ARN**对话框中，点击 **AWS Console with CloudFormation Template**。

    2. 登录 [AWS 管理控制台](https://console.aws.amazon.com)，你将被重定向到 AWS CloudFormation **快速创建堆栈**页面。

    3. 填写**角色名称**。

    4. 确认创建新角色并点击**创建堆栈**以创建角色 ARN。

    5. CloudFormation 堆栈执行完成后，你可以点击**输出**选项卡，在**值**列中找到角色 ARN 值。

        ![img.png](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

如果你在使用 AWS CloudFormation 创建角色 ARN 时遇到任何问题，可以按照以下步骤手动创建：

<details>
<summary>点击此处查看详细信息</summary>

1. 在前面说明中描述的**添加新 ARN**对话框中，点击**遇到问题？手动创建角色 ARN**。你将获得 **TiDB Cloud 账户 ID** 和 **TiDB Cloud 外部 ID**。

2. 在 AWS 管理控制台中，为你的 Amazon S3 存储桶创建托管策略。

    1. 登录 [AWS 管理控制台](https://console.aws.amazon.com/) 并打开 [Amazon S3 控制台](https://console.aws.amazon.com/s3/)。

    2. 在**存储桶**列表中，选择包含源数据的存储桶名称，然后点击**复制 ARN**以获取你的 S3 存储桶 ARN（例如，`arn:aws:s3:::tidb-cloud-source-data`）。记下存储桶 ARN 以供后续使用。

        ![复制存储桶 ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/)，在左侧导航栏中点击**策略**，然后点击**创建策略**。

        ![创建策略](/media/tidb-cloud/aws-create-policy.png)

    4. 在**创建策略**页面，点击 **JSON** 选项卡。

    5. 根据你的需求在策略文本字段中配置策略。以下是一个可用于从 TiDB Cloud Serverless 集群导出数据和导入数据的示例。

        - 从 TiDB Cloud Serverless 集群导出数据需要 **s3:PutObject** 和 **s3:ListBucket** 权限。
        - 将数据导入 TiDB Cloud Serverless 集群需要 **s3:GetObject**、**s3:GetObjectVersion** 和 **s3:ListBucket** 权限。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        在策略文本字段中，将以下配置替换为你自己的值。

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`。例如：

            - 如果你的源数据存储在 `tidb-cloud-source-data` 存储桶的根目录中，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`。
            - 如果你的源数据存储在存储桶的 `mydata` 目录中，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`。

          确保在目录末尾添加 `/*`，以便 TiDB Cloud 可以访问此目录中的所有文件。

        - `"Resource": "<Your S3 bucket ARN>"`，例如 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`。

        - 如果你已启用带有客户管理密钥加密的 AWS Key Management Service 密钥（SSE-KMS），请确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是存储桶的示例 KMS 密钥。

            ```
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

        - 如果你的存储桶中的对象是从另一个加密存储桶复制的，KMS 密钥值需要包含两个存储桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

    6. 点击**下一步**。

    7. 设置策略名称，添加策略标签（可选），然后点击**创建策略**。

3. 在 AWS 管理控制台中，为 TiDB Cloud 创建访问角色并获取角色 ARN。

    1. 在 [IAM 控制台](https://console.aws.amazon.com/iam/)中，在左侧导航栏中点击**角色**，然后点击**创建角色**。

        ![创建角色](/media/tidb-cloud/aws-create-role.png)

    2. 要创建角色，填写以下信息：

        - 在**可信实体类型**中，选择 **AWS 账户**。
        - 在 **AWS 账户**中，选择**其他 AWS 账户**，然后将 TiDB Cloud 账户 ID 粘贴到**账户 ID**字段中。
        - 在**选项**中，点击**需要外部 ID（当第三方将承担此角色时的最佳实践）**，然后将 TiDB Cloud 外部 ID 粘贴到**外部 ID**字段中。如果创建角色时没有需要外部 ID，一旦为项目中的一个 TiDB 集群完成配置，该项目中的所有 TiDB 集群都可以使用相同的角色 ARN 访问你的 Amazon S3 存储桶。如果使用账户 ID 和外部 ID 创建角色，则只有相应的 TiDB 集群可以访问存储桶。

    3. 点击**下一步**打开策略列表，选择你刚刚创建的策略，然后点击**下一步**。

    4. 在**角色详细信息**中，为角色设置名称，然后点击右下角的**创建角色**。创建角色后，将显示角色列表。

    5. 在角色列表中，点击你刚刚创建的角色名称以进入其摘要页面，然后你可以获取角色 ARN。

        ![复制 AWS 角色 ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### 使用 AWS 访问密钥配置 Amazon S3 访问

建议你使用 IAM 用户（而不是 AWS 账户根用户）创建访问密钥。

按照以下步骤配置访问密钥：

1. 创建 IAM 用户。更多信息，请参见[创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。

2. 使用你的 AWS 账户 ID 或账户别名以及你的 IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam)。

3. 创建访问密钥。更多信息，请参见[为 IAM 用户创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

> **注意：**
>
> TiDB Cloud 不会存储你的访问密钥。建议你在导入或导出完成后[删除访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

## 配置 GCS 访问

要允许 TiDB Cloud Serverless 集群访问你的 GCS 存储桶，你需要为存储桶配置 GCS 访问。你可以使用服务账号密钥配置存储桶访问：

按照以下步骤配置服务账号密钥：

1. 在 Google Cloud [服务账号页面](https://console.cloud.google.com/iam-admin/serviceaccounts)，点击**创建服务账号**以创建服务账号。更多信息，请参见[创建服务账号](https://cloud.google.com/iam/docs/creating-managing-service-accounts)。

    1. 输入服务账号名称。
    2. 可选：输入服务账号的描述。
    3. 点击**创建并继续**以创建服务账号。
    4. 在`授予此服务账号对项目的访问权限`中，选择具有所需权限的 [IAM 角色](https://cloud.google.com/iam/docs/understanding-roles)。

        - 从 TiDB Cloud Serverless 集群导出数据需要具有 `storage.objects.create` 权限的角色。
        - 将数据导入 TiDB Cloud Serverless 集群需要具有 `storage.buckets.get`、`storage.objects.get` 和 `storage.objects.list` 权限的角色。

    5. 点击**继续**进入下一步。
    6. 可选：在`授予用户访问此服务账号的权限`中，选择需要[将服务账号附加到其他资源](https://cloud.google.com/iam/docs/attach-service-accounts)的成员。
    7. 点击**完成**以完成服务账号创建。

   ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2. 点击服务账号，然后在`密钥`页面点击**添加密钥**以创建服务账号密钥。

   ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3. 选择默认的 `JSON` 密钥类型，然后点击**创建**以下载 Google Cloud 凭证文件。该文件包含配置 TiDB Cloud Serverless 集群的 GCS 访问时需要使用的服务账号密钥。

## 配置 Azure Blob Storage 访问

要允许 TiDB Cloud Serverless 访问你的 Azure Blob 容器，你需要为容器创建服务 SAS 令牌。

你可以使用 [Azure ARM 模板](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)（推荐）或手动配置创建 SAS 令牌。

要使用 Azure ARM 模板创建 SAS 令牌，请按照以下步骤操作：

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/) 并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    2. 点击目标集群的名称以进入其概览页面，然后在左侧导航栏中点击 **Data** > **Import**。

2. 打开**通过 ARM 模板部署生成新的 SAS 令牌**对话框。
        
    1. 点击**导出数据到...** > **Azure Blob Storage**。如果你的集群之前从未导入或导出过任何数据，请点击页面底部的**点击此处导出数据到...** > **Azure Blob Storage**。
   
    2. 滚动到 **Azure Blob Storage 设置**区域，然后在 SAS 令牌字段下点击**点击此处使用 Azure ARM 模板创建新的**。
   
3. 使用 Azure ARM 模板创建 SAS 令牌。

    1. 在**通过 ARM 模板部署生成新的 SAS 令牌**对话框中，点击**点击打开预配置 ARM 模板的 Azure 门户**。
   
    2. 登录 Azure 后，你将被重定向到 Azure **自定义部署**页面。

    3. 在**自定义部署**页面中填写**资源组**和**存储账号名称**。你可以从容器所在的存储账号概览页面获取所有信息。

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4. 点击**查看 + 创建**或**下一步**以查看部署。点击**创建**开始部署。
   
    5. 完成后，你将被重定向到部署概览页面。导航到**输出**部分以获取 SAS 令牌。

如果你在使用 Azure ARM 模板创建 SAS 令牌时遇到任何问题，请按照以下步骤手动创建：

<details>
<summary>点击此处查看详细信息</summary>

1. 在 [Azure 存储账号](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)页面，点击容器所属的存储账号。
   
2. 在你的**存储账号**页面，点击**安全性 + 网络**，然后点击**共享访问签名**。

   ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3. 在**共享访问签名**页面，按如下方式创建具有所需权限的服务 SAS 令牌。更多信息，请参见[创建服务 SAS 令牌](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。

    1. 在**允许的服务**部分，选择 **Blob** 服务。
    2. 在**允许的资源类型**部分，选择**容器**和**对象**。
    3. 在**允许的权限**部分，根据需要选择权限。

        - 从 TiDB Cloud Serverless 集群导出数据需要**读取**和**写入**权限。
        - 将数据导入 TiDB Cloud Serverless 集群需要**读取**和**列表**权限。

    4. 根据需要调整**开始和到期日期/时间**。
    5. 其他设置可以保持默认值。

   ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4. 点击**生成 SAS 和连接字符串**以生成 SAS 令牌。

</details>

## 配置阿里云对象存储服务（OSS）访问

要允许 TiDB Cloud Serverless 访问你的阿里云 OSS 存储桶，你需要为存储桶创建 AccessKey 对。

按照以下步骤配置 AccessKey 对：

1. 创建 RAM 用户并获取 AccessKey 对。更多信息，请参见[创建 RAM 用户](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)。
    
    在**访问方式**部分，选择**使用永久 AccessKey 访问**。

2. 创建具有所需权限的自定义策略。更多信息，请参见[创建自定义策略](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)。
    
    - 在**效果**部分，选择**允许**。
    - 在**服务**部分，选择**对象存储服务**。
    - 在**操作**部分，根据需要选择权限。
   
        要将数据导入 TiDB Cloud Serverless 集群，授予 **oss:GetObject**、**oss:GetBucketInfo** 和 **oss:ListObjects** 权限。

        要从 TiDB Cloud Serverless 集群导出数据，授予 **oss:PutObject**、**oss:GetBucketInfo** 和 **oss:ListBuckets** 权限。
        
    - 在**资源**部分，选择存储桶和存储桶中的对象。

3. 将自定义策略附加到 RAM 用户。更多信息，请参见[为 RAM 用户授权](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)。
