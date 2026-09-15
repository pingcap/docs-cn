---
title: ti fs generate-file-system-scoped-token
summary: 为单个 TiDB Cloud Filesystem 生成一个受路径和操作限制的令牌。
---

# ti fs generate-file-system-scoped-token

从所有者令牌生成一个具有受限路径和操作访问权限的范围受限令牌。令牌值只会出现在命令输出中，之后无法再次获取。范围受限令牌只能访问其被允许的路径前缀和操作。

范围受限令牌仅在请求的路径和操作被覆盖时，支持普通文件、上传、Layer 和挂载操作。`chmod`、Git workspace API、日志（Journal）、Vault、SQL、派生、事件以及令牌管理操作不适用于范围受限令牌。范围受限令牌可以在不改变其作用域的情况下自行刷新。

这些操作的含义如下。一个命令可能需要多个操作，例如对复制源需要 `read`，对复制目标需要 `write`。

| 操作 | 允许 |
| --- | --- |
| `read` | 读取文件内容和元信息。 |
| `list` | 列出目录下的条目。 |
| `search` | 在此前缀下搜索或查找文件。需要 `read`。 |
| `write` | 创建或更改文件、目录、链接和复制目标。 |
| `delete` | 删除路径，或在移动操作期间移除源路径。 |

> **重要：**
>
> 允许搜索时，请在同一个 `--allow` 值中同时包含 `search` 和 `read`。如果作用域中包含 `search` 但不包含 `read`，CLI 会拒绝该作用域。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs generate-file-system-scoped-token
  --ttl <duration>
  --allow <prefix:ops>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--subject <string>]
  [--store-locally]
  [--replace]
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--ttl <duration>`：设置一个有限的正令牌有效期，并解析为整秒。此选项为必需项。
- `--allow <prefix:ops>`：允许在一个远程路径前缀下执行操作。对多个前缀可重复使用此选项。操作包括 `read`、`list`、`search`、`write` 和 `delete`；其中 `search` 需要 `read`。此选项为必需项。
- `--file-system-id <string>`：校验嵌入在所有者令牌中的 Filesystem ID。仅当加载本地存储的所有者令牌时，此选项才是必需的。
- `--fs-token <string>`：提供所有者 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--subject <string>`：设置一个可选的服务端审计标签，最大长度为 64 字节。它不是唯一选择器。
- `--store-locally`：为此配置（Profile）和 Filesystem 存储并选中生成的范围受限令牌。
- `--replace`：替换当前已选中的本地令牌。需要与 `--store-locally` 一起使用，且不会（权限）回收之前的远程令牌。
- `--dry-run`：在不生成令牌的情况下，校验所有者凭证、Region、有效期、作用域以及本地存储前置条件。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 为一个 workspace 提供 sandbox 的读写访问权限：

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager, then create a token limited to /workspace.
    ti fs generate-file-system-scoped-token \
      --subject sandbox-agent \
      --ttl 24h \
      --allow /workspace:read,list,write
    ```

- 将可写的 workspace 数据与只读 artifacts 分离：

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager. Repeat --allow to assign different operations to independent prefixes.
    ti fs generate-file-system-scoped-token \
      --ttl 8h \
      --allow /workspace:read,list,write,delete \
      --allow /artifacts:read,list
    ```

- 选中生成的范围受限令牌，以供后续本地命令使用：

    ```bash
    # Replacing the local selection does not revoke the previous remote owner token.
    ti fs generate-file-system-scoped-token \
      --file-system-id "<file-system-id>" \
      --ttl 1h \
      --allow /task:read,list,write \
      --store-locally \
      --replace
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md)