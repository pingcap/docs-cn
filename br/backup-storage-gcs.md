---
title:  使用 BR 在 Google Cloud Storage 备份和恢复数据
summary: 介绍使用 BR 在外部存储 GCS 上进行备份与恢复时的方法。
---

# 使用 BR 在 Google Cloud Storage 备份和恢复数据

TiDB 备份恢复功能 (BR，Backup & Restore) 支持将 Google Cloud Storage 作为外部存储来进行数据备份与恢复。

## 使用场景

使用 Google Cloud Storage 保存备份数据。方便你将部署在 GCE 上的 TiDB 集群数据快速备份到 gcs 中，或者从 gcs 中快速恢复出来一个 TiDB 集群。

## 备份数据到 GCS

{{< copyable "shell-regular" >}}

```shell
br backup full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

备份数据到 GCS 的时候需要在 br 运行节点放置 credentials 文件。 credentials 文件包含访问 GCS 的账户凭证。 显示指定参数 `--send-credentials-to-tikv`, 表示将 GCS 的账户访问凭证传递给 TiKV 节点。

如果你需要获取 credentials 文件可以参考 [CREATE AND DOWNLOAD THE GCS CREDENTIALS FILE](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/google_cloud_backup_guide/creds).

## 从 GCS 恢复集群数据

```shell
br restore full --pd "${PDIP}:2379" --Storage 'gcs://bucket-name/prefix?credentials-file=${credentials-file-path}' --send-credentials-to-tikv=true
```

## 探索更多

如需了解 BR 支持的其他外部存储，请参阅[外部存储](/br/backup-and-restore-storages.md)。
