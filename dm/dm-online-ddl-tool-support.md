---
title: TiDB Data Migration Support for Online DDL Tools
summary: Learn about the support for common online DDL tools, usage, and precautions in DM.
---

# TiDB Data Migration Support for Online DDL Tools

In the MySQL ecosystem, tools such as gh-ost and pt-osc are widely used. TiDB Data Migration (DM) provides supports for these tools to avoid migrating unnecessary intermediate data.

This document introduces the support for common online DDL tools, usage, and precautions in DM.

For the working principles and implementation methods of DM for online DDL tools, refer to [online-ddl](/dm/feature-online-ddl.md).

## Restrictions

- DM only supports gh-ost and pt-osc.
- When `online-ddl` is enabled, the checkpoint corresponding to incremental replication should not be in the process of online DDL execution. For example, if an upstream online DDL operation starts at `position-A` and ends at `position-B` of the binlog, the starting point of incremental replication should be earlier than `position-A` or later than `position-B`; otherwise, an error occurs. For details, refer to [FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-true-is-set).

## Configure parameters

<SimpleTab>
<div label="v2.0.5 and later">

In v2.0.5 and later versions, you need to use the `online-ddl` configuration item in the `task` configuration file.

- If the upstream MySQL/MariaDB (at the same time) uses the gh-ost or pt-osc tool, set `online-ddl` to `true` in the task configuration file:

```yml
online-ddl: true
```

> **Note:**
>
> Since v2.0.5, `online-ddl-scheme` has been deprecated, so you need to use `online-ddl` instead of `online-ddl-scheme`. That means that setting `online-ddl: true` overwrites `online-ddl-scheme`, and setting `online-ddl-scheme: "pt"` or `online-ddl-scheme: "gh-ost"` is converted to `online-ddl: true`.

</div>

<div label="earlier than v2.0.5">

Before v2.0.5 (not including v2.0.5), you need to use the `online-ddl-scheme` configuration item in the `task` configuration file.

- If the upstream MySQL/MariaDB uses the gh-ost tool, set it in the task configuration file:

```yml
online-ddl-scheme: "gh-ost"
```

- If the upstream MySQL/MariaDB uses the pt tool, set it in the task configuration file:

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>
