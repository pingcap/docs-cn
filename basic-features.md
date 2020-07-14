---
title: TiDB Basic Features
summary: Learn about the basic features of TiDB.
aliases: ['/docs/dev/basic-features/']
---

# TiDB Basic Features

This document introduces the basic features of TiDB.

## Data types

- Numeric types: `BIT`, `BOOL|BOOLEAN`, `SMALLINT`, `MEDIUMINT`, `INT|INTEGER`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL`.

- Date and time types: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR`.

- String types: `CHAR`, `VARCHAR`, `TEXT`, `TINYTEXT`, `MEDIUMTEXT`, `LONGTEXT`, `BINARY`, `VARBINARY`, `BLOB`, `TINYBLOB`, `MEDIUMBLOB`, `LONGBLOB`, `ENUM`, `SET`.

- The `JSON` type.

## Operators

- Arithmetic operators, bit operators, comparison operators, logical operators, date and time operators, and so on.

## Character sets and collations

- Character sets: `UTF8`, `UTF8MB4`, `BINARY`, `ASCII`, `LATIN1`.

- Collations: `UTF8MB4_GENERAL_CI`, `UTF8MB4_GENERAL_BIN`, `UTF8_GENERAL_CI`, `UTF8_GENERAL_BIN`, `BINARY`.

## Functions

- Control flow functions, string functions, date and time functions, bit functions, data type conversion functions, data encryption and decryption functions, compression and decompression functions, information functions, JSON functions, aggregation functions, window functions, and so on.

## SQL statements

- Fully supports standard Data Definition Language (DDL) statements, such as `CREATE`, `DROP`, `ALTER`, `RENAME`, `TRUNCATE`, and so on.

- Fully supports standard Data Manipulation Language (DML) statements, such as `INSERT`, `REPLACE`, `SELECT`, subqueries, `UPDATE`, `LOAD DATA`, and so on.

- Fully supports standard transactional and locking statements, such as `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SET TRANSACTION`, and so on.

- Fully supports standard database administration statements, such as `SHOW`, `SET`, and so on.

- Fully supports standard utility statements, such as `DESCRIBE`, `EXPLAIN`, `USE`, and so on.

- Fully supports the `GROUP BY` and `ORDER BY` clauses.

- Fully supports the standard `LEFT OUTER JOIN` and `RIGHT OUTER JOIN` SQL statements.

- Fully supports the standard SQL table and column aliases.

## Partitioning

- Supports Range partitioning
- Supports Hash partitioning

## Views

- Supports general views

## Constraints

- Supports non-empty constraints
- Supports primary key constraints
- Supports unique constraints

## Security

- Supports privilege management based on RBAC (role-based access control)
- Supports password management
- Supports communication and data encryption
- Supports IP allowlist
- Supports audit

## Tools

- Supports fast backup
- Supports data migration from MySQL to TiDB using tools
- Supports deploying and maintaining TiDB using tools
