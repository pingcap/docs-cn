---
title: ticloud cluster connect-info
summary: The reference of `ticloud cluster connect-info`.
---

# ticloud cluster connect-info

Get the connection string of a cluster:

```shell
ticloud cluster connect-info [flags]
```

> **Note:**
>
> Currently, this command only supports getting the connection string of a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster.

## Examples

Get the connection string of a cluster in interactive mode:

```shell
ticloud cluster connect-info
```

Get the connection string of a cluster in non-interactive mode:

```shell
ticloud cluster connect-info --project-id <project-id> --cluster-id <cluster-id> --client <client-name> --operating-system <operating-system>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                       | Description                                                                                                                                                                                                                                                                                                                                                                | Required | Note                                                 |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -p, --project-id string    | The ID of the project, in which the cluster is created                                                                                                                                                                                                                                                                                                                | Yes      | Only works in non-interactive mode.                  |
| -c, --cluster-id string    | The ID of the cluster                                                                                                                                                                                                                                                                                                                                                      | Yes      | Only works in non-interactive mode.                  |
| --client string            | The desired client used for the connection. Supported clients include `general`, `mysql_cli`, `mycli`, `libmysqlclient`, `python_mysqlclient`, `pymysql`, `mysql_connector_python`, `mysql_connector_java`, `go_mysql_driver`, `node_mysql2`, `ruby_mysql2`, `php_mysqli`, `rust_mysql`, `mybatis`, `hibernate`, `spring_boot`, `gorm`, `prisma`, `sequelize_mysql2`, `django_tidb`, `sqlalchemy_mysqlclient`, and `active_record`. | Yes      | Only works in non-interactive mode.                  |
| --operating-system string  | The operating system name. Supported operating systems include `macOS`, `Windows`, `Ubuntu`, `CentOS`, `RedHat`, `Fedora`, `Debian`, `Arch`, `OpenSUSE`, `Alpine`, and `Others`.                                                                                                                    | Yes      | Only works in non-interactive mode.                  |
| -h, --help                 | Help information for this command                                                                                                                                                                                                                                                                                                                                          | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                           | Required | Note                                                                                                              |
|----------------------|-------------------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                             | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components.  |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command.  | No       | Works in both non-interactive and interactive modes.                                                              |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
