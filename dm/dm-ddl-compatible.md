---
title: Data Migration DDL 特殊处理说明
summary: 数据迁移中，根据不同的 DDL 语句和场景，采用不同处理方式。DM 不支持的 DDL 语句会直接跳过。部分 DDL 语句在同步到下游前会进行改写。在合库合表迁移任务中，DDL 同步行为存在变更。Online DDL 特性也会对 DDL 事件进行特殊处理。
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
        <td><code>^SAVEPOINT</code></td>
    </tr>
    <tr>
        <td>skip all flush sqls</td>
        <td><code>^FLUSH</code></td>
    </tr>
    <tr>
        <td rowspan="3">table maintenance</td>
        <td><code>^OPTIMIZE\\s+TABLE</code></td>
    </tr>
    <tr>
        <td><code>^ANALYZE\\s+TABLE</code></td>
    </tr>
    <tr>
        <td><code>^REPAIR\\s+TABLE</code></td>
    </tr>
    <tr>
        <td>temporary table</td>
        <td><code>^DROP\\s+(\\/\\*\\!40005\\s+)?TEMPORARY\\s+(\\*\\/\\s+)?TABLE</code></td>
    </tr>
    <tr>
        <td rowspan="2">trigger</td>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?TRIGGER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+TRIGGER</code></td>
    </tr>
    <tr>
        <td rowspan="3">procedure</td>
        <td><code>^DROP\\s+PROCEDURE</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?PROCEDURE</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+PROCEDURE</code></td>
    </tr>
    <tr>
        <td rowspan="3">view</td>
        <td><code>^CREATE\\s*(OR REPLACE)?\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?\\s+(SQL SECURITY DEFINER)?VIEW</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+VIEW</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?(SQL SECURITY DEFINER)?VIEW</code></td>
    </tr>
    <tr>
        <td rowspan="4">function</td>
        <td><code>^CREATE\\s+(AGGREGATE)?\\s*?FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+FUNCTION</code></td>
    </tr>
    <tr>
        <td rowspan="3">tableSpace</td>
        <td><code>^CREATE\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td rowspan="3">event</td>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?EVENT</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+(DEFINER\\s?=.+?)?EVENT</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+EVENT</code></td>
    </tr>
    <tr>
        <td rowspan="7">account management</td>
        <td><code>^GRANT</code></td>
    </tr>
    <tr>
        <td><code>^REVOKE</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^RENAME\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+USER</code></td>
    </tr>
</table>

## 改写的 DDL 语句

以下语句在同步到下游前会进行改写。

|原始语句|实际执行语句|
|-|-|
|`^CREATE DATABASE...`|`^CREATE DATABASE...IF NOT EXISTS`|
|`^CREATE TABLE...`|`^CREATE TABLE..IF NOT EXISTS`|
|`^DROP DATABASE...`|`^DROP DATABASE...IF EXISTS`|
|`^DROP TABLE...`|`^DROP TABLE...IF EXISTS`|
|`^DROP INDEX...`|`^DROP INDEX...IF EXISTS`|

## 合库合表迁移任务

当使用悲观协调模式和乐观协调模式进行分库分表合并迁移时，DDL 同步的行为存在变更，具体请参考[悲观模式](/dm/feature-shard-merge-pessimistic.md)和[乐观模式](/dm/feature-shard-merge-optimistic.md)。

## Online DDL

Online DDL 特性也会对 DDL 事件进行特殊处理，详情可参考[迁移使用 GH-ost/PT-osc 的源数据库](/dm/feature-online-ddl.md)。
