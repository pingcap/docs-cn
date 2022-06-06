---
title: SHOW BUILTINS
summary: TiDB 数据库中 SHOW BUILTINS 的使用概况。
---

# SHOW BUILTINS

`SHOW BUILTINS` 语句用于列出 TiDB 中所有的内置函数。

## 语法图

**ShowBuiltinsStmt:**

![ShowBuiltinsStmt](/media/sqlgram/ShowBuiltinsStmt.png)

## 示例

{{< copyable "sql" >}}

```sql
SHOW BUILTINS;
```

```
+-----------------------------+
| Supported_builtin_functions |
+-----------------------------+
| abs                         |
| acos                        |
| adddate                     |
| addtime                     |
| aes_decrypt                 |
| aes_encrypt                 |
| and                         |
| any_value                   |
| ascii                       |
| asin                        |
| atan                        |
| atan2                       |
| benchmark                   |
| bin                         |
| bit_count                   |
| bit_length                  |
| bitand                      |
| bitneg                      |
| bitor                       |
| bitxor                      |
| case                        |
| ceil                        |
| ceiling                     |
| char_func                   |
| char_length                 |
| character_length            |
| charset                     |
| coalesce                    |
| coercibility                |
| collation                   |
| compress                    |
| concat                      |
| concat_ws                   |
| connection_id               |
| conv                        |
| convert                     |
| convert_tz                  |
| cos                         |
| cot                         |
| crc32                       |
| curdate                     |
| current_date                |
| current_role                |
| current_time                |
| current_timestamp           |
| current_user                |
| curtime                     |
| database                    |
| date                        |
| date_add                    |
| date_format                 |
| date_sub                    |
| datediff                    |
| day                         |
| dayname                     |
| dayofmonth                  |
| dayofweek                   |
| dayofyear                   |
| decode                      |
| default_func                |
| degrees                     |
| des_decrypt                 |
| des_encrypt                 |
| div                         |
| elt                         |
| encode                      |
| encrypt                     |
| eq                          |
| exp                         |
| export_set                  |
| extract                     |
| field                       |
| find_in_set                 |
| floor                       |
| format                      |
| format_bytes                |
| format_nano_time            |
| found_rows                  |
| from_base64                 |
| from_days                   |
| from_unixtime               |
| ge                          |
| get_format                  |
| get_lock                    |
| getparam                    |
| getvar                      |
| greatest                    |
| gt                          |
| hex                         |
| hour                        |
| if                          |
| ifnull                      |
| in                          |
| inet6_aton                  |
| inet6_ntoa                  |
| inet_aton                   |
| inet_ntoa                   |
| insert_func                 |
| instr                       |
| intdiv                      |
| interval                    |
| is_free_lock                |
| is_ipv4                     |
| is_ipv4_compat              |
| is_ipv4_mapped              |
| is_ipv6                     |
| is_used_lock                |
| isfalse                     |
| isnull                      |
| istrue                      |
| json_array                  |
| json_array_append           |
| json_array_insert           |
| json_contains               |
| json_contains_path          |
| json_depth                  |
| json_extract                |
| json_insert                 |
| json_keys                   |
| json_length                 |
| json_merge                  |
| json_merge_patch            |
| json_merge_preserve         |
| json_object                 |
| json_pretty                 |
| json_quote                  |
| json_remove                 |
| json_replace                |
| json_search                 |
| json_set                    |
| json_storage_size           |
| json_type                   |
| json_unquote                |
| json_valid                  |
| last_day                    |
| last_insert_id              |
| lastval                     |
| lcase                       |
| le                          |
| least                       |
| left                        |
| leftshift                   |
| length                      |
| like                        |
| ln                          |
| load_file                   |
| localtime                   |
| localtimestamp              |
| locate                      |
| log                         |
| log10                       |
| log2                        |
| lower                       |
| lpad                        |
| lt                          |
| ltrim                       |
| make_set                    |
| makedate                    |
| maketime                    |
| master_pos_wait             |
| md5                         |
| microsecond                 |
| mid                         |
| minus                       |
| minute                      |
| mod                         |
| month                       |
| monthname                   |
| mul                         |
| name_const                  |
| ne                          |
| nextval                     |
| not                         |
| now                         |
| nulleq                      |
| oct                         |
| octet_length                |
| old_password                |
| or                          |
| ord                         |
| password_func               |
| period_add                  |
| period_diff                 |
| pi                          |
| plus                        |
| position                    |
| pow                         |
| power                       |
| quarter                     |
| quote                       |
| radians                     |
| rand                        |
| random_bytes                |
| regexp                      |
| release_all_locks           |
| release_lock                |
| repeat                      |
| replace                     |
| reverse                     |
| right                       |
| rightshift                  |
| round                       |
| row_count                   |
| rpad                        |
| rtrim                       |
| schema                      |
| sec_to_time                 |
| second                      |
| session_user                |
| setval                      |
| setvar                      |
| sha                         |
| sha1                        |
| sha2                        |
| sign                        |
| sin                         |
| sleep                       |
| space                       |
| sqrt                        |
| str_to_date                 |
| strcmp                      |
| subdate                     |
| substr                      |
| substring                   |
| substring_index             |
| subtime                     |
| sysdate                     |
| system_user                 |
| tan                         |
| tidb_decode_key             |
| tidb_decode_plan            |
| tidb_is_ddl_owner           |
| tidb_parse_tso              |
| tidb_version                |
| time                        |
| time_format                 |
| time_to_sec                 |
| timediff                    |
| timestamp                   |
| timestampadd                |
| timestampdiff               |
| to_base64                   |
| to_days                     |
| to_seconds                  |
| trim                        |
| truncate                    |
| ucase                       |
| unaryminus                  |
| uncompress                  |
| uncompressed_length         |
| unhex                       |
| unix_timestamp              |
| upper                       |
| user                        |
| utc_date                    |
| utc_time                    |
| utc_timestamp               |
| uuid                        |
| uuid_short                  |
| validate_password_strength  |
| version                     |
| week                        |
| weekday                     |
| weekofyear                  |
| weight_string               |
| xor                         |
| year                        |
| yearweek                    |
+-----------------------------+
268 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
