---
title: TiFlash FAQ
summary: Learn the frequently asked questions (FAQs) and answers about TiFlash.
category: faq
---

# TiFlash FAQ

This document lists the frequently asked questions (FAQs) and answers about TiFlash.

## Does TiFlash support direct writes?

Currently, TiFlash does not support direct writes. You can only write data to TiKV, and then replicate the data to TiFlash.

## How can I estimate the storage resources if I want to add TiFlash to an existing cluster?

You can evaluate which tables might require acceleration. The size of a single replica of these tables data is roughly equal to the storage resources required by two replicas of TiFlash. Note that you need to take into account the free space required.

## How can data in TiFlash be highly available?

TiFlash restores data through TiKV. As long as the corresponding Regions in TiKV are available, TiFlash can restore data from these Regions.

## How many replicas does TiFlash recommend to set up?

If you need highly available TiFlash services (rather than highly available data), it is recommended to set up two replicas for TiFlash. If you allow TiKV replicas to provide analytical services when TiFlash is down, you can set up a single TiFlash replica.

## Should I use TiSpark or TiDB server for a query?

It is recommended to use TiDB server if you query a single table mainly using filtering and aggregation, because the TiDB server has better performance on the columnar storage. It is recommended to use TiSpark if you query a table mainly using joins.
