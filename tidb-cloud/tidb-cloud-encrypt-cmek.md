---
title: 使用客户管理的加密密钥进行静态加密
summary: 了解如何在 TiDB Cloud 中使用客户管理的加密密钥（CMEK）。
---

# 使用客户管理的加密密钥进行静态加密

客户管理的加密密钥（Customer-Managed Encryption Key，CMEK）允许你使用完全由你控制的对称加密密钥来保护 TiDB Cloud Dedicated 集群中的静态数据。这个密钥被称为 CMEK 密钥。

当为项目启用 CMEK 后，该项目中创建的所有集群都会使用 CMEK 密钥加密其静态数据。此外，这些集群生成的任何备份数据也会使用相同的密钥进行加密。如果未启用 CMEK，TiDB Cloud 会使用托管密钥来加密集群中的所有静态数据。

> **注意：**
>
> 目前，此功能仅供申请使用。如果你需要试用此功能，请联系[技术支持](/tidb-cloud/tidb-cloud-support.md)。

## 限制

- 目前，TiDB Cloud 仅支持使用 AWS KMS 提供 CMEK。
- 要使用 CMEK，你需要在创建项目时启用 CMEK，并在创建集群之前完成 CMEK 相关配置。你无法为现有项目启用 CMEK。
- 目前，在启用 CMEK 的项目中，你只能创建在 AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。不支持在其他云服务提供商上托管的 TiDB Cloud Dedicated 集群和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。
- 目前，对于特定项目，你只能为一个 AWS 区域启用 CMEK。配置完成后，你无法在同一项目中的其他区域创建集群。

## 启用 CMEK

如果你想使用你账号拥有的 KMS 加密数据，请执行以下步骤。

### 步骤 1. 创建启用 CMEK 的项目

如果你是组织的 `Organization Owner` 角色，你可以使用 TiDB Cloud 控制台或 API 创建启用 CMEK 的项目。

<SimpleTab groupId="method">
<div label="使用控制台" value="console">

要创建启用 CMEK 的项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标组织。
2. 在左侧导航栏中，点击 **Projects**。
3. 在 **Projects** 页面，点击右上角的 **Create New Project**。
4. 填写项目名称。
5. 选择启用项目的 CMEK 功能。
6. 点击 **Confirm** 完成项目创建。

</div>
<div label="使用 API" value="api">

你可以通过 [Create a CMEK-enabled project](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject) 端点使用 TiDB Cloud API 完成此步骤。确保将 `aws_cmek_enabled` 字段设置为 `true`。

目前，TiDB Cloud API 仍处于测试阶段。有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

### 步骤 2. 完成项目的 CMEK 配置

你可以使用 TiDB Cloud 控制台或 API 完成项目的 CMEK 配置。

> **注意：**
>
> 确保密钥的策略满足要求，并且没有权限不足或账号问题等错误。这些错误可能导致使用此密钥创建的集群出现问题。

<SimpleTab groupId="method">
<div label="使用控制台" value="console">

要完成项目的 CMEK 配置，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的组合框切换到目标项目。
2. 在左侧导航栏中，点击 **Project Settings** > **Encryption Access**。
3. 在 **Encryption Access** 页面，点击 **Create Encryption Key** 进入密钥创建页面。
4. 密钥提供者仅支持 AWS KMS。你可以选择加密密钥可以使用的区域。
5. 复制并保存 JSON 文件为 `ROLE-TRUST-POLICY.JSON`。此文件描述了信任关系。
6. 将此信任关系添加到 AWS KMS 的密钥策略中。有关更多信息，请参见 [AWS KMS 中的密钥策略](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
7. 在 TiDB Cloud 控制台中，滚动到密钥创建页面底部，然后填写从 AWS KMS 获取的 **KMS Key ARN**。
8. 点击 **Create** 创建密钥。

</div>
<div label="使用 API" value="api">

1. 在 AWS KMS 上配置密钥策略，并将以下信息添加到密钥策略中：

    ```json
    {
        "Version": "2012-10-17",
        "Id": "cmek-policy",
        "Statement": [
            // EBS 相关策略
            {
                "Sid": "Allow access through EBS for all principals in the account that are authorized to use EBS",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:CreateGrant",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": "<pingcap-account>",
                        "kms:ViaService": "ec2.<region>.amazonaws.com"
                    }
                }
            },
            // S3 相关策略
            {
                "Sid": "Allow TiDB cloud role to use KMS to store encrypted backup to S3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<pingcap-account>:root"
                },
                "Action": [
                    "kms:Decrypt",
                    "kms:GenerateDataKey"
                ],
                "Resource": "*"
            },
            ... // 用户自己的 KMS 管理员访问权限
        ]
    }
    ```

    - `<pingcap-account>` 是运行集群的账号。如果你不知道账号，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。
    - `<region>` 是你想要创建集群的区域，例如 `us-west-2`。如果你不想指定区域，请将 `<region>` 替换为通配符 `*`，并将其放在 `StringLike` 块中。
    - 有关上述块中的 EBS 相关策略，请参见 [AWS 文档](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account)。
    - 有关上述块中的 S3 相关策略，请参见 [AWS 博客](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption)。

2. 调用 TiDB Cloud API 的 [Configure AWS CMEK](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek) 端点。

    目前，TiDB Cloud API 仍处于测试阶段。有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

> **注意：**
>
> 此功能将在未来进一步增强，即将推出的功能可能需要额外的权限。因此，此策略要求可能会发生变化。

### 步骤 3. 创建集群

在[步骤 1](#步骤-1-创建启用-cmek-的项目) 中创建的项目下，创建一个在 AWS 上托管的 TiDB Cloud Dedicated 集群。有关详细步骤，请参见[此文档](/tidb-cloud/create-tidb-cluster.md)。确保集群所在的区域与[步骤 2](/tidb-cloud/tidb-cloud-encrypt-cmek.md#步骤-2-完成项目的-cmek-配置)中的区域相同。

> **注意：**
>
> 启用 CMEK 后，集群节点使用的 EBS 卷和集群备份使用的 S3 都将使用 CMEK 进行加密。

## 轮换 CMEK

你可以在 AWS KMS 上配置[自动 CMEK 轮换](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)。启用此轮换后，你无需在 TiDB Cloud 的项目设置中更新 **Encryption Access**，包括 CMEK ID。

## 撤销和恢复 CMEK

如果你需要临时撤销 TiDB Cloud 对 CMEK 的访问权限，请执行以下步骤：

1. 在 AWS KMS 控制台上，撤销相应的权限并更新 KMS 密钥策略。
2. 在 TiDB Cloud 控制台上，暂停项目中的所有集群。

> **注意：**
>
> 在 AWS KMS 上撤销 CMEK 后，你正在运行的集群不会受到影响。但是，当你暂停集群然后恢复集群时，由于无法访问 CMEK，集群将无法正常恢复。

撤销 TiDB Cloud 对 CMEK 的访问权限后，如果你需要恢复访问权限，请执行以下步骤：

1. 在 AWS KMS 控制台上，恢复 CMEK 访问策略。
2. 在 TiDB Cloud 控制台上，恢复项目中的所有集群。
