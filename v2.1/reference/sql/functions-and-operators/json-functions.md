---
title: JSON Functions
summary: Learn about JSON functions.
category: reference
---

# JSON Functions

TiDB supports most of the JSON functions that shipped with the GA release of MySQL 5.7. Additional JSON functions were added to MySQL 5.7 after its release, and not all are available in TiDB (see [unsupported functions](#unsupported-functions)).

## Functions that create JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAY([val[, val] ...])][json_array]  | Evaluates a (possibly empty) list of values and returns a JSON array containing those values |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]   | Evaluates a (possibly empty) list of key-value pairs and returns a JSON object containing those pairs  |
| [JSON_QUOTE(string)][json_quote] | Returns a string as a JSON value with quotes |

## Functions that search JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_CONTAINS(target, candidate[, path])][json_contains] | Indicates by returning 1 or 0 whether a given candidate JSON document is contained within a target JSON document |
| [JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)][json_contains_path] | Returns 0 or 1 to indicate whether a JSON document contains data at a given path or paths |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]| Returns data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [->][json_short_extract]  | Returns the value from a JSON column after the evaluating path; the syntactic sugar of `JSON_EXTRACT(doc, path_literal)`   |
| [->>][json_short_extract_unquote]  | Returns the value from a JSON column after the evaluating path and unquoting the result; the syntactic sugar of `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` |
| [JSON_KEYS(json_doc[, path])][json_keys] | Returns the keys from the top-level value of a JSON object as a JSON array, or, if a path argument is given, the top-level keys from the selected path |

## Functions that modify JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | Inserts data into a JSON document and returns the result |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | A deprecated alias for `JSON_MERGE_PRESERVE` |
| [JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)][json_merge_preserve]  | Merges two or more JSON documents and returns the merged result |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | Removes data from a JSON document and returns the result |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | Replaces existing values in a JSON document and returns the result |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | Inserts or updates data in a JSON document and returns the result |
| [JSON_UNQUOTE(json_val)][json_unquote] |  Unquotes a JSON value and returns the result as a string |

## Functions that return JSON value attributes

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_DEPTH(json_doc)][json_depth] | Returns the maximum depth of a JSON document |
| [JSON_LENGTH(json_doc[, path])][json_length] | Returns the length of a JSON document, or, if a path argument is given, the length of the value within the path |
| [JSON_TYPE(json_val)][json_type] | Returns a string indicating the type of a JSON value |

## Unsupported functions

The following JSON functions are unsupported in TiDB. You can track the progress in adding them in [TiDB #7546](https://github.com/pingcap/tidb/issues/7546):

* `JSON_APPEND` and its alias `JSON_ARRAY_APPEND`
* `JSON_ARRAY_INSERT`
* `JSON_MERGE_PATCH`
* `JSON_PRETTY`
* `JSON_SEARCH`
* `JSON_STORAGE_SIZE`
* `JSON_VALID`
* `JSON_ARRAYAGG`
* `JSON_OBJECTAGG`

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg
[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth
