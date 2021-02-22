---
title: tiup dm list
---

# tiup dm list

tiup-dm 支持使用同一个中控机部署多套集群，而命令 `tiup dm list` 可以查看当前登陆的用户使用该中控机部署了哪些集群。

> **注意：**
> 
> 部署的集群数据默认放在 `~/.tiup/storage/dm/clusters/` 目录下，因此在同一台中控机上，当前登录用户无法查看其他用户部署的集群。

## 语法

```sh
tiup dm list [flags]
```

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

输出含有以下字段的表格：

- Name：集群名字
- User：部署用户
- Version：集群版本
- Path：集群部署数据在中控机上的路径
- PrivateKey：连接集群的私钥所在路径
