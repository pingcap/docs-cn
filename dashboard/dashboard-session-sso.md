---
title: Configure SSO for TiDB Dashboard
summary: Learn how to enable SSO to sign into TiDB Dashboard.
---

# Configure SSO for TiDB Dashboard

TiDB Dashboard supports [OIDC](https://openid.net/connect/)-based Single Sign-On (SSO). After enabling the SSO feature of TiDB Dashboard, the configured SSO service is used for your sign-in authentication and then you can access TiDB Dashboard without entering the SQL user password.

## Configure OIDC SSO

### Enable SSO

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configuration page.

3. In the **Single Sign-On** section, select **Enable to use SSO when sign into TiDB Dashboard**.

4. Fill the **OIDC Client ID** and the **OIDC Discovery URL** fields in the form.

    Generally, you can obtain the two fields from the SSO service provider:

    - OIDC Client ID is also called OIDC Token Issuer.
    - OIDC Discovery URL is also called OIDC Token Audience.

5. Click **Authorize Impersonation** and input the SQL password.

    TiDB Dashboard will store this SQL password and use it to impersonate a normal SQL sign-in after an SSO sign-in is finished.

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **Note:**
    >
    > The password you have entered will be encrypted and stored. The SSO sign-in will fail after the password of the SQL user is changed. In this case, you can re-enter the password to bring SSO back.

6. Click **Authorize and Save**.

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7. Click **Update** (Update) to save the configuration.

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

Now SSO sign-in has been enabled for TiDB Dashboard.

> **Note:**
>
> For security reasons, some SSO services require additional configuration for the SSO service, such as the trusted sign-in and sign-out URIs. Refer to the documentation of the SSO service for further information.

### Disable SSO

You can disable the SSO, which will completely erase the stored SQL password:

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configuration page.

3. In the **Single Sign-On** section, deselect **Enable to use SSO when sign into TiDB Dashboard**.

4. Click **Update** (Update) to save the configuration.

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### Re-enter the password after a password change

The SSO sign-in will fail once the password of the SQL user is changed. In this case, you can bring back the SSO sign-in by re-entering the SQL password:

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configuration page.

3. In the **Single Sign-On** section, Click **Authorize Impersonation** and input the updated SQL password.

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4. Click **Authorize and Save**.

## Sign in via SSO

Once SSO is configured for TiDB Dashboard, you can sign in via SSO by taking following steps:

1. In the sign-in page of TiDB Dashboard, click **Sign in via Company Account**.

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2. Sign into the system with SSO service configured.

3. You are redirected back to TiDB Dashboard to finish the sign-in.

## Example 1: Use Okta for TiDB Dashboard SSO sign-in

[Okta](https://www.okta.com/) is an OIDC SSO identity service, which is compatible with the SSO feature of TiDB Dashboard. The steps below demonstrate how to configure Okta and TiDB Dashboard so that Okta can be used as the TiDB Dashboard SSO provider.

### Step 1: Configure Okta

First, create an Okta Application Integration to integrate SSO.

1. Access the Okta administration site.

2. Navigate from the left sidebar **Applications** > **Applications**.

3. Click **Create App Integration**.

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4. In the poped up dialog, choose **OIDC - OpenID Connect** in **Sign-in method**.

5. Choose **Single-Page Application** in **Application Type**.

6. Click the **Next** button.

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7. Fill **Sign-in redirect URIs** as follows:

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    Substitute `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port that you use to access the TiDB Dashboard in the browser.

8. Fill **Sign-out redirect URIs** as follows:

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    Similarly, substitute `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port.

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9. Configure what type of users in your organization is allowed for SSO sign-in in the **Assignments** field, and then click **Save** to save the configuration.

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### Step 2: Obtain OIDC information and fill in TiDB Dashboard

1. In the Application Integration just created in Okta, click **Sign On**.

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2. Copy values of the **Issuer** and **Audience** fields from the **OpenID Connect ID Token** section.

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3. Open the TiDB Dashboard configuration page, fill **OIDC Client ID** with **Issuer** obtained from the last step and fill **OIDC Discovery URL** with **Audience**. Then finish the authorization and save the configuration. For example:

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

Now TiDB Dashboard has been configured to use Okta SSO for sign-in.

## Example 2: Use Auth0 for TiDB Dashboard SSO sign-in

Similar to Okta, [Auth0](https://auth0.com/) also provides OIDC SSO identity service. The following steps describe how to configure Auth0 and TiDB Dashboard so that Auth0 can be used as the TiDB Dashboard SSO provider.

### Step 1: Configure Auth0

1. Access the Auth0 administration site.

2. Navigate on the left sidebar **Applications** > **Applications**.

3. Click **Create App Integration**.

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    In the popped-up dialog, fill **Name**, for example, "TiDB Dashboard". Choose **Single Page Web Applications** in **Choose an application type**. Click **Create**.

4. Click **Settings**.

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5. Fill **Allowed Callback URLs** as follows:

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    Replace `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port that you use to access the TiDB Dashboard in your browser.

6. Fill **Allowed Logout URLs** as follows:

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    Similarly, replace `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port.

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7. Keep the default values for other settings and click **Save Changes**.

### Step 2: Obtain OIDC information and fill in TiDB Dashboard

1. Fill **OIDC Client ID** of TiDB Dashboard with **Client ID** in **Basic Information** under the **Settings** tab of Auth0.

2. Fill **OIDC Discovery URL** with the **Domain** field value prefixed with `https://` and suffixed with `/`, for example, `https://example.us.auth0.com/`. Complete authorization and save the configuration.

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

Now TiDB Dashboard has been configured to use Auth0 SSO for sign-in.

## Example 3: Use Casdoor for TiDB Dashboard SSO sign-in

[Casdoor](https://casdoor.org/) is an open-source SSO platform that can be deployed in your own hosts. It is compatible with the SSO feature of TiDB Dashboard. The following steps describe how to configure Casdoor and TiDB Dashboard so that Casdoor can be used as the TiDB Dashboard SSO provider.

### Step 1: Configure Casdoor

1. Deploy and access the Casdoor administration site.

2. Navigate from the top sidebar **Applications**.

3. Click **Applications - Add**.
    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4. Fill **Name** and **Display name**, for example, **TiDB Dashboard**.

5. Add **Redirect URLs** as follows:

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    Replace `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port that you use to access the TiDB Dashboard in your browser.

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6. Keep the default values for other settings and click **Save & Exit**.

7. Save the **Client ID** seen on the page.

### Step 2: Obtain OIDC information and fill in TiDB Dashboard

1. Fill **OIDC Client ID** of TiDB dashboard with **Client ID** saved in the previous step.

2. Fill **OIDC Discovery URL** with the **Domain** field value prefixed with `https://` and suffixed with `/`, for example, `https://casdoor.example.com/`. Complete authorization and save the configuration.

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

Now TiDB Dashboard has been configured to use Casdoor SSO for sign-in.