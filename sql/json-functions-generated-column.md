---
title: JSON Functions and Generated Column
summary: Learn how to use JSON functions and generated column to handle scenarios with uncertain schema.
category: user guide
---

# JSON Functions and Generated Column

## About

To be compatible with MySQL 5.7 or later and better support the document store, TiDB supports JSON in the latest version. In TiDB, a document is a set of Key-Value pairs, encoded as a JSON object. You can use the JSON datatype in a TiDB table and create indexes for the JSON document fields using generated columns. In this way, you can flexibly deal with the business scenarios with uncertain schema and are no longer limited by the read performance and the lack of support for transactions in traditional document databases.

## JSON functions

The support for JSON in TiDB mainly refers to the user interface of MySQL 5.7. For example, you can create a table that includes a JSON field to store complex information:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON
);
```

When you insert data into a table, you can deal with those data with uncertain schema like this:

```sql
INSERT INTO person (name, address_info) VALUES ("John", '{"city": "Beijing"}');
```

You can insert JSON data into the table by inserting a legal JSON string into the column corresponding to the JSON field. TiDB will then parse the text and save it in a more compact and easy-to-access binary form.

You can also convert other data type into JSON using CAST:

```sql
INSERT INTO person (name, address_info) VALUES ("John", CAST('{"city": "Beijing"}' AS JSON));
INSERT INTO person (name, address_info) VALUES ("John", CAST('123' AS JSON));
INSERT INTO person (name, address_info) VALUES ("John", CAST(123 AS JSON));
```

Now, if you want to query all the users living in Beijing from the table, you can simply use the following SQL statement:

```sql
SELECT id, name FROM person WHERE JSON_EXTRACT(address_info, '$.city') = 'Beijing';
```

TiDB supports the `JSON_EXTRACT` function which is exactly the same as in MySQL. The function is to extract the `city` field from the `address_info` document. The second argument is a "path expression" and is used to specify which field to extract. See the following few examples to help you understand the "path expression":

```sql
SET @person = '{"name":"John","friends":[{"name":"Forest","age":16},{"name":"Zhang San","gender":"male"}]}';

SELECT JSON_EXTRACT(@person,  '$.name'); -- gets "John"
SELECT JSON_EXTRACT(@person,  '$.friends[0].age'); -- gets 16
SELECT JSON_EXTRACT(@person,  '$.friends[1].gender'); -- gets "male"
SELECT JSON_EXTRACT(@person,  '$.friends[2].name'); -- gets NULL
``` 

In addition to inserting and querying data, TiDB also supports editing JSON. In general, TiDB currently supports the following JSON functions in MySQL 5.7:

- [JSON_EXTRACT](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract)
- [JSON_ARRAY](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array)
- [JSON_OBJECT](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object)
- [JSON_SET](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set)
- [JSON_REPLACE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace)
- [JSON_INSERT](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert)
- [JSON_REMOVE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove)
- [JSON_TYPE](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type)
- [JSON_UNQUOTE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote)
- [JSON_MERGE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge)
- [JSON_CONTAINS](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains)
- [JSON_CONTAINS_PATH](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path)
- [JSON_LENGTH](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length)

You can get the general use of these functions directly from the function name. These functions in TiDB behave the same as in MySQL 5.7. For more information, see the [JSON Functions document of MySQL 5.7](https://dev.mysql.com/doc/refman/5.7/en/json-functions.html). If you are a user of MySQL 5.7, you can migrate to TiDB seamlessly.

Currently TiDB does not support all the JSON functions in MySQL 5.7. You can track our progress in adding this functionality in [TiDB #7546](https://github.com/pingcap/tidb/issues/7546).

## Index JSON using generated column

The full table scan is executed when you query a JSON field. When you run the `EXPLAIN` statement in TiDB, the results show that it is full table scan. Then, can you index the JSON field?

First, this type of index is wrong:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

This is not because of technical impossibility but because the direct comparison of JSON itself is meaningless. Although we can agree on some comparison rules, such as `ARRAY` is bigger than all `OBJECT`, it is useless. Therefore, as what is done in MySQL 5.7, TiDB prohibits the direct creation of index on JSON field, but you can index the fields in the JSON document in the form of generated column:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL,
    KEY (city)
);
```

In this table, the `city` column is a **generated column**. As the name implies, the column is generated by other columns in the table, and cannot be assigned a value when inserted or updated. For generating a column, you can specify it as `VIRTUAL` to prevent it from being explicitly saved in the record, but by other columns when needed. This is particularly useful when the column is wide and you need to save storage space. With this generated column, you can create an index on it, and it looks the same with other regular columns. In query, you can run the following statements:  

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

In this way, you can create an index. 

> **Note**: In the JSON document, if the field in the specified path does not exist, the result of `JSON_EXTRACT` will be `NULL`. The value of the generated column with index is also `NULL`. If this is not what you want to see, you can add a `NOT NULL` constraint on the generated column. In this way, when the value of the `city` field is `NULL` after you insert data, it can be detected.

## Limitations

The current limitations of JSON and generated column are as follows:

- You cannot add the generated column in the storage type of `STORED` through `ALTER TABLE`.
- You cannot create an index on the generated column through `ALTER TABLE`. 

The above functions and some other JSON functions are under development.
