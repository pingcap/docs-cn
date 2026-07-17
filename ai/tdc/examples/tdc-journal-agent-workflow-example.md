---
title: 使用文件系统 Journal 记录 Agent Workflow
summary: 创建 journal、追加结构化 agent event、搜索 workflow 并验证 journal hash chain。
---

# 使用文件系统 Journal 记录 Agent Workflow

本示例使用结构化、有序 event 记录 agent task，而不是向可修改文件追加未验证文本。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

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
