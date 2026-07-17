---
title: 使用 TiDB Cloud 文件系统 Journal
summary: 创建仅追加 workflow journal，追加和搜索结构化事件，并验证 hash chain。
---

# 使用 TiDB Cloud 文件系统 Journal

`tdc fs-journal` 为 agent 和 workflow 事件提供仅追加、可验证的 ledger。与可修改文本文件不同，journal 会分配有序 sequence number、支持结构化搜索，并维护可检测篡改的 hash chain。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

通过 profile 选择文件系统，或者提供 `TDC_FS_TOKEN`、`TDC_REGION_CODE` 和 `TDC_FS_FILE_SYSTEM_NAME`。

## 创建 journal

```bash
tdc fs-journal create-journal \
  --journal-id jrn-demo \
  --journal-kind agent \
  --title "demo task" \
  --actor agent:tdc \
  --label env=dev
```

`--journal-id` 可省略，由系统生成。Label 可重复。

## 追加 entry

追加一个或多个 JSON object：

```bash
tdc fs-journal append-journal-entries \
  --journal-id jrn-demo \
  --entry-json '{"type":"task.started","status":"running"}' \
  --entry-json '{"type":"tool.called","tool":"tdc"}'
```

使用 `--entry-type` 为缺少 `type` 的 entry 提供默认值，并通过 `--source` 或可重复 `--subject` 添加 metadata。`--idempotency-key` 使重试行为确定；省略时由 tdc 生成。

Pipeline 可以从 stdin 发送 JSON Lines，或使用 `--json-array` 读取 JSON array。

## 读取和搜索

读取某个 sequence 后的 entry：

```bash
tdc fs-journal read-journal-entries \
  --journal-id jrn-demo \
  --after-seq 0 \
  --limit 100
```

跨 journal 搜索：

```bash
tdc fs-journal search-journal-entries \
  --entry-type task.started \
  --journal-kind agent \
  --label env=dev \
  --include-entries
```

搜索还支持 status、actor、subject、`--since`、`--until`、`--limit` 和 pagination cursor。

## 验证完整性

```bash
tdc fs-journal verify-journal \
  --journal-id jrn-demo \
  --output text
```

验证会重新计算有序 hash chain，并报告 entry 是否保持内部一致。它不能证明 event payload 在最初追加时是真实的。

## 后续步骤

- [使用 Journal 记录 Agent Workflow](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
