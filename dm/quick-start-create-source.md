---
title: Create a Data Source for TiDB Data Migration
summary: Learn how to create a data source for Data Migration (DM).
---

# Create a Data Source for TiDB Data Migration

> **Note:**
>
> Before creating a data source, you need to [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md).

The document describes how to create a data source for the data migration task of TiDB Data Migration (DM).

A data source contains the information for accessing the upstream migration task. Because a data migration task requires referring its corresponding data source to obtain the configuration information of access, you need to create the data source of a task before creating a data migration task. For specific data source management commands, refer to [Manage Data Source Configurations](/dm/dm-manage-source.md).

## Step 1: Configure the data source

1. (optional) Encrypt the data source password

    In DM configuration files, it is recommended to use the password encrypted with dmctl. You can follow the example below to obtain the encrypted password of the data source, which can be used to write the configuration file later.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

    ```
    MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
    ```

2. Write the configuration file of the data source

    For each data source, you need an individual configuration file to create it. You can follow the example below to create a data source whose ID is "mysql-01". First create the configuration file `./source-mysql-01.yaml`:

    ```yaml
    source-id: "mysql-01"    # The ID of the data source, you can refer this source-id in the task configuration and dmctl command to associate the corresponding data source.

    from:
      host: "127.0.0.1"
      port: 3306
      user: "root"
      password: "MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=" # The user password of the upstream data source. It is recommended to use the password encrypted with dmctl.
      security:                                        # The TLS configuration of the upstream data source. If not necessary, it can be deleted.
        ssl-ca: "/path/to/ca.pem"
        ssl-cert: "/path/to/cert.pem"
        ssl-key: "/path/to/key.pem"
    ```

## Step 2: Create a data source

You can use the following command to create a data source:

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr <master-addr> operate-source create ./source-mysql-01.yaml
```

For other configuration parameters, refer to [Upstream Database Configuration File](/dm/dm-source-configuration-file.md).

The returned results are as follows:

{{< copyable "" >}}

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

## Step 3: Query the data source you created

After creating a data source, you can use the following command to query the data source:

- If you konw the `source-id` of the data source, you can use the `dmctl config source <source-id>` command to directly check the configuration of the data source:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> config source mysql-01
    ```

    ```
    {
      "result": true,
      "msg": "",
      "cfg": "enable-gtid: false
        flavor: mysql
        source-id: mysql-01
        from:
          host: 127.0.0.1
          port: 3306
          user: root
          password: '******'
    }
    ```

- If you do not know the `source-id`, you can use the `dmctl operate-source show` command to check the source database list, from which you can find the corresponding data source.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> operate-source show
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "source is added but there is no free worker to bound",
                "source": "mysql-02",
                "worker": ""
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-01",
                "worker": "dm-worker-1"
            }
        ]
    }
    ```
