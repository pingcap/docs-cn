---
title: TiDB Data Type
summary: Learn about the JSON data type in TiDB.
aliases: ['/docs/dev/data-type-json/','/docs/dev/reference/sql/data-types/json/']
---

# JSON Type

> **Warning:**
>
> This is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

TiDB supports the `JSON` (JavaScript Object Notation) data type, which is useful for storing semi-structured data.  The `JSON` data type provides the following advantages over storing `JSON`-format strings in a string column:

- Use the Binary format for serialization. The internal format permits quick read access to `JSON` document elements.
- Automatic validation of the JSON documents stored in `JSON` columns. Only valid documents can be stored.

`JSON` columns, like columns of other binary types, are not indexed directly, but you can index the fields in the `JSON` document in the form of generated column:

```sql
CREATE TABLE city (
    id INT PRIMARY KEY,
    detail JSON,
    population INT AS (JSON_EXTRACT(detail, '$.population')),
    index index_name (population)
    );
INSERT INTO city (id,detail) VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

For more information, see [JSON Functions](/functions-and-operators/json-functions.md) and [Generated Columns](/generated-columns.md).
