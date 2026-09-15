---
title: 使用 TiDB Cloud Filesystem 数据
summary: 了解如何使用 CLI 在 TiDB Cloud Filesystem 中复制、读取、组织、搜索和检查文件及目录。
---

# 使用 TiDB Cloud Filesystem 数据

在 TiDB Cloud CLI 中，你可以使用 [`ti fs` 命令](/ai/ti/reference/ti-filesystem.md) 在本地存储与 TiDB Cloud Filesystem 之间传输数据，并管理其远程命名空间。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- [创建一个 Filesystem](/ai/ti/guides/manage-filesystem-resources.md) 或获取现有 Filesystem 的访问权限。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择 Filesystem。请为每项操作提供具有相应权限的 FS token。

## 复制数据 {#copy-data}

将本地文件上传到远程路径：

```shell
ti fs copy-file --from-local ./report.md --to-remote /reports/report.md
```

[`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) 还支持下载、流式传输、追加、断点续传和递归复制。

## 读取和检查数据 {#read-and-inspect-data}

将文件或字节范围读取到标准输出：

```shell
ti fs read-file --path /reports/report.md --offset 0 --length 1024
```

列出一个目录并检查某个路径：

```shell
ti fs list-files --path /reports --output text
ti fs describe-file --path /reports/report.md
```

## 组织命名空间 {#organize-the-namespace}

使用相应命令创建目录、移动文件以及删除数据：

```shell
ti fs create-directory --path /reports/archive
ti fs move-file --from-remote /draft.md --to-remote /reports/final.md
ti fs delete-file --path /scratch --recursive
```

你还可以使用 `chmod-file`、`create-symlink` 和 `create-hardlink` 来管理 POSIX 风格的元信息和链接。

> **警告：**
>
> `delete-file --recursive` 会永久删除目标目录及其内容。运行该命令前，请先验证远程路径。

## 搜索数据 {#search-for-data}

搜索某一路径下的文件内容：

```shell
ti fs search-file-content --path /reports --pattern "TODO"
```

按名称、类型、标签、大小或时间戳查找路径：

```shell
ti fs find-files --path /reports --file-name-pattern "*.md" --tag stage=review
```

## 后续操作 {#what-s-next}

- [管理 TiDB Cloud Filesystem 的层和检查点](/ai/ti/guides/manage-filesystem-layers.md)
- [挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)