---
title: tiup mirror merge
---

# tiup mirror merge

命令 `tiup mirror merge` 用于合并一个或多个镜像到当前镜像。

执行此命令需要满足几个条件：

- 目标镜像的所有组件的管理员 ID 必须在当前镜像中存在。
- 执行该命令用户的 `${TIUP_HOME}/keys` 目录中有上述管理员 ID 在当前镜像中对应的所有私钥（可以使用命令 [`tiup mirror set`](/tiup/tiup-command-mirror-set.md) 将当前镜像切换成目前有权限修改的镜像）。

## 语法

```shell
tiup mirror merge <mirror-dir-1> [mirror-dir-N] [flags]
```

- `<mirror-dir-1>`：要合并到当前镜像的第一个镜像
- `[mirror-dir-N]`：要合并到当前镜像的第 N 个镜像

## 选项

无

## 输出

- 成功：无输出
- 当前镜像缺失目标镜像某个组件的管理员，或 `${TIUP_HOME}/keys` 缺失该管理员的私钥：`Error: missing owner keys for owner %s on component %s`

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-component-mirror.md#命令清单)