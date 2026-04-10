---
title: DM 安全模式
summary: 介绍 DM safe mode 作用和原理
---

# DM 安全模式

安全模式 (safe mode) 是 DM 在进行增量同步时候的一种运行模式，在安全模式中，DM 增量同步组件在同步 binlog event 时，将把所有 `INSERT` 和 `UPDATE` 操作强制进行改写后再在下游执行。

安全模式的目的是在增量同步过程中，同一条 binlog event 能够在下游被重复同步且保证幂等性，从而确保增量同步能够“安全”进行。

DM 从 checkpoint 恢复数据同步任务后，可能重复执行某些 binlog 事件而导致下述问题：

1. 在进行增量同步过程中，执行 DML 的操作和写 checkpoint 的操作并不是同步的；写 checkpoint 的操作和写下游数据的操作也并不能保证原子性。因此，**当 DM 异常退出时，checkpoint 可能只记录到退出时刻之前的一个恢复点**。
2. 当 DM 重启同步任务，并从 checkpoint 重新开始增量数据同步时，checkpoint 之后的部分数据可能已经在异常退出前被处理过了，从而**导致部分 SQL 语句重复执行**。
3. 如果重复执行 `INSERT` 操作，会导致主键或唯一索引冲突，引发同步中断；如果重复执行 `UPDATE` 操作，会导致不能根据筛选条件找到之前对应的更新记录。

在安全模式下，通过改写 SQL 语句，DM 可以解决上述问题。

## 安全模式原理

安全模式通过 SQL 语句改写来保证 binlog event 的幂等性。具体来说，在安全模式下：

* `INSERT` 语句会被改写成 `REPLACE` 语句。
* `UPDATE` 语句会被分析，得到该语句涉及的行的主键或唯一索引的值，然后改写成 `DELETE` + `REPLACE` 语句 ：先根据主键或唯一索引的定位删除对应的行，然后使用 `REPLACE` 语句插入一条最新值的行记录。

    从 v8.5.6 起，当你在同步任务的会话中设置 `foreign_key_checks=1` 时，对于未修改主键或唯一索引值的 `UPDATE` 语句，DM 会跳过 `DELETE` 步骤。详情参见[外键处理](#外键处理-从-v856-版本开始引入)。

`REPLACE` 操作是 MySQL 特有的数据插入语法。使用 `REPLACE` 语法插入数据时，如果新插入的数据和现有数据存在主键或唯一约束冲突，MySQL 会删除所有冲突的记录，然后再执行插入记录操作，相当于“强制插入”的操作。具体请参考 [MySQL 官方文档的 `REPLACE` 语句相关介绍](https://dev.mysql.com/doc/refman/8.0/en/replace.html)。

比如，假设一张表 `dummydb.dummytbl` 的主键是 `id`，在这张表中重复执行下面的 SQL 语句：

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   # 假设没有其他 int_value = 999的数据
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    # 更新主键操作
```

启用安全模式后，上述 SQL 语句再次在下游执行时，会被改写为下面的 SQL 语句：

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

上述语句中，`UPDATE` 被改写为 `DELETE` + `REPLACE`，而不是 `DELETE` + `INSERT`。如果这里使用 `INSERT`，那么 `id = 999` 的记录在已经存在的情况下重复插入时，数据库会报错主键冲突。因此这里使用了 `REPLACE`，新的记录会替换之前已经插入的记录。

通过这样的语句改写，在进行重复的插入或更新操作时，DM 都会使用执行该操作后的行数据来覆盖之前已经存在的行数据。这样保证了插入和更新操作的可重复执行。

## 开启安全模式

### 自动开启

当 DM 从 checkpoint 恢复增量同步任务（例如 worker 重启，网络中断重连等）时，会自动开启一段时间的安全模式。开启安全模式的逻辑，与 checkpoint 中的 `safemode_exit_point` 信息相关。当一个增量同步任务异常暂停时，DM 会先尝试将内存中所有的 DML 全部同步到下游，然后记录当前内存中从上游拉取到的最新的 binlog 位置点，记作 `safemode_exit_point`，把 `safemode_exit_point` 保存在异常暂停之前最后一个 checkpoint 当中。

当 DM 从 checkpoint 恢复增量同步任务时，会根据下面的判断逻辑来开启安全模式：

- 如果 checkpoint 信息里面额外记录了 `safemode_exit_point`，说明该增量同步任务属于异常暂停。如果 DM 在恢复该增量同步任务时，发现待恢复的 checkpoint 的 binlog 位置点在 `safemode_exit_point` 之前，那么说明从这个 checkpoint 到 `safemode_exit_point` 之间的 binlog 可能已经在下游被执行；恢复该任务后，部分 binlog 会被重复执行。因此，DM 判断在这段 binlog 范围内需要开启安全模式。在当前的 binlog 位置点超过了 `safemode_exit_point` 后，未手动开启 safe-mode 的情况下，DM 将关闭安全模式。

- 如果 checkpoint 信息里没有 `safemode_exit_point` 信息，则有两种情况：

    1. 这是一个全新的任务，或该任务是正常暂停。
    2. 该任务异常暂停时，记录 `safemode_exit_point` 失败；或是 DM 进程异常退出。
    
    第二种情况下，DM 并不知道哪些 checkpoint 之后的 binlog 已经被执行过。为了保险起见，只要没有在 checkpoint 找到 `safemode_exit_point` 信息，DM 就会在前 2 个 checkpoint 间隔中都开启安全模式，确保这段时间里的 binlog 被重复执行不会引发问题。默认的 checkpoint 间隔是 30 秒，也就是说，一个正常的增量同步任务开始时，前 2 * 30 = 60 秒会自动强制开启安全模式。
    
如果你需要调整增量同步任务开始时安全模式的持续时间，可以设置 `syncers` 的配置项 [`safe-mode-duration`](/dm/task-configuration-file-full.md)。

### 手动开启

你可以通过调整增量任务配置文件中 syncer 的配置项 `safe-mode`，控制是否需要全程开启安全模式。`safe-mode` 是布尔类型参数，默认为 `false`。如果设置为 `true`，则表示在增量同步的全过程中都会开启安全模式。例如，下面是一个开启了安全模式的任务配置示例：

```
syncers:                             # sync 处理单元的运行配置参数
  global:                            # 配置名称
    # 其他配置省略
    safe-mode: true                  # 增量同步任务全程开启"安全模式"
    # 其他配置省略
# ----------- 实例配置 -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"
    # 其他配置省略
    syncer-config-name: "global"            # syncers 配置的名称
```

## 外键处理 <span class="version-mark">从 v8.5.6 版本开始引入</span>

> **警告：**
>
> 该功能为实验特性。不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tiflow/issues) 反馈。

当你启用安全模式并在下游任务会话中设置 `foreign_key_checks=1` 时，`UPDATE` 语句默认的 `DELETE` + `REPLACE` 改写方式可能会在子表行上触发非预期的 `ON DELETE CASCADE` 效果。从 v8.5.6 起，DM 引入以下改进来解决此问题。

### 非键值 `UPDATE` 优化

对于未修改主键或唯一键值的 `UPDATE` 语句，DM 会跳过 `DELETE` 步骤，仅执行 `REPLACE INTO`。由于主键保持不变，`REPLACE INTO` 会覆盖现有行，而不会触发外键级联删除。该优化在安全模式下自动生效。

以下面这个上游语句为例，其中 `id` 为主键：

```sql
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE id = 123;
```

在 v8.5.6 之前的版本中，安全模式会将该语句改写为：

```sql
DELETE FROM dummydb.dummytbl WHERE id = 123;       -- 触发 ON DELETE CASCADE
REPLACE INTO dummydb.dummytbl (id, int_value, ...) VALUES (123, 888999, ...);
```

从 v8.5.6 开始，安全模式会将该语句改写为：

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, ...) VALUES (123, 888999, ...);  -- 不触发级联
```

> **警告：**
>
> 当 `foreign_key_checks=1` 时，DM 不支持同步修改了主键或唯一键值的 `UPDATE` 语句。在这种情况下，同步任务会暂停，并报错：`safe-mode update with foreign_key_checks=1 and PK/UK changes is not supported`。如需在包含外键的表上同步此类 `UPDATE` 语句，请将 `safe-mode` 设置为 `false`。

### 会话级 `foreign_key_checks`

在安全模式下执行批处理时，DM 会在执行 `INSERT` 和 `UPDATE` 批处理之前执行 `SET SESSION foreign_key_checks=0`，并在执行完成后恢复 `foreign_key_checks` 原始值。这可以防止 `REPLACE INTO`（其内部实现为 `DELETE` + `INSERT`）在下游触发外键级联操作。

该会话级设置在每个批次中会引入少量开销（两次 `SET SESSION` 往返）。在大多数工作负载中，这种开销可以忽略不计。

### 多 worker 外键因果关系

当你将 `worker-count` 设置为大于 1 且同步任务包含带有外键的表时，DM 会在任务启动时从下游的 `CREATE TABLE` schema 中读取外键关系。对于每个 DML 操作，DM 会基于这些关系注入因果键，从而确保父表行及其依赖的子表行的操作被分配到同一个 DML worker 队列中。

详细限制参见 [DM 兼容性目录](/dm/dm-compatibility-catalog.md#外键-cascade-操作)。

## 注意事项

如果你出于安全考虑，希望全程开启安全模式，你需要注意以下事项：

- **安全模式对于增量同步有额外开销**。频繁的 `DELETE` + `REPLACE` 操作会带来主键或唯一索引的频繁变化，带来了比单纯 `UPDATE` 语句更大的性能开销。
- **安全模式会强制替换主键相同的记录，可能导致下游的记录数据丢失**。如果由于上游分片表合并导入下游的配置不当，可能导致在上游合并导入到下游数据库的时候，出现大量的主键或唯一索引冲突。如果此时全程开启安全模式，会导致下游大量的数据丢失，并且可能无法从任务中看到有任何的异常，导致大量数据不一致。
- **安全模式依赖于通过主键或唯一索引来判断冲突**。如果下游数据库对应的表没有主键或唯一索引，会导致 `REPLACE` 语句无法实现替换插入的目的。这种情况下，即使开启了安全模式，DM 将 `INSERT` 语句改写成 `REPLACE` 并执行后，依旧会向下游插入重复记录。

因此，如果上游存在主键重复的数据，业务可以接受丢失重复数据和性能损失，你可以开启安全模式来忽略数据重复错误。