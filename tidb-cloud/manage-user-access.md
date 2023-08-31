---
title: Identity Access Management
summary: Learn how to manage identity access in TiDB Cloud.
---

# Identity Access Management

This document describes how to manage access to organizations, projects, roles, and user profiles in TiDB Cloud.

Before accessing TiDB Cloud, [create a TiDB cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password so that you can [manage your password using TiDB Cloud](/tidb-cloud/tidb-cloud-password-authentication.md), or choose your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

## Organizations and projects

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of TiDB Cloud users and clusters. If you are an organization owner, you can create multiple projects in your organization.

For example:

```
- Your organization
    - Project 1
        - Cluster 1
        - Cluster 2
    - Project 2
        - Cluster 3
        - Cluster 4
    - Project 3
        - Cluster 5
        - Cluster 6
```

Under this structure:

- To access an organization, a user must be a member of that organization.
- To access a project in an organization, a user must at least have the read access to the project in that organization.
- To manage clusters in a project, a user must be in the `Project Owner` role.

For more information about user roles and permissions, see [User Roles](#user-roles).

### Organizations

An organization can contain multiple projects.

TiDB Cloud calculates billing at the organization level and provides the billing details for each project.

If you are an organization owner, you have the highest permission in your organization.

For example, you can do the following:

- Create different projects (such as development, staging, and production) for different purposes.
- Assign different users with different organization roles and project roles.
- Configure organization settings. For example, configure the time zone for your organization.

### Projects

A project can contain multiple clusters.

If you are a project owner, you can manage clusters and project settings for your project.

For example, you can do the following:

- Create multiple clusters according to your business need.
- Assign different users with different project roles.
- Configure project settings. For example, configure different alert settings for different projects.

## User roles

TiDB Cloud defines different user roles to manage different permissions of TiDB Cloud users in organizations, projects, or both.

You can grant roles to a user at the organization level or at the project level. Make sure to carefully plan the hierarchy of your organizations and projects for security considerations.

### Organization roles

At the organization level, TiDB Cloud defines four roles, in which `Organization Owner` can invite members and grant organization roles to members.

| Permission  | `Organization Owner` | `Organization Billing Admin` | `Organization Console Audit Admin` | `Organization Member` |
|---|---|---|---|---|
| Manage organization settings, such as projects, API keys, and time zones. | ✅ | ❌ | ❌ | ❌ |
| Invite users to or remove users from an organization, and edit organization roles of users. | ✅ | ❌ | ❌ | ❌ |
| All the permissions of `Project Owner` for all projects in the organization. | ✅ | ❌ | ❌ | ❌ |
| Create projects with Customer-Managed Encryption Key (CMEK) enabled | ✅ | ❌ | ❌ | ❌ |
| View bills and edit payment information for the organization. | ✅ | ✅ | ❌ | ❌ |
| Manage TiDB Cloud [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) for the organization. | ✅ | ❌ | ✅ | ❌ |
| View users in the organization and projects in which the member belong to. | ✅ | ✅ | ✅ | ✅ |

> **Note:**
>
> The `Organization Console Audit Admin` role is only visible upon request. It is recommended that you use the `Organization Owner` role for [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md). If you need to use the `Organization Console Audit Admin` role, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for the Organization Console Audit Admin role" in the **Description** field and click **Send**.

### Project roles

At the project level, TiDB Cloud defines three roles, in which `Project Owner` can invite members and grant project roles to members.

> **Note:**
>
> - `Organization Owner` has all the permissions of <code>Project Owner</code> for all projects so `Organization Owner` can invite project members and grant project roles to members too.
> - Each project role has all the permissions of <code>Organization Member</code> by default.
> - If a user in your organization does not belong to any projects, the user does not have any project permissions.

| Permission  | `Project Owner` | `Project Data Access Read-Write` | `Project Data Access Read-Only` |
|---|---|---|---|
| Manage project settings | ✅ | ❌ | ❌ |
| Invite users to or remove users from a project, and edit project roles of users. | ✅ | ❌ | ❌ |
| Manage [database audit logging](/tidb-cloud/tidb-cloud-auditing.md) of the project. | ✅ | ❌ | ❌ |
| Manage [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) for all TiDB Serverless clusters in the project. | ✅ | ❌ | ❌ |
| Manage cluster operations in the project, such as cluster creation, modification, and deletion. | ✅ | ❌ | ❌ |
| Manage branches for TiDB Serverless clusters in the project, such as branch creation, connection, and deletion. | ✅ | ❌ | ❌ |
| Manage cluster data such as data import, data backup and restore, and data migration. | ✅ | ✅ | ❌ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read-only operations such as using or creating endpoints to read data. | ✅ | ✅ | ✅ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read and write operations. | ✅ | ✅ | ❌ |
| View cluster data using [Chat2Query](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ✅ |
| Modify and delete cluster data using [Chat2Query](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ❌ |
| View clusters in the project, view cluster backup records, and manage [changefeeds](/tidb-cloud/changefeed-overview.md). | ✅ | ✅ | ✅ |

## Manage organization access

### View organizations

To check which organizations you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.
2. Click **Organization Settings**. You can view your organization on the page that is displayed.

### Switch between organizations

If you are a member of multiple organizations, you can switch your account between organizations.

To switch between organizations, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.
2. Click the name of the organization you want to switch to.

### Set the time zone for your organization

If you are in the `Organization Owner` role, you can modify the system display time according to your time zone.

To change the local timezone setting, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **Time Zone** tab.

4. Click the drop-down list and select your time zone.

5. Click **Save**.

### Invite an organization member

If you are in the `Organization Owner` role, you can invite users to your organization.

> **Note:**
>
> You can also [invite a user to your project](#invite-a-project-member) directly according to your need, which also makes the user your organization member.

To invite a member to an organization, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By Organization**.

4. Click **Invite**.

5. Enter the email address of the user to be invited, and then select an organization role for the user.

    > **Tip:**
    >
    > - If you want to invite multiple members at one time, you can enter multiple email addresses.
    > - The invited user does not belong to any projects by default. To invite a user to a project, see [Invite a project member](#invite-a-project-member).

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page, and after sign-in, the account joins the organization automatically.

> **Note:**
>
> The verification link in the email expires in 24 hours. If the user you want to invite does not receive the email, click **Resend**.

### Modify organization roles

If you are in the `Organization Owner` role, you can modify organization roles of all members in your organization.

To modify the organization role of a member, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By Organization**.

4. Click the role of the target member, and then modify the role.

### Remove an organization member

If you are in the `Organization Owner` role, you can remove organization members from your organization.

To remove a member from an organization, take the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By Organization**.

4. Click **Delete** in the user row that you want to delete.

## Manage project access

### View projects

To check which project you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

> **Tip:**
>
> If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

### Create a project

> **Note:**
>
> For free trial users, you cannot create a new project.

If you are in the `Organization Owner` role, you can create projects in your organization.

To create a new project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. Click **Create New Project**.

4. Enter your project name.

5. Click **Confirm**.

### Rename a project

If you are in the `Organization Owner` role, you can rename any projects in your organization. If you are in the `Project Owner` role, you can rename your project.

To rename a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. In the row of your project to be renamed, click **Rename**.

4. Enter a new project name.

5. Click **Confirm**.

### Invite a project member

If you are in the `Organization Owner` or `Project Owner` role, you can invite members to your projects.

> **Note:**
>
> When a user not in your organization joins your project, the user automatically joins your organization as well.

To invite a member to a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, select **By Project**, and then select your project from the drop-down list.

4. Click **Invite**.

5. Enter the email address of the user to be invited, and then select a project role for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page. After sign-in, the account joins the project automatically.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

### Modify project roles

If you are in the `Organization Owner` role, you can modify project roles of all project members in your organization. If you are in the `Project Owner` role, you can modify project roles of all members in your project.

To modify the project role of a member, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, select **By Projects**, and then choose your project in the drop-down list.

4. Click the role of the target member, and then modify the role.

### Remove a project member

If you are in the `Organization Owner` or `Project Owner` role, you can remove project members.

To remove a member from a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select the **By Project**.

4. Click **Delete** in the user row that you want to delete.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. Click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Account Settings**. The **Profile** tab is displayed by default.

3. Update the profile information, and then click **Save**.
