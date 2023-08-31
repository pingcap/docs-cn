---
title: TiDB Cloud Release Notes in 2021
summary: Learn about the release notes of TiDB Cloud in 2021.
---

# TiDB Cloud Release Notes in 2021

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2021.

## December 28, 2021

New feature:

* Support [importing Apache Parquet files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-parquet-files.md)

Bug fixes:

* Fix the import error that occurs when importing more than 1000 files to TiDB Cloud
* Fix the issue that TiDB Cloud allows to import data to existing tables that already have data

## November 30, 2021

General change:

* Upgrade TiDB Cloud to [TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0) for Developer Tier

New feature:

* Support [adding VPC CIDR for your TiDB cloud project](/tidb-cloud/set-up-vpc-peering-connections.md)

Improvements:

* Improve the monitoring ability for Developer Tier
* Support setting the auto backup time the same as the creation time of a Developer Tier cluster

Bug fixes:

* Fix the TiKV crash issue due to full disk in Developer Tier
* Fix the vulnerability of HTML injection

## November 8, 2021

* Launch [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless), which offers you a one-year free trial of TiDB Cloud

    Each Developer Tier cluster is a full-featured TiDB cluster and comes with the following:

    * One TiDB shared node
    * One TiKV shared node (with 500 MiB of OLTP storage)
    * One TiFlash shared node (with 500 MiB of OLAP storage)

  Get started [here](/tidb-cloud/tidb-cloud-quickstart.md).

## October 21, 2021

* Open user registration to personal email accounts
* Support [importing or migrating from Amazon S3 or GCS to TiDB Cloud](/tidb-cloud/import-csv-files.md)

## October 11, 2021

* Support [viewing and exporting billing details of TiDB Cloud](/tidb-cloud/tidb-cloud-billing.md#billing-details), including the cost of each service and each project
* Fix several issues of TiDB Cloud internal features

## September 16, 2021

* Upgrade the default TiDB version from 5.2.0 to 5.2.1 for newly deployed clusters. See [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1) release notes for detailed changes in 5.2.1.

## September 2, 2021

* Upgrade the default TiDB version from 5.0.2 to 5.2.0 for newly deployed clusters. See [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0) and [5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0) release notes for details of TiDB 5.1.0 and 5.2.0 features.
* Fix several issues of TiDB Cloud internal features.

## August 19, 2021

* Fix several issues of TiDB Cloud internal features. This release does not bring any user behavior changes.

## August 5, 2021

* Support organization role management. Organization owners can configure permissions of organization members as needed.
* Support the isolation of multiple projects within an organization. Organization owners can create and manage projects as needed, and the members and instances between projects support network and authority isolation.
* Optimize the bill to show the billing of each item in the current month and previous month.

## July 22, 2021

* Optimize the user experience of adding credit cards
* Strengthen the security management of credit cards
* Fix the issue that the cluster recovered from backup cannot be charged normally

## July 6, 2021

* Upgrade the default TiDB version from 4.0.11 to 5.0.2 for newly deployed clusters. The upgrade brings significant performance and functionality improvements. See [here](https://docs.pingcap.com/tidb/stable/release-5.0.0) for details.

## June 25, 2021

* Fix the **Select Region** not working issue on the [TiDB Cloud Pricing](https://en.pingcap.com/products/tidbcloud/pricing/) page

## June 24, 2021

* Fix the parse errors of the parquet files when importing the Aurora snapshot into a TiDB instance
* Fix the Estimated Hours not being updated issue when PoC users create a cluster and change the cluster configuration

## June 16, 2021

* **China** is added to the **Country/Region** drop-down list when you sign up for an account

## June 14, 2021

* Fix the mounting EBS error when importing the Aurora snapshot into a TiDB instance

## May 10, 2021

General

* TiDB Cloud is now in Public Preview. You can [sign up](https://tidbcloud.com/signup) and select one of the trial options:

    * 48-Hour Free Trial
    * 2-Week PoC Free Trial
    * Preview On-Demand

Management Console

* Email verification and anti-robot reCAPTCHA have been added to the sign up process
* [TiDB Cloud Service Agreement](https://pingcap.com/legal/tidb-cloud-services-agreement) and [PingCAP Privacy Policy](https://pingcap.com/legal/privacy-policy/) have been updated
* You can apply for a [PoC](/tidb-cloud/tidb-cloud-poc.md) by filling out an application form in the console
* You can import sample data into TiDB Cloud cluster through UI
* Clusters with the same name are not allowed to avoid confusion
* You can give feedback by clicking **Give Feedback** in the **Support** menu
* Data backup and restore features are available for PoC and on-demand trial options
* Points calculator and points usage dashboard have been added for Free Trial and PoC. Data storage and transfer costs are waived for all trial options
