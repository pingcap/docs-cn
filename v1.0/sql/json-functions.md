---
title: JSON Functions
category: user guide
---

# JSON Functions

| Function Name and Syntactic Sugar  | Description  |
| ---------- | ------------------ |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]| Return data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [JSON_UNQUOTE(json_val)][json_unquote] |  Unquote JSON value and return the result as a `utf8mb4` string |
| [JSON_TYPE(json_val)][json_type] | Return a `utf8mb4` string indicating the type of a JSON value |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | Insert or update data in a JSON document and return the result |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | Insert data into a JSON document and return the result |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | Replace existing values in a JSON document and return the result |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | Remove data from a JSON document and return the result |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | Merge two or more JSON documents and return the merged result |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]   | Evaluate a (possibly empty) list of key-value pairs and return a JSON object containing those pairs  |
| [JSON_ARRAY([val[, val] ...])][json_array]  | Evaluate a (possibly empty) list of values and return a JSON array containing those values |
| ->  | Return value from JSON column after evaluating path; the syntactic sugar of `JSON_EXTRACT(doc, path_literal)`   |
| ->>  | Return value from JSON column after evaluating path and unquoting the result; the syntactic sugar of `JSON_UNQUOTE(JSONJSON_EXTRACT(doc, path_literal))` |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
