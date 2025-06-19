---
title: 标准 SSO 认证
summary: 了解如何通过 Google、GitHub 或 Microsoft 账号登录 TiDB Cloud 控制台。
---

# 标准 SSO 认证

本文档介绍如何通过基本的单点登录（SSO）认证登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，这种方式快速且方便。

TiDB Cloud 支持 Google、GitHub 和 Microsoft 账号的 SSO 认证。如果你通过 SSO 认证登录 TiDB Cloud，由于你的 ID 和凭据存储在第三方 Google、GitHub 和 Microsoft 平台上，你将无法使用 TiDB 控制台修改账号密码和启用多因素认证（MFA）。

> **注意：**
>
> 如果你想通过用户名和密码登录 TiDB Cloud，请参见[密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 使用 Google SSO 登录

要使用 Google 账号登录，请执行以下步骤：

1. 访问 TiDB Cloud [登录](https://tidbcloud.com/)页面。

2. 点击 **Sign in with Google**。你将被重定向到 Google 登录页面。

3. 按照屏幕上的说明输入你的 Google 用户名和密码。

    如果登录成功，你将被重定向到 TiDB Cloud 控制台。

    > **注意：**
    >
    > - 如果这是你第一次使用 Google 登录，系统会询问你是否接受 TiDB Cloud 条款。在你阅读并同意条款后，你将看到 TiDB Cloud 欢迎页面，然后被重定向到 TiDB Cloud 控制台。
    > - 如果你为 Google 账号启用了两步验证（也称为双因素认证），在输入用户名和密码后，你还需要提供验证码。

## 使用 GitHub SSO 登录

要使用 GitHub 账号登录，请执行以下步骤：

1. 访问 TiDB Cloud [登录](https://tidbcloud.com/)页面。

2. 点击 **Sign in with GitHub**。你将被重定向到 GitHub 登录页面。

3. 按照屏幕上的说明输入你的 GitHub 用户名和密码。

    如果登录成功，你将被重定向到 TiDB Cloud 控制台。

     > **注意：**
     >
     > - 如果这是你第一次使用 GitHub 登录，系统会询问你是否接受 TiDB Cloud 条款。在你阅读并同意条款后，你将看到 TiDB Cloud 欢迎页面，然后被重定向到 TiDB Cloud 控制台。
     > - 如果你为 GitHub 账号配置了双因素认证，在输入用户名和密码后，你还需要提供验证码。

## 使用 Microsoft SSO 登录

要使用 Microsoft 账号登录，请执行以下步骤：

1. 访问 TiDB Cloud [登录](https://tidbcloud.com/)页面。

2. 点击 **Sign in with Microsoft**。你将被重定向到 Microsoft 登录页面。

3. 按照屏幕上的说明输入你的 Microsoft 用户名和密码。

    如果登录成功，你将被重定向到 TiDB Cloud 控制台。

     > **注意：**
     >
     > - 如果这是你第一次使用 Microsoft 登录，系统会询问你是否接受 TiDB Cloud 条款。在你阅读并同意条款后，你将看到 TiDB Cloud 欢迎页面，然后被重定向到 TiDB Cloud 控制台。
     > - 如果你为 Microsoft 账号设置了两步验证，在输入用户名和密码后，你还需要提供验证码。
