# Build requirements

## Supported platforms

The following table lists TiDB support for common architectures and operating systems. 

|Architecture|Operating System|Status|
|------------|----------------|------|
|AMD64|Linux Ubuntu (14.04+)|Stable|
|AMD64|Linux CentOS (7+)|Stable|
|AMD64|Mac OSX|Experimental|

## Prerequisites

+ Go [1.9+](https://golang.org/doc/install)
+ Rust [nightly version](https://www.rust-lang.org/downloads.html)
+ GCC 4.8+ with static library
+ CMake 3.1+

The [check requirement script](../scripts/check_requirement.sh) can help you check prerequisites and 
install the missing ones automatically.


TiKV is well tested in a certain Rust version by us, and the exact version can be found in the `RUST_VERSION` file in TiKV's root directory. We recommend you to use the same version as we do. To set Rust version, execute following command in your TiKV project directory:

```bash
rustup override set nightly-2018-01-12  # For example if our current version is `nightly-2018-01-12`
cargo +nightly-2018-01-12 install rustfmt-nightly --version 0.3.4
```
