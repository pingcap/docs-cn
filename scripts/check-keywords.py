#!/bin/python3
import argparse
from http.client import IncompleteRead
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

aparser = argparse.ArgumentParser()
aparser.add_argument(
    "--parser_file", default="../tidb/pkg/parser/parser.y", help="Path to parser.y"
)
aparser.add_argument(
    "--parser_url",
    default="https://github.com/pingcap/tidb/raw/refs/heads/master/pkg/parser/parser.y",
    help="URL to parser.y",
)
aparser.add_argument("--download_from_url", action="store_true")
args = aparser.parse_args()

if args.download_from_url:
    try:
        print(f"Fetching {args.parser_url}")
        with urlopen(args.parser_url, timeout=30) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            lines = response.read().decode(encoding).splitlines()
    except (
        HTTPError,
        URLError,
        TimeoutError,
        ConnectionError,
        IncompleteRead,
        UnicodeError,
        LookupError,
    ) as e:
        sys.exit(f"Failed to download parser file: {e}")
else:
    parser = Path(args.parser_file)
    if not parser.exists():
        sys.exit(f"{parser} doesn't exist")
    lines = parser.read_text(encoding="utf-8").splitlines()

kwdocs = Path("keywords.md")
if not kwdocs.exists():
    sys.exit(f"{kwdocs} doesn't exist")

keywords = kwdocs.read_text()

errors = 0
section = "Unknown"
for line in lines:
    if line == "":
        section = "NotKeywordToken"

    elif line.find("The following tokens belong to ReservedKeyword") >= 0:
        section = "ReservedKeyword"

    elif line.find("The following tokens belong to UnReservedKeyword") >= 0:
        section = "UnReservedKeyword"

    elif line.find("The following tokens belong to TiDBKeyword") >= 0:
        section = "TiDBKeyword"

    elif line.find("The following tokens belong to NotKeywordToken") >= 0:
        section = "NotKeywordToken"

    if section == "ReservedKeyword":
        if m := re.match(r'^\t\w+\s+"(\w+)"$', line):
            kw = m.groups()[0]
            if not (
                kwm := re.search(f"^- {kw} \\((R|R-Window)\\)$", keywords, re.MULTILINE)
            ):
                if kwm := re.search(f"^- {kw}$", keywords, re.MULTILINE):
                    print(f"Reserved keyword not labeled as reserved: {kw}")
                else:
                    print(f"Missing docs for reserved keyword: {kw}")
                errors += 1

    if section in ["UnReservedKeyword", "TiDBKeyword"]:
        if m := re.match(r'^\t\w+\s+"(\w+)"$', line):
            kw = m.groups()[0]
            if not (kwm := re.search(f"^- {kw}$", keywords, re.MULTILINE)):
                if kwm := re.search(
                    f"^- {kw} \\((R|R-Window)\\)$", keywords, re.MULTILINE
                ):
                    print(
                        f"Non-reserved keyword from {section} labeled as reserved: {kw}"
                    )
                else:
                    print(f"Missing docs for non-reserved keyword from {section}: {kw}")
                errors += 1

sys.exit(1 if errors else 0)
