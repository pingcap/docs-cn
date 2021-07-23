---
title: 分享 TiDB Dashboard 会话
summary: 了解如何将当前的 TiDB Dashboard 会话分享给其他用户访问。
---

# 分享 TiDB Dashboard 会话

你可以将当前的 TiDB Dashboard 会话安全地分享给其他用户访问，这样其他用户无需要知道登录账号密码即可访问 TiDB Dashboard 并进行操作。

## 分享者操作步骤

1. 登录 TiDB Dashboard。

2. 点击边栏左下角的用户名访问配置界面。

3. 点击**分享当前会话** (Share Current Session)。

   ![操作示例](/media/dashboard/dashboard-session-share-settings-1.png)

   > **注意：**
   >
   > 出于安全考虑，已分享的会话中不能使用分享功能将该会话再次分享给其他人。

4. 在弹出的对话框中，对分享进行细节配置：

   - 有效时间：分享的会话在多少时间内有效。登出当前会话不影响已分享会话的有效时间。

   - 以只读权限分享：分享的会话为只读，例如不允许进行配置修改等操作。

   备注：“以只读权限分享”功能仅在 v4.0.14 或更高版本中可用。

5. 点击**生成授权码** (Generate Authorization Code)。

   ![操作示例](/media/dashboard/dashboard-session-share-settings-2.png)

6. 将生成出来的**授权码**提供给要分享的用户。

   ![操作示例](/media/dashboard/dashboard-session-share-settings-3.png)

   > **警告：**
   >
   > 请妥善地保管授权码。不要将授权码分发给不受信任的用户，否则他们也将具备访问和操作 TiDB Dashboard 的能力。

## 受邀请者操作步骤

1. 在 TiDB Dashboard 登录界面上，点击**使用其他登录方式** (Use Alternative Authentication)。

   ![操作示例](/media/dashboard/dashboard-session-share-signin-1.png)

2. 选择使用**授权码** (Authorization Code) 登录。

   ![操作示例](/media/dashboard/dashboard-session-share-signin-2.png)

3. 输入从分享者取得的授权码。

4. 点击**登录** (Sign In)。

   ![操作示例](/media/dashboard/dashboard-session-share-signin-3.png)
