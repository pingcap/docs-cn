---
title: Share TiDB Dashboard Sessions
summary: Learn how to share the current TiDB Dashboard session to other users.
---

# Share TiDB Dashboard Sessions

You can share the current session of the TiDB Dashboard to other users so that they can access and operate the TiDB Dashboard without entering the user password.

## Steps for the Inviter

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configuration page.

3. Click **Share Current Session**.

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-1.png)

   > **Note:**
   >
   > For security reasons, the shared session cannot be shared again.

4. Adjust sharing settings in the popup dialog:

   - Expire in: How long the shared session will be effective. Signing out of the current session does not affect the effective time of the shared session.

   - Share as read-only privilege: The shared session only permits read operations but not write operations (such as modifying configurations).

5. Click **Generate Authorization Code**.

   ![Sample Step](/media/dashboard/dashboard-session-share-settings-2.png)

6. Provide the generated **Authorization Code** to the user to whom you want to share the session.

   ![Sample Step](/media/dashboard/dashboard-session-share-settings-3.png)

   > **Warning:**
   >
   > Keep your authorization code secure and do not send it to anyone who is untrusted. Otherwise, they will be able to access and operate TiDB Dashboard without your authorization.

## Steps for the Invitee

1. On the sign-in page of TiDB Dashboard, click **Use Alternative Authentication**.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-1.png)

2. Click **Authorization Code** to use it to sign in.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-2.png)

3. Enter the authorization code you have received from the inviter.

4. Click **Sign In**.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-3.png)
