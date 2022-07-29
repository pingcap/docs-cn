---
title: Console Audit Logging
summary: Learn about the log auditing feature for the TiDB Cloud Console.
---

# Console Audit Logging

TiDB Cloud provides the audit logging feature for TiDB Cloud console operations, which records the history of user access details (such as user login to the Console and cluster creation operations).

> **Note:**
>
> Currently, the **audit logging** feature is experimental. The output is subject to change.

## Limitations

Currently, the console audit logging feature has the following limitations:

- Console audit logging is enabled by default and cannot be disabled by users.
- You cannot specify the audit filtering rules for the feature. 
- You can access the audit logs only with the help of PingCAP support.

## Audit event types

All user operations on the TiDB Cloud Console are recorded in the audit logs as events. Audit logs cover the following event types:

| Audit event type | Description |
|---|---|
| AuditEventSignIn | Sign in |
| AuditEventSignOut | Sign out |
| AuditEventUpdateUserProfile | Update user's first name and last name |
| AuditEventUpdateMFA | Enable or disable MFA |
| AuditEventCreateProject | Create a new project |
| AuditEventUpdateProject | Update the project name |
| AuditEventDeleteProject | Delete a project |
| AuditEventInviteUserIntoProject | Invite a user into a project |
| AuditEventDeleteProjectUser | Delete a project user |
| AuditEventUpdateOrg | Update organization name and time zone |
| AuditEventCreateIntegration | Create an integration |
| AuditEventDeleteIntegration | Delete an integration |
| AuditEventListOrgUsers | List users in organization |
| AuditEventListProjectUsers | List users in a project |
| AuditEventAddNewPaymentMethod | Add a new credit card |
| AuditEventUpdatePaymentMethod | Update credit card information |
| AuditEventDeletePaymentMethod | Delete a credit card |
| AuditEventCreateAWSVpcPeering | Create an AWS VPC Peering |
| AuditEventCreateGCPVpcPeering | Create a GCP VPC Peering | 
| AuditEventListAWSVpcPeering | List all AWS VPC Peerings in a project |
| AuditEventListGCPVpcPeering | List all GCP VPC Peerings in a project |
| AuditEventDeleteAWSVpcPeering | Delete an AWS VPC Peering |
| AuditEventDeleteGCPVpcPeering | Delete a GCP VPC Peering |
| AuditEventGetProjectTrafficFilter | Get traffic filter list of a project |
| AuditEventUpdateProjectTrafficFilter | Update traffic filter list of a project |
| AuditEventGetTrafficFilter | Get traffic filter list of a cluster |
| AuditEventUpdateTrafficFilter | Update traffic filter list of a cluster |
| AuditEventCreateProjectCIDR | Create a new project CIDR |
| AuditEventGetProjectCIDR | List the CIDR of a region |
| AuditEventGetProjectRegionCIDR | List all CIDRs in a project |
| AuditEventDeleteBackupInRecycleBin | Delete backups of deleted clusters in recycle bin |
| AuditEventChangeClusterRootPassword | Reset the root password of a cluster |
| AuditEventCreateImportTask | Create an import task |
| AuditEventCancleImportTask | Cancel an import task |
| AuditEventExitImportTask | Exit an import task |
| AuditEventCreateCluster | Create a cluster |
| AuditEventDeleteCluster | Delete a cluster |
| AuditEventScaleCluster | Scale a cluster |
| AuditEventCreateBackup | Make a backup |
| AuditEventDeleteBackup | Delete a backup |
| AuditEventRestoreBackup | Restore from a backup |
| AuditEventUpdateAuditLogStatus | Enable or disable database audit logging |
| AuditEventCreateAuditLogAccessRecord | Add database audit log filter conditions |
| AuditEventDeleteAuditLogAccessRecord | Delete database audit log filter conditions |
| AuditEventUpdateUserRole | Modify user roles |

## Audit log storage policy

- The audit log information is stored in AWS ES.
- The storage time is 90 days, after which the audit logs will be automatically cleaned up.

## View audit logs

The console audit logs are temporarily accessible only to internal personnel of TiDB Cloud. If you need to view the logs, contact [PingCAP support team](/tidb-cloud/tidb-cloud-support.md).

## Audit log fields

The fields in audit logs include basic fields and extended fields.

The basic fields are as follows:

| Field name | Data type | Description |
|---|---|---|
| timestamp | timestamp | Time of event |
| auditEventType | string | Event type |
| userID | uint64 | User ID |
| clientIP | string | Client IP |
| isSuccess | bool | Event result |

Extended fields supplement the description information of events based on different event types to ensure the integrity and availability of audit information

> **Note:**
>
> For scenarios where the basic fields cannot clearly describe the event, the following table shows the extended field information of these event types. Events not in the table have no extension fields.

| Audit event type | Extended fields | Data type for extended fields | Description for extended fields |
|---|---|---|---|
| AuditEventUpdateMFA | enableMFA | bool |Enable or disable MFA |
| AuditEventCreateProject | projectName | string | Project name |
| AuditEventUpdateProject | oldProjectName <br/> newProjectName | string <br/> string | Old Project name <br/> New project name |
| AuditEventDeleteProject | projectName | string | Project name |
| AuditEventInviteUserIntoProject | email <br/> Role | string <br/> string | Email <br/> Role name |
| AuditEventDeleteProjectUser | email <br/> Role | string <br/> string | Email <br/> Role name |
| AuditEventUpdateOrg | orgName <br/> timeZone | string <br/> uint| Organization name <br/> Time zone |
| AuditEventCreateIntegration | integrationType | string | Integration type |
| AuditEventDeleteIntegration | integrationType | string | Integration type |
| AuditEventAddNewPaymentMethod | cardNumber | string | Payment card number (information desensitized) |
| AuditEventUpdatePaymentMethod | cardNumber | string | Payment card number (information desensitized) <br/> (Currently not getting full field information) |
| AuditEventDeletePaymentMethod |  |  | (Currently not getting full field information) |
| AuditEventCreateCluster | clusterName | string | Cluster name |
| AuditEventDeleteCluster | clusterName | string | Cluster name |
| AuditEventCreateBackup | backupName | string | Backup name |
| AuditEventRestoreBackup | clusterName | string | Cluster name |
| AuditEventUpdateAuditLogStatus | enableAuditLog | bool | Enable or disable database audit logging |
| AuditEventUpdateUserRole | oldRole <br/> newRole | string <br/> string | Old role name <br/> New role name |
