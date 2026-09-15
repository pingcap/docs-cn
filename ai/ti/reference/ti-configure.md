---
title: ti configure
summary: 以交互式或非交互式方式配置本地 TiDB Cloud CLI 配置（Profile）。
---

# ti configure

配置本地 TiDB Cloud CLI 配置（Profile）。在不带任何参数时，这是 TiDB Cloud CLI 中唯一的交互式命令。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti configure
  [--help]
  [--non-interactive]
  [--region-code <string>]
  [--tidb-cloud-private-key <string>]
  [--tidb-cloud-public-key <string>]
  [--version]
```

## 选项 {#options}

- `--help`：显示帮助信息。
- `--non-interactive`：避免交互提示。通过对应的命令选项或环境变量提供 region code、公钥和私钥。这在脚本或自动化环境中运行 `ti` 时非常有用。
- `--region-code <string>`：默认 region code，例如 `aws-us-east-1` 或 `aws-ap-southeast-1`。
- `--tidb-cloud-private-key <string>`：TiDB Cloud API 私钥。
- `--tidb-cloud-public-key <string>`：TiDB Cloud API 公钥。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 配置值来源 {#configuration-value-sources}

以下命令选项和环境变量提供相同的配置值：

| 配置值 | 命令选项 | 环境变量 |
| --- | --- | --- |
| 默认 region code | `--region-code` | `TI_REGION_CODE` |
| TiDB Cloud API 公钥 | `--tidb-cloud-public-key` | `TIDB_CLOUD_PUBLIC_KEY` |
| TiDB Cloud API 私钥 | `--tidb-cloud-private-key` | `TIDB_CLOUD_PRIVATE_KEY` |

对于每个值，显式提供的命令选项优先于其对应的环境变量。使用 `--non-interactive` 时，这三个值都必须能从这些来源中解析得到。

## 示例 {#examples}

- 以交互方式配置 `ti`：

    ```bash
    # Enter the default region code and TiDB Cloud API keys when prompted.
    ti configure
    ```

- 为自动化场景配置 `ti`：

    ```bash
    # Supply all required values without interactive prompts.
    TI_REGION_CODE="aws-us-east-1" \
    TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
    TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
    ti configure --profile ci --non-interactive
    ```

## 相关文档 {#related-documentation}

- [安装、配置和更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)