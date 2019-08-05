---
title: String types
summary: Learn about the string types supported in TiDB.
category: reference
---

# String Types

TiDB supports all the MySQL string types, including `CHAR`, `VARCHAR`, `BINARY`, `VARBINARY`, `BLOB`, `TEXT`, `ENUM`, and `SET`. For more information, see [String Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/string-types.html).

## Supported types

### `CHAR` type

`CHAR` is a fixed length string. Values stored as `CHAR` are right-padded with spaces to the specified length. M represents the column-length in characters (not bytes).  The range of M is 0 to 255:

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` type

`VARCHAR` is a string of variable-length. M represents the maximum column length in characters (not bytes). The range of M is 0 to 65,535, but the effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB).

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` type

`TINYTEXT` is a string of variable-length. The length (M) is optional, with a maximum length of 255 characters:

```sql
TINYTEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` type

`TEXT` is a string of variable-length. M represents the maximum column length ranging from 0 to 65,535. The effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` type

`MEDIUMTEXT` is a string of variable-length. M represents the maximum column length ranging from 0 to 16,777,215, but the effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` type

`LONGTEXT` is a string of variable-length. M represents the maximum column length ranging from 0 to 4,294,967,295, but the effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` type

The `BINARY` type is similar to the `CHAR` type, but stores binary byte strings rather than nonbinary character strings. M represents the maximum length in bytes:

```sql
BINARY(M)
```

### `VARBINARY` type

The `VARBINARY` type is similar to the `VARCHAR` type, but stores binary byte strings rather than nonbinary character strings. M represents the maximum length, ranging from 0 to 65,535 bytes:

```sql
VARBINARY(M)
```

### `TINYBLOB` type

The `TINYBLOB` type is similar to the `TINYTEXT` type, but stores binary byte strings rather than nonbinary character strings:

```sql
TINYBLOB
```

### `BLOB` type

The `BLOB` type is similar to the `TEXT` type, but stores binary byte strings rather than nonbinary character strings. M represents the maximum column length ranging from 0 to 65,535 bytes. The effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

```sql
BLOB[(M)]
```

### `MEDIUMBLOB` type

The `MEDIUMBLOB` type is similar to the `TEXT` type, but stores binary byte strings rather than nonbinary character strings. The maximum length is 16,777,215 bytes, but the effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

```sql
MEDIUMBLOB
```

### `LONGBLOB` type

The `LONGBLOB` type is similar to the `LONGTEXT` type, but stores binary byte strings rather than nonbinary character strings. The maximum length is 4,294,967,295 bytes, but the effective maximum-length will be shorter since the total size of all columns must not exceed 65,535 bytes (the maximum row-size in TIDB):

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
