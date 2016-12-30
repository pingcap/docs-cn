## 使用 `docker-compose`, 更方便地构建集群

只需要一个简单的 `docker-compose.yml`:

```yaml
version: '2'

services:
  pd1:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd1
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd1:2379
      - --advertise-peer-urls=http://pd1:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  pd2:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd2
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd2:2379
      - --advertise-peer-urls=http://pd2:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  pd3:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd3
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd3:2379
      - --advertise-peer-urls=http://pd3:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv2:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv3:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tidb:
    image: pingcap/tidb
    ports:
      - "4000"
      - "10080"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --store=tikv
      - --path=pd1:2379,pd2:2379,pd3:2379
      - -L=warn

    depends_on:
      - "tikv1"
      - "tikv2"
      - "tikv3"

    privileged: true
```

+ 使用 `docker-compose up -d` 创建并启动集群
+ 使用 `docker-compose port tidb 4000` 获得 TiDB 的对外服务端口。由于 Docker 做了端口转发, 你可能会获得一个类似 `0.0.0.0:32966` 的结果, 那么就可以通过 `32966` 端口访问 TiDB
+ 运行 `mysql -h 127.0.0.1 -P 32966 -u root -D test` 连接到 TiDB 进行测试
+ 运行 `docker-compose down` 关闭并销毁集群