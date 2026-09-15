---
title: ti fs refresh-file-system-token
summary: 轮转一个 TiDB Cloud Filesystem 访问令牌，并一次性返回其替换后的明文值。
---

# ti fs refresh-file-system-token

轮转提供的 Filesystem 访问令牌，并一次性返回其替换值。认证变更传播后，旧值将停止生效，这个过程大约需要 10 秒。

> **Warning:**
>
> 刷新操作不是幂等的。如果请求成功但你没有收到响应，请不要使用旧令牌重试。请改为生成并分发一个替换令牌。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs refresh-file-system-token
  [--file-system-id <string>]
  [--fs-token <string>]
  [--ttl <duration>]
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：校验从提供的令牌中解码出的 Filesystem ID。加载本地已选中的令牌时，此选项为必需。
- `--fs-token <string>`：提供当前令牌。建议优先使用 `TI_FS_TOKEN`，以避免在 shell 历史记录和进程列表中暴露。默认按以下顺序获取：`TI_FS_TOKEN`，然后是本地已选中的凭证。
- `--ttl <duration>`：设置新的正生命周期，单位为整秒，最长可达 365 天。省略此选项可保留之前的生命周期时长。
- `--dry-run`：在不轮转令牌的情况下，校验令牌选择、Region、TTL 以及已知的本地挂载冲突。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 刷新本地已选中的凭证：

    ```bash
    # ti atomically replaces the local credential after receiving the new token.
    ti fs refresh-file-system-token --file-system-id "<file-system-id>"
    ```

- 刷新由 Secret 管理器提供的令牌：

    ```bash
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Capture the one-time replacement and update the external secret manager yourself.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token > ./refreshed-token.json
    unset TI_FS_TOKEN
    ```

- 在刷新时修改令牌生命周期：

    ```bash
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Rotate the token and set its new lifetime to 30 days.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token --ttl 720h
    unset TI_FS_TOKEN
    ```

## 相关文档 {#related-documentation}

- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [TiDB Cloud CLI 故障排查](/ai/ti/reference/ti-troubleshooting.md)