---
title: 静态加密
summary: 了解如何启用静态加密功能保护敏感数据。
aliases: ['/docs-cn/dev/encryption-at-rest/']
---

# 静态加密

> **注意：**
>
> 如果集群部署在 AWS 上并在使用 EBS (Elastic Block Store) 存储数据，建议使用 EBS 加密，详细信息请参考 [AWS 文档 - EBS 加密](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/EBSEncryption.html)。如果集群部署在 AWS 上，但未使用 EBS 存储（例如使用本地 NVMe 存储），则建议使用本文中介绍的静态加密方式。

静态加密 (encryption at rest) 即在存储数据时进行数据加密。对于数据库，静态加密功能也叫透明数据加密 (TDE)，区别于传输数据加密 (TLS) 或使用数据加密（很少使用）。SSD 驱动器、文件系统、云供应商等都可进行静态加密。但区别于这些加密方式，若 TiKV 在存储数据前就进行数据加密，攻击者则必须通过数据库的身份验证才能访问数据。例如，即使攻击者获得物理机的访问权限时，也无法通过复制磁盘上的文件来访问数据。

## 各 TiDB 组件支持的加密方式

在一个 TiDB 集群中，不同的组件使用不同的加密方式。本节介绍 TiKV、 TiFlash、PD 和 Backup & Restore (BR) 等不同 TiDB 组件支持的加密方式。

部署好一个 TiDB 集群后，大部分用户数据会存储在 TiKV 和 TiFlash 节点上。此外，一些元数据会存储在 PD 节点上，例如用作为 TiKV Region 边界的二级索引密钥。为了能够充分发挥静态加密的优势，所有组件都需要启用加密功能。此外，进行加密时，也需要对备份、日志文件和通过网络传输的数据进行加密。

### TiKV

TiKV 支持静态加密，即在 [CTR](https://zh.wikipedia.org/wiki/分组密码工作模式) 模式下使用 [AES](https://zh.wikipedia.org/wiki/高级加密标准) 或 [SM4](https://zh.wikipedia.org/wiki/SM4) 对数据文件进行透明加密。要启用静态加密，用户需提供一个加密密钥，即主密钥。TiKV 自动轮换 (rotate) 用于加密实际数据文件的密钥，主密钥则可以由用户手动轮换。请注意，静态加密仅加密静态数据（即磁盘上的数据），而不加密网络传输中的数据。建议 TLS 与静态加密一起使用。

可以选择将 AWS KMS (Key Management Service) 用于云上部署或本地部署，也可以指定将密钥以明文形式存储在文件中。

TiKV 当前不从核心转储 (core dumps) 中排除加密密钥和用户数据。建议在使用静态加密时禁用 TiKV 进程的核心转储，该功能目前无法由 TiKV 独立处理。

TiKV 使用文件的绝对路径来跟踪已加密的数据文件。一旦 TiKV 节点开启了加密功能，用户就不应更改数据文件的路径配置，例如 `storage.data-dir`，`raftstore.raftdb-path`，`rocksdb.wal-dir` 和 `raftdb.wal-dir`。

SM4 加密只在 v6.3.0 及之后版本的 TiKV 上支持。v6.3.0 之前的 TiKV 仅支持 AES 加密。SM4 加密会对吞吐造成 50% 到 80% 的回退。

### TiFlash

TiFlash 支持静态加密。数据密钥由 TiFlash 生成。TiFlash（包括 TiFlash Proxy）写入的所有文件，包括数据文件、Schema 文件、临时文件等，均由当前数据密钥加密。TiFlash 支持的加密算法、加密配置方法（配置项在 [`tiflash-learner.toml`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) 中）和监控项含义等均与 TiKV 一致。

如果 TiFlash 中部署了 Grafana 组件，可以查看 **TiFlash-Proxy-Details** -> **Encryption**。

SM4 加密只在 v6.4.0 及之后版本的 TiFlash 上支持。v6.4.0 之前的 TiFlash 仅支持 AES 加密。

### PD

PD 的静态加密为实验特性，其配置方式与 TiKV 相同。

### BR 备份

BR 支持对备份到 S3 的数据进行 S3 服务端加密 (SSE)。BR S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥进行加密，详细信息请参考 [BR S3 服务端加密](/encryption-at-rest.md#br-s3-服务端加密)。

### 日志

TiKV，TiDB 和 PD 信息日志中可能包含用于调试的用户数据。信息日志不会被加密，建议开启[日志脱敏](/log-redaction.md)功能。

## TiKV 静态加密

TiKV 当前支持的加密算法包括 AES128-CTR、AES192-CTR、AES256-CTR 和 SM4-CTR (仅 v6.3.0 及之后版本)。TiKV 使用信封加密 (envelop encryption)，所以启用加密后，TiKV 使用以下两种类型的密钥：

* 主密钥 (master key)：主密钥由用户提供，用于加密 TiKV 生成的数据密钥。用户在 TiKV 外部进行主密钥的管理。
* 数据密钥 (data key)：数据密钥由 TiKV 生成，是实际用于加密的密钥。

多个 TiKV 实例可共用一个主密钥。在生产环境中，推荐通过 AWS KMS 提供主密钥。首先通过 AWS KMS 创建用户主密钥 (CMK)，然后在配置文件中将 CMK 密钥的 ID 提供给 TiKV。TiKV 进程在运行时可以通过 [IAM 角色](https://aws.amazon.com/iam/)访问 KMS CMK。如果 TiKV 无法访问 KMS CMK，TiKV 就无法启动或重新启动。详情参阅 AWS 文档中的 [KMS](https://docs.aws.amazon.com/zh_cn/kms/index.html) and [IAM](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/introduction.html)。

用户也可以通过文件形式提供主密钥。该文件须包含一个用十六进制字符串编码的 256 位（32 字节）密钥，并以换行符结尾（即 `\n`），且不包含其他任何内容。将密钥存储在磁盘上会泄漏密钥，因此密钥文件仅适合存储在 RAM 内存的 `tempfs` 中。

数据密钥由 TiKV 传递给底层存储引擎（即 RocksDB）。RocksDB 写入的所有文件，包括 SST 文件，WAL 文件和 MANIFEST 文件，均由当前数据密钥加密。TiKV 使用的其他临时文件（可能包括用户数据）也由相同的数据密钥加密。默认情况下，TiKV 每周自动轮换数据密钥，但是该时间段是可配置的。密钥轮换时，TiKV 不会重写全部现有文件来替换密钥，但如果集群的写入量恒定，则 RocksDB compaction 会将使用最新的数据密钥对数据重新加密。TiKV 跟踪密钥和加密方法，并使用密钥信息对读取的内容进行解密。

无论用户配置了哪种数据加密方法，数据密钥都使用 AES256-GCM 算法进行加密，以方便对主密钥进行验证。所以当使用文件而不是 KMS 方式指定主密钥时，主密钥必须为 256 位（32 字节）。

### 配置加密

要启用加密，你可以在 TiKV 和 PD 的配置文件中添加加密部分：

```
[security.encryption]
data-encryption-method = "aes128-ctr"
data-key-rotation-period = "168h" # 7 days
```

`data-encryption-method` 的可选值为 `"aes128-ctr"`、`"aes192-ctr"`、`"aes256-ctr"`、`"sm4-ctr"` (仅 v6.3.0 及之后版本) 和 `"plaintext"`。默认值为 `"plaintext"`，即默认不开启加密功能。`data-key-rotation-period` 指定 TiKV 轮换密钥的频率。可以为新 TiKV 集群或现有 TiKV 集群开启加密，但只有启用后写入的数据才保证被加密。要禁用加密，请在配置文件中删除 `data-encryption-method`，或将该参数值为 `"plaintext"`，然后重启 TiKV。若要替换加密算法，则将 `data-encryption-method` 替换成已支持的加密算法，然后重启 TiKV。替换加密算法后，旧加密算法生成的加密文件会随着新数据的写入逐渐被重写成新加密算法所生成的加密文件。

如果启用了加密（即 `data-encryption-method` 的值不是 `"plaintext"`），则必须指定主密钥。TiKV 支持 KMS 和文件两种方式指定密钥。

#### 配置 KMS 密钥

TiKV 支持 AWS、GCP 和 Azure 3 个平台的 KMS 加密，根据服务部署的平台，使用不同的方式配置 KMS 加密。

<SimpleTab>

<div label="AWS KMS">

创建密钥

在 AWS 上创建一个密钥，请执行以下步骤：

1. 进入 AWS 控制台的 [AWS KMS](https://console.aws.amazon.com/kms)。
2. 确保在控制台的右上角选择正确的区域。
3. 点击**创建密钥**，选择**对称** (Symmetric) 作为密钥类型。
4. 为钥匙设置一个别名。

你也可以使用 AWS CLI 执行该操作：

```shell
aws --region us-west-2 kms create-key
aws --region us-west-2 kms create-alias --alias-name "alias/tidb-tde" --target-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

需要在第二条命令中输入的 `--target-key-id` 是第一条命令的结果。

配置密钥

使用 AWS KMS 方式指定为主密钥，请在 `[security.encryption]` 部分之后添加 `[security.encryption.master-key]` 部分：

```
[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
endpoint = "https://kms.us-west-2.amazonaws.com"
```

`key-id` 指定 KMS CMK 的密钥 ID。`region` 为 KMS CMK 的 AWS 区域名。`endpoint` 通常无需指定，除非你在使用非 AWS 提供的 AWS KMS 兼容服务或需要使用 [KMS VPC endpoint](https://docs.aws.amazon.com/kms/latest/developerguide/kms-vpc-endpoint.html)。

你也可以使用 AWS [多区域键](https://docs.aws.amazon.com/zh_cn/kms/latest/developerguide/multi-region-keys-overview.html)。为此，你需要在一个特定的区域设置一个主键，并在需要的区域中添加副本密钥。
</div>

<div label="GCP KMS">

创建密钥

在 GCP 平台上创建一个密钥，请执行以下步骤：

1. 进入 GCP 控制台的 [密钥管理](https://console.cloud.google.com/security/kms/keyrings)。
2. 点击**创建密钥环**，创建密钥环，注意密钥环所在的位置需要覆盖 TiDB 集群部署的区域。
3. 选择上一步创建的密钥环，在密钥环详情页面点击**创建密钥**，注意密钥的**保护级别**选择**软件**或 **HSM**，**密钥材料**选择**生成的密钥**，**用途**选择 **Symmetric encrypt/decrypt**。

你也可以使用 gcloud CLI 执行该操作：

```shell
gcloud kms keyrings create "key-ring-name" --location "global"
gcloud kms keys create "key-name" --keyring "key-ring-name" --location "global" --purpose "encryption" --rotation-period "30d" 
```

请将上述命令中的 "key-ring-name"、"key-name"、"global"、"30d" 等字段替换为实际密钥对应的名称和配置。

配置密钥

使用 GCP KMS 方式指定为主密钥，请在 `[security.encryption]` 部分之后添加 `[security.encryption.master-key]` 部分：

```
[security.encryption.master-key]
type = "kms"
key-id = "projects/project-name/locations/global/keyRings/key-ring-name/cryptoKeys/key-name"
vendor = "gcp"

[security.encryption.master-key.gcp]
credential-file-path = "/path/to/credential.json"
```

`key-id` 指定 KMS CMK 的密钥 ID, `credential-file-path` 指向验证凭据配置文件的路径，目前支持 Serivce Account 和 Authentition User 两种凭据。如果 TiKV 的运行环境已配置 [应用默认凭据](https://cloud.google.com/docs/authentication/application-default-credentials?hl=zh-cn)，则无须此配置项。
</div>

<div label="Azure KMS">

创建密钥

在 Azure 平台创建密钥，请参考文档 [使用 Azure 门户在 Azure Key Vault 中设置和检索密钥](https://learn.microsoft.com/zh-cn/azure/key-vault/keys/quick-create-portal)。

配置密钥

要使用 Azure KMS 方式指定为主密钥，请在 `[security.encryption]` 部分之后添加 `[security.encryption.master-key]` 部分：

```
[security.encryption.master-key]
type = 'kms'
key-id = 'your-kms-key-id'
region = 'region-name'
endpoint = 'endpoint'
vendor = 'azure'

[security.encryption.master-key.azure]
tenant-id = 'tenant_id'
client-id = 'client_id'
keyvault-url = 'keyvault_url'
hsm-name = 'hsm_name'
hsm-url = 'hsm_url'
# 如下 4 个参数为可选字段，用于设置 client 认证的凭证，请根据实际的使用场景进行设置
client_certificate = ""
client_certificate_path = ""
client_certificate_password = ""
client_secret = ""
```

请将上述配置中除 "vendor" 之外的其他字段设置为实际需要使用的密钥对应的配置。
</div>

</SimpleTab>

#### 配置文件密钥

若要使用文件方式指定主密钥，主密钥配置应如下所示：

```
[security.encryption.master-key]
type = "file"
path = "/path/to/key/file"
```

以上示例中，`path` 为密钥文件的路径。该文件须包含一个 256 位（32 字节）的十六进制字符串，并以换行符结尾（即 `\n`），且不包含其他任何内容。密钥文件示例如下：

```
3b5896b5be691006e0f71c3040a29495ddcad20b14aff61806940ebd780d3c62
```

### 轮换主密钥

要轮换主密钥，你必须在配置中同时指定新的主密钥和旧的主密钥，然后重启 TiKV。用 `security.encryption.master-key` 指定新的主密钥，用 `security.encryption.previous-master-key` 指定旧的主密钥。`security.encryption.previous-master-key` 配置的格式与 `encryption.master-key` 相同。重启时，TiKV 必须能同时访问旧主密钥和新主密钥，但一旦 TiKV 启动并运行，就只需访问新密钥。此后，可以将 `encryption.previous-master-key` 项保留在配置文件中。即使重启时，TiKV 也只会在无法使用新的主密钥解密现有数据时尝试使用旧密钥。

TiKV 当前不支持在线轮换主密钥，因此你需要重启 TiKV 进行主密钥轮换。建议对运行中的、提供在线查询的 TiKV 集群进行滚动重启。

轮换 AWS KMS CMK 的配置示例如下：

```
[security.encryption.master-key]
type = "kms"
key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
region = "us-west-2"

[security.encryption.previous-master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

### 监控和调试

要监控静态加密（如果 TiKV 中部署了 Grafana 组件），可以查看 **TiKV-Details** -> **Encryption** 面板中的监控项：

* Encryption initialized：如果在 TiKV 启动期间初始化了加密，则为 `1`，否则为 `0`。进行主密钥轮换时可通过该监控项确认主密钥轮换是否已完成。
* Encryption data keys：现有数据密钥的数量。每次轮换数据密钥后，该数字都会增加 `1`。通过此监控指标可以监测数据密钥是否按预期轮换。
* Encrypted files：当前的加密数据文件数量。为先前未加密的集群启用加密时，将此数量与数据目录中的当前数据文件进行比较，可通过此监控指标估计已经被加密的数据量。
* Encryption meta file size：加密元数据文件的大小。
* Read/Write encryption meta duration：对用于加密的元数据进行操作带来的额外开销。

在调试方面，可使用 `tikv-ctl` 命令查看加密元数据（例如使用的加密方法和数据密钥列表）。该操作可能会暴露密钥，因此不推荐在生产环境中使用。详情参阅 [TiKV Control](/tikv-control.md#打印加密元数据)。

### TiKV 版本间兼容性

为了减少 TiKV 管理加密元数据造成的 I/O 操作和互斥锁竞争引发的开销，TiKV v4.0.9 对此进行了优化。此优化可以通过 TiKV 配置文件中的 `security.encryption.enable-file-dictionary-log` 参数启用或关闭。此配置参数仅在 TiKV v4.0.9 或更高版本中生效。

该配置项默认开启，此时 TiKV v4.0.8 或更早期的版本无法识别加密元数据的数据格式。例如，假设你正在使用 TiKV v4.0.9 或更高版本，开启了静态加密和默认开启了 `enable-file-dictionary-log` 配置。如果将集群降级到 TiKV v4.0.8 或更早版本，TiKV 将无法启动，并且信息日志中会有类似如下的报错：

```
[2020/12/07 07:26:31.106 +08:00] [ERROR] [mod.rs:110] ["encryption: failed to load file dictionary."]
[2020/12/07 07:26:33.598 +08:00] [FATAL] [lib.rs:483] ["called `Result::unwrap()` on an `Err` value: Other(\"[components/encryption/src/encrypted_file/header.rs:18]: unknown version 2\")"]
```

为了避免上面所示错误，你可以首先将 `security.encryption.enable-file-dictionary-log` 设置为 `false`，然后启动 TiKV v4.0.9 或更高版本。TiKV 成功启动后，加密元数据的数据格式将降级为 TiKV 早期版本可以识别的格式。此时，你可再将 TiKV 集群降级到较早的版本。

## TiFlash 静态加密

TiFlash 当前支持的加密算法与 TiKV 一致，包括 AES128-CTR、AES192-CTR、AES256-CTR 和 SM4-CTR（仅 v6.4.0 及之后版本）。TiFlash 同样使用信封加密 (envelop encryption)，所以启用加密后，TiFlash 使用以下两种类型的密钥：

* 主密钥 (master key)：主密钥由用户提供，用于加密 TiFlash 生成的数据密钥。用户在 TiFlash 外部进行主密钥的管理。
* 数据密钥 (data key)：数据密钥由 TiFlash 生成，是实际用于加密的密钥。

多个 TiFlash 实例可共用一个主密钥，并且也可以和 TiKV 共用一个主密钥。在生产环境中，推荐通过 AWS KMS 提供主密钥。另外，你也可以通过文件形式提供主密钥。具体的主密钥生成方式和格式均与 TiKV 相同。

TiFlash 使用数据密钥加密所有落盘的数据文件，包括数据文件、Schmea 文件和计算过程中产生的临时数据文件等。默认情况下，TiFlash 每周自动轮换数据密钥，该轮换周期也可根据需要自定义配置。密钥轮换时，TiFlash 不会重写全部现有文件来替换密钥，但如果集群的写入量恒定，则后台 compaction 任务将会用最新的数据密钥对数据重新加密。TiFlash 跟踪密钥和加密方法，并使用密钥信息对读取的内容进行解密。

### 创建密钥

如需在 AWS 上创建一个密钥，请参考 TiKV 密钥的创建方式。

### 配置加密

启用加密的配置，可以在 `tiflash-learner.toml` 文件中添加以下内容：

```
[security.encryption]
data-encryption-method = "aes128-ctr"
data-key-rotation-period = "168h" # 7 days
```

或者，在 TiUP 集群模板文件中添加以下内容：

```
server_configs:
  tiflash-learner:
    security.encryption.data-encryption-method: "aes128-ctr"
    security.encryption.data-key-rotation-period: "168h" # 7 days
```

`data-encryption-method` 的可选值为 `"aes128-ctr"`、`"aes192-ctr"`、`"aes256-ctr"`、`"sm4-ctr"` (仅 v6.4.0 及之后版本) 和 `"plaintext"`。默认值为 `"plaintext"`，即默认不开启加密功能。`data-key-rotation-period` 指定 TiFlash 轮换密钥的频率。可以为新 TiFlash 集群或现有 TiFlash 集群开启加密，但只有启用后写入的数据才保证被加密。要禁用加密，请在配置文件中删除 `data-encryption-method`，或将该参数值为 `"plaintext"`，然后重启 TiFlash。若要替换加密算法，则将 `data-encryption-method` 替换成已支持的加密算法，然后重启 TiFlash。替换加密算法后，旧加密算法生成的加密文件会随着新数据的写入逐渐被重写成新加密算法所生成的加密文件。

如果启用了加密（即 `data-encryption-method` 的值不是 `"plaintext"`），则必须指定主密钥。要使用 AWS KMS 方式指定为主密钥，配置方式如下：

在 `tiflash-learner.toml` 配置文件的 `[security.encryption]` 部分之后添加 `[security.encryption.master-key]`：

```
[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
endpoint = "https://kms.us-west-2.amazonaws.com"
```

或者，在 TiUP 集群模板文件中添加以下内容：

```
server_configs:
  tiflash-learner:
    security.encryption.master-key.type: "kms"
    security.encryption.master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
    security.encryption.master-key.region: "us-west-2"
    security.encryption.master-key.endpoint: "https://kms.us-west-2.amazonaws.com"
```

上述配置项的含义与 TiKV 均相同。

若要使用文件方式指定主密钥，可以在 `tiflash-learner.toml` 配置文件中添加以下内容：

```
[security.encryption.master-key]
type = "file"
path = "/path/to/key/file"
```

或者，在 TiUP 集群模板文件中添加以下内容：

```
server_configs:
  tiflash-learner:
    security.encryption.master-key.type: "file"
    security.encryption.master-key.path: "/path/to/key/file"
```

上述配置项的含义以及密钥文件的内容格式与 TiKV 均相同。

### 轮换主密钥

TiFlash 轮换主秘钥的方法与 TiKV 相同。TiFlash 当前也不支持在线轮换主密钥，因此你需要重启 TiFlash 进行主密钥轮换。建议对运行中的、提供在线查询的 TiFlash 集群进行滚动重启。

要轮换 KMS CMK，可以在 `tiflash-learner.toml` 配置文件中添加以下内容：

```
[security.encryption.master-key]
type = "kms"
key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
region = "us-west-2"

[security.encryption.previous-master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

或者，在 TiUP 集群模板文件中添加以下内容：

```
server_configs:
  tiflash-learner:
    security.encryption.master-key.type: "kms"
    security.encryption.master-key.key-id: "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    security.encryption.master-key.region: "us-west-2"
    security.encryption.previous-master-key.type: "kms"
    security.encryption.previous-master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
    security.encryption.previous-master-key.region: "us-west-2"
```

### 监控和调试

要监控静态加密（如果 TiFlash 中部署了 Grafana 组件），可以查看 **TiFlash-Proxy-Details** -> **Encryption** 面板中的监控项，其中监控项的含义与 TiKV 相同。

在调试方面，由于 TiFlash 复用了 TiKV 管理加密元数据的逻辑，因此也可使用 `tikv-ctl` 命令查看加密元数据（例如使用的加密方法和数据密钥列表）。该操作可能会暴露密钥，因此不推荐在生产环境中使用。详情参阅 [TiKV Control](/tikv-control.md#打印加密元数据)。

### TiFlash 版本间兼容性

TiFlash 在 v4.0.9 同样对加密元数据操作进行了优化，其兼容性要求与 TiKV 相同，详情参考 [TiKV 版本间兼容性](#tikv-版本间兼容性)。

## BR S3 服务端加密

使用 BR 备份数据到 S3 时，若要启用 S3 服务端加密，需要传递 `--s3.sse` 参数并将参数值设置为 `aws:kms`。S3 将使用自己的 KMS 密钥进行加密。示例如下：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms
```

若要使用用户创建和拥有的自定义 AWS KMS CMK，需另外传递 `--s3.sse-kms-key-id` 参数。此时，BR 进程和集群中的所有 TiKV 节点都需访问该 KMS CMK（例如，通过 AWS IAM），并且该 KMS CMK 必须与存储备份的 S3 bucket 位于同一 AWS 区域。建议通过 AWS IAM 向 BR 进程和 TiKV 节点授予对 KMS CMK 的访问权限。参见 AWS 文档中的 [IAM](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/introduction.html)。示例如下：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

恢复备份时，不需要也不可指定 `--s3.sse` 和 `--s3.sse-kms-key-id` 参数。S3 将自动相应进行解密。用于恢复备份数据的 BR 进程和集群中的 TiKV 节点也需要访问 KMS CMK，否则恢复将失败。示例如下：

```
./br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix>"
```

## BR Azure Blob Storage 服务端加密

使用 BR 备份数据到 Azure Blob Storage 时，可以选择使用加密范围 (Encryption Scope) 或加密密钥 (Encryption Key) 进行数据的服务端加密。

### 方法一：使用加密范围

你可以通过以下两种方式为备份数据指定加密范围：

- 在 `backup` 命令中添加 `--azblob.encryption-scope` 参数，并设置为加密范围名：

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-scope scope1
    ```

- 在 URI 中添加 `encryption-scope`，并设置为加密范围名：

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-scope=scope1"
    ```

更多信息请参考 Azure 文档中的[上传具有加密范围的 blob](https://learn.microsoft.com/zh-cn/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)。

在恢复备份时，不需要指定加密范围，Azure Blob Storage 将自动进行解密。示例如下：

```shell
./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
```

### 方法二：使用加密密钥

你可以通过以下三种方式为备份数据指定加密密钥：

- 在 `backup` 命令中添加 `--azblob.encryption-key` 参数，并设置为 AES256 加密密钥：

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

- 在 URI 中添加 `encryption-key`，并设置为 AES256 加密密钥。如果密钥包含 URI 保留字符，例如 `&`、`%` 等，需要先进行百分号编码：

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

- 在 BR 的环境变量中添加 `AZURE_ENCRYPTION_KEY`，并设置为 AES256 加密密钥。在运行前，请确保环境变量中的加密密钥是已知的，避免忘记密钥。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```

更多信息请参考 Azure 文档中的[在对 Blob 存储的请求中提供加密密钥](https://learn.microsoft.com/zh-cn/azure/storage/blobs/encryption-customer-provided-keys)。

在恢复备份时，需要指定加密密钥。示例如下：

- 在 `restore` 命令中传递 `--azblob.encryption-key` 参数：

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

- 在 URI 中添加 `encryption-key`：

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

- 在 BR 的环境变量中添加 `AZURE_ENCRYPTION_KEY`：

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```
