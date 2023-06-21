---
title: String types
summary: Learn about the string types supported in TiDB.
aliases: ['/docs/dev/data-type-string/','/docs/dev/reference/sql/data-types/string/']
---

# String Types

TiDB supports all the MySQL string types, including `CHAR`, `VARCHAR`, `BINARY`, `VARBINARY`, `BLOB`, `TEXT`, `ENUM`, and `SET`. For more information, see [String Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/string-types.html).

## Supported types

### `CHAR` type

`CHAR` is a fixed length string. M represents the column-length in characters (not bytes). The range of M is 0 to 255. Different from the `VARCHAR` type, when data is inserted into a `CHAR` column, the trailing spaces are truncated.

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` type

`VARCHAR` is a string of variable-length. M represents the maximum column length in characters (not bytes). The maximum size of `VARCHAR` cannot exceed 65,535 bytes. The maximum row length and the character set being used determine the `VARCHAR` length.

The space occupied by a single character might differ for different character sets. The following table shows the bytes consumed by a single character, and the range of the `VARCHAR` column length in each character set:

| Character Set | Byte(s) per Character | Range of the Maximum `VARCHAR` Column Length |
| ----- | ---- | ---- |
| ascii | 1 | (0, 65535] |
| latin1 | 1 | (0, 65535] |
| binary | 1 | (0, 65535] |
| utf8 | 3 | (0, 21845] |
| utf8mb4 | 4 | (0, 16383] |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` type

`TEXT` is a string of variable-length. The maximum column length is 65,535 bytes. The optional M argument is in characters and is used to automatically select the fittest type of a `TEXT` column. For example `TEXT(60)` will yield a `TINYTEXT` data type that can hold up to 255 bytes, which fits a 60-character UTF-8 string that has up to 4 bytes per character (4×60=240). Using the M argument is not recommended.

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` type

The `TINYTEXT` type is similar to the [`TEXT` type](#text-type). The difference is that the maximum column length of `TINYTEXT` is 255.

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` type

<CustomContent platform="tidb">

The `MEDIUMTEXT` type is similar to the [`TEXT` type](#text-type). The difference is that the maximum column length of `MEDIUMTEXT` is 16,777,215. But due to the limitation of [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>
<CustomContent platform="tidb-cloud">

The `MEDIUMTEXT` type is similar to the [`TEXT` type](#text-type). The difference is that the maximum column length of `MEDIUMTEXT` is 16,777,215. But due to the limitation of [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` type

<CustomContent platform="tidb">

The `LONGTEXT` type is similar to the [`TEXT` type](#text-type). The difference is that the maximum column length of `LONGTEXT` is 4,294,967,295. But due to the limitation of [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>
<CustomContent platform="tidb-cloud">

The `LONGTEXT` type is similar to the [`TEXT` type](#text-type). The difference is that the maximum column length of `LONGTEXT` is 4,294,967,295. But due to the limitation of [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` type

The `BINARY` type is similar to the [`CHAR` type](#char-type). The difference is that `BINARY` stores binary byte strings.

```sql
BINARY(M)
```

### `VARBINARY` type

The `VARBINARY` type is similar to the [`VARCHAR` type](#varchar-type). The difference is that the `VARBINARY` stores binary byte strings.

```sql
VARBINARY(M)
```

### `BLOB` type

`BLOB` is a large binary file. M represents the maximum column length in bytes, ranging from 0 to 65,535.

```sql
BLOB[(M)]
```

### `TINYBLOB` type

The `TINYBLOB` type is similar to the [`BLOB` type](#blob-type). The difference is that the maximum column length of `TINYBLOB` is 255.

```sql
TINYBLOB
```

### `MEDIUMBLOB` type

<CustomContent platform="tidb">

The `MEDIUMBLOB` type is similar to the [`BLOB` type](#blob-type). The difference is that the maximum column length of `MEDIUMBLOB` is 16,777,215. But due to the limitation of [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>
<CustomContent platform="tidb-cloud">

The `MEDIUMBLOB` type is similar to the [`BLOB` type](#blob-type). The difference is that the maximum column length of `MEDIUMBLOB` is 16,777,215. But due to the limitation of [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>

```sql
MEDIUMBLOB
```

### `LONGBLOB` type

<CustomContent platform="tidb">

The `LONGBLOB` type is similar to the [`BLOB` type](#blob-type). The difference is that the maximum column length of `LONGBLOB` is 4,294,967,295. But due to the limitation of [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>
<CustomContent platform="tidb-cloud">

The `LONGBLOB` type is similar to the [`BLOB` type](#blob-type). The difference is that the maximum column length of `LONGBLOB` is 4,294,967,295. But due to the limitation of [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50), the maximum storage size of a single row in TiDB is 6 MiB by default and can be increased to 120 MiB by changing the configuration.

</CustomContent>

```sql
LONGBLOB
```

### `ENUM` type

An `ENUM` is a string object with a value chosen from a list of permitted values that are enumerated explicitly in the column specification when the table is created. The syntax is:

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

The value of the `ENUM` data type is stored as numbers. Each value is converted to a number according the definition order. In the previous example, each string is mapped to a number:

| Value | Number |
| ---- | ---- |
| NULL | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

For more information, see [the ENUM type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/enum.html).

### `SET` type

A `SET` is a string object that can have zero or more values, each of which must be chosen from a list of permitted values specified when the table is created. The syntax is:

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```

In the example, any of the following values can be valid:

```
''
'1'
'2'
'1,2'
```

In TiDB, the values of the `SET` type is internally converted to `Int64`. The existence of each element is represented using a binary: 0 or 1. For a column specified as `SET('a','b','c','d')`, the members have the following decimal and binary values.

| Member | Decimal Value | Binary Value |
| ---- | ---- | ------ |
| 'a' | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

In this case, for an element of `('a', 'c')`, it is `0101` in binary.

For more information, see [the SET type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/set.html).
