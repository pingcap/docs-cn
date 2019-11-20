---
title: Kubernetes 上从备份数据恢复 TiDB 集群
category: how-to
---

# Kubernetes 上从备份数据恢复 TiDB 集群
这篇文档详细描述了如何将 Kubernetes 上通过 tidb-operator 备份的 TiDB 集群数据恢复的具体操作过程, 底层通过使用 [`loader`](/dev/reference/tools/loader.md) 来进行集群恢复

## Ad-hoc 全量备份

Ad-hoc 全量备份用过创建一个自定义的 `Backup` CR 对象来描述一次备份，tidb-operator 根据这个 `Backup` 对象来完成具体的备份过程，如果备份过程中出现错误程序不会自动重试，此时需要人工介入处理。

为了更好的说明备份恢复的使用方式，我们假设备份数据来源于 Kubernetes `test1` 这个 namespace 中的 TiDB 集群 `demo1`，然后将其中的一个备份数据恢复到  Kubernetes `test2` 这个 namespace 中的 TiDB 集群 `demo2`, 下面是具体操作过程：

### 备份恢复环境准备

1. 在需要恢复的 `test2` 这个 namespace 中创建备份恢复需要的 RBAC 相关资源

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test2
    ```

    backup-rbac.yaml 文件内容如下:

    ```yaml
    ---
    kind: Role
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: tidb-backup-manager
      labels:
        app.kubernetes.io/component: tidb-backup-manager
    rules:
    - apiGroups: [""]
      resources: ["events"]
      verbs: ["*"]
    - apiGroups: ["pingcap.com"]
      resources: ["backups", "restores"]
      verbs: ["get", "watch", "list", "update"]

    ---
    kind: ServiceAccount
    apiVersion: v1
    metadata:
      name: tidb-backup-manager

    ---
    kind: RoleBinding
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: tidb-backup-manager
      labels:
        app.kubernetes.io/component: tidb-backup-manager
    subjects:
    - kind: ServiceAccount
      name: tidb-backup-manager
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: tidb-backup-manager
    ```

2. 创建 `backup-demo1-tidb-secret` secret, 里面存放用来访问 TiDB 集群的 root 账号和密钥

 kubectl create secret generic backup-demo1-tidb-secret --from-literal=user=root --from-literal=password=12345678 --namespace=test1

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic restore-demo2-tidb-secret --from-literal=user=root --from-literal=password=xxx --namespace=test2
    ```

### 从指定备份恢复 TiDB 集群

1. 创建 restore CR, 从指定备份数据恢复 TiDB 集群

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f restore.yaml
    ```

    restore.yaml 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: Restore
    metadata:
      name: demo2-restore
      namespace: test2
    spec:
      cluster: demo2
      ## specify a backup CR name to represent restore tidb cluster test2/demo2 from this backup
      backup: demo1-backup-schedule-2019-08-15t02-01-00
      secretName: restore-demo2-tidb-secret
      backupNamespace: test1
      storageClassName: rook-ceph-block
      storageSize: 10Gi
    ```


2. 创建好 `Restore` CR 后我们可以通过如下命令查看备份恢复状态：

    {{< copyable "shell-regular" >}}

     ```shell
     kubectl get rt -n test2 -owide
     ```

下面是对 restore CR 各个字段的详细解释:

`.spec.metadata.namespace`： 备份恢复目标 TiDB 集群所在的 namespace

`.spec.cluster`： 备份恢复目标 TiDB 集群的名字

`.spec.backupNamespace`：备份集群所在的 namespace，当前的 restore 需要的远端存储的访问信息，是通过源备份信息获取的，因此需要知道备份源来自哪个 namespace

`.spec.backup`： 备份源的一个 backup CR 名字，我们可以通过下面的命令获取备份集群下面有哪些备份条目，然后从中选择一个要恢复的 backup 进行恢复即可

    {{< copyable "shell-regular" >}}

     ```shell
     kubectl get bk -n test1
     ```

`.spec.secretName`：访问备份恢复目标 TiDB 集群所需密码的 secret

`.spec.storageClassName`：备份恢复时需要指定使用的 PV 类型，如果不指定则默认使用 tidb-operator 启动参数中 `default-backup-storage-class-name` 指定的值，这个值默认为 `standard`

`.spec.storageSize`：备份时指定备份使用的 PV 大小，这个值要大于备份恢复 TiDB 集群数据的大小
