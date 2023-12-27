# TiDB Documentation Contributing Guide

Welcome to [TiDB](https://github.com/pingcap/tidb) documentation! We are excited about the prospect of you joining [TiDB Community](https://github.com/pingcap/community/).

## What you can contribute

🚀 To provide you with better TiDB documentation, we sincerely invite you to participate in the [2024 TiDB Docs Dash](https://www.pingcap.com/event/tidb-docs-dash/). In this event, you'll have a chance to work with other members of the community while making a meaningful impact on [TiDB documentation](https://docs.pingcap.com/tidb/stable/) and [TiDB Cloud documentation](https://docs.pingcap.com/tidbcloud/).

- **Dates/Time:** January 9 at 08:00 UTC ([your local time](https://www.timeanddate.com/worldclock/fixedtime.html?msg=TiDB+Docs+Dash+2024%3A+Start&iso=20240109T08&p1=1440))  – January 12 at 07:59 UTC ([your local time](https://www.timeanddate.com/worldclock/fixedtime.html?msg=TiDB+Docs+Dash+2024%3A+End&iso=20240112T0759&p1=1440))
- **Event details**: <https://www.pingcap.com/event/tidb-docs-dash/>
- **Issue list**: <https://github.com/orgs/pingcap/projects/51/views/3>
- **Participation introduction**: <https://github.com/pingcap/docs/issues/15479>

In addition to the issues and tasks in the event, you can also start from any one of the following items to help improve [TiDB Docs at the PingCAP website](https://docs.pingcap.com/tidb/stable):

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

### Pick a doc template

If you are going to create a new document for TiDB, we provide [several doc templates](/resources/doc-templates) for you to use to align with our style.

Please check out these templates before you submit a pull request:

- [Concept](/resources/doc-templates/template-concept.md)
- [Task](/resources/doc-templates/template-task.md)
- [Reference](/resources/doc-templates/template-reference.md)
- [New Feature](/resources/doc-templates/template-new-feature.md)
- [Troubleshooting](/resources/doc-templates/template-troubleshooting.md)

### Learn about docs versions

We use separate branches to maintain different versions of TiDB documentation.

- The [documentation under development](https://docs.pingcap.com/tidb/dev) is maintained in the `master` branch.
- The [published documentation](https://docs.pingcap.com/tidb/stable/) is maintained in the corresponding `release-<verion>` branch. For example, TiDB v7.5 documentation is maintained in the `release-7.5` branch.
- The [archived documentation](https://docs-archive.pingcap.com/) is no longer maintained and does not receive any further updates.

### Use cherry-pick labels

As changes to one documentation version often apply to other documentation versions as well, we introduce [ti-chi-bot](https://github.com/ti-chi-bot) to automate the PR cherry-pick process based on cherry-pick labels.

- If your changes only apply to a specific documentation version, just create a PR based on the branch of that documentation version. There is no need to add any cherry-pick labels.

- If your changes apply to multiple documentation versions, instead of creating multiple PRs, you can just create one PR based on the latest applicable branch (such as `master`), and then add one or several `needs-cherry-pick-release-<version>` labels to the PR according to the applicable documentation versions. Then, after the PR is merged, ti-chi-bot will automatically create the corresponding cherry-pick PRs based on the branches of the specified versions.

- If most of your changes apply to multiple documentation versions but some differences exist among versions, in addition to the cherry-pick labels for all the target versions, you also need to add the `requires-version-specific-change` label as a reminder to the PR reviewer. After your PR is merged and ti-chi-bot creates the corresponding cherry-pick PRs, you can still make changes to these cherry-pick PRs.

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

## Guideline for choosing the affected version(s)

When you create a Pull Request, you need to choose the release version to which your document change applies in the description template on your Pull Request page.

If your change fits one of the following situations, it is recommended to **CHOOSE THE MASTER BRANCH ONLY**. After the PR is merged, the change will be soon displayed on the [Dev page of the PingCAP documentation website](https://docs.pingcap.com/tidb/dev/). After the next major or minor version of TiDB is released, the change will also be displayed on the website page for the new version.

- Relates to a documentation enhancement, such as supplementing missing or incomplete document contents.
- Fixes inaccurate or incorrect document contents, including values, descriptions, examples, or typos.
- Involves a documentation refactor in a specific topic module.

If your change fits one of the following situations, **CHOOSE THE AFFECTED RELEASE BRANCH(ES) AND MASTER**:

- Involves a feature behavior change that relates to a specific version.
- Involves a compatibility change, including changing the default value of a configuration item or a system variable.
- Fixes format to resolve a display error
- Fixes broken links

## Contact

Join [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) for discussion.
