---
title: (The same as L1 heading) Concept such as "Garbage Collection Overview" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells users what they can get from this doc. For example, "Learn how to quickly get started with the TiDB database". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# L1 heading (the same as title in the metadata)

> About this template:
>
> - This document is a template for concept topics, focusing on introducing concepts and explanatory information. You can directly copy and use this template and delete unnecessary annotations. An example of this type of document: [TiCDC Overview](/ticdc/ticdc-overview.md).
> - For a new document, please add a link to the appropriate location in the `TOC.md` file (consider where users are most likely to look for this document in the table of contents).
> - The headings within the document cannot skip levels, and try to avoid using level 5 headings.

**Required** In the first paragraph, summarize the content of this document in a few sentences.

You can clarify the important terms and definitions within one to three sentences in this paragraph.

## L2 heading (e.g. Architecture)

Taking the overall architecture as an example, you can first introduce the core components in one or two sentences, and then provide the corresponding architecture diagram.

<!--  ![Architecture](/path/to/image)  -->
Keep image size <= 300 KB. Use `.png` or `.jpg`; do not use `.gif` or `.svg`.

Write a more detailed description below the image. Use unordered lists (`*`/`+`/`-`) to introduce each component.

- Component 1: xxx
- Component 2: xxx

You can also describe the basic working principles here, or integrate the principles into the component introduction above.

### L3 heading (optional, e.g. “xxx component”)

If the component is complicated, you can elaborate it in a separate section like this one.

### L3 heading

xxx

## L2 heading (optional, e.g. "Key features/Limitations")

In the second L2 heading, introduce the basic info that users need to know beforehand, such as key features, usage scenarios, and limitations.

You can leave out this section if there's no need to provide this information.

If you need to add notes or warnings, strictly follow the following format.

> **Warning**
>
> If the information might bring risks to users, such as system availability, security, data loss, etc., use a warning. For example, the current feature is an experimental feature and is not recommended for production environments.

> **Note**
>
> For general tips and notes, use a note. For example, when reading historical data, even if the current table structure is different from the table structure of the historical data, the historical data will be returned in the table structure of the historical data at that time.

If the notes or warnings are nested in a list, indent them with four spaces.

To prevent incorrect display, all indentation on the PingCAP website must be 4 spaces.

## What's next

In this section, provide more related documents that users might want to read, such as:

- To learn how to deploy and maintain TiCDC, see [Deploy and Maintain TiCDC](/ticdc/deploy-ticdc.md).
- To learn changefeeds, see [Changefeed Overview](/ticdc/ticdc-changefeed-overview.md).

You can also directly provide the documents that users might be interested in, such as:

- [Explore HTAP](/explore-htap.md)
- [TiCDC FAQs](/ticdc/ticdc-faq.md)
- [TiCDC Glossary](/ticdc/ticdc-glossary.md)
