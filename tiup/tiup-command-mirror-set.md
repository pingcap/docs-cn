---
title: tiup mirror set
---

# tiup mirror set

命令 `tiup mirror set` 用于切换当前镜像，支持本地文件系统和远程网络两种镜像。

官方镜像为 `https://tiup-mirrors.pingcap.com`。

## 语法

```shell
tiup mirror set <mirror-addr> [flags]
```

`<mirror-addr>` 为镜像地址，可以有两种形式：

- 网络地址：以 http 或者 https 开头，如 `http://172.16.5.5:8080`，`https://tiup-mirrors.pingcap.com` 等
- 本地文件路径：镜像目录的绝对路径，比如 `/path/to/local-tiup-mirror`

## 选项

### -r, --root（string，默认 `{mirror-dir}/root.json`）

指定根证书。

每个镜像的根证书不相同，而根证书是镜像安全性最关键的一环，在使用网络镜像时，可能遭受中间人攻击，为了避免此类攻击，推荐手动将根网络镜像的根证书下载到本地：

```
wget <mirror-addr>/root.json -O /path/to/local/root.json
```

然后进行人工查验，认定无误之后，再通过手工指定根证书的方式切换镜像：

```
tiup mirror set <mirror-addr> -r /path/to/local/root.json
```

在这种操作方式下，如果中间人在 `wget` 之前攻击了镜像，用户可发现根证书不正确。如果在 `wget` 之后攻击了镜像，TiUP 会发现镜像和根证书不符。

## 输出

无

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-command-mirror.md#命令清单)