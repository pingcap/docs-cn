---
title: 使用文件系统 Journal 记录 Agent Workflow
summary: 创建 journal、追加结构化 agent event、搜索 workflow 并验证 journal hash chain。
---

# 使用文件系统 Journal 记录 Agent Workflow

本示例使用结构化、有序且可验证的事件历史记录 Agent 任务。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## Agent 面临的问题

一个 Agent 任务可能经历规划、工具调用、测试、重试以及多个 worker 之间的交接。任务失败时，运维人员需要知道发生了哪些事件以及准确顺序。普通控制台输出往往分散在多个进程中，而可修改的状态文件通常只保留最后状态。

## 向普通文件追加内容为什么不够

文本文件写入后仍然可以被修改或截断，没有内置 sequence 和 hash chain，也要求每个 producer 自行设计解析与并发规则。追加操作发生重试时，如果应用没有额外实现幂等逻辑，还可能生成重复事件。

## tdc 如何改变工作流

文件系统 Journal 保存带 sequence、可搜索字段、可选 idempotency key 和 hash-chain verification 的结构化只追加 entry。Agent 可以追加 `task.started`、`test.finished` 等语义事件；运维人员能够查询工作流并验证已保存的 chain，而不需要将可修改日志文件当作审计证据。

## 前置条件

通过已配置 profile 或 FS token 环境选择文件系统。

## 第 1 步：创建 journal

```bash
tdc fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## 第 2 步：追加 workflow event

```bash
tdc fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

tdc fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

## 第 3 步：读取和搜索

```bash
tdc fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

tdc fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

有序结果应包含 start、test 和 completion event。

## 第 4 步：验证完整性

```bash
tdc fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

成功结果表示已保存 sequence 和 hash chain 保持一致。

## 清理

Journal 仅追加，当前 tdc public surface 没有 delete command。请使用合成 journal ID，并将其作为 workflow evidence 保留。只有整个文件系统内容不再需要时才删除对应文件系统。

## 安全说明

- 不要在 journal payload 中放入 API key、password、包含 secret 的 SQL 或原始 file content。
- Hash-chain verification 检测已存储 chain 的不一致，不能证明原始 event 真实。

## 后续步骤

- [使用 TiDB Cloud 文件系统 Journal](/ai/tdc/guides/tdc-filesystem-journal.md)
- [向 Agent 委派 Vault 密钥](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)
