---
title: tiup mirror
---

# tiup mirror

在 TiUP 中，[镜像](/tiup/tiup-mirror-reference.md)是一个非常重要的概念，目前 TiUP 支持两种形式的镜像：

- 本地镜像：即 TiUP 客户端和镜像在同一台机器上，客户端通过文件系统访问镜像
- 远程镜像：即 TiUP 客户端和镜像不在同一台机器上，客户端通过网络访问镜像

命令 `tiup mirror` 用于管理镜像，提供了创建镜像，组件发布，密钥管理等多种功能。

## 语法

```shell
tiup mirror <command> [flags]
```

`<command>` 代表子命令，支持的子命令列表请参考下方命令清单。

## 选项

无

## 命令清单

- [genkey](/tiup/tiup-command-mirror-genkey.md): 生成私钥文件
- [sign](/tiup/tiup-command-mirror-sign.md): 使用私钥文件对特定文件进行签名
- [init](/tiup/tiup-command-mirror-init.md): 创建一个空的镜像
- [set](/tiup/tiup-command-mirror-set.md): 设置当前镜像
- [grant](/tiup/tiup-command-mirror-grant.md): 为当前镜像引入新的组件管理员
- [publish](/tiup/tiup-command-mirror-publish.md): 向当前镜像推送新的组件
- [modify](/tiup/tiup-command-mirror-modify.md): 修改当前镜像中的组件属性
- [rotate](/tiup/tiup-command-mirror-rotate.md): 更新当前镜像中的根证书
- [clone](/tiup/tiup-command-mirror-clone.md): 从已有镜像克隆一个新的镜像
- [merge](/tiup/tiup-command-mirror-merge.md): 合并镜像

[<< 返回上一页 - TiUP 命令清单](/tiup/tiup-reference.md#命令清单)