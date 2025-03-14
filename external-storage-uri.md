---
title: 外部存储服务的 URI 格式
summary: 介绍了外部存储服务 Amazon S3、GCS、和 Azure Blob Storage 的 URI 格式。
---

# 外部存储服务的 URI 格式

本文介绍 Amazon S3、GCS、和 Azure Blob Storage 存储服务的 URI 格式。基本格式如下：

```shell
[scheme]://[host]/[path]?[parameters]
```

## Amazon S3 URI 格式

- `scheme`：`s3`
- `host`：`bucket name`
- `parameters`：

    - `access-key`：访问密钥
    - `secret-access-key`：秘密访问密钥
    - `session-token`：临时会话令牌（BR 尚不支持该参数）
    - `use-accelerate-endpoint`：是否在 Amazon S3 上使用加速端点，默认为 `false`
    - `endpoint`：Amazon S3 兼容服务自定义端点的 URL，例如 `<https://s3.example.com/>`
    - `force-path-style`：使用路径类型 (path-style)，而不是虚拟托管类型 (virtual-hosted-style)，默认为 `true`
    - `storage-class`：上传对象的存储类别，例如 `STANDARD`、`STANDARD_IA`
    - `sse`：加密上传的服务端加密算法，可以设置为空、`AES256` 或 `aws:kms`
    - `sse-kms-key-id`：如果 `sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID
    - `acl`：上传对象的标准 ACL (Canned ACL)，例如 `private`、`authenticated-read`
    - `role-arn`：当需要使用特定的 [IAM 角色](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles.html)来访问第三方 Amazon S3 的数据时，使用这个参数来指定 IAM 角色的对应 [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/zh_cn/general/latest/gr/aws-arns-and-namespaces.html)（例如 `arn:aws:iam::888888888888:role/my-role`）。关于使用 IAM 角色访问第三方 Amazon S3 数据的场景，请参考 [AWS 相关文档介绍](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)。（BR 尚不支持该参数）
    - `external-id`：当需要使用特定的 [IAM 角色](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles.html)来访问第三方 Amazon S3 的数据时，可能需要同时提供正确的[外部 ID](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) 来确保用户有权限代入该 IAM 角色。这个参数用来指定对应的外部 ID，确保成功代入 IAM 角色。外部 ID 可以是任意字符串，并且不是必须的，一般由控制 Amazon S3 数据访问的第三方来指定。如果第三方对于 IAM 角色没有要求指定外部 ID，则可以不需要提供该参数也能顺利代入对应的 IAM 角色，从而访问对应的 Amazon S3 数据。

以下是用于 TiDB Lightning 和 BR 的 Amazon S3 URI 示例，需要指定文件夹路径 `testfolder`：

```shell
s3://external/testfolder?access-key=${access-key}&secret-access-key=${secret-access-key}
```

以下是用于 TiCDC `sink-uri` 的 Amazon S3 URI 示例：

```shell
tiup cdc:v7.5.6 cli changefeed create \
    --server=http://172.16.201.18:8300 \
    --sink-uri="s3://cdc?endpoint=http://10.240.0.38:9000&access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --changefeed-id="cdcTest" \
    --config=cdc_csv.toml
```

以下是用于 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 的 Amazon S3 URI 示例，需要指定具体的文件名 `test.csv`：

```shell
s3://external/test.csv?access-key=${access-key}&secret-access-key=${secret-access-key}
```

## GCS URI 格式

- `scheme`：`gcs` 或 `gs`
- `host`：`bucket name`
- `parameters`：

    - `credentials-file`：迁移工具节点上凭证 JSON 文件的路径
    - `storage-class`：上传对象的存储类别，例如 `STANDARD` 或 `COLDLINE`
    - `predefined-acl`：上传对象的预定义 ACL，例如 `private` 或 `project-private`

以下是用于 TiDB Lightning 和 BR 的 GCS URI 示例，需要指定文件夹路径 `testfolder`：

```shell
gcs://external/testfolder?credentials-file=${credentials-file-path}
```

以下是用于 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 的 GCS URI 示例，需要指定具体的文件名 `test.csv`：

```shell
gcs://external/test.csv?credentials-file=${credentials-file-path}
```

## Azure Blob Storage URI 格式

- `scheme`：`azure` 或 `azblob`
- `host`：`container name`
- `parameters`：

    - `account-name`：存储账户名
    - `account-key`：访问密钥
    - `sas-token`：共享访问签名令牌
    - `access-tier`：上传对象的存储类别，例如 `Hot`、`Cool`、`Archive`，默认值为该存储账户的默认访问层。
    - `encryption-scope`：服务端的[加密范围 (Encryption Scope)](https://learn.microsoft.com/zh-cn/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)
    - `encryption-key`：服务端使用的[加密密钥 (Encryption Key)](https://learn.microsoft.com/zh-cn/azure/storage/blobs/encryption-customer-provided-keys)，采用的加密算法为 AES256

以下是用于 BR 的 Azure Blob Storage URI 示例，需要指定文件夹路径 `testfolder`：

```shell
azure://external/testfolder?account-name=${account-name}&account-key=${account-key}
```
