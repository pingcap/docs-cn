#!/bin/python3
import glob
import subprocess

allowlist = {
    "_index.md",
    "TOC.md",
}

for mdfile in glob.iglob("**/*.md", recursive=True):
    if mdfile.startswith("node_modules/"):
        continue

    # There are quite a few dangling documents in the benchmarks,
    # but those are more likely to be referenced from outside of the docs
    # and might have historical relevance
    if mdfile.startswith("benchmark/"):
        continue

    if mdfile in allowlist:
        continue

    p = subprocess.run(
        ["git", "grep", "-l", f"/{mdfile}"], capture_output=True, encoding="utf-8"
    )
    if p.stdout == "":
        print(f"File {mdfile} has NO matches")
