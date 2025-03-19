---
title: TRAFFIC CAPTURE
summary: TiDB 数据库中 TRAFFIC CAPTURE 的使用概况。
---

# TRAFFIC CAPTURE

TiDB v9.0.0 引入了 `TRAFFIC CAPTURE` 语法，用于向集群中所有 [TiProxy](/tiproxy/tiproxy-overview.md) 实例发送请求，使 TiProxy 捕获客户端流量并保存到流量文件。

TiProxy 支持将流量捕获到本地存储或外部存储。捕获流量到本地时，需要在捕获流量之后手动将流量文件复制到回放的 TiProxy 集群上。而使用外部存储时则无需手动复制。

TiProxy 支持的外部存储包括 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage，以及兼容 S3 协议的其他文件存储服务。关于外部存储，请参见[外部存储服务的 URI 格式](/external-storage-uri.md)。

`TRAFFIC CAPTURE` 支持以下选项：

- `DURATION`：（必填）指定捕获的时长。可选单位为 `m`（分钟）、`h`（小时）或 `d`（天）。例如，`DURATION="1h"` 表示指定捕获一小时的流量。
- `COMPRESS`：（可选）指定是否压缩流量文件。`true` 表示压缩，压缩格式为 gzip。`false` 表示不压缩。默认值为 `true`。
- `ENCRYPTION_METHOD`：（可选）指定加密流量文件的算法。仅支持 `""`、`plaintext` 和 `aes256-ctr`。其中，`""` 和 `plaintext` 表示不加密，`aes256-ctr` 表示使用 AES256-CTR 算法加密。指定加密时，需要同时配置 [`encrytion-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path)。默认值为 `""`。

捕获流量要求当前用户具有 `SUPER` 或 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限。

## 语法图

```ebnf+diagram
TrafficStmt ::=
    "TRAFFIC" "CAPTURE" "TO" stringLit TrafficCaptureOptList

TrafficCaptureOptList ::=
    TrafficCaptureOpt
|   TrafficCaptureOptList TrafficCaptureOpt

TrafficCaptureOpt ::=
    "DURATION" EqOpt stringLit
|   "ENCRYPTION_METHOD" EqOpt stringLit
|   "COMPRESS" EqOpt Boolean
```

## 示例

捕获 1 天流量到 TiProxy 实例的本地 `/tmp/traffic` 目录：

```sql
TRAFFIC CAPTURE TO "/tmp/traffic" DURATION="1d";
```

捕获 10 分钟流量到 S3：

```sql
TRAFFIC CAPTURE TO "s3://external/traffic?access-key=${access-key}&secret-access-key=${secret-access-key}" DURATION="10m";
```

捕获时，流量文件自动加密，但不自动压缩：

```sql
TRAFFIC CAPTURE TO "/tmp/traffic" DURATION="1h" COMPRESS=false ENCRYPTION_METHOD="aes256-ctr";
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [TiProxy 流量回放](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
