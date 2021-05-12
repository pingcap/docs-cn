---
title: tiup mirror rotate
---

# tiup mirror rotate

TiUP 的镜像中有一个非常重要的文件：root.json，里面记录了整个系统需要使用的公钥，是 TiUP 信任链的基础，它的内容主要包含几个部分：

- N 个管理员的签名，对于官方镜像，N 为 5，默认初始化的镜像 N 为 3
- 用于验证以下文件的公钥：
    - root.json
    - index.json
    - snapshot.json
    - timestamp.json
- 过期时间，对于官方镜像，为 root.json 创建时间后延一年

关于镜像的详细介绍可以参考[镜像说明](/tiup/tiup-mirror-reference.md)。

在某些情况下，用户需要更新 root.json:

- 更换镜像的密钥
- 更新证书过期时间

更新 root.json 内容之后，必须由管理员对其进行重新签名，否则客户端会拒绝，更新流程如下：

1. 更新 root.json 的内容
2. N 个管理员对新的 root.json 进行签名
3. 更新 snapshot.json，记录新的 root.json 的 version
4. 对新的 snapshot.json 进行签名
5. 更新 timestamp.json，记录新的 snapshot.json 的 hash
6. 对新的 timestamp.json 进行签名

TiUP 使用命令 `tiup mirror rotate` 来自动化以上流程。

> **注意：**
>
> + 经测试，小于 TiUP v1.3.0 的版本无法正确获得新的 root.json [#983](https://github.com/pingcap/tiup/issues/983)。
> + 使用此功能前请确保所有的 TiUP 客户端升级到了 v1.3.0 或以上版本。

## 语法

```shell
tiup mirror rotate [flags]
```

该命令会启动一个编辑器，修改其内容为目标值（比如将 `expires` 字段的值向后推移），然后需要将 `version` 字段加一并保存。保存之后会启动一个临时的 http 服务器，等待 N 个不同的镜像管理员签名。

镜像管理员签名的方式参考 [sign 命令](/tiup/tiup-command-mirror-sign.md)。

## 选项

### --addr（string，默认 0.0.0.0:8080）

临时服务器的监听地址，需要确保该地址可以被其他镜像管理员访问，这样管理员才能使用 [sign 命令](/tiup/tiup-command-mirror-sign.md)签名。

## 输出

- 各个镜像管理员当前的签名状态

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-component-mirror.md#命令清单)