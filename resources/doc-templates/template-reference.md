---
title: (The same as L1 heading) Such as "Garbage Collection Configuration" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells the users what they can get from this doc. For example, "Learn all the configuration options that you can use in garbage collection". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# L1 heading (the same as title in the metadata)

> About this template:
>
> - This document is a template for reference topics, including commands, parameters, configuration options. You can directly copy and use this template and delete unnecessary annotations. An example of this type of document: [TiDB Cluster Alert Rules](/alert-rules.md)
> - For a new document, please add a link to the appropriate location in the `TOC.md` file (consider where users are most likely to look for this document in the table of contents).
> - The headings within the document cannot skip levels, and try to avoid using level 5 headings.

**Required** In the first paragraph, summarize the content of this document in a few sentences.

You can use the following sentence:

"This document describes..."

## L2 heading (A category or a parameter/configuration item)

Introduce the category/parameter/configuration item described in this section, using the following sentence:

"This section describes..."

### L3 Heading (optional, a parameter or a configuration item)

If you need to list multiple parameters, use unordered lists (`*`/`+`/`-`).

- xxx: xxx
- xxx: xxx
- xxx: xxx

### L3 Heading 2

xxx

## L2 Heading 2

If you need to add notes or warnings, strictly follow the following format.

> **Warning**
>
> If the information might bring risks to users, such as system availability, security, data loss, etc., use a warning. For example, the current feature is an experimental feature and is not recommended for production environments.

> **Note**
>
> For general tips and notes, use a note. For example, when reading historical data, even if the current table structure is different from the table structure of the historical data, the historical data will be returned in the table structure of the historical data at that time.

If the notes or warnings are nested in a list, indent them with four spaces.

To prevent incorrect display, all indentation on the PingCAP website must be 4 spaces.

## L2 heading 3

If you need to use a table, note that the table must have headers (namely, the first row).

The following table lists the description, default value, and example of the specific configuration item/parameter.

| Parameter | Description | Default value | Required | Example |
| :-- | :-- | :-- | :-- | :-- |
| xxx | xxx | xxx | xxx | xxx |
