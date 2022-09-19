---
title: 已知的第三方工具兼容问题
summary: 列出 PingCAP 在测试时遇到的第三方工具兼容问题
---

# 已知的第三方工具兼容问题

> **注意：**
>
> TiDB 已列举[不支持的功能特性](/mysql-compatibility.md#不支持的功能特性)，典型的不支持特性有：
>
> - 存储过程与函数
> - 触发器
> - 事件
> - 自定义函数
> - 外键约束
> - 空间类型的函数
> - `XA` 语法
>
> 这样的功能不兼容将被视为预期行为，将不再重复叙述。可查看[与 MySQL 兼容性对比](/mysql-compatibility.md)获得更多不支持或与 MySQL 不一致的特性说明。

## 通用

### `SELECT CONNECTION_ID()` 返回结果类型为 64 位整型

**描述**

TiDB 的 `CONNECTION_ID()` 返回值为 64 位，如 `2199023260887`。而 MySQL 为 32 位， 如 

**规避方法**

### TiDB 未设置 `COM_*` 计数器

**描述**

**规避方法**

### TiDB 错误日志区分 `timestamp` 与 `datetime`，MySQL 不区分

**描述**

**规避方法**

### 不支持 `CHECK TABLE` 语句

**描述**

**规避方法**

### `INET_ATON` 语句失败行为不一致

**描述**

**规避方法**

### `SHOW FULL COLUMNS` 结果与 `information_schema` 内数据不一致

**描述**

**规避方法**

## MySQL Connector/J

- 测试版本：8.0.29

### 默认排序规则不一致

**描述**

MySQL Connector/J 的排序规则保存在客户端内，通过获取的服务端版本进行判别。

已知的客户端与服务端排序规则不一致的字符集：

| 字符集 | 客户端默认排序规则 | 服务端默认排序规则 |
| - | - | - |
| `ascii` | `ascii_general_ci` | `ascii_bin` |
| `latin1` | `latin1_swedish_ci` | `latin1_bin` |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**规避方法**

手动设置排序规则，不要依赖客户端默认排序规则（客户端默认排序规则由 MySQL Connector/J 配置文件保存）。

### 参数 `NO_BACKSLASH_ESCAPES` 不生效

**描述**

无法使用 `NO_BACKSLASH_ESCAPES` 参数从而不进行 `\` 字符的转义。已提 [issue](https://github.com/pingcap/tidb/issues/35302)。

**规避方法**

不搭配使用 `NO_BACKSLASH_ESCAPES` 与 `\`，而是使用正常的 `\\` 进行 SQL 编写。

### 未设置索引使用情况参数

**描述**

TiDB 在通讯协议中未设置 `SERVER_QUERY_NO_GOOD_INDEX_USED` 与 `SERVER_QUERY_NO_INDEX_USED` 参数。这将导致以下参数返回与实际不一致：

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**规避方法**

不使用 `noIndexUsed()` 与 `noGoodIndexUsed()` 函数。

### 不支持 `enablePacketDebug` 参数

**描述**

**规避方法**

### 不支持 `UpdatableResultSet`

**描述**

**规避方法**

### 不支持 `useInformationSchema` 参数

**描述**

**规避方法**

### 不支持 `useLocalTransactionState` 参数

**描述**

**规避方法**