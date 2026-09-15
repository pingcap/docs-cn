---
title: ti db list-db-clusters
summary: 列出 TiDB Cloud Starter 集群。
---

# ti db list-db-clusters

列出所选 Region 中的 TiDB Cloud Starter 实例，并支持可选的分页、过滤、排序和 JMESPath 投影。必需的 `--db-cluster-type` 必须为 `starter`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti db list-db-clusters
  --db-cluster-type <string>
  [--filter <string>]
  [--help]
  [--order-by <string>]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## 选项 {#options}

- `--db-cluster-type <string>`：DB 集群类型；必须为 `starter`。\[required]
- `--filter <string>`：TiDB Cloud Starter API 过滤表达式。该 API 支持适用于 `region.provider`、`region.name`、`state`、`projectId`、`clusterId`、`displayName` 和 `labels.<key>` 的 Google AIP 风格 `=` 和 `AND` 表达式。
- `--help`：显示帮助信息。
- `--order-by <string>`：TiDB Cloud Starter API `orderBy` 表达式。`ti` 会将该值原样传递给 API，而不对其进行解释。
- `--page-size <int32>`：要返回的已验证集群数量。如果省略或设置为 `0`，默认值为 `10`。最大值为 `1000`。
- `--page-token <string>`：由之前兼容的 list-db-clusters 调用返回的不透明 ti page token。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出集群：

    ```bash
    # Return TiDB Cloud Starter instances in the profile's configured region as structured JSON.
    ti db list-db-clusters --db-cluster-type starter
    ```

- 列出其他 Region 中的集群：

    ```bash
    # Override the region for this invocation without changing the profile.
    ti --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
    ```

- 选择集群字段：

    ```bash
    # Reduce the result to IDs, names, and lifecycle states.
    ti db list-db-clusters --db-cluster-type starter --query 'clusters[].{id:id,name:display_name,state:state}'
    ```

- 过滤活动集群：

    ```bash
    # Combine this filter with the mandatory effective-region filter.
    ti db list-db-clusters --db-cluster-type starter --filter 'state="ACTIVE"'
    ```

## Region 解析 {#region-resolution}

生效的 Region 按以下顺序解析：全局 `--region`、`TI_REGION_CODE`，然后是所选配置（Profile）的 `region_code`。用户提供的 `--filter` 表达式会与这一必需的 Region 作用域组合使用，不能将结果扩展到其他 Region。

跨 Region 的实例和非 Starter 实例会被省略。如果缺失 service-plan 或 Region 信息，或者这些信息存在冲突，导致 `ti` 无法验证某个实例是否为所选 Region 中的 Starter 实例，该实例也会被省略。

## 过滤与排序行为 {#filter-and-ordering-behavior}

`ti` 会将用户提供的过滤和排序表达式传递给 TiDB Cloud Starter API。无效或不受支持的表达式会被 API 拒绝。有关 API 契约，请参见 [TiDB Cloud API v1beta1 概览](/api/tidb-cloud-api-v1beta1.md)。

## page token 复用 {#page-token-reuse}

该命令可以检索多个 TiDB Cloud API 页面来填充一个结果页，并返回一个 `ti` `next_page_token`。它会省略 API 的 `total_size`，因为该值可能包含已验证结果之外的资源。

page token 只能在相同的配置（Profile）、集群类型、Region、过滤条件和排序条件下复用。如果其重放页面已发生变化，请不要使用 `--page-token`，而是重新开始列出操作。

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)