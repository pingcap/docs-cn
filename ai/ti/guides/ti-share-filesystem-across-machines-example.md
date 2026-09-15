---
title: 在多台机器之间共享 TiDB Cloud Filesystem
summary: 创建一个 Filesystem，从第二台机器安全地访问它，并验证数据面和挂载可见性。
---

# 在多台机器之间共享 TiDB Cloud Filesystem

此工作流可让两台机器上的用户、自动化程序或代理共享同一个工作空间。当你需要让更改在两台机器上都保持可见，而不想通过 `scp` 或归档上传来交换某个时间点的副本时，可以使用此方法。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

机器 A 创建 Filesystem，并为机器 B 生成一个单独的所有者令牌。随后，两台机器都可以通过数据面命令或挂载目录访问同一个远程命名空间，因此在写入被刷写后，可通过任一接口看到这些写入。这种方式提供了共享目录的行为，而无需手动同步快照，也不需要编写特定于对象存储的传输逻辑。

| 参与方 | 凭证 | 在工作流中的角色 |
| --- | --- | --- |
| 机器 A | 已配置的 `ti` 配置（Profile）及其 FS 所有者令牌 | 创建并管理 Filesystem，写入初始数据，并为机器 B 生成令牌 |
| 机器 B | 它自己的 FS 所有者令牌和 Filesystem 的 Region 代码 | 无需 TiDB Cloud API 密钥或复制的配置（Profile）即可访问 Filesystem |
| TiDB Cloud Filesystem | 不适用 | 提供两台机器共同使用的共享远程命名空间 |

为每台机器使用单独的令牌，可以在不影响机器 A 的情况下对机器 B 执行（权限）回收。由于这两个令牌都授予 owner 访问权限，因此应将它们作为 Secret 进行传输和存储。

## 前提条件 {#prerequisites}

- 机器 A 已配置 `ti`。
- 两台机器都已安装 `ti`。
- 机器 A 已安装 `jq`。
- 你有一个安全的 Secret 传输通道。

## 步骤 1：在机器 A 上创建 Filesystem {#step-1-create-the-filesystem-on-machine-a}

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs generate-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-name machine-b \
  --ttl 720h > ./machine-b-token.json

printf 'from machine A\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /shared/origin.txt
```

通过 Secret 管理器传输 `machine-b-token.json` 中的 `fs_token`，并传达规范的 Region 代码。将 `FILE_SYSTEM_ID` 保留在机器 A 上用于控制面操作，然后在安全存储好令牌后删除这两个 JSON 文件。

## 步骤 2：在机器 B 的内存中进行配置 {#step-2-configure-machine-b-in-memory}

```bash
export TI_FS_TOKEN="<owner-token-from-secret-manager>"
export TI_REGION_CODE="<filesystem-region-code>"
```

将 `TI_REGION_CODE` 设置为创建 Filesystem 时所在的 Region。不需要执行 `ti configure`。

## 步骤 3：在机器 B 上验证直接可见性 {#step-3-verify-direct-visibility-on-machine-b}

```bash
ti fs read-file --path /shared/origin.txt
printf 'from machine B\n' | ti fs copy-file --from-stdin --to-remote /shared/second.txt
```

## 步骤 4：验证挂载和数据面可见性 {#step-4-verify-mount-and-data-plane-visibility}

```bash
mkdir -p /path/to/shared-workspace
ti fs mount-file-system \
  --mount-path /path/to/shared-workspace

cat /path/to/shared-workspace/shared/origin.txt
printf 'written through mount\n' > /path/to/shared-workspace/shared/mounted.txt

# Graceful unmount flushes pending writes before the data-plane read.
ti fs unmount-file-system --mount-path /path/to/shared-workspace
ti fs read-file --path /shared/mounted.txt
```

第一次读取证明数据面写入可通过挂载看到。最后一次读取证明挂载写入在被刷写后可通过数据面看到。

## 清理 {#cleanup}

### 在机器 B 上 {#on-machine-b}

完成步骤 4 中的优雅的卸载后，从当前 shell 中移除凭证：

```bash
unset TI_FS_TOKEN TI_REGION_CODE
```

### 在机器 A 上 {#on-machine-a}

```bash
rm -f ./filesystem.json ./machine-b-token.json

ti fs list-file-system-tokens --file-system-id "$FILE_SYSTEM_ID" --output text
ti fs delete-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-id "<machine-b-token-id>"
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## 安全说明 {#security-notes}

- 每个 FS token 都授予 owner 访问权限。应将其作为 Secret 传输，不要通过聊天工具或命令历史传递，并为每台机器使用单独的令牌。
- 并发写入者可能会覆盖相同路径；请在工作流级别协调所有权。
- 在优雅的卸载完成之前，不要终止机器。仅当你需要在保持 FUSE 挂载在线的同时确保远端持久性时，才使用显式的刷写。

## 后续操作 {#what-s-next}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [在 Agent Sandbox 中使用 Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md)
