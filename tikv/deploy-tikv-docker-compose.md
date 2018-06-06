---
title: Install and Deploy TiKV Using Docker Compose
category: user guide
---

# Install and Deploy TiKV Using Docker Compose

This guide describes how to quickly deploy a TiKV cluster using [Docker Compose](https://github.com/pingcap/tidb-docker-compose/). Currently, this installation method only supports the Linux system.

## Prerequisites

- Install Docker and Docker Compose.

    ```
    sudo yum install docker docker-compose
    ```

- Install Helm.

    ```
    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
    ```

## Install and deploy

1. Download `tidb-docker-compose`.

    ``` 
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. Edit the `compose/values.yaml` file to configure `networkMode` to `host` and comment the TiDB section out.

    ```
    cd tidb-docker-compose/compose
    networkMode: host
    ```

3. Generate the `generated-docker-compose.yml` file.

    ```
    helm template compose > generated-docker-compose.yml
    ```

4. Create and start the cluster using the `generated-docker-compose.yml` file.

    ```
    docker-compose -f generated-docker-compose.yml up -d
    ```

You can check whether the TiKV cluster has been successfully deployed using the following command:

```
curl localhost:2379/pd/api/v1/stores
```

If the state of all the TiKV instances is "Up", you have successfully deployed a TiKV cluster.

## What's next?

If you want to try the Go client, see [Try Two Types of APIs](go-client-api.md).