---
title: OAuth 2.0
summary: 了解如何在 TiDB Cloud 中使用 OAuth 2.0。
---

# OAuth 2.0

本文档介绍如何使用 OAuth 2.0 访问 TiDB Cloud。

OAuth（Open Authorization 的缩写）是一个开放标准的认证协议，允许代表用户安全地访问资源。它为第三方应用程序提供了一种访问用户资源的方式，而无需暴露用户的凭据。

[OAuth 2.0](https://oauth.net/2/) 是 OAuth 的最新版本，已成为授权的行业标准协议。OAuth 2.0 的主要优势包括：

- 安全性：通过使用基于令牌的认证，OAuth 2.0 最大限度地降低了密码被盗和未经授权访问的风险。
- 便利性：你可以授予和撤销对数据的访问权限，而无需管理多个凭据。
- 访问控制：你可以指定授予第三方应用程序的确切访问级别，确保仅授予必要的权限。

## OAuth 授权类型

OAuth 框架为不同的使用场景指定了几种授权类型。TiDB Cloud 支持两种最常见的 OAuth 授权类型：设备码和授权码。

### 设备码授权类型

通常用于无浏览器或输入受限的设备在设备流程中使用先前获得的设备码交换访问令牌。

### 授权码授权类型

这是最常见的 OAuth 2.0 授权类型，它使网络应用程序和原生应用程序都可以在用户授权应用程序后获取访问令牌。

## 使用 OAuth 访问 TiDB Cloud

你可以使用 OAuth 2.0 设备码授权类型访问 TiDB Cloud CLI：

- [ticloud auth login](/tidb-cloud/ticloud-auth-login.md)：向 TiDB Cloud 进行认证
- [ticloud auth logout](/tidb-cloud/ticloud-auth-logout.md)：从 TiDB Cloud 登出

如果你的应用程序需要使用 OAuth 访问 TiDB Cloud，请提交申请[成为云和技术合作伙伴](https://www.pingcap.com/partners/become-a-partner/)（在**合作伙伴计划**中选择**云和技术合作伙伴**）。我们会与你联系。

## 查看和撤销已授权的 OAuth 应用程序

你可以在 TiDB Cloud 控制台中查看已授权的 OAuth 应用程序记录，步骤如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左下角的 <MDSvgIcon name="icon-top-account-settings" />。
2. 点击**账号设置**。
3. 点击**已授权的 OAuth 应用程序**选项卡。你可以查看已授权的 OAuth 应用程序。

你可以随时点击**撤销**来撤销你的授权。
