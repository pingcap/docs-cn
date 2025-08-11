# TiDB 安全增强模式 (SEM)

## 概述与目的

安全增强模式 (Security Enhanced Mode, SEM) 主要目的是限制包括 `root` 用户在内的所有用户的能力。

此功能在数据库即服务 (DBaaS) 环境中尤为关键。服务提供商可以为租户提供其数据库的 `root` 访问权限——确保与应用程序的兼容性——同时防止他们执行可能危及底层集群安全性、稳定性或数据隔离的命令。

SEM 可以通过两种方式启用：一种是具有预定义限制集的默认模式，另一种是使用配置文件实现详细安全策略的自定义模式。

## 启用和配置 SEM

通过在 TiDB 服务器的配置文件 (`tidb.toml`) 中设置 `security.enable-sem = true` 来启用 SEM。SEM 的具体行为取决于你是否同时提供了配置文件。

你可以通过检查 `tidb_enable_enhanced_security` 系统变量来验证哪种模式处于活动状态。

```sql
SELECT @@tidb_enable_enhanced_security;
```

### 模式 1：默认限制

此模式提供了一套基准的安全增强功能，主要削弱了 `SUPER` 权限的广泛权力，并用细粒度的权限取而代之。

  * 激活方式：在 `tidb.toml` 中设置 `enable-sem = true`，但不设置 `sem-config` 路径。
  * 系统变量：`tidb_enable_enhanced_security` 将为 `ON`。

在此模式下，将强制执行以下限制：

| 受限操作 | 豁免所需的权限 |
| :------------------------------------------------------------------------------------------------------------ | :------------------------------- |
| 向 `mysql` schema 中的系统表写入数据，以及查看 `information_schema` 表中的敏感列。 | `RESTRICTED_TABLES_ADMIN` |
| 在 `SHOW STATUS` 中查看敏感变量。 | `RESTRICTED_STATUS_ADMIN` |
| 查看和设置敏感的系统变量。 | `RESTRICTED_VARIABLES_ADMIN` |
| 删除或修改持有 `RESTRICTED_USER_ADMIN` 权限的用户帐户。 | `RESTRICTED_USER_ADMIN` |

### 模式 2：通过配置文件进行自定义限制

此模式启用一个在 JSON 文件中定义的可定制的安全策略。它提供了对表、变量、权限和 SQL 命令的精细控制。

  * 激活方式：在 `tidb.toml` 中同时设置 `enable-sem = true` 和 `sem-config = '/path/to/your/sem-policy.json'`。
  * 系统变量：`tidb_enable_enhanced_security` 将为 `CONFIG`。

任何配置更改都需要重启 TiDB 集群才能生效。

## 自定义策略功能参考 (模式 2)

以下各节详细介绍了使用自定义配置文件（模式 2）时可用的功能。

### 限制对表和数据库的访问

此功能可防止访问指定的数据库或单个表。

  * 配置：
      * `restricted_databases`：一个数据库名称数组。这些数据库中的所有表都将变得不可访问。
      * `restricted_tables`：一个指定 `schema` 和 `name` 的对象数组。可选的 `"hidden": true` 标志会使表不可见。
  * 豁免权限：`RESTRICTED_TABLES_ADMIN`
  * 配置示例：
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_databases": ["mysql"],
      "restricted_tables": [{"schema": "information_schema", "name": "columns", "hidden": true}]
    }
    ```
    作为受限用户（例如 `root`）：
    ```
    mysql> select * from information_schema.columns;
    ERROR 1142 (42000): SELECT command denied to user 'root'@'%' for table 'columns'
    mysql> use mysql;
    ERROR 1044 (42000): Access denied for user 'root'@'%' to database 'mysql'
    ```

### 限制系统变量

此功能通过隐藏、设为只读或掩盖其值来控制与系统变量的交互。

  * 配置：`restricted_variables` 键包含一个带有控制标志的变量对象数组：
      * `"hidden": true`：变量不可访问。
      * `"readonly": true`：变量可以读取但不能修改。
      * `"value": "string"`：覆盖变量的返回值。注意：此选项仅支持本地只读变量。
  * 豁免权限：`RESTRICTED_VARIABLES_ADMIN`
  * 配置示例：
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_variables": [
        {"name": "tidb_config", "hidden": true},
        {"name": "hostname", "hidden": false, "value": "testhostname"}
      ]
    }
    ```
    作为受限用户（例如 `root`）：
    ```
    mysql> SELECT @@tidb_config;
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_VARIABLES_ADMIN privilege(s) for this operation
    mysql> SELECT @@hostname;
    +--------------+
    | @@hostname   |
    +--------------+
    | testhostname |
    +--------------+
    1 row in set (0.00 sec)
    ```

### 限制权限和用户管理

此功能可防止授予强大的权限，并保护管理帐户不被更改或删除。

  * 配置：`restricted_privileges` 键包含一个权限名称数组。一旦列出，该权限就不能被授予。列出 `RESTRICTED_USER_ADMIN` 本身可以保护持有该权限的用户。
  * 豁免权限：`RESTRICTED_PRIV_ADMIN`
  * 配置示例：
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_privileges": ["FILE"]
    }
    ```
    作为受限用户（例如 `root`）：
    ```
    mysql> GRANT FILE ON *.* TO 'some_user'@'%';
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_PRIV_ADMIN privilege(s) for this operation
    -- 假设 'sem_admin' 拥有 RESTRICTED_USER_ADMIN 权限，尝试删除该用户
    mysql> DROP USER 'sem_admin'@'%';
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_USER_ADMIN privilege(s) for this operation
    ```

### 限制状态变量

此功能可从 `SHOW STATUS` 的输出中过滤敏感的数据。

  * 配置：
      * `restricted_status_variables`：一个状态变量名称数组，用于在 `SHOW STATUS` 中隐藏。
  * 豁免权限：`RESTRICTED_STATUS_ADMIN`
  * 配置示例：
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_status_variables": ["tidb_gc_leader_desc"]
    }
    ```
    作为受限用户（例如 `root`）：
    ```
    mysql> SHOW STATUS LIKE 'tidb_gc_leader_desc';
    Empty set (0.01 sec)
    ```

### 限制 SQL 命令

此功能可阻止执行特定的 SQL 语句或整类命令。

  * 配置：
      * `restricted_sql`：一个包含两个数组的对象：
          * `sql`：要阻止的特定 SQL 命令列表（例如 `BACKUP`、`RESTORE`）。
          * `rule`：一个预定义的规则名称列表，用于阻止特定类别的语句。支持的规则有：
              * `time_to_live`：阻止与表 TTL 相关的 DDL 语句。
              * `alter_table_attributes`：阻止 `ALTER TABLE ... ATTRIBUTES="..."` 语句。
              * `import_with_external_id`：阻止使用 S3 `EXTERNAL_ID` 的 `IMPORT INTO` 语句。
              * `select_into_file`：阻止 `SELECT ... INTO OUTFILE` 语句。
              * `import_from_local`：阻止 `LOAD DATA LOCAL INFILE` 和从本地文件路径 `IMPORT INTO`。
  * 豁免权限：`RESTRICTED_SQL_ADMIN`
  * 配置示例：
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_sql": {
        "rule": ["time_to_live"],
        "sql": ["BACKUP"]
      }
    }
    ```
    作为受限用户（例如 `root`）：
    ```
    mysql> BACKUP DATABASE `test` TO 's3://bucket/backup';
    ERROR 8132 (HY000): Feature 'BACKUP DATABASE `test` TO 's3://bucket/backup'' is not supported when security enhanced mode is enabled
    mysql> CREATE TABLE test.t1 (id INT, created_at TIMESTAMP) TTL = `created_at` + INTERVAL 1 DAY;
    ERROR 8132 (HY000): Feature 'CREATE TABLE test.t1 (id INT, created_at TIMESTAMP) TTL = `created_at` + INTERVAL 1 DAY' is not supported when security enhanced mode is enabled
    ```
