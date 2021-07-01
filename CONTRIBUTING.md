# TiDB Documentation Contributing Guide

Welcome to [TiDB](https://github.com/pingcap/tidb) documentation! We are excited about the prospect of you joining [TiDB Community](https://github.com/pingcap/community/).

## What you can contribute

You can start from any one of the following items to help improve [TiDB Docs at the PingCAP website](https://docs.pingcap.com/tidb/stable):

- Fix typos or format (punctuation, space, indentation, code block, etc.)
- Fix or update inappropriate or outdated descriptions
- Add missing content (sentence, paragraph, or a new document)
- Translate docs changes from English to Chinese
- Submit, reply to, and resolve [docs issues](https://github.com/pingcap/docs/issues)
- (Advanced) Review Pull Requests created by others

## Before you contribute

Before you contribute, please take a quick look at some general information about TiDB documentation maintenance. This can help you to become a contributor soon.

### Get familiar with style

- [Commit Message Style](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
- [Pull Request Title Style](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
- [Markdown Rules](/resources/markdownlint-rules.md)
- [Code Comment Style](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
- Diagram Style: [Figma Quick Start Guide](https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md)

    To keep a consistent style for diagrams, we recommend using [Figma](https://www.figma.com/) to draw or design diagrams. If you need to draw a diagram, refer to the guide and use shapes or colors provided in the template.

### Learn about docs versions

Currently, we maintain six versions of TiDB documentation, each with a separate branch:

| Docs branch name | Version description |
| :--- | :--- |
| `master` branch | the latest development version |
| `release-5.1` branch | the 5.1 version |
| `release-5.0` branch | the 5.0 stable version |
| `release-4.0` branch | the 4.0 stable version |
| `release-3.1` branch | the 3.1 stable version |
| `release-3.0` branch | the 3.0 stable version |
| `release-2.1` branch | the 2.1 stable version |

> **Note:**
>
> Previously, we maintain all versions in the `master` branch, with directories like `dev` (the latest development version), `v3.0` and so on. Each docs version is updated very frequently and changes to one version often apply to another version or other versions as well.
>
> Since February 21, 2020, to reduce manual editing and updating work among versions, we have started to maintain each version in a separate branch and introduce sre-bot to automatically file PRs to other versions as long as you add corresponding cherry-pick labels to your PR.

### Use cherry-pick labels

- If your changes apply to only one docs version, just submit a PR to the corresponding version branch.

- If your changes apply to multiple docs versions, you don't have to submit a PR to each branch. Instead, after you submit your PR, trigger the sre-bot to submit a PR to other version branches by adding one or several of the following labels as needed. Once the current PR is merged, sre-bot will start to work.
    - `needs-cherry-pick-5.1` label: sre-bot will submit a PR to the `release-5.1` branch.
    - `needs-cherry-pick-5.0` label: sre-bot will submit a PR to the `release-5.0` branch.
    - `needs-cherry-pick-4.0` label: sre-bot will submit a PR to the `release-4.0` branch.
    - `needs-cherry-pick-3.1` label: sre-bot will submit a PR to the `release-3.1` branch.
    - `needs-cherry-pick-3.0` label: sre-bot will submit a PR to the `release-3.0` branch.
    - `needs-cherry-pick-2.1` label: sre-bot will submit a PR to the `release-2.1` branch.
    - `needs-cherry-pick-master` label: sre-bot will submit a PR to the `master` branch.

- If most of your changes apply to multiple docs versions but some differences exist among versions, you still can use cherry-pick labels to let sre-bot create PRs to other versions. After the PR to another version is successfully submitted by sre-bot, you can make changes to that PR.

## How to contribute

Please perform the following steps to create your Pull Request to this repository. If don't like to use commands, you can also use [GitHub Desktop](https://desktop.github.com/), which is easier to get started.

> **Note:**
>
> This section takes creating a PR to the `master` branch as an example. Steps of creating PRs to other branches are similar.

### Step 0: Sign the CLA

Your Pull Requests can only be merged after you sign the [Contributor License Agreement](https://cla-assistant.io/pingcap/docs) (CLA). Please make sure you sign the CLA before continuing.

### Step 1: Fork the repository

1. Visit the project: <https://github.com/pingcap/docs>
2. Click the **Fork** button on the top right and wait it to finish.

### Step 2: Clone the forked repository to local storage

```
cd $working_dir # Comes to the directory that you want put the fork in, for example, "cd ~/Documents/GitHub"
git clone git@github.com:$user/docs.git # Replace "$user" with your GitHub ID

cd $working_dir/docs
git remote add upstream git@github.com:pingcap/docs.git # Adds the upstream repo
git remote -v # Confirms that your remote makes sense
```

### Step 3: Create a new branch

1. Get your local master up-to-date with upstream/master.

    ```
    cd $working_dir/docs
    git fetch upstream
    git checkout master
    git rebase upstream/master
    ```

2. Create a new branch based on the master branch.

    ```
    git checkout -b new-branch-name
    ```

### Step 4: Do something

Edit some file(s) on the `new-branch-name` branch and save your changes. You can use editors like Visual Studio Code to open and edit `.md` files.

### Step 5: Commit your changes

```
git status # Checks the local status
git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add.`
git commit -m "commit-message: update the xx"
```

See [Commit Message Style](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message).

### Step 6: Keep your branch in sync with upstream/master

```
# While on your new branch
git fetch upstream
git rebase upstream/master
```

### Step 7: Push your changes to the remote

```
git push -u origin new-branch-name # "-u" is used to track the remote branch from origin
```

### Step 8: Create a pull request

1. Visit your fork at <https://github.com/$user/docs> (replace `$user` with your GitHub ID)
2. Click the `Compare & pull request` button next to your `new-branch-name` branch to create your PR. See [Pull Request Title Style](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style).

Now, your PR is successfully submitted! After this PR is merged, you will automatically become a contributor to TiDB documentation.

## Contact

Join the Slack channel: [#sig-docs](https://slack.tidb.io/invite?team=tidb-community&channel=sig-docs&ref=pingcap-docs)
