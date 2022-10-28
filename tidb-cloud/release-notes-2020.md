---
title: TiDB Cloud Release Notes in 2020
summary: Learn about the release notes of TiDB Cloud in 2020.
---

# TiDB Cloud Release Notes in 2020

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2020.

## December 30, 2020

* Upgrade the default TiDB version to v4.0.9
* Support upgrading and scaling in TiDB gracefully to achieve zero client failures
* Recover cluster configuration after restoring a new cluster from backup

## December 16, 2020

* Adjust the minimum number of TiDB nodes to one for all cluster tiers
* Prohibit executing system command on the SQL web shell
* Enable redact-log for TiDB clusters by default

## November 24, 2020

* Allow the traffic filter IP list of a TiDB cluster's public endpoint to be empty to disable public access
* Improve the delivery rate of invitation emails sent to customers with Outlook or Hotmail
* Polish the error notification message for sign-up
* New clusters will run on CentOS VM instead of Ubuntu
* Fix the issue that the cluster does not show in the recycle bin when the corresponding backup still exists

## November 4, 2020

* Implement the function of changing the organization name
* Prevent users from accessing TiDB during data restoring
* Update Terms of Service and Privacy location in the Sign Up page
* Add a feedback form entrance widget
* Prevent Members from deleting owner(s) in the Preference tab
* Change TiFlash and TiKV storage chart metrics
* Upgrade the default TiDB cluster version to 4.0.8

## October 12, 2020

* Change the SQL webshell client from Oracle MySQL client to `usql` client
* Upgrade the default TiDB version to 4.0.7
* Extend the manual backup retention period from 7 days to 30 days

## October 2, 2020

* Fix TiFlash disk storage configuration

## September 14, 2020

* Fix monitoring metrics by adding the `region` label
* Fix the issue that non-HTAP clusters cannot be scaled

## September 11, 2020

* Customers now can access TiDB using a public endpoint with traffic filters
* Add the time zone indicator at the auto backup settings dialog
* Fix the broken invitation link when registration is not finished

## September 4, 2020

* Fix an incorrect URL in invitation Email

## August 6, 2020

* Change email support to visiting TiDB Cloud Customer Support
* Add the simple 2fa feature for custom email login
* Add the feature of setting up VPC peering
* Add custom email support for signup/login

## July 17, 2020

* Adjust the default retention of automated daily backup to 7 days
* Add reasons at tooltip for clusters in unhealthy status
* Fix the issue that when the initial credit is 0, users can still create a cluster
* Optimize the integration of Dashboard
* Send emails when adding credits for customers
* Add the tenant ID in the tenant preference page
* Optimize the reasonable notice message for user's quota limit
* Fix backup/restore metrics
