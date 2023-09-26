---
title: (The same as L1 heading) Feature name such as "Clustered Indexes" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells users what they can get from this doc. For example, "Learn what is clustered indexes and how to use clustered index to help you...". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# New Feature Name (the same as title in the metadata)

> About this template:
>
> - This document is a template for new features, including feature concepts and how to use the feature. You can directly copy and use this template and delete unnecessary annotations. An example of this type of document: [Clustered Indexes](/clustered-indexes.md).
> - For a new document, please add a link to the appropriate location in the `TOC.md` file (consider where users are most likely to look for this document in the table of contents).
> - The headings within the document cannot skip levels, and try to avoid using level 5 headings.

> **Warning** (Optional)
>
> This is an experimental feature and is not recommended for production environments.

This document describes the Usage scenarios, usage methods, and limitations of [feature name] and the FAQs when using this feature.

[Feature name] is a XXX that can be used to do XXX. By using this feature, you can achieve or optimize [a summary of the usage scenario]. (The implementation details or principles can be omitted, or you can consider putting them in a separate section or another document).

If you need to add notes or warnings, strictly follow the following format.

> **Note**
>
> For general tips and notes, use a note.

> **Warning**
>
> If the information might bring risks to users, such as system availability, security, data loss, etc., use a warning.

If the notes or warnings are nested in a list, indent them with four spaces.

To prevent incorrect display, **all indentation on the PingCAP website must be 4 spaces.**

## Usage scenario(s)

Usage scenarios are very important. You need to introduce why users need to use this feature, in what cases they can use it, and what problems this feature can solve from the user's perspective.

[New feature] is suitable for the following scenarios:

- unordered list
- unordered list

### Usage scenario 1

### Usage scenario 2

## Prerequisites (optional)

- Prepare xxx. Describes how to prepare xxx. You can provide a link to the reference document.
- Ensure that xxx. Describes how to check whether xxx meets the requirements. If not, describe how to handle it.

## Usage or Procedures

TiDB provides x methods for xxx, which are AAA method and BBB method.

In the case of xxx, to achieve xxx, it is recommended to use the AAA method.

### Method 1: AAA (recommended)

1. first step
2. second step
3. third step

### Method 2: BBB

1. first step
2. second step
3. third step

## Parameter reference

If this feature is mainly a new syntax or command, list the specific configuration item or parameter description, default value, and example.

You can either use a table or an unordered list.

| Parameter | Description | Default value | Required | Example |
| :-- | :-- | :-- | :-- | :-- |
| xxx | xxx | xxx | xxx | xxx |

## Limitations

In this section, list the usage limitations. If there is no order between the limitations, use an unordered list.

## Compatibility

In this section, list the compatibility information of this feature, including:

- The compatibility with previous TiDB versions
- The compatibility with MySQL
- The compatibility under different architectures or platforms.

## FAQ (optional)

In this section, list the FAQs when using this feature.

If there are many FAQs, you can add a separate FAQ document for this feature.

### Q1: xxx

Answer.

### Q2: xxx

Answer.

## More resources

In this section, provide more related documents that users might want to read, such as:

- To view the TiFlash version, important logs, and system tables, see [Maintain a TiFlash Cluster](/tiflash/maintain-tiflash.md).
- If you need to remove a TiFlash node, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

You can also directly provide the documents that users might be interested in, such as:

- [Explore HTAP](/explore-htap.md)
- [TiFlash Architecture](/tiflash/tiflash-overview.md#architecture)
- [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md)
