---
title: TiCDC Open Protocol
category: reference
---

# TiCDC Open Protocol

TiCDC Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and master-slave replication between different databases. TiCDC complies with TiCDC Open Protocol and replicates data changes of TiDB to third-party data medium such as MQ (Message Queue).

TiCDC Open Protocol uses Event as the basic unit to replicate data change events to the downstream. The Event is divided into three categories:

* Row Changed Event: Represents the data change in a row. When a row is changed, this Event is sent and contains information about the changed row.
* DDL Event: Represents the DDL change. This Event is sent after a DDL statement is successfully executed in the upstream. The DDL Event is broadcasted to every MQ Partition.
* Resolved Event: Represents a special time point before which the Event received is complete.

## Restrictions

* In most cases, the Row Changed Event of a version is sent only once, but in special situations such as node failure and network partition, the Row Changed Event of the same version might be sent multiple times.
* On the same table, the Row Changed Events of each version which is first sent are incremented in the order of timestamps (TS) in the Event stream.
* Resolved Events are periodically broadcasted to each MQ Partition. The Resolved Event means that any Event with a TS earlier than Resolved Event TS has been sent to the downstream.
* DDL Events are broadcasted to each MQ Partition.
* Multiple Row Changed Events of a row are sent to the same MQ Partition.

## Message format

A Message contains one or more Events, arranged in the following format:

Key:

| Offset(Byte) | 0~7     | 8~15 | 16~(15+length1) | ... | ... |
| :----------- | :------ | :--- | :----------- | :--- | :----------- |
| Parameter         | Protocol version | Length1 | Event Key1         | LengthN | Event KeyN         |

Value:

| Offset(Byte) | 0~7 | 8~(7+length1) | ... | ... |
| :----------- | :--- | :-------- | :--- | :------ |
| Parameter         | Length1 | Event Value1     | LengthN | Event ValueN |

* `LengthN` represents the length of the `N`th key/value.
* The length and protocol version are the big-endian `int64` type.
* The version of the current protocol is `1`.

## Event format

This section introduces the formats of Row Changed Event, DDL Event, and Resolved Event.

### Row Changed Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":1
    }
    ```

    | Parameter         | Type   | Description                    |
    | :---------- | :----- | :--------------------- |
    | TS          | Number |  The timestamp of the transaction that causes the row change.  |
    | Schema Name | String |  The name of the schema where the row is in. |
    | Table Name  | String |  The name of the table where the row is in. |

+ **Value:**

    ```
    {
        <UpdateOrDelete>:{
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            },
            <Column Name>:{
                "t":<Column Type>,
                "h":<Where Handle>,
                "v":<Column Value>
            }
        }
    }
    ```

    | Parameter         | Type   | Description                    |
    | :---------- | :----- | :--------------------- |
    | UpdateOrDelete | String |  Identifies whether the row is updated or deleted in the Event. The optional values are `u` or `d`. |
    | Column Name    | String |  The column name.  |
    | Column Type    | Number |  The column type. See [Column and DDL Type Codes](/ticdc/column-ddl-type-codes.md) for details.  |
    | Where Handle   | Bool   |  Determines whether this column can be the filter condition of the `Where` clause. When this column is unique on the table, `Where Handle` is `true`. |
    | Column Value   | Any    | The Column value.   |

### DDL Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "scm":<Schema Name>,
        "tbl":<Table Name>,
        "t":2
    }
    ```

    | Parameter         | Type   | Description                                 |
    | :---------- | :----- | :---------------------------------- |
    | TS          | Number |  The timestamp of the transaction that performs the DDL change.    |
    | Schema Name | String |  The schema name of the DDL change, which might be an empty string.  |
    | Table Name  | String |  The table name of the DDL change, which might be am empty string. |

+ **Value:**

    ```
    {
        "q":<DDL Query>,
        "t":<DDL Type>
    }
    ```

    | Parameter       | Type   | Description           |
    | :-------- | :----- | :------------ |
    | DDL Query | String | DDL Query SQL |
    | DDL Type  | String | The DDL type. See [Column and DDL Type Codes](/ticdc/column-ddl-type-codes.md) for details.    |

### Resolved Event

+ **Key:**

    ```
    {
        "ts":<TS>,
        "t":3
    }
    ```

    | Parameter         | Type   | Description                                         |
    | :---------- | :----- | :------------------------------------------ |
    | TS          | Number | The Resolved timestamp. Any TS earlier than this Event has been sent. |

+ **Value:** None

## Examples of the Event stream output

This section shows and displays the output logs of the Event stream.

Suppose that you execute the following SQL statement in the upstream and the MQ Partition number is 2:

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1(id int primary key, val varchar(16));
```

From the following Log 1 and Log 3, you can see that the DDL Event is broadcasted to all MQ Partitions, and that the Resolved Event is periodically broadcasted to each MQ Partition.

```
1. [partition=0] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
2. [partition=0] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
3. [partition=1] [key="{\"ts\":415508856908021766,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":2}"] [value="{\"q\":\"CREATE TABLE test.t1(id int primary key, val varchar(16))\",\"t\":3}"]
4. [partition=1] [key="{\"ts\":415508856908021766,\"t\":3}"] [value=]
```

Execute the following SQL statements in the upstream:

{{< copyable "sql" >}}

```sql
BEGIN;
INSERT INTO test.t1(id, val) VALUES (1, 'aa');
INSERT INTO test.t1(id, val) VALUES (2, 'aa');
UPDATE test.t1 SET val = 'bb' WHERE id = 2;
INSERT INTO test.t1(id, val) VALUES (3, 'cc');
COMMIT;
```

+ From the following Log 5 and Log 6, you can see that Row Changed Events on the same table might be sent to different partitions based on the primary key, but changes to the same row are sent to the same partition so that the downstream can easily process the Event concurrently.
+ From Log 6, multiple changes to the same row in a transaction are only sent in one Row Changed Event.
+ Log 8 is a repeated event of Log 7. Row Changed Event might be repeated, but the first Event of each version is sent orderly.

```
5. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":1},\"val\":{\"t\":15,\"v\":\"YWE=\"}}}"]
6. [partition=1] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":2},\"val\":{\"t\":15,\"v\":\"YmI=\"}}}"]
7. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
8. [partition=0] [key="{\"ts\":415508878783938562,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"Y2M=\"}}}"]
```

Execute the following SQL statements in the upstream:

{{< copyable "sql" >}}

```sql
BEGIN;
DELETE FROM test.t1 WHERE id = 1;
UPDATE test.t1 SET val = 'dd' WHERE id = 3;
UPDATE test.t1 SET id = 4, val = 'ee' WHERE id = 2;
COMMIT;
```

+ Log 9 is the Row Changed Event of the `Delete` type. This type of Event only contains primary key columns or unique index columns.
+ Log 13 and Log 14 are Resolved Events. The Resolved Event means that in this Partition, any events smaller than the Resolved TS (including Row Changed Event and DDL Event) have been sent.

```
9. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":1}}}"]
10. [partition=1] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"d\":{\"id\":{\"t\":3,\"h\":true,\"v\":2}}}"]
11. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":3},\"val\":{\"t\":15,\"v\":\"ZGQ=\"}}}"]
12. [partition=0] [key="{\"ts\":415508881418485761,\"scm\":\"test\",\"tbl\":\"t1\",\"t\":1}"] [value="{\"u\":{\"id\":{\"t\":3,\"h\":true,\"v\":4},\"val\":{\"t\":15,\"v\":\"ZWU=\"}}}"]
13. [partition=0] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
14. [partition=1] [key="{\"ts\":415508881038376963,\"t\":3}"] [value=]
```
