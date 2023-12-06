---
title: 通过系统变量 `tidb_external_ts` 读取历史数据
summary: 了解如何通过系统变量 `tidb_external_ts` 读取历史数据。
---

# 通过系统变量 `tidb_external_ts` 读取历史数据

为了支持读取历史版本数据，TiDB 从 v6.4.0 起引入了一个新的系统变量 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入)。本文档介绍如何通过该系统变量读取历史数据，其中包括具体的操作流程。

## 场景介绍

通过配置让 TiDB 能够读取某一固定时间点的历史数据对于 TiCDC 等数据同步工具非常有用。在数据同步工具完成了某一时间点前的数据同步之后，可以通过设置下游 TiDB 的 `tidb_external_ts` 系统变量，使得下游 TiDB 的请求能够读取到该时间点前的数据。这将避免在同步过程中，下游 TiDB 读取到尚未完全同步而不一致的数据。

## 功能介绍

系统变量 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) 用于指定启用 `tidb_enable_external_ts_read` 时，读取历史数据使用的时间戳。

系统变量 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) 控制着是否在当前会话或全局启用读取历史数据的功能。默认值为 `OFF`，这意味着该功能关闭，并且设置 `tidb_external_ts` 没有作用。当该变量被全局地设置为 `ON` 时，所有的请求都将读取到 `tidb_external_ts` 指定时间之前的历史数据。如果 `tidb_enable_external_ts_read` 仅在某一会话被设置为 `ON`，则只有该会话中的请求会读取到历史数据。

当 `tidb_enable_external_ts_read` 被设置为 `ON` 时，TiDB 会进入只读模式，任何写请求都会失败并且返回错误 `ERROR 1836 (HY000): Running in read-only mode`。

## 示例

以下是一个使用该功能的示例：

1. 创建一个表后，在表中插入几行数据：

    ```sql
    CREATE TABLE t (c INT);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    ```sql
    INSERT INTO t VALUES (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查看表中的数据：

    ```sql
    SELECT * FROM t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. 将 `tidb_external_ts` 设置为 `@@tidb_current_ts`：

    ```sql
    START TRANSACTION;
    SET GLOBAL tidb_external_ts = @@tidb_current_ts;
    COMMIT;
    ```

4. 插入新的一行并确认新的一行已经被插入：

    ```sql
    INSERT INTO t VALUES (4);
    ```

    ```
    Query OK, 1 row affected (0.001 sec)
    ```

    ```sql
    SELECT * FROM t;
    ```

    ```
    +------+
    | id   |
    +------+
    |    1 |
    |    2 |
    |    3 |
    |    4 |
    +------+
    4 rows in set (0.00 sec)
    ```

5. 将 `tidb_enable_external_ts_read` 设置为 `ON` 后，再次查询表中的数据：

    ```sql
    SET tidb_enable_external_ts_read = ON;
    SELECT * FROM t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

    因为 `tidb_external_ts` 被设置为插入这一行之前的时间，在启动 `tidb_enable_external_ts_read` 后，将读取不到新插入的行。
