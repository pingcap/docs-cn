---
title: TiUniManager 登录与初始化
summary: 了解如何登录 TiUniManager 并进行产品初始化。
---

# TiUniManager 登录与初始化

本文档介绍如何登录 TiUniManager、进行产品初始化，以及如何退出登录。

## 登录 TiUniManager 控制台

使用 TiUniManager 进行操作前，你需要先登录 TiUniManager 控制台。

要登录 TiUniManager 控制台，你需要先参考 [TiUniManager 安装手册](/tiunimanager/tiunimanager-install-and-maintain.md) 开启 TiUniManager 服务。

> **注意：**
>
> 当前 TiUniManager 暂不支持找回密码。

按照以下步骤进行登录：

1. 在浏览器中输入 TiUniManager 地址，跳转至登录页面。
2. 在登录页面输入用户名和密码。默认用户名为 admin，密码为 admin。
3. 点击**登录**按钮进行登录并跳转至概览页面。

## 退出登录

已登录 TiUniManager 控制台的用户可以退出登录，返回登录页面。

> **注意：**
>
> 退出登录后，TiUniManager 会清除缓存数据。如果再次登录同一用户，之前未保存的编辑信息会丢失。

操作步骤：点击用户图标，出现**退出登录**按钮，点击该按钮可退出登录并返回登录页面。

## 产品初始化

首次登录 TiUniManager 系统后，需要完成对 TiDB 所在数据中心、TiDB 产品组件、TiDB 版本信息的初始化。

数据中心当前默认为本地数据中心 (Local)，本地数据中心下按照区域 (Region) - 可用区(Available Zone) 2层层级来组织主机资源。

以下为主机资源组织结构示例：

```
- 本地数据中心（Local）
    - 区域 Region 1
        - 可用区 Zone1_1
        - 可用区 Zone1_2
    - 区域 Region 2
        - 可用区 Zone2_1
        - 可用区 Zone2_2
```

**操作步骤**

1. 登录 TiUniManager 控制台。
2. 进入数据中心初始化页面
    1. 自定义填写本地数据中心的厂商名称。
    2. 自定义填写区域 ID、区域名称。
    3. 自定义填写可用区 ID、可用区名称。
    4. 自定义填写 TiDB、PD、TiKV、TiFlash 实例规格。
3. 点击**下一步**进入产品组件初始化页面。
    5. 自定义填写组件名称。
    6. 设置组件端口范围。
4. 点击**下一步**进入产品版本初始化页面。选择希望安装的 TiDB 版本和架构。
5. 点击**完成**按钮。
