---
title: 密码认证
summary: 了解如何在 TiDB Cloud 控制台中管理密码和启用多因素认证（MFA）。
---

# 密码认证

本文档介绍如何在 TiDB Cloud 控制台中管理密码和启用多因素认证（MFA）。本文档仅适用于使用邮箱和密码[注册](https://tidbcloud.com/free-trial) TiDB Cloud 的用户。

## 注册

你可以使用邮箱和密码[注册](https://tidbcloud.com/free-trial) TiDB Cloud，或选择使用 Google、GitHub 或 Microsoft 账号进行单点登录（SSO）。

- 如果你使用邮箱和密码注册 TiDB Cloud，可以按照本文档管理密码。
- 如果你选择使用 Google、GitHub 或 Microsoft SSO 登录 TiDB Cloud，你的密码由所选平台管理，无法使用 TiDB Cloud 控制台更改。

要使用邮箱和密码注册 TiDB Cloud 账号，请执行以下步骤：

1. 访问 TiDB Cloud [注册](https://tidbcloud.com/free-trial)页面并填写注册信息。

2. 阅读隐私政策和服务协议，然后选择**我同意隐私政策和服务协议**。

3. 点击**注册**。

你将收到 TiDB Cloud 的验证邮件。要完成整个注册过程，请检查你的邮箱并确认注册。

## 登录或登出

### 登录

要使用邮箱和密码登录 TiDB Cloud，请执行以下步骤：

1. 访问 TiDB Cloud [登录](https://tidbcloud.com/)页面。

2. 填写你的邮箱和密码。

3. 点击**登录**。

如果登录成功，你将被引导至 TiDB Cloud 控制台。

### 登出

在 TiDB Cloud 控制台左下角，点击 <MDSvgIcon name="icon-top-account-settings" /> 并选择**退出登录**。

## 密码策略

TiDB Cloud 为注册用户设置了默认密码策略。如果你的密码不符合策略要求，在设置密码时会收到提示。

默认密码策略如下：

- 至少 8 个字符长度。
- 至少包含 1 个大写字母（A-Z）。
- 至少包含 1 个小写字母（a-z）。
- 至少包含 1 个数字（0-9）。
- 新密码不能与前四个密码相同。

## 重置密码

> **注意：**
>
> 本节仅适用于使用邮箱和密码注册的 TiDB Cloud 用户。如果你使用 Google SSO 或 GitHub SSO 注册 TiDB Cloud，你的密码由 Google 或 GitHub 管理，无法使用 TiDB Cloud 控制台更改。

如果你忘记了密码，可以通过邮箱重置密码，步骤如下：

1. 访问 TiDB Cloud [登录](https://tidbcloud.com/)页面。

2. 点击**忘记密码**，然后检查你的邮箱获取重置密码的链接。

## 更改密码

> **注意：**
>
> 如果你使用邮箱和密码注册 TiDB Cloud，建议每 90 天重置一次密码。否则，当你登录 TiDB Cloud 时，会收到密码过期提醒，提示你更改密码。

1. 点击 TiDB Cloud 控制台左下角的 <MDSvgIcon name="icon-top-account-settings" />。

2. 点击**账号设置**。

3. 在**密码**部分，点击**更改密码**，然后检查你的邮箱获取 TiDB Cloud 重置密码的链接。

## 管理多因素认证（可选）

> **注意：**
>
> - 本节仅适用于使用邮箱和密码[注册](https://tidbcloud.com/free-trial) TiDB Cloud 的用户。如果你使用 Google、GitHub 或 Microsoft SSO 注册 TiDB Cloud，你可以在所选身份管理平台上启用 MFA。
> - 如果你在 SSO 登录场景下启用了 TiDB Cloud MFA，请在 **2025 年 9 月 30 日**之前将 MFA 管理迁移到你的 SSO 身份管理平台，以确保账号安全。

多因素认证（MFA）通过要求使用认证器应用程序生成一次性验证码来增加额外的安全性。登录时，TiDB Cloud 会同时验证你的密码和 MFA 验证码。你可以使用 iOS 或 Android 应用商店中的任何认证器应用程序生成此密码，例如 Google Authenticator 和 Authy。

### 启用 MFA

1. 点击 TiDB Cloud 控制台左下角的 <MDSvgIcon name="icon-top-account-settings" />。

2. 点击**账号设置**。

3. 在**多因素认证**部分，点击**启用**。

4. 输入你的账号密码以确认身份。

5. 在**设置认证器应用程序**部分，使用认证器应用程序扫描二维码并关联你的 MFA 设备。

6. 输入应用程序生成的认证码以完成 MFA 设备关联。

7. 保存一次性恢复码，当你的 MFA 设备不可用时，可以使用该恢复码进行认证。

> **注意：**
>
> - 你需要安全地存储恢复码以维护账号安全。
> - 如果你在登录时使用恢复码进行 MFA 验证，系统会在验证成功后自动生成新的恢复码。

### 禁用 MFA

1. 点击 TiDB Cloud 控制台左下角的 <MDSvgIcon name="icon-top-account-settings" />。

2. 点击**账号设置**。

3. 在**多因素认证**部分，点击**禁用**。

4. 输入你的账号密码和 MFA 认证码以确认操作。

> **注意：**
>
> 禁用 MFA 会降低你的账号安全性。请谨慎操作。
