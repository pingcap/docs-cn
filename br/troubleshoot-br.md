---
title: 故障处理
summary: 了解 BR 相关的故障以及解决方法。
---

# 故障处理

本文介绍在使用 Backup & Restore (BR) 时可能会遇到的故障及解决方案。

## 如果对数据进行了误操作，如何快速恢复？

如果对数据进行了错误的 UPDATE、DELETE、Truncate 或 DROP 时，你可以通过使用 tidb_snapshot 将数据恢复到误操作之前的状态。本文以误操作 UPDATE 和 TRUNCATE 为例，介绍如何恢复数据。

### 如何快速恢复被 UPDATE 的数据？

本文假设存在表 snap_tab，该表有 3 行数据。

1. 查看表中的数据：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM snap_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

2. 查看当前时间：

    {{< copyable "sql" >}}

    ```sql
    SELECT now ();
    +----------------------+
    |  now ()              |
    +----------------------+
    |2020-10-08 16:45:26   |
    +----------------------+
    1 row in set (0.00 sec)
    ```

3. 模拟数据误更新。

    修改某一行数据，例如：

    {{< copyable "sql" >}}

    ```sql
    UPDATE snap_tab SET c=22 WHERE c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

    确认数据已经更新：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM snap_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

4. 确认是否满足 GC 要求。

    查看当前 GC 保留的 safe point，此处为 `20201008-16:15:09 +0800`，小于 `2020-10-08 16:45`，因此判定这个误操作可以被恢复：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    +---------------------+-------------------------+--------------------------------------------------------------+
    | VARIABLE_NAME       | VARIABLE_VALUE          | COMMENT                                                      |
    | tikv_gc_safe_point  | 20201008-16:15:09 +0800 | All versions after safe point can be accessed. (DO NOT EDIT) |
    +---------------------+-------------------------+--------------------------------------------------------------+

    1 row in set (0.00 sec)
    ```

    此时，可以调整 GC interval time， 避免数据的 MVCC 历史版本被清理掉，影响数据恢复，此处为 720 h：

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE
    VARIABLE_NAME = 'tikv_gc_life_time';
    ```

5. 开始数据恢复。

    设置 tidb_snapshot 为数据修改前的时间点，此处为 "2020-10-08 16:45:26";

    {{< copyable "sql" >}}

    ```sql
    SET @@tidb_snapshot="2020-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)

    SELECT * FROM snap_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

    可以看到，数据已恢复到修改前的状态。如果数据未恢复到目标状态，请继续反复修改 tidb_snapshot，查看历史数据是否满足数据恢复需求，根据 tidb_snapshot 的查询结果生成反向 SQL。

6. 清空当前 session tidb_snapshot 变量：

    {{< copyable "sql" >}}

    ```sql
    SET @@tidb_snapshot="";
    Query OK, 0 rows affected (0.00 sec)

    SELECT * FROM snap_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)

    UPDATE snap_tab SET c=2 WHERE c=22;
    1 rows in set (0.00 sec)

    SELECT * FROM snap_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

7. 调整 GC interval time 为原值：

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '原值' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### 如何快速恢复被 TRUNCATE 掉的数据？

假设存在表 trun_tab，该表有 3 行数据。

1. 查看表中的数据：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM trun_tab;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

2. 模拟误 TRUNCATE 表：

    重复执行两次 TRUNCATE 操作。并在两次 TRUNCATE 后 INSERT 新的记录。

    {{< copyable "sql" >}}

    ```sql

    TRUNCATE TABLE trun_tab;
    Query OK, 0 rows affected (0.22 sec)

    SELECT * FROM trun_tab;
    Empty set (0.00 sec)

    INSERT INTO trun_tab VALUES (4), (5), (6);
    Query OK, 3 rows affected (0.03 sec)
    Records: 3 Duplicates: 0 Warnings: 0

    SELECT * FROM trun_tab;
    +------+
    | c    |
    +------+
    |    4 |
    |    5 |
    |    6 |
    +------+
    3 rows in set (0.00 sec)

    TRUNCATE TABLE trun_tab;
    Query OK, 0 rows affected (0.13 sec)

    INSERT INTO trun_tab VALUES (7), (8), (9), (10);
    Query OK, 4 rows affected (0.04 sec)
    Records: 4 Duplicates: 0 Warnings: 0
    SELECT * FROM trun_tab;
    +------+
    | c    |
    +------+
    |    7 |
    |    8 |
    |    9 |
    |   10 |
    +------+
    4 rows in set (0.00 sec)
    ```

3. 查看 GC safe point，确认是否满足数据恢复需求：

    执行 `admin show ddl jobs` 查看两次 TRUNCATE 操作的时间：

    {{< copyable "sql" >}}

    ```sql
    admin show ddl jobs WHERE table_name = 'trun_tab';
    +--------+------------+--------------+----------------+--------------+------------+----------+-----------+---------------------+---------------------+--------+
    | JOB_ID | DB_NAME    | TABLE_NAME   | JOB_TYPE       | SCHEMA_STATE | SCHEMA_ID  | TABLE_ID | ROW_COUNT | START_TIME          | END_TIME            | STATE  |
    +--------+------------+--------------+----------------+--------------+------------+----------+-----------+---------------------+---------------------+--------+
    |     82 | gzj_test   |  trun_tab    | truncate table | public       |         45 |       79 |         0 | 2021-08-03 16:57:14 | 2021-08-03 16:57:14 | synced |
    |     80 | gzj_test   |  trun_tab    | truncate table | public       |         45 |       77 |         0 | 2021-08-03 16:55:25 | 2021-08-03 16:55:25 | synced |
    |     78 | gzj_test   |  trun_tab    | create table   | public       |         45 |       77 |         0 | 2021-08-03 16:54:05 | 2021-08-03 16:54:05 | synced |
    +--------+ -----------+--------------+----------------+--------------+------------+----------+-----------+---------------------+---------------------+--------+
    3 rows in set (0.04 sec)
    ```

    - 第一次 TRUNCATE：2021-08-03 16:55:25
    - 第二次 TRUNCATE：2021-08-03 16:57:14

    查看当前 GC 保留的 safe point，本示例中为 2021-08-03 16:55:09 +0800，因此满足数据恢复要求：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    +--------------------+-------------------------+--------------------------------------------------------------+
    |      VARIABLE_NAME |          VARIABLE_VALUE | COMMENT                                                      |
    | tikv_gc_safe_point | 20210803-16:55:09 +0800 | All versions after safe point can be accessed. (DO NOT EDIT) |
    +--------------------+-------------------------+--------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

    为避免数据的 MVCC 历史版本被清理掉，影响数据恢复，将 GC interval time 调整为 `720 h`：

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    1 row in set (0.00 sec)
    ```

4. 恢复第一次 TRUNCATE 操作的数据：

    1. 设置 `tidb_snapshot` 为第一次 TRUNCATE 操作前的时间，此处为 `2021-08-03 16:55:24`，小于第一次 TRUNCATE 操作的时间 `2021-08-03 16:55:25`。

        {{< copyable "sql" >}}

        ```sql
        SET session tidb_snapshot = '2021-08-03 16:55:24';
        Query OK, 0 rows affected (0.04 sec)
        ```

    2. 查看目标数据是否存在：

        {{< copyable "sql" >}}

        ```sql
        SELECT * FROM trun_tab;
        +------+
        | c    |
        +------+
        |    1 |
        |    2 |
        |    3 |
        +------+
        3 rows in set (0.01 sec)
        ```

    3. 使用 Dumpling 备份 trun-tab 表的数据，snapshot 的时间为 `2021-08-03 16:55:24`：

        {{< copyable "shell" >}}

        ```
        [root@centos76_vm ~] #tiup dumpling \
        -u root \
        -P 4000 \
        --host 172.x.x.x \
        --filetype sql
        -o /tmp/test \
        -r 200000 \
        -F 256MiB \
        -T test.trun_tab \
        --snapshot "2021-08-03 16:55:24"

        $ more /tmp/test/test.trun_tab.0000000010000.sql
        /*!40101 SET NAMES binary*/;
        INSERT INTO `trun_tab` VALUES
        (1),
        (2),
        (3);
        ```

    4. 查看数据是否恢复：

        {{< copyable "sql" >}}

        ```sql
        SELECT * FROM trun_tab;

        +------+
        | c    |
        +------+
        |    7 |
        |    8 |
        |    9 |
        |   10 |
        |    1 |
        |    2 |
        |    3 |
        +------+
        7 rows in set (0.00 sec)
        ```

5. 恢复第二次 TRUNCATE 操作的数据：

    1. 执行 `Flashback trun_tab` 语句恢复第二次 TRUNCATE 前的数据到 trun_tab_02 中：

        {{< copyable "sql" >}}

        ```sql
        FLASHBACK TABLE trun_tab TO trun_tab_02;
        Query OK, 0 rows affected (1.21 sec)

        SELECT * FROM trun_tab_02;

        +------+
        | c    |
        +------+
        |    4 |
        |    5 |
        |    6 |
        +------+
        3 rows in set (0.01 sec)
        ```

    2. 将 trun_tab_02 的数据重新 INSERT 到 trun_tab 中：

        {{< copyable "sql" >}}

        ```sql
        SELECT * FROM trun_tab;
        +------+
        | c    |
        +------+
        |    7 |
        |    8 |
        |    9 |
        |   10 |
        |    1 |
        |    2 |
        |    3 |
        +------+
        7 rows in set (0.00 sec)

        INSERT trun_tab SELECT * FROM trun_tab_02;
        Query OK, 3 rows affected (0.02 sec)
        Records: 3 Duplicates: 0 Warnings: 0

        SELECT * FROM trun_tab;
        +------+
        | c    |
        +------+
        |    7 |
        |    8 |
        |    9 |
        |   10 |
        |    1 |
        |    2 |
        |    3 |
        |    4 |
        |    5 |
        |    6 |
        +------+
        10 rows in set (0.00 sec)
        ```

至此，两次 TRUNCATE 操作的数据均恢复完成。

> **注意：**
>
> 第一次恢复操作未使用 Flashback 语句，因为该语句无法与 `set tidb_snapshot` 一起使用，即无法使用 Flashback 多次恢复同一张表。
