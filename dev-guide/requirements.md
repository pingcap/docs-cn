# Build requirements

## Supported platforms

The following table lists TiDB support for common architectures and operating systems. 

|Architecture|Operating System|Status|
|------------|----------------|------|
|AMD64|Linux Ubuntu (14.04+)|Stable|
|AMD64|Linux CentOS (7+)|Stable|
|AMD64|Mac OSX|Experimental|

## Prerequisites

+ Go [1.5+](https://golang.org/doc/install)
+ Rust [nightly version](https://www.rust-lang.org/downloads.html)
+ GCC 4.8+ with static library

The [check requirement script](../scripts/check_requirement.sh) can help you check prerequisites and 
install the missing ones automatically.

## Building and installing TiDB components

You can use the [build script](../scripts/build.sh) to build and install TiDB components in the `bin` directory.

You can use the [update script](../scripts/update.sh) to update all the TiDB components to the latest version.
