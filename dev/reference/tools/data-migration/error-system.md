---
title: DM 错误含义和诊断
category: reference
---

# DM 错误含义和诊断

本文介绍了 DM 的错误输出的详细含义，根据错误信息诊断系统的具体方法，以及针对常见的错误的运维方法。

## 错误输出内容解析

在 DM 1.0.0-GA 版本中引入新的错误系统，错误系统提供了新的错误码机制、增加 class, scope, level 等错误信息、优化错误信息输出、错误调用链和调用堆栈信息，关于错误系统的详细设计和实现可以参考 [RFC 文档: Proposal: Improve Error System](https://github.com/pingcap/dm/blob/master/docs/RFCS/20190722_error_handling.md)。本文以一条实际错误输出来解析错误信息中各个字段的含义。

```
[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"
github.com/pingcap/dm/pkg/terror.(*Error).Delegate
        /root/code/gopath/src/github.com/pingcap/dm/pkg/terror/terror.go:267
github.com/pingcap/dm/dm/master/workerrpc.callRPC
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/workerrpc/rawgrpc.go:124
github.com/pingcap/dm/dm/master/workerrpc.(*GRPCClient).SendRequest
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/workerrpc/rawgrpc.go:64
github.com/pingcap/dm/dm/master.(*Server).getStatusFromWorkers.func2
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/server.go:1125
github.com/pingcap/dm/dm/master.(*AgentPool).Emit
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/agent_pool.go:117
runtime.goexit
        /root/.gvm/gos/go1.12/src/runtime/asm_amd64.s:1337
```

DM 中所有的错误都按照固定格式输出：[错误基本信息] + 错误 message 描述 + 可选的错误堆栈

### 错误基本信息

- code: 错误码，错误唯一标识，同一种错误具有相同的错误码，错误码在各个版本保持唯一不变，需要注意在 DM 迭代过程中可能会移除部分错误但不会移除错误码；新增加的错误会使用新的错误码，不会复用已有的错误码。
- class: 错误分类，用于标识错误发生在哪个系统子模块，所有的错误分类名字，错误对应系统子模块和错误示例如下表所示

| class 名字 | 对应错误系统子模块             | 错误样例                                                     |
| ---------- | ------------------------------ | ------------------------------------------------------------ |
| database   | 执行数据库操作发生错误         | [code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection |
| functional | 系统底层基础函数错误           | [code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement |
| config     | 配置错误                       | [code=20005:class=config:scope=internal:level=medium] empty source-id not valid |
| binlog-op  | binlog 操作出现错误            | [code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid |
| checkpoint | checkpoint 相关操作出现错误    | [code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371 |
| task-check | 进行任务检查时发生的错误       | [code=26002:class=dm-master:scope=upstream:level=high] fail to initial checker: failed to open DSN root:***@127.0.0.1:3306: Error 1045: Access denied for user 'root'@'127.0.0.1' |
| relay-util | relay 模块基础功能执行发生错误 | [code=28001:class=relay-util:scope=internal:level=high] parse server-uuid.index |
| relay-unit | relay 处理单元内发生的错误     | [code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file |
| dump-unit  | dump 处理单元内发生的错误      | [code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO) |
| load-unit  | load 处理单元内发生的错误      | [code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found |
| sync-unit  | sync 处理单元内发生的错误      | [code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values) |
| dm-master  | dm-master 服务内部发生的错误   | [code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused" |
| dm-worker  | dm-worker 服务内部发生的错误   | [code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use `query-status` to query whether the DDL is still blocking |
| dm-tracer  | dm-tracer 服务内部发生的错误   | [code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found |

- scope: 错误作用域，用于标识错误发生时 DM 作用对象的范围、来源，包含 未设置（not-set），上游数据库（upstream），下游数据库（downstream），内部（internal）四种类型。如果出错的逻辑直接涉及到上下游数据库请求，会设置 upstream 或 downstream，其他出错场景目前设置的作用域都为 internal。
- level: 错误级别，错误的严重级别，包括 低级别（low），中级别（medium），高级别（high）。低级别通常是用户操作、输入错误，不影响正常同步任务；中级别通常是用户配置等错误，会影响部分新启动服务，不影响已有系统同步状态；高级别通常是用户需要关注的一些错误，可能存在同步任务中断等风险，需要用户进行处理。

在上述的错误示例中

- code=38008，这是一个 gRPC 通信出错的错误码。
- class=dm-master，表示错误发生在 DM-master 对外发送（请求发送至 DM-worker）的 gRPC 请求出错。
- scope=interal，表示是 DM 内部发生的错误。
- level=high，表示这是一个高级别错误，需要用户注意，更进一步的错误信息可以通过错误 message 和错误堆栈判断。

### 错误 message 描述

错误 message 使用描述性语言来表示错误的详细信息，对于错误调用链上每一层额外增加的错误 message，采用 [errors.Wrap](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error) 的模式进行错误 message 的叠加和保存。wrap 最外层 message 是 DM 内部该错误的描述，wrap 最内层的 message 是该错误最底层出错位置的错误描述。

以上述示例错误的 message 为例

- wrap 最外层 message，grpc request error 是 DM 该错误的描述。
- wrap 最内层 message，connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"， 这是一个 gRPC 底层建立连接失败时返回的错误。

通过对基本错误信息和错误 message 的分析，我们就可以定位该错误发生在 DM-master 向 DM-worker 发送 gRPC 请求时建立连接失败。这个错误通常发生在 DM-worker 没有正常运行。

### 错误堆栈信息

DM 会根据错误的严重程度和必要性来选择是否输出错误堆栈，错误堆栈记录了错误发生时的完整调用堆栈信息，如果通过错误基本信息和错误 message 描述不能完全定位错误发生的原因，可以通过错误堆栈进一步跟进错误发生时代码的运行路径。

## 错误码列表

目前完整的错误码列表可以通过 DM 代码仓库 [已发布错误码](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt) 查询

## 常见错误解释和运维方法

- code=10001: 数据库操作异常，需要进一步分析错误信息和错误堆栈
- code=10002: 数据库底层 bad connection 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。DM 提供针对此类错误的自动恢复，如果长期未恢复需要用户检查网络或 TiDB 状态。
- code=10003: 数据库底层 invalid connection 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。DM 提供针对此类错误的自动恢复，如果未能正常恢复需要用户进一步检查错误信息并根据具体场景进行分析。
- code=10005: 数据库查询类语句出错。
- code=10006: 数据库exexute 类型语句出错，包括 DDL，insert/update/delete 类型 DML。更详细的错误信息可以通过错误 message 获取，错误 message 中通常会包含操作数据库返回的错误码和错误信息。
- code=11006: 该错误是 DM 内置 parser 解析不兼容的 DDL 时出错，出现此类错误时可参考 [Data Migration 故障诊断](/dev/how-to/troubleshoot/data-migration.md) 提供的方案解决。
- code=20010: 处理任务配置时解密数据库密码出错。发生此错误时需要检查任务配置中提供的下游数据库密码是否有使用 dmctl 正确加密。
- code=26002: 任务检查创建数据库连接失败，更详细的错误信息可以通过错误 message 获取，错误 message 中会包含操作数据库返回的错误码和错误信息。发生此错误时可以首先检查 DM-master 所在的机器是否有权限访上游。
- code=38008: DM 组件间 gRPC 通信出错。出现此类错误时可以检查 class 定位错误发生在哪些组件交互环节，根据错误 message 判断是哪类通信错误。譬如如果时 gRPC 建立连接出错，可以检查通信服务端是否服务正常。
