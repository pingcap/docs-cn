---
title: tiup mirror modify
---

# tiup mirror modify

命令 `tiup mirror modify` 用于修改已发布的组件。只有合法的组件管理员才可以修改组件，且只能修改其自己发布的组件。组件发布方式参考 [`publish` 命令](/tiup/tiup-command-mirror-publish.md)。

## 语法

```shell
tiup mirror modify <component>[:version] [flags]
```

各个参数解释如下：

- `<component>`：组件名称
- `[version]`：想要修改的版本，若不指定，则表示修改整个组件

## 选项

### -k, --key（string，默认 ${TIUP_HOME}/keys/private.json）

组件管理员的私钥，客户端需要使用该私钥对组件信息 (`{component}.json`) 进行签名。

### --yank

- 将指定组件或指定版本标记为不可用：

    - 标记组件不可用之后 `tiup list` 将看不到该组件，也无法安装该组件的新版本。
    - 标记版本不可用之后 `tiup list <component>` 将看不到该版本，也无法安装该版本。

- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --hide

- 将该组件设置为隐藏，隐藏之后该组件将不在 `tiup list` 的列表中显示，但是可通过执行 `tiup list --all` 查看。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

> **注意：**
>
> 该选项只能应用于组件上，无法应用于组件的版本上。

<!-- ### --standalone

- 该组件是否可独立运行。本参数目前尚未启用。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

> **注意：**
>
> 该选项只能应用于组件上，无法应用于组件的版本上。-->

## 输出

- 若成功：无输出
- 若该组件管理员无权修改目标组件：
    - 若使用远程镜像：`Error: The server refused, make sure you have access to this component`
    - 若使用本地镜像：`Error: the signature is not correct`
