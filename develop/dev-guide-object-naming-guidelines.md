---
title: Object Naming Convention
summary: Learn the object naming convention in TiDB.
---

# Object Naming Convention

This document introduces the rules to name database objects, such as database, table, index, and user.

## General rules

- It is recommended to use meaningful English words separated by underscores.
- Use only letters, numbers, and underscores in a name.
- Avoid using TiDB reserved words, such as `group` and `order`, as column names.
- It is recommended to use lowercase letters for all database objects.

## Database naming convention

It is recommended to differentiate database names by business, product, or other metrics and use no more than 20 characters in a database name. For example, you can name a temporary library as `tmp_crm` or a test library as `test_crm`.

## Table naming convention

- Use the same prefix for tables of the same business or module, and make sure that the table name is self-explanatory as much as possible.
- Separate words in a name by underscores. It is recommended to use no more than 32 characters in a table name.
- It is recommended to annotate the purpose of the table for a better understanding. For example:
    - Temporary table: `tmp_t_crm_relation_0425`
    - Backup table: `bak_t_crm_relation_20170425`
    - Temporary table of business operations: `tmp_st_{business code}_{creator abbreviation}_{date}`
    - Record table of accounts period: `t_crm_ec_record_YYYY{MM}{dd}`
- Create separate databases for tables of different business modules and add annotations accordingly.

## Column naming convention

- The column naming is the actual meaning or abbreviation of the column.
- It is recommended to use the same column name between tables with the same meaning.
- It is recommended to add annotations to columns and specify named values for enumerated types, such as "0: offline, 1: online".
- It is recommended to name the boolean column as `is_{description}`. For example, the column of a `member` table that indicates whether the member is enabled, can be named as `is_enabled`.
- It is not recommended to name a column with more than 30 characters, and the number of columns should be less than 60.
- Avoid using TiDB reserved words as column names, such as `order`, `from`, and `desc`. To check whether a keyword is reserved, see [TiDB keywords](/keywords.md).

## Index naming convention

- Primary key index: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
- Unique index: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
- Common index: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
- Column name with multiple words: use meaningful abbreviations