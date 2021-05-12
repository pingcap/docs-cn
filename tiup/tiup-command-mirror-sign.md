---
title: tiup mirror sign
---

# tiup mirror sign

命令 `tiup mirror sign` 用于对[镜像](/tiup/tiup-mirror-reference.md)中定义的元信息文件（*.json）进行签名，这些文件可能储存在本地文件系统，也可以放在远端使用 http 协议提供签名入口。

## 语法

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>` 为被签名的文件地址，可以有两种地址：

- 网络地址：http 或者 https 开头，如 `http://172.16.5.5:8080/rotate/root.json`
- 本地文件路径：相对路径或绝对路径均可

如果是网络地址，该地址必须提供以下功能：

- 支持以 `http get` 访问，此时应当返回被签名文件的完整内容（包含 signatures 字段）
- 支持以 `http post` 访问，客户端会在 `http get` 返回的内容的 signatures 字段中加上本次的签名 POST 到该地址

## 选项

### -k, --key (string, 默认 ${TIUP_HOME}/keys/private.json)

指定用于签名的私钥位置。

### --timeout (int，默认 10)

通过网络签名时网络的访问超时时间，单位为秒。

> **注意：**
>
> 只有当 `<manifest-file>` 为网络地址时该选项有效。

## 输出

- 成功：无输出
- 文件已被指定的 key 签名过：`Error: this manifest file has already been signed by specified key`
- 文件不是合法的 manifest：`Error: unmarshal manifest: %s`

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-component-mirror.md#命令清单)