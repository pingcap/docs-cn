---
title: Table Selector
summary: Learn about Table Selector used by the table routing, binlog event filtering, and column mapping rule of Data Migration.
category: reference
aliases: ['/docs/tools/dm/table-selector/']
---

# Table Selector

Table selector provides a match rule based on [wildcard characters](https://en.wikipedia.org/wiki/Wildcard_character) for schema/table. To match a specified table, configure `schema-pattern`/`table-pattern`.

## Wildcard character

Table selector uses the following two wildcard characters in `schema-pattern`/`table-pattern`:

+ The asterisk character (`*`, also called "star")

    - `*` matches zero or more characters. For example, `doc*` matches `doc` and `document` but not `dodo`.
    - `*` can only be placed at the end of the word. For example, `doc*` is supported, while `do*c` is not supported.

+ The question mark (`?`)

    `?` matches exactly one character except the empty character.

## Match rules

- `schema-pattern` cannot be empty.
- `table-pattern` can be empty. When you configure it as empty, only `schema` is matched according to `schema-pattern`.
- When `table-pattern` is not empty, the `schema` is matched according to `schema-pattern` and `table` is matched according to `table-pattern`. Only when both `schema` and `table` are successfully matched, you can get the match result.

## Usage examples

- Matching all schemas and tables that have a `schema_` prefix in the schema name:

    ```yaml
    schema-pattern： "schema_*"
    table-pattern： ""
    ```

- Matching all tables that have a `schema_` prefix in the schema name and a `table_` prefix in the table name:

    ```yaml
    schema-pattern = "schema_*"
    table-pattern = "table_*"
    ```
