---
title: 挂载 TiDB Cloud Filesystem
summary: 了解如何在 macOS、Linux 或容器中安全地挂载、使用、刷写和卸载 TiDB Cloud Filesystem。
---

# 挂载 TiDB Cloud Filesystem

在 TiDB Cloud CLI 中，当应用需要通过本地文件系统路径访问远程数据时，你可以挂载 TiDB Cloud Filesystem。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择一个 Filesystem。
- 通过 `--fs-token`、`TI_FS_TOKEN`，或为所选 Filesystem 存储在本地的凭证来提供 FS token。
- 在 Linux 上，安装 FUSE3 并提供对 `/dev/fuse` 的访问权限。

## 选择挂载驱动 {#choose-a-mount-driver}

| 平台 | `--driver auto` | 说明 |
|---|---|---|
| macOS | WebDAV | 安装 macFUSE，并选择 `--driver fuse` 以支持 FUSE。 |
| Linux | FUSE | 不支持 WebDAV 挂载。 |
| Windows | 不支持 | 使用 `ti fs` 数据平面命令而不进行挂载。 |

## 挂载 Filesystem {#mount-the-filesystem}

在 macOS 或 Linux 上，创建一个本地路径，并在后台挂载 Filesystem：

```shell
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path /path/to/workspace
```

CLI 会启动一个后台挂载进程，并写入本地挂载定位文件，以便刷写和卸载命令能够找到正确的进程。

使用 `--remote-path` 可以暴露某个子树，使用 `--read-only` 可以防止写入。要挂载某个层或检查点，请选择 FUSE 驱动，并传入 [`mount-file-system` 参考文档](/ai/ti/reference/ti-fs-mount-file-system.md)中描述的相应层选项。

## 在容器中挂载 {#mount-in-a-container}

仅在镜像中安装 FUSE3 并不足够。主机必须暴露 `/dev/fuse`，并且容器必须被允许执行挂载。对于 Docker，请提供与以下内容等效的设置：

```shell
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  --env TI_FS_FILE_SYSTEM_ID \
  <image>
```

对于 Docker Compose，请传递相同的设备、capability、安全和环境设置：

```yaml
services:
  agent:
    image: <image>
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE}
      TI_FS_FILE_SYSTEM_ID: ${TI_FS_FILE_SYSTEM_ID}
```

> **Warning:**
>
> `SYS_ADMIN` 和未受限的 AppArmor profile 会削弱容器隔离。仅应将它们用于专用且可信的容器。当无法提供 FUSE 访问时，请使用不带挂载的 `ti fs` 数据命令。

## Ubuntu 26.04 挂载路径 {#ubuntu-2604-mount-paths}

Ubuntu 26.04 会将 AppArmor profile 应用于 `/usr/bin/fusermount3`。默认情况下，请使用当前用户主目录、`/mnt`、`/media`、`/tmp` 或 `/run/user/<uid>` 下的路径，而不要使用 `/workspace`。

例如：

```shell
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path "$HOME/workspace"
```

如果应用必须使用 `/workspace`，请将以下规则添加到 `/etc/apparmor.d/local/fusermount3`：

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

然后重新加载该 profile：

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

有关相关错误，请参见[排查 TiDB Cloud CLI 问题](/ai/ti/reference/ti-troubleshooting.md)。

## 刷写或卸载 {#drain-or-unmount}

当你运行 `unmount-file-system` 时，CLI 会在停止挂载之前自动刷写打开的文件句柄和待处理的 FUSE 工作：

```shell
ti fs unmount-file-system --mount-path /path/to/workspace
```

如果你需要在保持 FUSE 挂载在线的同时建立持久性屏障（例如，在创建层检查点之前），请显式运行 `drain-file-system`。该命令会刷写待处理的写入，并等待其完成，而不会卸载：

```shell
ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
```

> **Note:**
>
> 仅 FUSE 挂载支持刷写。WebDAV 挂载会通过正常的文件关闭操作来刷写写入。

> **Warning:**
>
> 当仍有写入处于待处理状态时，或在卸载返回错误后，不要终止机器。内存中的写入和仅存在于本地的 overlay 文件可能会丢失。对于 FUSE 挂载，请在关机前运行 `drain-file-system`，以确认待处理写入已到达远程 Filesystem。对于 WebDAV 挂载，请在应用中关闭文件，并验证 `unmount-file-system` 成功执行。

## 后续操作 {#what-s-next}

- [管理 TiDB Cloud Filesystem 的层和检查点](/ai/ti/guides/manage-filesystem-layers.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)