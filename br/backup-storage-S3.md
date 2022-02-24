---
title:  使用 S3 存储备份数据
summary: 介绍使用 BR 在外部存储 S3 上进行备份与恢复时的方法。
---

# 在 AWS 上进行备份恢复

TiDB 备份恢复功能 (BR) 支持将 Amazon S3 ，或支持 S3 协议的其他文件存储，作部存储来保存备份数据。

如需了解 BR 支持的其他外部存储，请参阅[外部存储](/br/backup-and-restore-storages.md)。

## 使用场景

使用 AWS S3 保存备份数据。方便你将部署在 AWS EC2 上的 TiDB 集群数据快速备份到 AWS S3 中，或者从 S3 中快速恢复出来一个 TiDB 集群。

## 配置访问 S3 权限

进行备份恢复之前需要先配置访问 S3 的权限。

### S3 目录访问权限

在备份之前，需要为 BR 访问 S3 中的备份目录设置相应的访问权限。

如果你还没有创建备份数据保存目录，你可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的 `Region` 区域中创建一个 S3 桶 `Bucket`；如果有需要，还可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)在 Bucket 中创建一个文件夹 `Folder`。

- 备份的时候，TiKV 和 BR 需要的最小权限，赋予备份数据目录 `s3:ListBucket`，`s3:PutObject` 和 `s3:AbortMultipartUpload`；
- 恢复的时候，TiKV 和 BR 需要的最小权限，赋予备份数据目录 `s3:ListBucket` 和 `s3:GetObject`。

### 配置访问 S3 的账户

推荐使用以下两种方式配置 S3 的账户

- 为运行 TiKV 和 BR 的 EC2 实例关联一个配置了访问 S3 访问权限的 IAM role，正确设置后，BR 可以直接访问对应的 S3 中的备份目录，而不需要额外的设置。

  {{< copyable "shell-regular" >}}

  ```shell
  br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}" --s3.region "${region}"
  ```

- 通过 `br` 命令行参数设置访问 S3 的 `access-key` 和 `serect-acccess-key`, 同时设置 `--send-credentials-to-tikv=true` 将 access key 从 BR 传递到每个 TiKV 上。

  {{< copyable "shell-regular" >}}

  ```shell
  br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" --s3.region "${region}" --send-credentials-to-tikv=true
  ```

在通常情况下，为了避免 `access-key` 等密钥信息记录在命令行中被泄漏，推荐使用为 EC2 实例关联 IAM role 的方法。 

## 备份数据到 S3

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --s3.region "${region}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backuptable.log
```

在进行 BR 备份和恢复时，显示指定参数 `--s3.region` 和 `--send-credentials-to-tikv`, `--s3.region` 表示 S3 存储所在的区域，`--send-credentials-to-tikv` 表示将 S3 的访问权限传递给 TiKV 节点。

## 从 S3 恢复集群

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

## 其他资料

- 如需了解 BR 支持的其他外部存储，请参阅[外部存储](/br/backup-and-restore-storages.md)。
