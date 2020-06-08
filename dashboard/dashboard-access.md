---
title: Access TiDB Dashboard
summary: Learn how to access TiDB Dashboard.
category: how-to
---

# Access TiDB Dashboard

To access TiDB Dashboard, visit <http://127.0.0.1:2379/dashboard> via your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

> **Note:**
>
> If you have deployed multiple PD components in your cluster, you can use the address of only one PD component to access TiDB Dashboard, because the Dashboard operates on only one PD component. If you access via other PD components, your browser is redirected to that PD component. Therefore, if the firewall is not configured for this instance on which PD operates, you might not be able to access TiDB Dashboard.

## Browser compatibility

You can use TiDB Dashboard in the following common desktop browsers of a relatively newer version:

- Chrome >= 77
- Firefox >= 68
- Edge >= 17

> **Note:**
>
> If you use the browsers above of earlier versions or other browsers to access TiDB Dashboard, some functions might not work properly.

## Sign in

For the first-time access, TiDB Dashboard displays the user sign in interface, as shown in the image below. You can sign in using the TiDB `root` account.

![Login interface](/media/dashboard/dashboard-access-login.png)

If one of the following situations exists, the login might fail:

- TiDB `root` user does not exist.
- PD is not started or cannot be accessed.
- TiDB is not started or cannot be accessed.
- Wrong `root` password.

Once you have signed in, the session remains valid within the next 24 hours. To learn how to sign out, refer to the [Logout](#logout) section.

## Switch language

The following languages are supported in TiDB Dashboard:

- English
- Chinese (simplified)

In the **SQL User Sign In** page, you can click the **Switch Language** drop-down list to switch the interface language.

![Switch language](/media/dashboard/dashboard-access-switch-language.png)

## Logout

Once you have logged in, click the login user name in the left navigation bar to switch to the user page. Click the **Logout** button on the user page to log out the current user. After logging out, you need to re-enter your username and password.

![Logout](/media/dashboard/dashboard-access-logout.png)
