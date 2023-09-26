---
title: (The same as L1 heading) Such as "Get Started with TiDB" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells the users what they can get from this doc. For example, "Learn how to quickly get started with TiDB in 10 minutes". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# L1 heading (the same as title in the metadata)

> About this template:
>
> - This document is a template for task topics, which tells users how to perform a specific task step by step. You can directly copy and use this template and delete unnecessary annotations. An example of this type of document: [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md)
> - For a new document, please add a link to the appropriate location in the `TOC.md` file (consider where users are most likely to look for this document in the table of contents).
> - The headings within the document cannot skip levels, and try to avoid using level 5 headings.

**Required** In the first paragraph, summarize the content of this document in a few sentences.

You can describe the task of this document as follows:

"This document describes how to ... (task) using ... (tool)."

## L2 heading (usually "Prerequisites" or "Prepare the environment")

Introduce the prerequisites for the task, including the hardware, network, and software versions.

## Step 1. xxx

You can divide the step into smaller sub-steps by using ordered lists (1, 2, 3, …)

1. xxx

    If you want to explain this step, indent **4 spaces** and leave a blank line before this paragraph.

    If you need to use a **note** or a **warning**, write the note in the following format.

    > **Warning**
    >
    > If the information may bring risks to users, such as system availability, security, data loss, etc., use a warning. For example, "The current feature is an experimental feature and is not recommended for production environments."

    > **Note**
    >
    > For general tips and notes, use a note. For example, "When reading historical data, even if the current table structure is different from the table structure of the historical data, the historical data will be returned in the table structure of the historical data at that time."

    If the notes or warnings are nested in a list, indent them with four spaces.

    To prevent incorrect display, all indentation on the PingCAP website must be 4 spaces.

2. xxx

    If you want to use a code block, indent 4 spaces and leave a blank line before the block.

    ```bash
    # command
    ```

    After each step, it is recommended that you provide an expected result for users to verify if their operations are successful:

    ```bash
    # expected output
    ```

    Tell users what to do if they encounter an error.

3. xxx

    If you want to nest another list inside the list, use the ordered list (1, 2, 3, …) or unordered list (*/+/-) and indent 4 spaces as well.

    1. Substep 1
    2. Substep 2
    3. Substep 3

    Or:

    + One item
    + Another item
    + One more item

4. xxx

    If a step involves updating a configuration file, give the detailed location of the configuration file, such as which node and which directory, the name of the configuration file, and explain the key fields in the configuration file to help users understand.

    ```toml
    ### tidb-lightning global configuration

    [lightning]
    # The HTTP port used to pull the web interface and Prometheus metrics. Set to 0 to disable the port.
    status-addr = ':8289'

    # Switch to server mode and use the web interface
    # For details, see the "TiDB Lightning Web UI" document.
    server-mode = false

    # log
    level = "info"
    file = "tidb-lightning.log"
    max-size = 128 # MB
    max-days = 28
    max-backups = 14
    ```

5. xxx

    After each step, it is recommended that you provide an expected result for users to verify if their operations are successful.

## Step 2. xxx

1. xxx

    1. xxx
    2. xxx

2. xxx

3. xxx

## Step 3. xxx

## What's next

In this section, provide more related documents that users may want to read, such as:

- To view the TiFlash version, important logs, and system tables, see [Maintain a TiFlash Cluster](/tiflash/maintain-tiflash.md).
- If you need to remove a TiFlash node, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

You can also directly provide the documents that users may be interested in, such as:

- [Explore HTAP](/explore-htap.md)
- [TiFlash Architecture](/tiflash/tiflash-overview.md#architecture)
- [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md)
