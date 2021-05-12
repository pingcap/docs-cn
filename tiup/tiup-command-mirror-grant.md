---
title: tiup mirror grant
---

# tiup mirror grant

命令 `tiup mirror grant` 用来向当前镜像中引入一个组件管理员。

组件管理员可以使用其密钥发布新的组件，也可以对其之前发布的组件作出修改。添加组件管理员时，待添加的组件管理员需要先将其公钥发送给镜像管理员。

> **注意：**
>
> 该命令仅支持在当前镜像为本地镜像时使用。

## 语法

```shell
tiup mirror grant <id> [flags]
```

`<id>` 为该组件管理员的 ID，该 ID 需要在整个镜像中唯一，建议使用符合正则 `^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$` 的字符串。

## 选项

### -k, --key（string，默认 ${TIUP_HOME}/keys/private.json）

指定引入的组件管理员的密钥。该密钥可以是公钥也可以是私钥。如果传入私钥，会被转换成对应的公钥储存在镜像中。

一个密钥只能被一个组件管理员使用。

### -n, --name（string，默认 `<id>`）

指定组件管理员的名字，该名字会展示在组件列表的 `Owner` 字段上。若未指定 `-n/--name` 则使用 `<id>` 作为组件管理员名字。

### 输出

- 若执行成功：无输出
- 若管理员 ID 重复：`Error: owner %s exists`
- 若密钥已被其他管理员使用：`Error: key %s exists`

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-command-mirror.md#命令清单)
