#!/bin/python3
# https://github.com/pingcap/docs/pull/13016
import re
import sys
import logging
from pathlib import Path
from glob import iglob

import requests

logging.basicConfig(level=logging.INFO)
urls: dict[str, bool] = {}


def validate_url(url: str) -> bool:
    url = re.sub(
        "https://dev.mysql.com/doc/refman/5\.[67]/",
        "https://dev.mysql.com/doc/refman/8.0/",
        url,
    )

    if url in urls:
        return urls[url]

    r = requests.get(url)
    if r.status_code == 200:
        urls[url] = True
    else:
        logging.warning("Got HTTP status code %s for %s", r.status_code, url)
        urls[url] = False
    return urls[url]


def update_file(filename: str) -> None:
    with open(filename, "r+") as fh:
        content = fh.read()
        # Look for reference manual urls and stop at:
        # - the end of the url target `)`
        # - the end of the url text `]`
        # - at an anchor `#`
        for m in re.findall(
            "https://dev.mysql.com/doc/refman/5\.[67]/[^#\])]*", content
        ):
            validate_url(m)
        newcontent = re.sub(
            "https://dev.mysql.com/doc/refman/5\.[67]/",
            "https://dev.mysql.com/doc/refman/8.0/",
            content,
        )
        newcontent = re.sub(
            "(https://dev.mysql.com/doc/refman)/8\.0/(.*available in MySQL 5.7)",
            r"\1/5.7/\2",
            newcontent,
        )
        for m in re.findall(
            "https://dev.mysql.com/doc/refman/8\.0/[^#\])]*", content
        ):
            validate_url(m)
        fh.seek(0)
        fh.truncate()
        fh.write(newcontent)


if Path().cwd().name != "docs":
    print("Please run this from the root of the docs repo.")
    sys.exit(1)

for f in iglob("**/*.md", recursive=True):
    # Skip updating release notes
    if f.startswith("releases/"):
        continue
    update_file(f)
