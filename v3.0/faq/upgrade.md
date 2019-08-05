---
title: FAQs After Upgrade
summary: Learn about the FAQs after upgrading TiDB.
category: faq
aliases: ['/docs/op-guide/upgrade-faq/','/docs/faq/upgrades/','/docs/faq/upgrade/']
---

# FAQs After Upgrade

This document lists some FAQs and their solutions after you upgrade TiDB.

## The character set (charset) errors when executing DDL operations

In v2.1.0 and earlier versions (including all versions of v2.0), the character set of TiDB is UTF-8 by default. But starting from v2.1.1, the default character set has been changed into UTF8MB4.

If you explicitly specify the charset of a newly created table as UTF-8 in v2.1.0 or earlier versions, then you might fail to execute DDL operations after upgrading TiDB to v2.1.1.

To avoid this issue, you need to pay attention to:

- Point #1: before v2.1.3, TiDB does not support modifying the charset of the column. Therefore, when you execute DDL operations, you need to make sure that the charset of the new column is consistent with that of the original column.

- Point #2: before v2.1.3, even if the charset of the column is different from that of the table, `show create table` does not show the charset of the column. But as shown in the following example, you can view it by obtaining the metadata of the table through the HTTP API.

### Issue #1: `unsupported modify column charset utf8mb4 not match origin utf8`

- Before upgrading, the following operations are executed in v2.1.0 and earlier versions.

    ```sql
    tidb > create table t(a varchar(10)) charset=utf8;
    Query OK, 0 rows affected
    Time: 0.106s
    tidb > show create table t
    +-------+-------------------------------------------------------+
    | Table | Create Table                                          |
    +-------+-------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                    |
    |       |   `a` varchar(10) DEFAULT NULL                        |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
    +-------+-------------------------------------------------------+
    1 row in set
    Time: 0.006s
    ```

- After upgrading, the following error is reported in v2.1.1 and v2.1.2 but there is no such error in v2.1.3 and the later versions.

    ```sql
    tidb > alter table t change column a a varchar(20);
    ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8
    ```

Solution:

You can explicitly specify the column charset as the same with the original charset.

```sql
alter table t change column a a varchar(22) character set utf8;
```

- According to Point #1, if you do not specify the column charset, UTF8MB4 is used by default, so you need to specify the column charset to make it consistent with the original one.

- According to Point #2, you can obtain the metadata of the table through the HTTP API, and find the column charset by searching the column name and the keyword "Charset".

    ```sh
    ▶ curl "http://$IP:10080/schema/test/t" | python -m json.tool  # A python tool is used here to format JSON, which is not required and only for the convenience to add comments.
    {
        "ShardRowIDBits": 0,
        "auto_inc_id": 0,
        "charset": "utf8",   # The charset of the table.
        "collate": "",
        "cols": [            # The relevant information about the columns.
            {
                ...
                "id": 1,
                "name": {
                    "L": "a",
                    "O": "a"   # The column name.
                },
                "offset": 0,
                "origin_default": null,
                "state": 5,
                "type": {
                    "Charset": "utf8",   # The charset of column a.
                    "Collate": "utf8_bin",
                    "Decimal": 0,
                    "Elems": null,
                    "Flag": 0,
                    "Flen": 10,
                    "Tp": 15
                }
            }
        ],
        ...
    }
    ```

### Issue #2: `unsupported modify charset from utf8mb4 to utf8`

- Before upgrading, the following operations are executed in v2.1.1 and v2.1.2.

    ```sql
    tidb > create table t(a varchar(10)) charset=utf8;
    Query OK, 0 rows affected
    Time: 0.109s
    tidb > show create table t
    +-------+-------------------------------------------------------+
    | Table | Create Table                                          |
    +-------+-------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                    |
    |       |   `a` varchar(10) DEFAULT NULL                        |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
    +-------+-------------------------------------------------------+
    ```

    In the above example, `show create table` only shows the charset of the table, but the charset of the column is actually UTF8MB4, which can be confirmed by obtaining the schema through the HTTP API. However, when a new table is created, the charset of the column should stay consistent with that of the table. This bug has been fixed in v2.1.3.

- After upgrading, the following operations are executed in v2.1.3 and the later versions.

    ```sql
    tidb > show create table t
    +-------+--------------------------------------------------------------------+
    | Table | Create Table                                                       |
    +-------+--------------------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                                 |
    |       |   `a` varchar(10) CHARSET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin              |
    +-------+--------------------------------------------------------------------+
    1 row in set
    Time: 0.007s
    tidb > alter table t change column a a varchar(20);
    ERROR 1105 (HY000): unsupported modify charset from utf8mb4 to utf8
    ```

Solution:

- Starting from v2.1.3, TiDB supports modifying the charsets of the column and the table, so it is recommended to modify the table charset into UTF8MB4.

    ```sql
    alter table t convert to character set utf8mb4;
    ```

- You can also specify the column charset as done in Issue #1, making it stay consistent with the original column charset (UTF8MB4).

    ```sql
    alter table t change column a a varchar(20) character set utf8mb4;
    ```

### Issue #3: `ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a`

In TiDB v2.1.1 and earlier versions, if the charset is UTF-8, there is no UTF-8 Unicode encoding check on the inserted 4-byte data. But in v2.1.2 and the later versions, this check is added.

- Before upgrading, the following operations are executed in v2.1.1 and earlier versions.

    ```sql
    tidb> create table t(a varchar(100) charset utf8);
    Query OK, 0 rows affected
    tidb> insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

- After upgrading, the following error is reported in v2.1.2 and the later versions.

    ```sql
    tidb> insert t values (unhex('f09f8c80'));
    ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a
    ```

Solution:

- In v2.1.2: this version does not support modifying the column charset, so you have to skip the UTF-8 check.

    ```sql
    tidb > set @@session.tidb_skip_utf8_check=1;
    Query OK, 0 rows affected
    tidb > insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

- In v2.1.3 and the later versions: it is recommended to modify the column charset into UTF8MB4. Or you can set `tidb_skip_utf8_check` to skip the UTF-8 check. But if you skip the check, you might fail to replicate data from TiDB to MySQL because MySQL executes the check.

    ```sql
    tidb > alter table t change column a a varchar(100) character set utf8mb4;
    Query OK, 0 rows affected
    tidb > insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

    Specifically, you can use the variable `tidb_skip_utf8_check` to skip the legal UTF-8 and UTF8MB4 check on the data. But if you skip the check, you might fail to replicate the data from TiDB to MySQL because MySQL executes the check.

    If you only want to skip the UTF-8 check, you can set `tidb_check_mb4_value_in_utf8`. This variable is added to the `config.toml` file in v2.1.3, and you can modify `check-mb4-value-in-utf8` in the configuration file and then restart the cluster to enable it.

    Starting from v2.1.5, you can set `tidb_check_mb4_value_in_utf8` through the HTTP API and the session variable:

    * HTTP API（the HTTP API can be enabled only on a single server）

        ```sh
        # Enabled.
        curl -X POST -d "check_mb4_value_in_utf8=1" http://{TiDBIP}:10080/settings
        # Disabled.
        curl -X POST -d "check_mb4_value_in_utf8=0" http://{TiDBIP}:10080/settings
        ```

    * Session variable

        ```sql
        # Enabled.
        set @@session.tidb_check_mb4_value_in_utf8 = 1;
        # Disabled.
        set @@session.tidb_check_mb4_value_in_utf8 = 0;
        ```
