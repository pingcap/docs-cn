---
title: Manage Console User Access
summary: Learn how to manage the user access of the TiDB Cloud console.
---

# Manage Console User Access

This document describes how to manage user access of the [TiDB Cloud console](https://tidbcloud.com/console).

## Sign in

1. Navigate to the TiDB Cloud login page: <https://tidbcloud.com>.

2. Depending on how you signed up TiDB Cloud, do one of the following:

    - If you signed up with a Google account, click **Sign in with Google**.
    - If you signed up with a GitHub account, click **Sign in with GitHub**.
    - If you signed up with an email address and password, enter your email and password, and then click **Sign In**.

## Sign out

After you have signed into TiDB Cloud, if you need to sign out, perform the following steps:

1. Click the account name on the upper right of the window.

2. Click **Logout**.

## Manage user passwords

> **Note:**
>
> The content in this section is only applicable to TiDB Cloud registration with email and password. If you sign up for TiDB Cloud with Google or GitHub, your password is managed by Google or GitHub and you cannot change it using the TiDB Cloud console.

To improve your system security, if you sign up for TiDB Cloud with email and password, it is recommended that you reset your password every 90 days.

To change the password, take the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Account**.

3. Click the **Change Password** tab.

4. Click **Change Password**, and then check your mail box for the link to reset the password.

If your password is not changed within 90 days, you will get a prompt to reset your password when you log in to TiDB Cloud. It is recommended that you follow the prompt to reset the password.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last time, company name, country, and phone number.

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Account**. The **Profile** tab is selected by default.

3. Update the profile information, and then click **Save**.

## View the organization and project

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of your TiDB cluster. In the hierarchy of organizations and projects, an organization can contain multiple projects and organization members, and a project can contain multiple clusters and project members.

Under this structure:

- Billing occurs at the organization level, while retaining visibility of usage in each project and cluster.

- You can view all members in your organization.

- You can also view all members in your project.

To access a cluster in a project under an organization, a user must be both a member of the organization and a member of the project. Organization owners can invite users to join the project to create and manage clusters in the project.

To check which project you belong to, perform these steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Organization Settings**. The **Projects** tab is displayed by default.

## Invite an organization member

If you are the owner of an organization, you can invite organization members. Otherwise, skip this section.

To invite a member to an organization, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **User Management**, and then select the **By All Users** tab.

4. Click **Invite**.

5. Enter the email address of the user to be invited, select a role for the user, and then choose a project for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. On the new page, the user needs to view and agree with our license, and then click **Submit** to create the account in TiDB Cloud. After that, the user is redirected to the login page.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

## Invite a project member

If you are the owner of an organization, you can invite project members. Otherwise, skip this section.

To invite a member to a project, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **User Management**, and then select the **By Project** tab.

4. Click **Invite**.

5. Enter the email address of the user to be invited, select a role for the user, and then choose a project for the user.

    > **Tip:**
    > 
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. On the new page, the user needs to view and agree with our license, and then click **Submit** to create the account in TiDB Cloud. After that, the user is redirected to the login page.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

## Configure member roles

If you are the owner of an organization, you can perform the following steps to configure roles for your organization members:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Organization Settings**. The organization settings page is displayed.
3. Click **User Management**, and then select the **By All Users** tab.
4. Click the role of the target member, and then modify the role.

There are four roles in an organization. The permissions of each role are as follows:

- Owner:
    - Invite members to join the organization and remove members from the the organization
    - Configure the roles of organization members
    - Create and rename projects
    - Invite members to join a project and remove members from a project
    - Edit time zone
    - View bills and edit payment information
- Member:
    - Can be invited to join a project and obtain project instance management rights
- Billing Admin:
    - View bills and edit payment information
    - Can be invited to join a project and obtain project instance management rights
- Audit Admin:
    - View and configure audit logging
    - Can be invited to join a project and obtain project instance management rights

## Remove an organization member

If you are the owner of an organization, you can remove organization members. Otherwise, skip this section.

To remove a member from an organization, perform the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **By All Users**.

4. Click **Delete** in the user row that you want to delete.

## Remove a project member

If you are the owner of an organization, you can remove project members. Otherwise, skip this section.

To remove a member from a project, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **By Project**.

4. Click **Delete** in the user row that you want to delete.

## Set the local time zone

If you are the organization owner, you can modify the system display time according to your time zone. 

To change the local timezone setting, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **Time Zone**.

4. Click the drop-down list and select your time zone.

5. Click **Confirm**.
