---
title: Placement Rules 使用文档
summary: 如何配置 Placement Rules
category: how-to
---

# Placement Rules 使用文档

Placement Rules 是一套强大灵活的副本规则系统。通过组合不同的调度规则，用户可以精细控制任何一段数据的副本数，每个副本的存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft Leader 等等。

## 开启 Placement Rules

可通过 pd-ctl 设置 enable-placement-rules 为 true 开启。

```sh
>> config set enable-placement-rules true
```

开启后会根据之前的副本配置默认生成一条规则，下面的生成的规则对应于之前版本的 `max-replicas=3,location-labels=[zone,rack,host]` 配置：

```json
{
  "group_id": "pd",
  "id": "default",
  "start_key": "",
  "end_key": "",
  "role": "voter",
  "count": "3",
  "location_labels": ["zone", "rack", "host"]
}
```

## 字段的具体含义

### group_id

标识规则的创建者，不同创建者之间互不影响

### id

group 内唯一标识，由创建者自行生成

### index

适用多条规则时，控制调度时的适配顺序(group 内生效)

### override

是否覆盖 index 更小的规则（group 内生效）

### start_key

开始的 key，表示从哪一个 key 开始该规则生效

### end_key

结束的 key，表示到哪一个 key 结束该规则就不再生效

### role

Raft 算法当中的角色，包括：`voter`，`leader`，`follower` 以及 `learner`

### count

所要添加角色的数量，特别的，对于 `leader` 而言，该值不能大于 1

### label_constraints

用于过滤 store 的限制条件，支持通过 `in`, `notIn`, `exists`, `notExists` 四种原语来筛选 label

### location_labels

用于实现根据拓扑进行隔离，与之前的意义相同

## 添加规则

可通过 HTTP POST 方法添加规则：

```sh
curl -X POST -H "Content-Type: application/json" -data '{rule}' https://ip:port/pd/api/v1/config/rules
```

把 `{rule}` 部分替换成对应添加的规则

## 典型场景举例

### 场景一：普通 table 数据使用 3 副本，meta 元数据使用 5 副本提升集群容灾能力

新建一条规则，为 meta 对应的 key range 添加 2 副本，具体规则如下：

```json
{
  "group_id": "pd",
  "id": "meta",
  "start_key": "6D", // 6D 是 'm' 的十六进制表示方式
  "end_key": "6E", // 6E 是 'n' 的十六进制表示方式
  "role": "voter",
  "count": "2",
  "label_constraints": [],
  "location_labels": ["zone", "rack", "host"]
}
```

加上这条规则后，普通 table 数据仍适用于 default 规则，meta 数据根据 key range 将适配 default 和 meta，分别配置了 3 副本和 2 副本，共 5 副本。

*注意* 由于不同的 Rule 调度时单独计算，只能保证 default 规则的 3 副本按照 `location-labels` 隔离，meta 规则的 2 副本也隔离，而不能防止 default 规则的副本和 meta 规则的副本被调度在一起。

可以通过 default 规则的范围拆分成 2 个，key range 分别为 `["", "6D")` 和 `["6E", "")`，然后把 meta 规则的 `count` 调整为 5，让 meta 数据只适配一条 5 副本的规则，实现 `location-label` 的隔离。

更合适的方式是通过设置 meta 规则的 `override` 属性来避免更新 default 规则，此时要注意设置 `index` 来保证 meta 规则堆叠在 default 的上面。

```json
{
  "group_id": "pd",
  "id": "meta",
  "index": 1,
  "override": true,
  "start_key": "6D",
  "end_key": "6E",
  "role": "voter",
  "count": "5",
  "location_labels": ["zone", "rack", "host"]
}
```

### 场景二：5 副本按 2-2-1 的比例放置在 3 个数据中心，且第 3 个中心不调度 Leader

设置以下 3 条规则即可：

```json
{
  "group_id": "pd",
  "id": "zone1",
  "start_key": "",
  "end_key": "",
  "role": "voter",
  "count": 2,
  "label_constraints": [
    {"key": "zone", "op": "in", "values": ["zone1"]}
  ],
  "location_labels": ["rack", "host"]
}
{
  "group_id": "pd",
  "id": "zone2",
  "start_key": "",
  "end_key": "",
  "role": "voter",
  "count": 2,
  "label_constraints": [
    {"key": "zone", "op": "in", "values": ["zone2"]}
  ],
  "location_labels": ["rack", "host"]
}
{
  "group_id": "pd",
  "id": "zone3",
  "start_key": "",
  "end_key": "",
  "role": "follower",
  "count": 1,
  "label_constraints": [
    {"key": "zone", "op": "in", "values": ["zone3"]}
  ],
  "location_labels": ["rack", "host"]
}
```

每个数据中心对应一条规则，通过 `count` 设置副本数，通过 `role` 标识副本角色（是否需要 `leader`）。由于每个规则对应的副本都使用 `label_constraints` 约束在单个数据中心内了，`location_labels` 只需配置 `rack`，`host` 两级。

### 场景三：为某个 table 添加 2 个 TiFlash 副本

具体规则如下：

```json
{
  "group_id": "tiflash",
  "id": "learner-replica-table-03",
  "start_key": "748000000000000003", // start key of table 3
  "end_key": "748000000000000004",   // start key of table 4
  "role": "learner",
  "count": 2,
  "label_constraints": [
    {"key": "engine", "op": "in", "values": ["tiflash"]}
  ],
  "location_labels": ["host"]
}
```

该规则指定添加的角色为 `learner`，并且通过 `label_constraints` 被用于筛选 `engine` 的类型，指定 `engine` 类型为 `tiflash`。

### 场景四：为某个 table 在有高性能磁盘的北京节点添加 2 个 Follower 副本

具体规则如下：

```json
{
  "group_id": "follower-read",
  "id": "follower-read-table-03",
  "start_key": "748000000000000003", // table 3 的 start key
  "end_key": "748000000000000004",   // table 4 的 start key
  "role": "follower",
  "count": 2,
  "label_constraints": [
    {"key": "zone", "op": "in", "values": ["bj1", "bj2"]},
    {"key", "disk", "op": "notIn", "values": ["hdd"]}
  ],
  "location_labels": ["host"]
}
```
