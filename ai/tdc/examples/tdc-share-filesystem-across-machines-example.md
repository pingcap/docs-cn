---
title: 在不同机器间共享 TiDB Cloud 文件系统
summary: 创建一个文件系统，通过安全方式从第二台机器访问，并验证 data plane 与 mount 的可见性。
---

# 在不同机器间共享 TiDB Cloud 文件系统

本示例在机器 A 上创建文件系统，并在不复制 tdc profile 的情况下让机器 B 访问相同数据。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

- 机器 A 已配置 tdc。
- 两台机器均已安装 tdc。
- 你可以使用安全的 secret-transfer channel。

## 第 1 步：在机器 A 创建文件系统

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name shared-workspace \
  --query fs_token \
  --output text)"

printf 'from machine A\n' | tdc fs copy-file \
  --file-system-name shared-workspace \
  --from-stdin \
  --to-remote /shared/origin.txt
```

通过 secret manager 传输 token，同时传达 canonical region code 和文件系统名称。

## 第 2 步：在机器 B 以内存方式配置

```bash
export TDC_FS_TOKEN="<owner-token-from-secret-manager>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="shared-workspace"
```

无需运行 `tdc configure`。

## 第 3 步：验证机器 B 的直接可见性

```bash
tdc fs read-file --path /shared/origin.txt
printf 'from machine B\n' | tdc fs copy-file --from-stdin --to-remote /shared/second.txt
```

## 第 4 步：验证 mount 与 data-plane 可见性

```bash
mkdir -p /path/to/shared-workspace
tdc fs mount-file-system \
  --file-system-name shared-workspace \
  --mount-path /path/to/shared-workspace

cat /path/to/shared-workspace/shared/origin.txt
printf 'written through mount\n' > /path/to/shared-workspace/shared/mounted.txt
tdc fs read-file --path /shared/mounted.txt
```

第一次读取证明 data-plane write 对 mount 可见；最后一次读取证明 mount write 刷出后对 data plane 可见。

## 清理

停止 writer。如果 mount 是 FUSE：

```bash
tdc fs drain-file-system --mount-path /path/to/shared-workspace
```

Unmount 任一 driver：

```bash
tdc fs unmount-file-system --mount-path /path/to/shared-workspace
unset TDC_FS_TOKEN TDC_REGION_CODE TDC_FS_FILE_SYSTEM_NAME
```

在机器 A 上：

```bash
tdc fs delete-file-system \
  --file-system-name shared-workspace \
  --confirm-file-system-name shared-workspace
```

## 安全说明

- FS token 授予 owner access，应作为 secret 传输，不能放入聊天或 command history。
- 并发 writer 可以覆盖相同路径，请在 workflow 层协调 ownership。
- Pending FUSE write 未 drain 前不要终止机器。

## 后续步骤

- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [在 Agent Sandbox 中使用文件系统](/ai/tdc/examples/tdc-agent-sandbox-example.md)
