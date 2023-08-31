---
title: Organization SSO Authentication
summary: Learn how to log in to the TiDB Cloud console via your customized organization authentication.
---

# Organization SSO Authentication

Single Sign-On (SSO) is an authentication scheme that enables members in your TiDB Cloud [organization](/tidb-cloud/tidb-cloud-glossary.md#organization) to log in to TiDB Cloud using identities from an identity provider (IdP) instead of email addresses and passwords.

TiDB Cloud supports the following two types of SSO authentication:

- [Basic SSO](/tidb-cloud/tidb-cloud-sso-authentication.md): members can log in to the [TiDB Cloud console](https://tidbcloud.com/) using their GitHub, Google, or Microsoft authentication methods. The basic SSO is enabled by default for all organizations in TiDB Cloud.

- Cloud Organization SSO: members can log in to a custom login page of TiDB Cloud using the authentication methods specified by your organization. The Cloud Organization SSO is disabled by default.

Compared with basic SSO, Cloud Organization SSO provides more flexibility and customization so you can better meet your organization's security and compliance requirements. For example, you can specify which authentication methods are displayed on the login page, limit which email address domains are allowed for login, and let your members log in to TiDB Cloud with your identity provider (IdP) that uses the [OpenID Connect (OIDC)](https://openid.net/connect/) or [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) identity protocol.

In this document, you will learn how to migrate the authentication scheme of your organization from basic SSO to Cloud Organization SSO.

> **Note:**
>
> - The Cloud Organization SSO feature is in beta and is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for Cloud Organization SSO" in the **Description** field and click **Send**.
> - If your current TiDB login URL starts with `https://tidbcloud.com/enterprise/`, it means that Cloud Organization SSO is already enabled for your organization.

## Before you begin

Before migrating to Cloud Organization SSO, check and confirm the items in this section for your organization.

> **Note:**
>
> - Once Cloud Organization SSO is enabled, it cannot be disabled.
> - To enable Cloud Organization SSO, you need to be in the `Organization Owner` role of your TiDB Cloud organization. For more information about roles, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

### Decide a custom URL for the TiDB Cloud login page of your organization

When Cloud Organization SSO is enabled, your members must use your custom URL instead of the public login URL (`https://tidbcloud.com`) to log in to TiDB Cloud.

The custom URL cannot be changed after the enablement, so you need to decide which URL to be used in advance.

The format of the custom URL is `https://tidbcloud.com/enterprise/signin/your-company-name`, in which you can customize your company name.

### Decide authentication methods for your organization members

TiDB Cloud provides the following authentication methods for Organization SSO.

- Google
- GitHub
- Microsoft
- OIDC
- SAML

When you enable Cloud Organization SSO, the first three methods are enabled by default.

All the enabled authentication methods will be displayed on your custom TiDB Cloud login page, so you need to decide which authentication methods to be enabled or disabled in advance.

### Decide whether to enable auto-provision

Auto-provision is a feature that allows members to automatically join an organization without requiring an invitation from the `Organization Owner` or `Project Owner`. In TiDB Cloud, it is disabled by default for all the supported authentication methods.

- When auto-provision is disabled for an authentication method, only users who have been invited by an `Organization Owner` or `Project Owner` can log in to your custom URL.
- When auto-provision is enabled for an authentication method, any users using this authentication method can log in to your custom URL. After login, they are automatically assigned the default **Member** role within the organization.

For security considerations, if you choose to enable auto-provision, it is recommended to limit the allowed email domains for authentication when you [configure the authentication method details](#step-2-configure-authentication-methods).

### Notify your members about the Cloud Organization SSO migration plan

Before enabling Cloud Organization SSO, make sure to inform your members about the following:

- The custom login URL of TiDB Cloud
- The time when to start using the custom login URL instead of `https://tidbcloud.com` for login
- The available authentication methods
- Whether members need invitations to log in to the custom URL

## Step 1. Enable Cloud Organization SSO

To enable Cloud Organization SSO, take the following steps:

1. Log in to [TiDB Cloud console](https://tidbcloud.com) as a user with the `Organization Owner` role.
2. In the lower-left corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" />, and then click **Organization Settings**.
3. On the **Organization Settings** page, click the **Authentication** tab, and then click **Enable**.
4. In the dialog, fill in the custom URL for your organization, which must be unique in TiDB Cloud.

    > **Note:**
    >
    > The URL cannot be changed once Cloud Organization SSO is enabled. Members in your organization will only be able to log in to TiDB Cloud using your custom URL. If you need to change the configured URL later, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance.

5. Click the **I understand and confirm** check box, and then click **Enable**.

    > **Note:**
    >
    > If the dialog includes a list of users to be re-invited and re-join for Cloud Organization SSO, TiDB Cloud will automatically send the invitation emails to those users after you enable Cloud Organization SSO. After receiving the invitation email, each user needs to click the link in the email to verify their identity, and the custom login page shows.

## Step 2. Configure authentication methods

Enabling an authentication method in TiDB Cloud allows members using that method to log in to TiDB Cloud using your custom URL.

### Configure Google, GitHub, or Microsoft authentication methods

After enabling Cloud Organization Cloud, you can configure Google, GitHub, or Microsoft authentication methods as follows:

1. On the **Organization Settings** page, enable or disable the Google, GitHub, or Microsoft authentication methods according to your need.
2. For an enabled authentication method, you can click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to configure the method details.
3. In the method details, you can configure the following:

    - [**Auto-provision Accounts**](#decide-whether-to-enable-auto-provision)

        It is disabled by default. You can enable it according to your need. For security considerations, if you choose to enable auto-provision, it is recommended to limit the allowed email domains for authentication.

    - **Allowed Email Domains**

        After this field is configured, only the specified email domains of this authentication method can log in to TiDB Cloud using the custom URL. When filling in domain names, you need to exclude the `@` symbol and separate them with commas. For example, `company1.com,company2.com`.

        > **Note:**
        >
        > If you have configured email domains, before saving the settings, make sure that you add the email domain that you currently use for login, to avoid that you are locked out by TiDB Cloud.

4. Click **Save**.

### Configure the OIDC authentication method

If you have an identity provider that uses the OIDC identity protocol, you can enable the OIDC authentication method for TiDB Cloud login.

In TiDB Cloud, the OIDC authentication method is disabled by default. After enabling Cloud Organization Cloud, you can enable and configure the OIDC authentication method as follows:

1. Get the following information from your identity provider for TiDB Cloud Organization SSO:

    - Issuer URL
    - Client ID
    - Client secret

2. On the **Organization Settings** page, click the **Authentication** tab, locate the row of OIDC in the **Authentication Methods** area, and then click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to show the OIDC method details.
3. In the method details, you can configure the following:

    - **Name**

        Specify a name for the OIDC authentication method to be displayed on your custom login page.

    - **Issuer URL**, **Client ID**, and **Client Secret**

        Paste the corresponding values that you get from your IdP.

    - [**Auto-provision Accounts**](#decide-whether-to-enable-auto-provision)

        It is disabled by default. You can enable it according to your need. For security considerations, if you choose to enable auto-provision, it is recommended to limit the allowed email domains for authentication.

    - **Allowed Email Domains**

        After this field is configured, only the specified email domains of this authentication method can log in to TiDB Cloud using the custom URL. When filling in domain names, you need to exclude the `@` symbol and separate them with commas. For example, `company1.com,company2.com`.

        > **Note:**
        >
        > If you have configured email domains, before saving the settings, make sure that you add the email domain that you currently use for login, to avoid that you are locked out by TiDB Cloud.

4. Click **Save**.

### Configure the SAML authentication method

If you have an identity provider that uses the SAML identity protocol, you can enable the SAML authentication method for TiDB Cloud login.

In TiDB Cloud, the SAML authentication method is disabled by default. After enabling Cloud Organization Cloud, you can enable and configure the SAML authentication method as follows:

1. Get the following information from your identity provider for TiDB Cloud Organization SSO:

    - Sign on URL
    - Signing Certificate

2. On the **Organization Settings** page, click the **Authentication** tab, locate the row of SAML in the **Authentication Methods** area, and then click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to show the SAML method details.
3. In the method details, you can configure the following:

    - **Name**

        Specify a name for the SAML authentication method to be displayed on your custom login page.

    - **Sign on URL**

        Paste the URL that you get from your IdP.

    - **Signing Certificate**

        Paste the entire signing certificate from your IdP, including the starting line `---begin certificate---` and the end line `---end certificate---`.

    - [**Auto-provision Accounts**](#decide-whether-to-enable-auto-provision)

        It is disabled by default. You can enable it according to your need. For security considerations, if you choose to enable auto-provision, it is recommended to limit the allowed email domains for authentication.

    - **Allowed Email Domains**

        After this field is configured, only the specified email domains of this authentication method can log in to TiDB Cloud using the custom URL. When filling in domain names, you need to exclude the `@` symbol and separate them with commas. For example, `company1.com,company2.com`.

        > **Note:**
        >
        > If you have configured email domains, before saving the settings, make sure that you add the email domain that you currently use for login, to avoid that you are locked out by TiDB Cloud.

4. Click **Save**.