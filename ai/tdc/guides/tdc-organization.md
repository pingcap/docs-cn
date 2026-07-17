---
title: 使用 tdc 管理 TiDB Cloud Organization
summary: 列出可访问的 TiDB Cloud project，并了解 tdc 使用的普通 project 与 virtual project 类型。
---

# 使用 tdc 管理 TiDB Cloud Organization

使用 `tdc organization` 查看已配置 TiDB Cloud API key 能访问的 project。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

使用能够列出 organization project 的 TiDB Cloud API key 运行 `tdc configure`。

## 列出 project

```bash
tdc organization list-projects
```

JSON 响应包含 project ID、名称和 `type`：

- `tidbx` 表示普通 project；
- `tidbx_virtual` 表示作为 Starter 默认 project 的 virtual project。

指定 page size，或者使用返回的 page token 继续：

```bash
tdc organization list-projects --page-size 50
tdc organization list-projects --page-size 50 --page-token "<next-page-token>"
```

输出终端表格或选择字段：

```bash
tdc organization list-projects --output text
tdc organization list-projects --query 'projects[].{id:id,name:name,type:type}'
```

## 默认 virtual project

`tdc configure` 会调用同一 project-listing API。只有找到恰好一个可访问的 `tidbx_virtual` project 时配置才会成功，并将其 ID 保存到所选 profile：

```toml
[default]
region_code = "aws-us-east-1"
project_id = "..."
```

省略 `--project-id` 时，`tdc db create-db-cluster` 会使用该 project。为单个集群覆盖它：

```bash
tdc db create-db-cluster \
  --db-cluster-name project-specific-cluster \
  --db-cluster-type starter \
  --project-id "<project-id>"
```

## 后续步骤

- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
