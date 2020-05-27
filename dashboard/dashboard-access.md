---
title: 访问 TiDB Dashboard
category: how-to
---

# 访问 TiDB Dashboard

通过浏览器访问 <http://127.0.0.1:2379/dashboard> （请将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）即可打开 TiDB Dashboard。

> **注意：**
>
> 部署了多个 PD 组件时，填写任意一个 PD 组件地址都可以访问 TiDB Dashboard，但其中仅有一个 PD 组件会真正运行 TiDB Dashboard。访问其他 PD 组件时浏览器都将会被重定向到该 PD 组件。因此若防火墙没有为这个运行 PD 的实例进行配置，可能会出现无法访问 TiDB Dashboard 的情况。

## 浏览器兼容性

TiDB Dashboard 可在常见的、更新及时的桌面浏览器中使用，具体版本号为：

- Chrome >= 77
- Firefox >= 68
- Edge >= 17

> **注意：**
>
> 若使用旧版本浏览器或其他浏览器访问 TiDB Dashboard，部分界面可能不能正常工作。

## 登录

首次访问 TiDB Dashboard 将会显示用户登录界面，如下图所示，可使用 TiDB root 账号登录。

![登录界面](/media/dashboard/dashboard-access-login.png)

如果存在以下情况，则可能会登录失败：

- TiDB root 用户不存在
- PD 未启动或无法访问
- TiDB 未启动或无法访问
- root 密码错误

登录后，24 小时内将保持自动登录状态。参见[登出](#登出)章节了解如何登出用户。

## 切换语言

TiDB Dashboard 目前支持以下语言：

- 简体中文
- 英文

在登录界面中，可点击 Switch Language 下拉框切换界面显示语言：

![切换语言](/media/dashboard/dashboard-access-switch-language.png)

## 登出

登录后，在左侧导航处点击登录用户名，可切换到用户页面。在用户页面点击 **登出**（Logout）按钮即可登出当前用户。登出后，需重新输入用户名密码。

![登出](/media/dashboard/dashboard-access-logout.png)
