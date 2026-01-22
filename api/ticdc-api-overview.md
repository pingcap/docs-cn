---
title: TiCDC API Overview
summary: Learn the API of TiCDC services.
---

# TiCDC API Overview

[TiCDC](/ticdc/ticdc-overview.md) is a tool used to replicate incremental data from TiDB. Specifically, TiCDC pulls TiKV change logs, sorts captured data, and exports row-based incremental data to downstream databases.

TiCDC provides the following two versions of APIs for querying and operating the TiCDC cluster:

- [TiCDC OpenAPI v1](/ticdc/ticdc-open-api.md)
- [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)

> **Note:**
>
> TiCDC OpenAPI v1 will be removed in the future. It is recommended to use TiCDC OpenAPI v2.

For more information about each API, including request parameters, response examples, and usage instructions, see [TiCDC OpenAPI v1](/ticdc/ticdc-open-api.md) and [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md).