---
title: SESSION_CONNECT_ATTRS
summary: Learn the `SESSION_CONNECT_ATTRS` performance_schema table.
---

# SESSION\_CONNECT\_ATTRS

The `SESSION_CONNECT_ATTRS` table provides information about connection attributes. Session attributes are key-value pairs that are sent by the client when establishing a connection.

Common attributes:

| Attribute Name    | Example       | Description                |
|-------------------|---------------|----------------------------|
| `_client_name`    | `libmysql`    | Client library name        |
| `_client_version` | `8.0.33`      | Client library version     |
| `_os`             | `Linux`       | Operating System           |
| `_pid`            | `712927`      | Process ID                 |
| `_platform`       | `x86_64`      | CPU Architecture           |
| `program_name`    | `mysqlsh`     | Program name               |

You can view the columns of the `SESSION_CONNECT_ATTRS` table as follows:

{{< copyable "sql" >}}

```sql
USE performance_schema;
DESCRIBE session_connect_attrs;
```

```
+------------------+---------------------+------+-----+---------+-------+
| Field            | Type                | Null | Key | Default | Extra |
+------------------+---------------------+------+-----+---------+-------+
| PROCESSLIST_ID   | bigint(20) unsigned | NO   |     | NULL    |       |
| ATTR_NAME        | varchar(32)         | NO   |     | NULL    |       |
| ATTR_VALUE       | varchar(1024)       | YES  |     | NULL    |       |
| ORDINAL_POSITION | int(11)             | YES  |     | NULL    |       |
+------------------+---------------------+------+-----+---------+-------+
```

You can view the information on session attributes stored in the `SESSION_CONNECT_ATTRS` table as follows:

{{< copyable "sql" >}}

```sql
USE performance_schema;
TABLE SESSION_CONNECT_ATTRS;
```

```
+----------------+-----------------+------------+------------------+
| PROCESSLIST_ID | ATTR_NAME       | ATTR_VALUE | ORDINAL_POSITION |
+----------------+-----------------+------------+------------------+
|        2097154 | _client_name    | libmysql   |                0 |
|        2097154 | _client_version | 8.1.0      |                1 |
|        2097154 | _os             | Linux      |                2 |
|        2097154 | _pid            | 1299203    |                3 |
|        2097154 | _platform       | x86_64     |                4 |
|        2097154 | program_name    | mysqlsh    |                5 |
+----------------+-----------------+------------+------------------+
```

Fields in the `SESSION_CONNECT_ATTRS` table are described as follows:

* `PROCESSLIST_ID`: Processlist ID of the session.
* `ATTR_NAME`: Attribute name.
* `ATTR_VALUE`: Attribute value.
* `ORDINAL_POSITION`: Ordinal position of the name/value pair.
