---
title: JSON Functions
summary: Learn about JSON functions.
aliases: ['/docs/dev/functions-and-operators/json-functions/','/docs/dev/reference/sql/functions-and-operators/json-functions/']
---

# JSON Functions

TiDB supports most of the JSON functions that shipped with the GA release of MySQL 5.7.

## Functions that create JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAY([val[, val] ...])][json_array]  | Evaluates a (possibly empty) list of values and returns a JSON array containing those values |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]   | Evaluates a (possibly empty) list of key-value pairs and returns a JSON object containing those pairs  |
| [JSON_QUOTE(string)][json_quote] | Returns a string as a JSON value with quotes |

## Functions that search JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_CONTAINS(target, candidate[, path])][json_contains] | Indicates by returning 1 or 0 whether a given candidate JSON document is contained within a target JSON document |
| [JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)][json_contains_path] | Returns 0 or 1 to indicate whether a JSON document contains data at a given path or paths |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]| Returns data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [->][json_short_extract]  | Returns the value from a JSON column after the evaluating path; an alias for `JSON_EXTRACT(doc, path_literal)`   |
| [->>][json_short_extract_unquote]  | Returns the value from a JSON column after the evaluating path and unquoting the result; an alias for `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` |
| [JSON_KEYS(json_doc[, path])][json_keys] | Returns the keys from the top-level value of a JSON object as a JSON array, or, if a path argument is given, the top-level keys from the selected path |
| [JSON_SEARCH(json_doc, one_or_all, search_string)][json_search] | Search a JSON document for one or all matches of a string |
| [value MEMBER OF(json_array)][MEMBER_OF] | If the passed value is an element of the JSON array, returns 1. Otherwise, returns 0. |
| [JSON_OVERLAPS(json_doc1, json_doc2)][json_overlaps] | Indicates whether two JSON documents have overlapping part. If yes, returns 1. If not, returns 0. |

## Functions that modify JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_APPEND(json_doc, path, value)][json_append] | An alias to `JSON_ARRAY_APPEND` |
| [JSON_ARRAY_APPEND(json_doc, path, value)][json_array_append] | Appends a value to the end of a JSON array at a specified path |
| [JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)][json_array_insert] | Inserts an array into the json document and returns the modified document |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | Inserts data into a JSON document and returns the result |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | A deprecated alias for `JSON_MERGE_PRESERVE` |
| [JSON_MERGE_PATCH(json_doc, json_doc[, json_doc] ...)][json_merge_patch]  | Merge JSON documents |
| [JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)][json_merge_preserve]  | Merges two or more JSON documents and returns the merged result |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | Removes data from a JSON document and returns the result |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | Replaces existing values in a JSON document and returns the result |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | Inserts or updates data in a JSON document and returns the result |
| [JSON_UNQUOTE(json_val)][json_unquote] |  Unquotes a JSON value and returns the result as a string |
| [JSON_ARRAY_APPEND(json_doc, path, val[, path, val] ...)][json_array_append] | Appends values to the end of the indicated arrays within a JSON document and returns the result |
| [JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)][json_array_insert] | Insert values into the specified location of a JSON document and returns the result |

## Functions that return JSON value attributes

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_DEPTH(json_doc)][json_depth] | Returns the maximum depth of a JSON document |
| [JSON_LENGTH(json_doc[, path])][json_length] | Returns the length of a JSON document, or, if a path argument is given, the length of the value within the path |
| [JSON_TYPE(json_val)][json_type] | Returns a string indicating the type of a JSON value |
| [JSON_VALID(json_doc)][json_valid] | Checks if a json\_doc is valid JSON. Useful for checking a column before converting it to the json type. |

## Utility Functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_PRETTY(json_doc)][json_pretty] | Pretty formatting of a JSON document |
| [JSON_STORAGE_FREE(json_doc)][json_storage_free] | Returns how much storage space was freed in the binary representation of the JSON value after it was updated in place. As TiDB has different storage architecture from MySQL, this function always returns 0 for a valid JSON value, and it is implemented for compatibility with MySQL 8.0. |
| [JSON_STORAGE_SIZE(json_doc)][json_storage_size] | Returns an approximate size of bytes required to store the json value. As the size does not account for TiKV using compression, the output of this function is not strictly compatible with MySQL. |

## Aggregate Functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG(key)][json_arrayagg] | Provides an aggregation of keys. |
| [JSON_OBJECTAGG(key, value)][json_objectagg] | Provides an aggregation of values for a given key. |

## See also

* [JSON Function Reference](https://dev.mysql.com/doc/refman/5.7/en/json-function-reference.html)
* [JSON Data Type](/data-type-json.md)

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

[json_merge_patch]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-patch

[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve

[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object

[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array

[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys

[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length

[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid

[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote

[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains

[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path

[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg

[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth

[json_search]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search

[json_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-append

[json_array_append]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-append

[json_array_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-insert

[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg

[json_objectagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-objectagg

[json_pretty]: https://dev.mysql.com/doc/refman/5.7/en/json-utility-functions.html#function_json-pretty

[json_storage_free]: https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free

[json_storage_size]: https://dev.mysql.com/doc/refman/5.7/en/json-utility-functions.html#function_json-storage-size

[MEMBER_OF]: https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of

[json_overlaps]: https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps
