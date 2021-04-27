---
title: tiup mirror genkey
---

# tiup mirror genkey

在 TiUP [镜像](/tiup/tiup-mirror-reference.md)的定义中，有三类角色：

- 镜像管理员：拥有 `root.json`、`index.json`、`snapshot.json` 以及 `timestamp.json` 的修改权限
- 组件管理员：拥有相关组件的修改权限
- 普通用户：可以下载并使用组件

由于修改文件需要相关的管理员进行签名，因此管理员必须拥有自己的私钥。命令 `tiup mirror genkey` 就是用于生成私钥的。

> **警告：**
>
> 请勿通过网络传输私钥。

## 语法

```shell
tiup mirror genkey [flags]
```

## 选项

### -n, --name

- 密钥的名字，该名字决定最终生成的文件名。生成的私钥文件路径为：`${TIUP_HOME}/keys/{name}.json`，其中 `TIUP_HOME` 为 TiUP 的家目录，默认路径为 `$HOME/.tiup`，`name` 为 `-n/--name` 指定的密钥名字。
- 数据类型：`STRING`
- 如果不指定该选项，密钥名默认为 `private`。

### -p, --public

- 显示当前私钥对应的公钥，当前私钥名字由 `-n/--name` 选项指定。
- 当指定了 `-p/--public` 时，不会创建新的私钥。若 `-n/--name` 指定的私钥不存在，则报错。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --save

- 将公钥信息储存为文件放置于当前目录，文件名称为 `{hash-prefix}-public.json`，其中 `hash-prefix` 为该密钥 ID 的前 16 位。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 若未指定 `-p/--public`：
    - 若指定的密钥已存在：`Key already exists, skipped`
    - 若指定的密钥不存在：`private key have been write to ${TIUP_HOME}/keys/{name}.json`
- 若指定 `-p/--public`：
    - 若指定的密钥不存在：`Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`
    - 若指定的密钥存在：输出该密钥对应的公钥内容
