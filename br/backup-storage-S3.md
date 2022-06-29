---
title: Back Up and Restore Data on Amazon S3 Using BR
summary: Learn how to use BR to back up data to and restore data from Amazon S3 storage.
---

# Back Up and Restore Data on Amazon S3 Using BR

The Backup & Restore (BR) tool supports using Amazon S3 or other Amazon S3-compatible file storages as the external storage for backing up and restoring data.

## Application scenarios

By using Amazon S3, you can quickly back up the data of a TiDB cluster deployed on Amazon EC2 to Amazon S3, or quickly restore a TiDB cluster from the backup data in Amazon S3.

## Configure privileges to access S3

Before performing backup or restoration using S3, you need to configure the privileges required to access S3.

### Configure access to the S3 directory

Before backup, configure the following privileges to access the backup directory on S3.

- Minimum privileges for TiKV and BR to access the backup directories of `s3:ListBucket`, `s3:PutObject`, and `s3:AbortMultipartUpload` during backup 
- Minimum privileges for TiKV and BR to access the backup directories of `s3:ListBucket` and `s3:GetObject` during restoration

If you have not yet created a backup directory, refer to [AWS Official Document](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) to create an S3 bucket in the specified region. If necessary, you can also create a folder in the bucket by referring to [AWS official documentation - Create Folder](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html).

### Configure a user to access S3

It is recommended that you configure access to S3 using either of the following ways:

- Associate an IAM role that can access S3 with the EC2 instances where the TiKV and BR nodes run. After the association, BR can access the backup directories of S3.

    {{< copyable "shell-regular" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}" --s3.region "${region}"
    ```

- Configure `access-key` and `secret-access-key` for accessing S3 in the `br` CLI, and set `--send-credentials-to-tikv=true` to pass the access key from BR to each TiKV.

    {{< copyable "shell-regular" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" --s3.region "${region}" --send-credentials-to-tikv=true
    ```

Because the access key in a command is vulnerable to leakage, you are recommended to associate an IAM role to EC2 instances to access S3.

## Back up data to S3

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

In the preceding command:

- `--s3.region`: specifies the region of S3.
- `--send-credentials-to-tikv`: specifies that access key is passed to the TiKV nodes.

## Restore data from S3

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

## See also

To know more information about external storages supported by BR, see [External storages](/br/backup-and-restore-storages.md).
