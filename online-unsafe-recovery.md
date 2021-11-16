---
title: Online Unsafe Recovery
summary: Learn how to use Online Unsafe Recovery.
---

# Online Unsafe Recovery

> **Warning:**
>
> - Online Unsafe Recovery is a type of lossy recovery. If you use this feature, the integrity of data and data indexes cannot be guaranteed.
> - Online Unsafe Recovery is an experimental feature, and it is **NOT** recommended to use it in the production environment. The interface, strategy, and internal implementation of this feature might change when it becomes generally available (GA). Although this feature has been tested in some scenarios, it is not thoroughly validated and might cause system unavailability.
> - It is recommended to perform the feature-related operations with the support from the TiDB team. If any misoperation is performed, it might be hard to recover the cluster.

When permanently damaged replicas cause part of data on TiKV to be unreadable and unwritable, you can use the Online Unsafe Recovery feature to perform a lossy recovery operation.

## Feature description

In TiDB, the same data might be stored in multiple stores at the same time according to the replica rules defined by users. This guarantees that data is still readable and writable even if a single or a few stores are temporarily offline or damaged. However, when most or all replicas of a Region go offline during a short period of time, the Region becomes temporarily unavailable, by design, to ensure data integrity.

Suppose that multiple replicas of a data range encounter issues like permanent damage (such as disk damage), and these issues cause the stores to stay offline. In this case, this data range is temporarily unavailable. If you want the cluster back in use and also accept data rewind or data loss, in theory, you can re-form the majority of replicas by manually removing the failed replicas from the group. This allows application-layer services to read and write this data range (might be stale or empty) again.

In this case, if some stores with loss-tolerant data are permanently damaged, you can perform a lossy recovery operation by using Online Unsafe Recovery. Using this feature, PD, under its global perspective, collects the metadata of data shards from all stores and generates a real-time and complete recovery plan. Then, PD distributes the plan to all surviving stores to make them perform data recovery tasks. In addition, once the data recovery plan is distributed, PD periodically monitors the recovery progress and re-send the plan when necessary.

## User scenarios

The Online Unsafe Recovery feature is suitable for the following scenarios:

* The data for application services is unreadable and unwritable, because permanently damaged stores cause the stores to fail to restart.
* You can accept data loss and want the affected data to be readable and writable.
* You want to perform a one-stop online data recovery operation.

## Usage

### Prerequisites

Before using Online Unsafe Recovery, make sure that the following requirements are met:

* The offline stores indeed cause some pieces of data to be unavailable.
* The offline stores cannot be automatically recovered or restarted.

### Step 1. Disable all types of scheduling

You need to temporarily disable all types of internal scheduling, such as load balancing. After disabling them, it is recommended to wait for about 10 minutes so that the triggered scheduling can have sufficient time to complete the scheduled tasks.

> **Note:**
>
> After the scheduling is disabled, the system cannot resolve data hotspot issues. Therefore, you need to enable the scheduling as soon as possible after the recovery is completed.

1. Use PD Control to get the current configuration by running the [`config show`](/pd-control.md#config-show--set-option-value--placement-rules) command.
2. Use PD Control to disable all types of scheduling. For example:

    * [`config set region-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set replica-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set merge-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)

### Step 2. Remove the stores that cannot be automatically recovered

Use PD Control to remove the stores that cannot be automatically recovered by running the [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show--history) command.

> **Note:**
>
> The returned result of this command only indicates that the request is accepted, not that the recovery is completed successfully. The stores are actually recovered in the background.

### Step 3. Check the progress

When the above store removal command runs successfully, you can use PD Control to check the removal progress by running the [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules) command. When the command result shows "Last recovery has finished", the system recovery is completed.

### Step 4. Test read and write tasks

After the progress command shows that the recovery task is completed, you can try to execute some simple SQL queries like the following example or perform write tasks to ensure that the data is readable and writable.

```sql
select count(*) from table_that_suffered_from_group_majority_failure;
```

> **Note:**
>
> The situation that data can be read and written does not indicate there is no data loss.

### Step 5. Restart the scheduling

To restart the scheduling, you need to adjust the `0` value of `config set region-schedule-limit 0`, `config set replica-schedule-limit 0`, and `config set merge-schedule-limit 0` modified in step 1 to the initial values.

Then, the whole process is finished.