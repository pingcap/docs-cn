#!/bin/python3
import re
import sys
from pathlib import Path

parser = Path("../tidb/pkg/parser/parser.y")
if not parser.exists():
    sys.exit(f"{parser} doesn't exist")

kwdocs = Path("keywords.md")
if not kwdocs.exists():
    sys.exit(f"{kwdocs} doesn't exist")

keywords = kwdocs.read_text()

errors = 0
section = "Unknown"
for line in parser.read_text().split("\n"):
    if line.find("The following tokens belong to ReservedKeyword") >= 0:
        section = "ReservedKeyword"

    if line.find("The following tokens belong to UnReservedKeyword") >= 0:
        section = "UnReservedKeyword"

    if line.find("The following tokens belong to NotKeywordToken") >= 0:
        section = "NotKeywordToken"

    if section == "ReservedKeyword":
        if m := re.match(r'^\t\w+\s+"(\w+)"$', line):
            kw = m.groups()[0]
            if not (
                kwm := re.search(f"^- {kw} \((R|R-Window)\)$", keywords, re.MULTILINE)
            ):
                if kwm := re.search(f"^- {kw}$", keywords, re.MULTILINE):
                    print(f"Keyword not labeled as reserved: {kw}")
                    errors += 1
                else:
                    print(f"Missing docs for reserved keyword: {kw}")
                    errors += 1

    if section == "UnReservedKeyword":
        if m := re.match(r'^\t\w+\s+"(\w+)"$', line):
            kw = m.groups()[0]
            if not (kwm := re.search(f"^- {kw}$", keywords, re.MULTILINE)):
                print(f"Missing docs for non-reserved keyword: {kw}")
                errors += 1

sys.exit(errors)
