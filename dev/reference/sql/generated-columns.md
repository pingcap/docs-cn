---
title: Generated Columns
summary: Learn how to use generated columns
category: reference
aliases: ['/docs/sql/generated-columns/']
---

# Generated Columns

TiDB supports generated columns as part of MySQL 5.7 compatibility. One of the primary use cases for generated columns is to extract data out of a JSON data type and enable it to be indexed.

## Index JSON using generated column

In both MySQL 5.7 and TiDB, columns of type JSON can not be indexed directly. i.e. The following table structure is **not supported**:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

In order to index a JSON column, you must first extract it as a generated column. Using the `city` generated column as an example, you are then able to add an index:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL,
    KEY (city)
);
```

In this table, the `city` column is a **generated column**. As the name implies, the column is generated from other columns in the table, and cannot be assigned a value when inserted or updated. The column is also _virtual_ in that it does not require any storage or memory, and is generated on demand. The index on `city` however is _stored_ and uses the same structure as other indexes of the type `varchar(64)`.

You can use the index on the generated column in order to speed up the following statement:

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

If no data exists at path `$.city`, `JSON_EXTRACT` returns `NULL`. If you want to enforce a constraint that `city` must be `NOT NULL`, you can define the virtual column as follows:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL NOT NULL,
    KEY (city)
);
```

Both `INSERT` and `UPDATE` statements check virtual column definitions. Rows that do not pass validation return errors:

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## Limitations

The current limitations of JSON and generated columns are as follows:

- You cannot add the generated column in the storage type of `STORED` through `ALTER TABLE`.
- You cannot create an index on the generated column through `ALTER TABLE`. 
- Not all [JSON functions](/sql/json-functions.md) are supported.
