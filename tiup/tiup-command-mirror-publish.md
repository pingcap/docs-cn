---
title: tiup mirror publish
---

# tiup mirror publish

命令 `tiup mirror publish` 用于发布新组件，或已有组件的新版本。只有有权限的组件管理员才可以发布组件。引入组件管理员的方式可参考 [grant 命令](/tiup/tiup-command-mirror-grant.md)。

## 语法

```shell
tiup mirror publish <comp-name> <version> <tarball> <entry> [flags]
```

各个参数解释如下：

- `<comp-name>`：组件名，如 `tidb`，建议使用符合正则 `^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$` 的字符串
- `<version>`：当前正在发布的版本，版本号需要符合 [Semantic Versioning](https://semver.org/)
- `<tarball>`：`.tar.gz` 包的本地路径，需要将组件的可执行文件及依赖放在该包中，由 TiUP 上传到镜像
- `<entry>`：组件的可执行文件在 `<tarball>` 中的位置

## 选项

### -k, --key（string，默认 ${TIUP_HOME}/keys/private.json）

组件管理员的私钥，客户端需要使用该私钥对组件信息 (`{component}.json`) 进行签名。

### --arch（string，默认 ${GOARCH}）

该 `<tarlball>` 中的二进制文件运行的平台，一个 `<tarball>` 只能选以下三个平台之一：

- `amd64`：表示在 amd64 架构的机器上运行
- `arm64`：表示在 arm64 架构的机器上运行
- `any`：表示可以在以上两种架构的机器上运行（比如脚本）

> **注意：**
>
> 若 `--arch` 指定为 `any`，则 `--os` 也必须指定为 `any`。

### --os（string，默认 ${GOOS}）

该 `<tarlball>` 中的二进制文件运行的操作系统，一个 `<tarball>` 只能选以下三个操作系统之一：

- `linux`：表示在 Linux 操作系统上运行
- `darwin`：表示在 Darwin 操作系统上运行
- `any`：表示可以在以上两种操作系统上运行（比如脚本）

> **注意：**
>
> 若 `--os` 指定为 `any`，则 `--arch` 也必须指定为 `any`。

### --desc（string，默认为空）

该组件的描述信息。

### --hide

- 是否为隐藏组件。若为隐藏组件，则不在 `tiup list` 的列表中显示，但在 `tiup list --all` 的列表中会显示。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

<!-- ### --standalone

- 该组件是否可独立运行。该参数目前尚未启用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。-->

## 输出

- 若成功：无输出
- 若该组件管理员无权修改目标组件：
    - 若使用远程镜像：`Error: The server refused, make sure you have access to this component`
    - 若使用本地镜像：`Error: the signature is not correct`

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-command-mirror.md#命令清单)