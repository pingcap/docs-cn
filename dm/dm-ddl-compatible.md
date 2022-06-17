---
title: Data Migration DDL 特殊处理说明
---

# Data Migration DDL 特殊处理说明

DM 同步过程中，根据 DDL 语句以及所处场景的不同，将采用不同的处理方式。

## 忽略的 DDL 语句

以下语句 DM 并未支持，因此解析之后直接跳过。

<table>
    <tr>
        <th>描述</th>
        <th>SQL</th>
    </tr>
    <tr>
        <td>transaction</td>
        <td>`^SAVEPOINT`</td>
    </tr>
    <tr>
        <td>skip all flush sqls</td>
        <td>`^FLUSH`</td>
    </tr>
    <tr>
        <td rowspan="3">table maintenance</td>
        <td>`^OPTIMIZE\\s+TABLE`</td>
    </tr>
    <tr>
        <td>`^ANALYZE\\s+TABLE`</td>
    </tr>
    <tr>
        <td>`^REPAIR\\s+TABLE`</td>
    </tr>
    <tr>
        <td>temporary table</td>
        <td>`^DROP\\s+(\\/\\*\\!40005\\s+)?TEMPORARY\\s+(\\*\\/\\s+)?TABLE`</td>
    </tr>
    <tr>
        <td rowspan="2">trigger</td>
        <td>`^CREATE\\s+(DEFINER\\s?=.+?)?TRIGGER`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+TRIGGER`</td>
    </tr>
    <tr>
        <td rowspan="3">procedure</td>
        <td>`^DROP\\s+PROCEDURE`</td>
    </tr>
    <tr>
        <td>`^CREATE\\s+(DEFINER\\s?=.+?)?PROCEDURE`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+PROCEDURE`</td>
    </tr>
    <tr>
        <td rowspan="3">view</td>
        <td>`^CREATE\\s*(OR REPLACE)?\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?\\s+(SQL SECURITY DEFINER)?VIEW`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+VIEW`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?(SQL SECURITY DEFINER)?VIEW`</td>
    </tr>
    <tr>
        <td rowspan="4">function</td>
        <td>`^CREATE\\s+(AGGREGATE)?\\s*?FUNCTION`</td>
    </tr>
    <tr>
        <td>`^CREATE\\s+(DEFINER\\s?=.+?)?FUNCTION`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+FUNCTION`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+FUNCTION`</td>
    </tr>
    <tr>
        <td rowspan="3">tableSpace</td>
        <td>`^CREATE\\s+TABLESPACE`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+TABLESPACE`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+TABLESPACE`</td>
    </tr>
    <tr>
        <td rowspan="3">event</td>
        <td>`^CREATE\\s+(DEFINER\\s?=.+?)?EVENT`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+(DEFINER\\s?=.+?)?EVENT`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+EVENT`</td>
    </tr>
    <tr>
        <td rowspan="7">account management</td>
        <td>`^GRANT`</td>
    </tr>
    <tr>
        <td>`^REVOKE`</td>
    </tr>
    <tr>
        <td>`^CREATE\\s+USER`</td>
    </tr>
    <tr>
        <td>`^ALTER\\s+USER`</td>
    </tr>
    <tr>
        <td>`^RENAME\\s+USER`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+USER`</td>
    </tr>
    <tr>
        <td>`^DROP\\s+USER`</td>
    </tr>
</table>

## 改写的 DDL 语句

以下语句在同步到下游前会进行改写。

|原始语句|实际执行语句|
|-|-|
|`^CREATE DATABASE...`|`^CREATE DATABASE...IF NOT EXISTS`|
|`^CREATE TABLE...`|`^CREATE TABLE..IF NOT EXISTS`|
|`^DROP DATABASE...`|`^DROP TABLE...IF EXISTS`|
|`^DROP TABLE...`|`^DROP TABLE...IF EXISTS`|
|`^DROP INDEX...`|`^DROP INDEX...IF EXISTS`|

## 合库合表迁移任务

当使用悲观协调模式和乐观协调模式进行分库分表合并迁移时，DDL 同步的行为存在变更，具体请参考[悲观模式](/dm/feature-shard-merge-pessimistic.md)和[乐观模式](/dm/feature-shard-merge-optimistic.md)。

## Online DDL

Online DDL 特性也会对 DDL 事件进行特殊处理，详情可参考[迁移使用 GH-ost/PT-osc 的源数据库](/dm/feature-online-ddl.md)。
