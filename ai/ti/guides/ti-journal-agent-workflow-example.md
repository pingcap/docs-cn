---
title: 在文件系统日志中记录 Agent 工作流
summary: 创建日志，追加结构化的 agent 事件，搜索工作流，并验证日志哈希链。
---

# 在文件系统日志中记录 Agent 工作流

此工作流会将规划、工具调用、测试、重试和交接记录为结构化、有序且可验证的事件历史。当运维人员需要跨多个 worker 还原实际发生的过程，而不是依赖零散的控制台输出或仅显示最新状态的可变状态文件时，请使用此工作流。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

文件系统日志（Journal）会存储结构化的仅追加条目，这些条目包含序列信息、可搜索字段、可选的幂等键以及哈希链验证。与普通文本文件不同，日志条目一旦写入后就不能再编辑或截断，生产者也无需自行实现解析、并发或重试去重机制。Agent 会追加诸如 `task.started` 和 `test.finished` 之类的语义事件；运维人员则可以查询工作流并验证已存储的链。

## 前提条件 {#prerequisites}

通过已配置的 profile 或文件系统令牌环境选择一个文件系统。

## 步骤 1：创建日志 {#step-1-create-the-journal}

```bash
ti fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## 步骤 2：追加工作流事件 {#step-2-append-workflow-events}

```bash
ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

当工作流可能会重试同一次追加操作时，请指定一个幂等键，并在该逻辑运算的每次重试中复用该键。这样服务就会避免存储重复条目。如果省略此选项，则会生成一个新键，这适用于你不打算重试的追加操作。

## 步骤 3：读取和搜索 {#step-3-read-and-search}

```bash
ti fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

ti fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

`jrn-agent-demo` 的有序 `read-journal-entries` 结果应包含开始、测试和完成事件。

> **Note:**
>
> `search-journal-entries` 会搜索所选文件系统中的所有日志，因为它不接受 journal ID。因此，在此示例中，其他具有相同标签和事件字段的日志也可能匹配该搜索。

`--entry-type` 和 `--status` 过滤器会匹配每个 `--entry-json` 对象中的 `type` 和 `status` 字段。在此示例中，它们会选出 payload 中包含 `"type":"task.finished"` 和 `"status":"completed"` 的条目。

## 步骤 4：验证完整性 {#step-4-verify-integrity}

```bash
ti fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

成功的结果表明，已存储的序列和哈希链是一致的。

## 清理 {#cleanup}

日志是仅追加的，目前在公开的 `ti` 命令集中没有删除命令。对于会创建一次性日志的实验，请使用专用的测试文件系统和唯一的日志 ID，例如 `jrn-test-<run-id>`。仅当其中包含的文件或日志都不再需要时，才删除其所在的文件系统。

## 安全与运维说明 {#security-and-operational-notes}

- 不要在日志 payload 中放入 API keys、密码、包含 Secret 的 SQL 文本或原始文件内容。
- 哈希链验证能够检测已存储链中的不一致性；但它不能证明原始事件本身是真实的。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)
- [将 Secrets 委托给 Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)