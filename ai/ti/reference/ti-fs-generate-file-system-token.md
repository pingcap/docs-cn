---
title: ti fs generate-file-system-token
summary: 为一个 TiDB Cloud Filesystem 生成额外的所有者令牌。
---

# ti fs generate-file-system-token

使用 TiDB Cloud API 凭证为一个文件系统生成所有者令牌。令牌值只会显示在命令输出中，之后无法再次获取。使用 `--store-locally` 可将令牌保存到本地凭证存储中。现有的文件系统令牌不能用于生成所有者令牌。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs generate-file-system-token
  --file-system-id <string>
  --token-name <string>
  (--ttl <duration> | --no-expiration)
  [--dry-run]
  [--help]
  [--replace]
  [--store-locally]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：指定拥有该令牌的文件系统。文件系统令牌不能替代此选项，也不能用于授予权限以生成所有者令牌。此选项为必填项。
- `--token-name <string>`：设置一个最长为 64 字节的操作令牌名称。名称不要求唯一。此选项为必填项。
- `--ttl <duration>`：设置一个以整秒为单位的正有效期，最长为 365 天。必须且只能指定 `--ttl` 和 `--no-expiration` 其中之一。
- `--no-expiration`：创建一个永不过期的令牌。必须且只能指定 `--ttl` 和 `--no-expiration` 其中之一。
- `--store-locally`：为此配置（Profile）和文件系统存储并选中生成的令牌。
- `--replace`：替换当前已选中的本地令牌。需要与 `--store-locally` 一起使用，且不会对之前的远程令牌执行（权限）回收。
- `--dry-run`：在不生成令牌的情况下，验证凭证、Region、有效期以及本地存储前置条件。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 为 CI 作业生成一个短期有效的令牌：

    ```bash
    # Save the one-time plaintext response in an owner-only file.
    umask 077
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name ci-deploy \
      --ttl 24h > ./ci-token.json
    ```

- 为另一台机器生成一个永不过期的令牌：

    ```bash
    # Generation does not change the current local selection by default.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name workstation \
      --no-expiration
    ```

- 生成并选中一个替换用的本地令牌：

    ```bash
    # The old remote token remains active until you explicitly disable or delete it.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name local-owner-v2 \
      --ttl 720h \
      --store-locally \
      --replace
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)