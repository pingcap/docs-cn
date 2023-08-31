---
title: ticloud import start mysql
summary: The reference of `ticloud import start mysql`.
---

# ticloud import start mysql

Import a table from a MySQL-compatible database to a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster:

```shell
ticloud import start mysql [flags]
```

> **Note:**
>
> - Before running this command, make sure that you have installed the MySQL command-line tool first. For more details, see [Installation](/tidb-cloud/get-started-with-cli.md#installation).
> - If the target table already exists in the target database, to use this command for table import, make sure that the target table name is the same as the source table name and add the `skip-create-table` flag in the command.
> - If the target table does not exist in the target database, executing this command automatically creates a table with the same name as the source table in the target database.

## Examples

- Start an import task in interactive mode:

    ```shell
    ticloud import start mysql
    ```

- Start an import task in non-interactive mode (using the TiDB Serverless cluster default user `<username-prefix>.root`):

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password>
    ```

- Start an import task in non-interactive mode (using a specific user):

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --target-user <target-user>
    ```

- Start an import task that skips creating the target table if it already exists in the target database:

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --skip-create-table
    ```

> **Note:**
>
> MySQL 8.0 uses `utf8mb4_0900_ai_ci` as the default collation, which is currently not supported by TiDB. If your source table uses the `utf8mb4_0900_ai_ci` collation, before the import, you need to either alter the source table collation to a [supported collation of TiDB](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb) or manually create the target table in TiDB.

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag | Description | Required | Note |
|---|---|---|---|
| -c, --cluster-id string | Specifies the cluster ID. | Yes | Only works in non-interactive mode. |
| -h, --help | Displays help information for this command. | No | Works in both non-interactive and interactive modes. |
| -p, --project-id string | Specifies the project ID. | Yes | Only works in non-interactive mode. |
| --skip-create-table | Skips creating the target table if it already exists in the target database. | No | Only works in non-interactive mode. |
| --source-database string | The name of the source MySQL database. | Yes | Only works in non-interactive mode. |
| --source-host string | The host of the source MySQL instance. | Yes | Only works in non-interactive mode. |
| --source-password string | The password for the source MySQL instance. | Yes | Only works in non-interactive mode. |
| --source-port int | The port of the source MySQL instance. | Yes | Only works in non-interactive mode. |
| --source-table string | The source table name in the source MySQL database. | Yes | Only works in non-interactive mode. |
| --source-user string | The user to log in to the source MySQL instance. | Yes | Only works in non-interactive mode. |
| --target-database string | The target database name in the TiDB Serverless cluster. | Yes | Only works in non-interactive mode. |
| --target-password string | The password for the target TiDB Serverless cluster. | Yes | Only works in non-interactive mode. |
| --target-user string | The user to log in to the target TiDB Serverless cluster. | No | Only works in non-interactive mode. |

## Inherited flags

| Flag | Description | Required | Note |
|---|---|---|---|
| --no-color | Disables color in output. | No | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No | Works in both non-interactive and interactive modes. |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
