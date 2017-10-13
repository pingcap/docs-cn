---
title: TiDB User Guide
category: user guide
---

# TiDB User Guide

TiDB supports the SQL-92 standard and is compatible with MySQL. To help you easily get started with TiDB, TiDB user guide mainly inherits the MySQL document structure with some TiDB specific changes.

## Table of Contents

+ TiDB Server Administration
    - [The TiDB Server](tidb-server.md)
    - [The TiDB Data Directory](tidb-server.md#tidb-data-directory)
    - [The TiDB System Database](system-database.md)
    - [The Proprietary System Variables and Syntax in TiDB](tidb-specific.md)
    - [TiDB Server Logs](tidb-server.md#tidb-server-logs)
+ Security
    - [The TiDB Access Privilege System](privilege.md)
    - [TiDB User Account Management](user-account-management.md)
    - [Use Encrypted Connections](encrypted-connections.md)
+ Optimization
    - [Understand the Query Execution Plan](understanding-the-query-execution-plan.md)
    - [Introduction to Statistics](statistics.md)
+ Language Structure
    - Literal Values
    - Schema Object Names
    - [Keywords and Reserved Words](keywords-and-reserved-words.md)
    - User-Defined Variables
    - [Expression Syntax](expression-syntax.md)
    - [Comment Syntax](comment-syntax.md)
+ Globalization
    - Character Set Support
    - Character Set Configuration
    - MySQL Server Time Zone Support
+ Data Types
    - Numeric Types
    - Date and Time Types
    - String Types
    - Extensions for Spatial Data
    - The JSON Data Type
    - Data Type Default Values
    - Data Type Storage Requirements
    - Choosing the Right Type for a Column
    - Using Data Types from Other Database Engines
+ Functions and Operators
    - Function and Operator Reference
    - [Type Conversion in Expression Evaluation](type-conversion-in-expression-evaluation.md)
    - [Operators](operators.md)
    - [Control Flow Functions](control-flow-functions.md)
    - [String Functions](string-functions.md)
    - [Numeric Functions and Operators](numeric-functions-and-operators.md)
    - Date and Time Functions
    - [Cast Functions and Operators](cast-functions-and-operators.md)
    - Bit Functions and Operators
    - [Encryption and Compression Functions](encryption-and-compression-functions.md)
    - [Information Functions](information-functions.md)
    - [JSON Functions](json-functions.md)
    - Functions Used with Global Transaction IDs
    - [Aggregate (GROUP BY) Functions](aggregate-group-by-functions.md)
    - [Miscellaneous Functions](miscellaneous-functions.md)
    - Precision Math
+ SQL Statement Syntax
    - [Data Definition Statements](ddl.md)
    - Data Manipulation Statements
    - [Transactions](transaction.md)
    - Replication Statements
    - Prepared SQL Statement Syntax
    - Compound-Statement Syntax
    - Database Administration Statements
    - Utility Statements
    - [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/)
+ Document Store
+ Connectors and APIs
+ Troubleshooting
