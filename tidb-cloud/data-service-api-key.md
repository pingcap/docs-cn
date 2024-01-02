---
title: API Keys in Data Service
summary: Learn how to create, edit, and delete an API key for a Data App.
---

# API Keys in Data Service

The TiDB Cloud Data API supports both [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) and [Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication).

- [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) uses non-encrypted base64 encoding to transmit your public key and private key. HTTPS ensures the transmission security. For more information, see [RFC 7617 - The 'Basic' HTTP Authentication Scheme](https://datatracker.ietf.org/doc/html/rfc7617).
- [Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication) offers an additional security layer by hashing your public key, private key, a server-supplied nonce value, the HTTP method, and the requested URI before network transmission. This encrypts the private key to prevent it from being transmitted in plain text. For more information, see [RFC 7616 - HTTP Digest Access Authentication](https://datatracker.ietf.org/doc/html/rfc7616).

> **Note:**
>
> The Data API key in Data Service is different from the key used in the [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication). The Data API key is used to access data in the TiDB Cloud clusters, whereas the TiDB Cloud API key is used to manage resources such as projects, clusters, backups, restores, and imports.

## API key overview

- An API key contains a public key and a private key, which act as the username and password required in the authentication. The private key is only displayed upon the key creation.
- Each API key belongs to one Data App only and is used to access the data in the TiDB Cloud clusters.
- You must provide the correct API key in every request. Otherwise, TiDB Cloud responds with a `401` error.

## Rate limiting

Request quotas are subject to rate limits as follows:

- TiDB Cloud Data Service allows up to 100 requests per minute (rpm) per API key by default.

    You can edit the rate limit of an API key when you [create](#create-an-api-key) or [edit](#edit-an-api-key) the key. The supported value range is from `1` to `1000`. If your requests per minute exceed the rate limit, the API returns a `429` error. To get a quota of more than 1000 rpm per API key, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

    Each API request returns the following headers about the limit.

    - `X-Ratelimit-Limit-Minute`: The number of requests allowed per minute.
    - `X-Ratelimit-Remaining-Minute`: The number of remaining requests in the current minute. When it reaches `0`, the API returns a `429` error and indicates that you exceed the rate limit.
    - `X-Ratelimit-Reset`: The time in seconds at which the current rate limit resets.

  If you exceed the rate limit, an error response returns like this:

    ```bash
    HTTP/2 429
    date: Mon, 05 Sep 2023 02:50:52 GMT
    content-type: application/json
    content-length: 420
    x-debug-trace-id: 202309040250529dcdf2055e7b2ae5e9
    x-ratelimit-reset: 8
    x-ratelimit-remaining-minute: 0
    x-ratelimit-limit-minute: 10
    x-kong-response-latency: 1
    server: kong/2.8.1

    {"type":"","data":{"columns":[],"rows":[],"result":{"latency":"","row_affect":0,"code":49900007,"row_count":0,"end_ms":0,"limit":0,"message":"API key rate limit exceeded. The limit can be increased up to 1000 requests per minute per API key in TiDB Cloud console. For an increase in quota beyond 1000 rpm, please contact us: https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519","start_ms":0}}}
    ```

- TiDB Cloud Data Service allows up to 100 requests per day for each Chat2Query Data App.

## Manage API keys

The following sections describe how to create, edit, and delete an API key for a Data App.

### Create an API key

To create an API key for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Authentication** area, click **Create API Key**.
4. In the **Create API Key** dialog box, do the following:

    1. (Optional) Enter a description for your API key.
    2. Select a role for your API key.

        The role is used to control whether the API key can read or write data to the clusters linked to the Data App. You can select the `ReadOnly` or `ReadAndWrite` role:

        - `ReadOnly`: only allows the API key to read data, such as `SELECT`, `SHOW`, `USE`, `DESC`, and `EXPLAIN` statements.
        - `ReadAndWrite`: allows the API key to read and write data. You can use this API key to execute all SQL statements, such as DML and DDL statements.

    3. (Optional) Set a desired rate limit for your API key.

       If your requests per minute exceed the rate limit, the API returns a `429` error. To get a quota of more than 1000 requests per minute (rpm) per API key, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

5. Click **Next**. The public key and private key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

6. Click **Done**.

### Edit an API key

To edit the description or rate limit of an API key, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **API Key** area, locate the **Action** column, and then click **...** > **Edit** in the API key row that you want to change.
4. Update the description, role, or rate limit of the API key.
5. Click **Update**.

### Delete an API key

> **Note:**
>
> Before you delete an API key, make sure that the API key is not used by any Data App.

To delete an API key for a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **API Key** area, locate the **Action** column, and then click **...** > **Delete** in the API key row that you want to delete.
4. In the displayed dialog box, confirm the deletion.
