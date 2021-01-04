---
title: 静态加密
summary: 了解如何启用静态加密功能保护敏感数据。
aliases: ['/docs-cn/dev/encryption-at-rest/']
---

# 静态加密 <span class="version-mark">从 v4.0.0 版本开始引入</span>

静态加密 (encryption at rest) 即在存储数据时进行数据加密。对于数据库，静态加密功能也叫透明数据加密 (TDE)，区别于传输数据加密 (TLS) 或使用数据加密（很少使用）。SSD 驱动器、文件系统、云供应商等都可进行静态加密。但区别于这些加密方式，若 TiKV 在存储数据前就进行数据加密，攻击者则必须通过数据库的身份验证才能访问数据。例如，即使攻击者获得物理机的访问权限时，也无法通过复制磁盘上的文件来访问数据。

TiKV 从 v4.0.0 起支持静态加密，即在 [CTR](https://zh.wikipedia.org/wiki/%E5%88%86%E7%BB%84%E5%AF%86%E7%A0%81%E5%B7%A5%E4%BD%9C%E6%A8%A1%E5%BC%8F) 模式下使用 [AES](https://zh.wikipedia.org/wiki/%E9%AB%98%E7%BA%A7%E5%8A%A0%E5%AF%86%E6%A0%87%E5%87%86) 对数据文件进行透明加密。要启用静态加密，用户须提供一个加密密钥，即主密钥。可以通过 AWS Key Management Service（推荐），即 KMS，提供主密钥 (master key)，也可以指定将密钥以明文形式存储在文件中。TiKV 自动轮换 (rotate) 用于加密实际数据文件的密钥，主密钥则可以由用户手动轮换。请注意，静态加密仅加密静态数据（即磁盘上的数据），而不加密网络传输中的数据。建议 TLS 与静态加密一起使用。

同样，从 v4.0.0 起，Backup & Restore (BR) 支持对备份到 S3 的数据进行 S3 服务端加密 (SSE)。BR S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥进行加密。

## 注意事项及使用限制

当前版本 (v4.0.0) 的 TiKV 加密功能还有待改善，需要在启用加密前注意以下事项：

* TiDB 集群部署后，大部分用户数据都存储在 TiKV 节点上。这部分数据可使用加密功能进行加密。但有少量元数据存储在 PD 节点上（例如用作 TiKV Region 边界的二级索引键）。截至 v4.0.0，PD 尚未支持静态加密功能。建议使用存储级加密（例如文件系统加密）来保护存储在 PD 中的敏感数据。
* TiFlash 从 v4.0.5 开始支持静态加密功能，详情参阅 [TiFlash 静态加密](/encryption-at-rest.md#tiflash-静态加密-从-v405-版本开始引入)。TiKV 与 v4.0.5 之前版本的 TiFlash 一起部署时，存储在 TiFlash 中的数据不会被加密。
* TiKV 当前不从核心转储 (core dumps) 中排除加密密钥和用户数据。建议在使用静态加密时禁用 TiKV 进程的核心转储。
* TiKV 使用文件的绝对路径跟踪已加密的数据文件。一旦 TiKV 节点开启了加密功能，用户就不应更改数据文件的路径配置，例如 `storage.data-dir`、`raftstore.raftdb-path`、`rocksdb.wal-dir` 和 `raftdb.wal-dir`。
* TiKV 信息日志包含用于调试的用户数据。信息日志不会被加密。

## 功能概述

TiKV 当前支持的加密算法包括 AES128-CTR、AES192-CTR 和 AES256-CTR。TiKV 使用信封加密 (envelop encryption)，所以启用加密后，TiKV 使用以下两种类型的密钥：

* 主密钥 (master key)：主密钥由用户提供，用于加密 TiKV 生成的数据密钥。用户在 TiKV 外部进行主密钥的管理。
* 数据密钥 (data key)：数据密钥由 TiKV 生成，是实际用于加密的密钥。TiKV 会自动轮换数据密钥。

多个 TiKV 实例可共用一个主密钥。在生产环境中，推荐通过 AWS KMS 提供主密钥。首先通过 AWS KMS 创建用户主密钥 (CMK)，然后在配置文件中将 CMK 密钥的 ID 提供给 TiKV。TiKV 进程在运行时可以通过 [IAM 角色](https://aws.amazon.com/iam/)访问 KMS CMK。如果 TiKV 无法访问 KMS CMK，TiKV 就无法启动或重新启动。详情参阅 AWS 文档中的 [KMS](https://docs.aws.amazon.com/zh_cn/kms/index.html) and [IAM](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/introduction.html)。

用户也可以通过文件形式提供主密钥。该文件须包含一个用十六进制字符串编码的 256 位（32 字节）密钥，并以换行符结尾（即 `\n`），且不包含其他任何内容。将密钥存储在磁盘上会泄漏密钥，因此密钥文件仅适合存储在 RAM 内存的 `tempfs` 中。

数据密钥由 TiKV 生成并传递给底层存储引擎（即 RocksDB）。RocksDB 写入的所有文件，包括 SST 文件，WAL 文件和 MANIFEST 文件，均由当前数据密钥加密。TiKV 使用的其他临时文件（可能包括用户数据）也由相同的数据密钥加密。默认情况下，TiKV 每周自动轮换数据密钥，但是该时间段是可配置的。密钥轮换时，TiKV 不会重写全部现有文件来替换密钥，但如果集群的写入量恒定，则 RocksDB compaction 会将使用最新的数据密钥对数据重新加密。TiKV 跟踪密钥和加密方法，并使用密钥信息对读取的内容进行解密。

无论用户配置了哪种数据加密方法，数据密钥都使用 AES256-GCM 算法进行加密，以方便对主密钥进行验证。所以当使用文件而不是 KMS 方式指定主密钥时，主密钥必须为 256位（32字节）。

## 配置加密

要启用加密，你可以在 TiKV 的配置文件中添加加密部分：

```
[security.encryption]
data-encryption-method = aes128-ctr
data-key-rotation-period = 7d
```

`data-encryption-method` 的可选值为 `"aes128-ctr"`、`"aes192-ctr"`、`"aes256-ctr"` 和 `"plaintext"`。默认值为 `"plaintext"`，即默认不开启加密功能。`data-key-rotation-period` 指定 TiKV 轮换密钥的频率。可以为新 TiKV 群集或现有 TiKV 群集开启加密，但只有启用后写入的数据才保证被加密。要禁用加密，请在配置文件中删除 `data-encryption-method`，或将该参数值为 `"plaintext"`，然后重启 TiKV。

如果启用了加密（即 `data-encryption-method` 的值不是 `"plaintext"`），则必须指定主密钥。要使用 AWS KMS 方式指定为主密钥，请在 `[security.encryption]` 部分之后添加 `[security.encryption.master-key]` 部分：

```
[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
endpoint = "https://kms.us-west-2.amazonaws.com"
```

`key-id` 指定 KMS CMK 的密钥 ID。`region` 为 KMS CMK 的 AWS 区域名。除非你使用非 AWS 提供的 AWS KMS 兼容服务， `endpoint` 通常无需指定。

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

## 轮换主密钥

要轮换主密钥，你必须在配置中同时指定新的主密钥和旧的主密钥，然后重启 TiKV。用 `security.encryption.master-key` 指定新的主密钥，用 `security.encryption.previous-master-key` 指定旧的主密钥。`security.encryption.previous-master-key` 配置的格式与 `encryption.master-key` 相同。重启时，TiKV 必须能同时访问旧主密钥和新主密钥，但一旦 TiKV 启动并运行，就只需访问新密钥。此后，可以将 `encryption.previous-master-key` 项保留在配置文件中。即使重启时，TiKV 也只会在无法使用新的主密钥解密现有数据时尝试使用旧密钥。

TiKV 当前不支持在线轮换主密钥，因此你需要重启 TiKV 进行主密钥轮换。建议对运行中的、提供在线查询的 TiKV 集群进行滚动重启。

轮换 KMS CMK 的配置示例如下：

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

## 监控和调试

要监控静态加密（如果 TiKV 中部署了 Grafana 组件），可以查看 **TiKV-Details** -> **Encryption** 面板中的监控项：

* Encryption initialized：如果在 TiKV 启动期间初始化了加密，则为 `1`，否则为 `0`。进行主密钥轮换时可通过该监控项确认主密钥轮换是否已完成。
* Encryption data keys：现有数据密钥的数量。每次轮换数据密钥后，该数字都会增加 `1`。通过此监控指标可以监测数据密钥是否按预期轮换。
* Encrypted files：当前的加密数据文件数量。为先前未加密的群集启用加密时，将此数量与数据目录中的当前数据文件进行比较，可通过此监控指标估计已经被加密的数据量。
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

## BR S3 服务端加密

使用 BR 备份数据到 S3 时，若要启用 S3 服务端加密，需要传递 `--s3.sse` 参数并将参数值设置为 `aws:kms`。S3 将使用自己的 KMS 密钥进行加密。示例如下：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms
```

若要使用用户创建和拥有的自定义 AWS KMS CMK，需另外传递 `--s3.sse-kms-key-id` 参数。此时，BR 进程和集群中的所有 TiKV 节点都需访问该 KMS CMK（例如，通过 AWS IAM），并且该 KMS CMK 必须与存储备份的 S3 bucket 位于同一 AWS 区域。建议通过 AWS IAM 向 BR 进程和 TiKV 节点授予对 KMS CMK 的访问权限。参见 AWS 文档中的 [IAM](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/introduction.html)。示例如下：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.region <region> --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

恢复备份时，不需要也不可指定 `--s3.sse` 和 `--s3.sse-kms-key-id` 参数。S3 将自动相应进行解密。用于恢复备份数据的 BR 进程和集群中的 TiKV 节点也需要访问 KMS CMK，否则恢复将失败。示例如下：

```
./br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix> --s3.region <region>"
```

## TiFlash 静态加密 <span class="version-mark">从 v4.0.5 版本开始引入</span>

TiFlash 从 v4.0.5 起支持静态加密。数据密钥由 TiFlash 生成。TiFlash（包括 TiFlash Proxy）写入的所有文件，包括数据文件、Schema 文件、临时文件等，均由当前数据密钥加密。TiFlash 支持的加密算法、加密配置方法（配置项在 `tiflash-learner.toml` 中）和监控项含义等均与 TiKV 一致。

如果 TiFlash 中部署了 Grafana 组件，可以查看 **TiFlash-Proxy-Details** -> **Encryption**。
