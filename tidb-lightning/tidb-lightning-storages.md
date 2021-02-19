---
title: TiDB Lightning 源文件存储
summary: 了解 TiDB Lightning 支持的源文件存储格式和使用方式。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-storages/']
---

# TiDB Lightning 存储

TiDB Lightning 支持在本地文件系统、Amazon S3 上读取数据源文件。通过 TiDB Lightning 的 `data-source-dir` 参数中的不同 URL scheme，可以区分不同的存储方式。

## Scheme

TiDB Lightning 支持以下存储服务：

| 服务 | Scheme | 支持 TiDB Lightning 版本 | 示例 |
|---------|------|-------|-------------|
| 本地文件系统 | local | 所有版本 | `local:///path/to/source-directory/` 或 '/path/to/source-directory/' |
| Amazon S3 及其他兼容 S3 的服务 | s3 | >=v4.0.7 | `s3://bucket-name/prefix/of/dest/` |


## 参数

### 参数设置

TiDB Lightning 支持如下两种方式设置数据源文件的路径：

1. 在 TiDB Lightning 的 TOML 格式的配置文件中设置 `mydumper.data-source-dir` 字段。 例如：

```toml
[mydumper]
data-source-dir = 's3://bucket-name/prefix?region=us-west-2'
```

2. 通过命令行参数指定。 例如：

{{< copyable "shell-regular" >}}

```shell
./tidb-lightning -d '/path/to/source-directory/'
```

> **注意：**
>
> 如果同时在命令行指定 `-d` 参数，并在配置文件中设置 `mydumper.data-source-dir` 的值，此时命令行参数生效。

### S3 参数

在数据源存储类型指定为 S3 时，可以在 URL 的参数中设置如下这些参数：

| 参数 | 描述 |
|----------:|---------|
| `access-key` | 访问密钥 |
| `secret-access-key` | secret 访问密钥 |
| `region` | Amazon S3 服务区域（默认为 `us-east-1`） |
| `use-accelerate-endpoint` | 是否在 Amazon S3 上使用加速端点（默认为 `false`） |
| `endpoint` | S3 兼容服务自定义端点的 URL（例如 `https://s3.example.com/`）|
| `force-path-style` | 使用 path-style，而不是 virtual-hosted style（默认为 `false`） |
| `storage-class` | 上传对象的存储类别（例如 `STANDARD`、`STANDARD_IA`） |
| `sse` | 用于加密上传的服务器端加密算法（可以设置为空，`AES256` 或 `aws:kms`） |
| `sse-kms-key-id` | 如果 `sse` 设置为 `aws:kms`，则使用该参数指定 KMS ID |
| `acl` | 上传对象的 canned ACL（例如，`private`、`authenticated-read`） |

> **注意：**
>
> 不建议在存储 URL 中直接传递访问密钥和 secret 访问密钥，因为这些密钥是明文记录的。TiDB Lightning 尝试按照以下顺序从环境中推断这些密钥：

1. `$AWS_ACCESS_KEY_ID` 和 `$AWS_SECRET_ACCESS_KEY` 环境变量。
2. `$AWS_ACCESS_KEY` 和 `$AWS_SECRET_KEY` 环境变量。
3. TiDB Lightning 节点上的共享凭证文件，路径由 `$AWS_SHARED_CREDENTIALS_FILE` 环境变量指定。
4. TiDB Lightning 节点上的共享凭证文件，路径为 `~/.aws/credentials`。
5. 当前 Amazon EC2 容器的 IAM 角色。
6. 当前 Amazon ECS 任务的 IAM 角色。
