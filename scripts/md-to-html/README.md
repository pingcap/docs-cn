In the repo root dir, run the following command to generate `.build/full-doc.md`:

```shell
python3 scripts/md-to-html/merge_by_toc.py
```

And then open `.build/full-doc.md`. Search all `---\n\ntitle` and replace them with `---\ntitle`

Next, generate doc by running the following commands

```shell
./scripts/md-to-html/prepare.sh
python3 scripts/md-to-html/fix_gfm_doc.py
./scripts/md-to-html/generate.sh
```

**About Heading ID**

> https://learn.microsoft.com/en-us/contribute/content/how-to-write-links#explicit-anchor-links
