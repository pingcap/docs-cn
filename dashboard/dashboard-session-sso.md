---
title: 配置 TiDB Dashboard 使用 SSO 登录
summary: 了解如何配置 TiDB Dashboard 启用 SSO 登录。
---

# 配置 TiDB Dashboard 使用 SSO 登录

TiDB Dashboard 支持基于 [OIDC](https://openid.net/connect/) 协议的单点登录 (Single Sign-On)。配置 TiDB Dashboard 启用 SSO 登录后，你可以通过配置的 SSO 服务进行登录鉴权，无需输入 SQL 用户名和密码即可登录到 TiDB Dashboard。

## 配置 OIDC SSO

> **注意：**
>
> 该功能仅在 v5.1.1 或更高版本的集群中可用。

### 启用 SSO

1. 登录 TiDB Dashboard。

2. 点击边栏左下角的用户名访问配置界面。

3. 在**单点登录** (Single Sign-On) 区域下，开启**允许使用 SSO 登录到 TiDB Dashboard** (Enable to use SSO when sign into TiDB Dashboard)。

4. 在表单中填写 **OIDC Client ID** 和 **OIDC Discovery URL** 字段。

    一般可以从 SSO 服务的提供商处获取到这两个字段信息：

    - OIDC Client ID 有时也被称为 OIDC Token Issuer
    - OIDC Discovery URL 有时也被称为 OIDC Token Audience。

5. 将 SQL 登录密码录入到 TiDB Dashboard 中，以便在 SSO 鉴权通过后完成登录。点击**授权登录为该用户** (Authorize Impersonation) 录入密码。

    这是因为 TiDB Dashboard SSO 的原理是在 SSO 成功鉴权后，采用 TiDB Dashboard 内加密存储的 SQL 登录密码进行替代登录。

    ![操作示例](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **注意：**
    >
    > 你录入的密码将被加密存储。若 SQL 用户密码后续发生了变更，将导致 SSO 登录失败。这时可以重新录入密码使 SSO 登录恢复正常。

6. 在对话框中填写完密码后，点击**授权并保存** (Authorize and Save)。

    ![操作示例](/media/dashboard/dashboard-session-sso-enable-2.png)

7. 点击**更新** (Update) 保存配置。

    ![操作示例](/media/dashboard/dashboard-session-sso-enable-3.png)

至此 TiDB Dashboard 中已经成功开启了 SSO 登录。

> **注意：**
>
> 出于安全原因，部分 SSO 服务还需要你进一步在 SSO 服务中配置受信任的登录和登出跳转地址，请参见 SSO 服务的具体帮助完成配置。

### 禁用 SSO

你可以随时禁用 SSO。禁用后，之前已录入并存储在本地的替代登录 SQL 密码将被彻底清除。禁用步骤如下：

1. 登录 TiDB Dashboard。

2. 点击边栏左下角用户名访问配置界面。

3. 在**单点登录** (Single Sign-On) 区域下，关闭**允许使用 SSO 登录到 TiDB Dashboard** (Enable to use SSO when sign into TiDB Dashboard)。

4. 点击**更新** (Update) 保存配置。

    ![操作示例](/media/dashboard/dashboard-session-sso-disable.png)

### 密码发生变更后重新录入密码

若替代登录的 SQL 用户密码发生了变更，则 SSO 登录将会失败。此时，你可以将新的登录密码录入到 TiDB Dashboard 中以恢复正常 SSO 登录功能，步骤如下：

1. 登录 TiDB Dashboard。

2. 点击边栏左下角用户名访问配置界面。

3. 在**单点登录** (Single Sign-On) 区域下，点击**授权登录为该用户** (Authorize Impersonation) 来录入新的密码。

    ![操作示例](/media/dashboard/dashboard-session-sso-reauthorize.png)

4. 在对话框中填写完毕密码后，点击**授权并保存** (Authorize and Save)。

## 使用 SSO 登录

若 TiDB Dashboard 已经完成了 SSO 的配置，你可使用以下步骤完成登录：

1. 在 TiDB Dashboard 登录界面上，点击**使用公司账号 SSO 登录** (Sign in via Company Account)。

    ![操作示例](/media/dashboard/dashboard-session-sso-signin.png)

2. 在配置 SSO 的系统中进行登录。

3. 你将被重定向回 TiDB Dashboard 完成登录。

## 示例一：使用 Okta 进行 TiDB Dashboard SSO 登录认证

[Okta](https://www.okta.com/) 是一个提供 OIDC SSO 的身份认证服务。以下步骤展示了如何配置 Okta 及 TiDB Dashboard，使得 TiDB Dashboard 可以通过 Okta 进行 SSO 登录。

### 步骤一：配置 Okta

首先需要在 Okta 中创建一个用于集成 SSO 的 Application Integration。

1. 访问 Okta 管理后台。

2. 点击左侧边栏的 **Applications** > **Applications**。

3. 点击 **Create App Integration**。

    ![操作示例](/media/dashboard/dashboard-session-sso-okta-1.png)

4. 在弹出的对话框中，**Sign-in method** 字段选择 **OIDC - OpenID Connect**。

5. **Application Type** 字段选择 **Single-Page Application**。

6. 对话框中点击 **Next** 按钮。

    ![操作示例](/media/dashboard/dashboard-session-sso-okta-2.png)

7. **Sign-in redirect URIs** 字段填写如下内容：

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    以上内容中，将 `DASHBOARD_IP:PORT` 替换为你在浏览器中实际访问 TiDB Dashboard 所使用的域名（或 IP）及端口。

8. **Sign-out redirect URIs** 字段填写如下内容：

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    类似地，将 `DASHBOARD_IP:PORT` 替换为实际的域名（或 IP）及端口。

    ![操作示例](/media/dashboard/dashboard-session-sso-okta-3.png)

9. 在 **Assignments** 中按你的实际需求配置组织中哪些用户可以通过这个 SSO 登录 TiDB Dashboard，然后点击 **Save** 保存配置。

    ![操作示例](/media/dashboard/dashboard-session-sso-okta-4.png)

### 步骤二：获取 TiDB Dashboard 所需的配置参数并填入 TiDB Dashboard

1. 在 Okta 创建的 App Integration 中，点击 **Sign On**。

    ![操作示例 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2. **OpenID Connect ID Token** 区域中有 **Issuer** 和 **Audience** 字段，复制这两个字段的值。

    ![操作示例 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3. 打开 TiDB Dashboard 配置界面，将上一步获取到的 **Issuer** 填入 **OIDC Client ID**，将 **Audience** 填入 **OIDC Discovery URL** 后，完成授权并保存配置。示例如下：

    ![操作示例 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

至此，TiDB Dashboard 已被配置为使用 Okta 进行 SSO 登录。

## 示例二：使用 Auth0 进行 TiDB Dashboard SSO 登录认证

和 Okta 类似，[Auth0](https://auth0.com/) 也可以提供 OIDC SSO 的身份认证服务。

### 步骤一：配置 Auth0

1. 访问 Auth0 管理后台。

2. 点击左侧边栏的 **Applications** > **Applications**。

3. 点击 **Create Application**，在弹出窗口中输入 Name，比如 "TiDB Dashboard"，application type 选择 "Single Page Web Application"。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

4. 点击 **Settings** 栏。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5. **Allowed Callback URLs** 字段填写如下内容：

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    以上内容中，将 `DASHBOARD_IP:PORT` 替换为你在浏览器中实际访问 TiDB Dashboard 所使用的域名（或 IP）及端口。

6. **Allowed Logout URLs** 字段填写如下内容：

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    类似地，将 `DASHBOARD_IP:PORT` 替换为实际的域名（或 IP）及端口。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7. 其它设置保持默认，点击 **Save Changes** 保存。

### 步骤二：获取 TiDB Dashboard 所需的配置参数并填入 TiDB Dashboard

1. 将 Auth0 **Settings** 栏 **Basic Information** 项的 **Client ID** 字段的值填入 TiDB Dashboard 的 **OIDC Client ID**，将 **Domain** 字段的值，加上 `https://` 前缀和 `/` 后缀后填入 **OIDC Discovery URL** 中，比如 `https://example.us.auth0.com/`。完成授权并保存配置即可。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

至此，TiDB Dashboard 已被配置为使用 Auth0 进行 SSO 登录。
