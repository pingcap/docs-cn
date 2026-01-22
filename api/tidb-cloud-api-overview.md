---
title: TiDB Cloud API Overview
summary: Learn about what TiDB Cloud API is, its features, and how to use the API to manage your TiDB Cloud clusters.
---

# TiDB Cloud API Overview

> **Note:**
>
> TiDB Cloud API is in beta.

The TiDB Cloud API is a [REST interface](https://en.wikipedia.org/wiki/Representational_state_transfer) that provides you with programmatic access to manage administrative objects within TiDB Cloud. Through this API, you can automatically and efficiently manage resources such as projects, clusters, backups, restores, imports, billings, and resources in the [Data Service](https://docs.pingcap.com/tidbcloud/data-service-overview).

The API has the following features:

- **JSON entities.** All entities are expressed in JSON.
- **HTTPS-only.** You can only access the API via HTTPS, ensuring all the data sent over the network is encrypted with TLS.
- **Key-based access and digest authentication.** Before you access the TiDB Cloud API, you must generate an API key. For more information, see [API Key Management](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management). All requests are authenticated through [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), ensuring the API key is never sent over the network.

The TiDB Cloud API is available in two versions:

- [v1beta1](/api/tidb-cloud-api-v1beta1.md): manage TiDB Cloud Starter, Essential, and Dedicated clusters, as well as billing, Data Service, and IAM resources.
- [v1beta](/api/tidb-cloud-api-v1beta.md): manage projects, clusters, backups, imports, and restores for TiDB Cloud.
