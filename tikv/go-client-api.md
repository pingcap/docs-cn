---
title: Try Two Types of APIs
category: user guide
---

# Try Two Types of APIs

To apply to different scenarios, TiKV provides [two types of APIs](tikv-overview.md#two-types-of-apis) for developers: the Raw Key-Value API and the Transactional Key-Value API. This document guides you through how to use the two APIs in TiKV using two examples.

The usage examples are based on the [deployment of TiKV using binary files on multiple nodes for test](deploy-tikv-using-binary.md#deploy-the-tikv-cluster-on-multiple-nodes-for-test). You can also quickly try the two types of APIs on a single machine.

## Try the Raw Key-Value API

To use the Raw Key-Value API in applications developed by golang, take the following steps:

1. Install the necessary packages.

    ```bash
    go get -v -u github.com/pingcap/tidb/store/tikv
    ```

2. Import the dependency packages.

    ```bash
    import (
        "fmt"
        "github.com/pingcap/tidb/config"
        "github.com/pingcap/tidb/store/tikv"
    )
    ```

3. Create a Raw Key-Value client.

    ```bash
    cli, err := tikv.NewRawKVClient([]string{"192.168.199.113:2379"}, config.Security{})
    ```

    Description of two parameters in the above command:

    - `string`: a list of PD servers’ addresses
    - `config.Security`: used for establishing TLS connections, usually left empty when you do not need TLS

4. Call the Raw Key-Value client methods to access the data on TiKV. The Raw Key-Value API contains the following methods, and you can also find them at [GoDoc](https://godoc.org/github.com/pingcap/tidb/store/tikv#RawKVClient).

    ```bash
    type RawKVClient struct
    func (c *RawKVClient) Close() error
    func (c *RawKVClient) ClusterID() uint64
    func (c *RawKVClient) Delete(key []byte) error
    func (c *RawKVClient) Get(key []byte) ([]byte, error)
    func (c *RawKVClient) Put(key, value []byte) error
    func (c *RawKVClient) Scan(startKey []byte, limit int) (keys [][]byte, values [][]byte, err error)
    ```

### Usage example of the Raw Key-Value API

```bash
package main

import (
    "fmt"

    "github.com/pingcap/tidb/config"
    "github.com/pingcap/tidb/store/tikv"
)

func main() {
    cli, err := tikv.NewRawKVClient([]string{"192.168.199.113:2379"}, config.Security{})
    if err != nil {
        panic(err)
    }
    defer cli.Close()

    fmt.Printf("cluster ID: %d\n", cli.ClusterID())

    key := []byte("Company")
    val := []byte("PingCAP")

    // put key into tikv
    err = cli.Put(key, val)
    if err != nil {
        panic(err)
    }
    fmt.Printf("Successfully put %s:%s to tikv\n", key, val)

    // get key from tikv
    val, err = cli.Get(key)
    if err != nil {
        panic(err)
    }
    fmt.Printf("found val: %s for key: %s\n", val, key)

    // delete key from tikv
    err = cli.Delete(key)
    if err != nil {
        panic(err)
    }
    fmt.Printf("key: %s deleted\n", key)

    // get key again from tikv
    val, err = cli.Get(key)
    if err != nil {
        panic(err)
    }
    fmt.Printf("found val: %s for key: %s\n", val, key)
}
```

The result is like:

```bash
INFO[0000] [pd] create pd client with endpoints [192.168.199.113:2379]
INFO[0000] [pd] leader switches to: http://127.0.0.1:2379, previous:
INFO[0000] [pd] init cluster id 6554145799874853483
cluster ID: 6554145799874853483
Successfully put Company:PingCAP to tikv
found val: PingCAP for key: Company
key: Company deleted
found val:  for key: Company
```

RawKVClient is a client of the TiKV server and only supports the GET/PUT/DELETE/SCAN commands. The RawKVClient can be safely and concurrently accessed by multiple goroutines, as long as it is not closed. Therefore, for one process, one client is enough generally.

## Try the Transactional Key-Value API

The Transactional Key-Value API is complicated than the Raw Key-Value API. Some transaction related concepts are listed as follows. For more details, see the [KV package](https://github.com/pingcap/tidb/tree/master/kv).

- Storage
    
    Like the RawKVClient, a Storage is an abstract TiKV cluster.

- Snapshot

    A Snapshot is the state of a Storage at a particular point of time, which provides some readonly methods. The multiple times read from a same Snapshot is guaranteed consistent.

- Transaction

    Like the Transaction in SQL, a Transaction symbolizes a series of read and write operations performed within the Storage. Internally, a Transaction consists of a Snapshot for reads, and a MemBuffer for all writes. The default isolation level of a Transaction is Snapshot Isolation.

To use the Transactional Key-Value API in applications developed by golang, take the following steps:

1. Install the necessary packages.

    ```bash
    go get -v -u github.com/pingcap/tidb/kv
    go get -v -u github.com/pingcap/tidb/store/tikv
    ```

2. Import the dependency packages.

    ```bash
    import (
        "github.com/pingcap/tidb/kv"
        "github.com/pingcap/tidb/store/tikv"
        "fmt"
    )
    ```

3. Create Storage using a URL scheme.

    ```bash
    driver := tikv.Driver{}
    storage, err := driver.Open("tikv://192.168.199.113:2379")
    ```

4. (Optional) Modify the Storage using a Transaction.

    The lifecycle of a Transaction is: _begin → {get, set, delete, scan} → {commit, rollback}_.

5. Call the Transactional Key-Value API's methods to access the data on TiKV. The Transactional Key-Value API contains the following methods:

    ```bash
    Begin() -> Txn
    Txn.Get(key []byte) -> (value []byte)
    Txn.Set(key []byte, value []byte)
    Txn.Seek(begin []byte) -> Iterator
    Txn.Delete(key []byte)
    Txn.Commit()
    ```

### Usage example of the Transactional Key-Value API

```bash
package main

import (
    "context"
    "fmt"
    "strconv"

    "github.com/pingcap/tidb/kv"
    "github.com/pingcap/tidb/store/tikv"
)

// if key not found, set value to zero
// else increase the value
func increase(storage kv.Storage, key []byte) error {
    txn, err := storage.Begin()
    if err != nil {
        return err
    }
    defer txn.Rollback()
    var oldValue int
    val, err := txn.Get(key)
    if err != nil {
        if !kv.ErrNotExist.Equal(err) {
            return err
        }
    } else {
        oldValue, err = strconv.Atoi(string(val))
        if err != nil {
            return err
        }
    }

    err = txn.Set(key, []byte(strconv.Itoa(oldValue+1)))
    if err != nil {
        return err
    }
    err = txn.Commit(context.Background())
    return nil
}

// lookup value for key
func lookup(storage kv.Storage, key []byte) (int, error) {
    var value int
    txn, err := storage.Begin()
    if err != nil {
        return value, err
    }
    defer txn.Rollback()
    val, err := txn.Get(key)
    if err != nil {
        return value, err
    }
    value, err = strconv.Atoi(string(val))
    if err != nil {
        return value, err
    }
    return value, nil
}

func main() {
    driver := tikv.Driver{}
    storage, err := driver.Open("tikv://192.168.199.113:2379")
    if err != nil {
        panic(err)
    }
    defer storage.Close()

    key := []byte("Account")
    // lookup account
    account, err := lookup(storage, key)
    if err != nil {
        fmt.Printf("failed to lookup key %s: %v\n", key, err)
    } else {
        fmt.Printf("Account is %d\n", account)
    }

    // increase account
    err = increase(storage, key)
    if err != nil {
        panic(err)
    }

    // lookup account again
    account, err = lookup(storage, key)
    if err != nil {
        fmt.Printf("failed to lookup key %s: %v\n", key, err)
    } else {
        fmt.Printf("Account increased to %d\n", account)
    }
}
```

The result is like:

```bash
INFO[0000] [pd] create pd client with endpoints [192.168.199.113:2379]
INFO[0000] [pd] leader switches to: http://127.0.0.1:2379, previous:
INFO[0000] [pd] init cluster id 6554145799874853483
INFO[0000] [kv] Rollback txn 400197262324006914
failed to lookup key Account: [kv:2]Error: key not exist
INFO[0000] [kv] Rollback txn 400197262324006917
Account increased to 1

# run the program again
INFO[0000] [pd] create pd client with endpoints [192.168.199.113:2379]
INFO[0000] [pd] leader switches to: http://127.0.0.1:2379, previous:
INFO[0000] [pd] init cluster id 6554145799874853483
INFO[0000] [kv] Rollback txn 400198364324954114
Account is 1
INFO[0000] [kv] Rollback txn 400198364324954117
Account increased to  2
```