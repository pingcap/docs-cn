#!/usr/bin/env python3
"""Resolve source files for the AI docs EN-to-ZH sync workflow."""

import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico"}
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)


def is_image(path):
    return PurePosixPath(path).suffix.lower() in IMAGE_EXTENSIONS


def dedupe(paths):
    result = []
    seen = set()
    for path in paths:
        if path and path not in seen:
            result.append(path)
            seen.add(path)
    return result


def run_git(repo_path, *args):
    return subprocess.check_output(["git", "-C", repo_path, *args], text=True)


def git_show(repo_path, ref, path):
    try:
        return subprocess.check_output(
            ["git", "-C", repo_path, "show", f"{ref}:{path}"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return ""


def list_ai_markdown(repo_path, ref, source_folder):
    try:
        output = run_git(repo_path, "ls-tree", "-r", "--name-only", ref, "--", source_folder)
    except subprocess.CalledProcessError:
        return []
    return [path for path in output.splitlines() if path.endswith(".md")]


def is_ai_doc_path(path, source_folder, source_toc_file):
    return path == source_toc_file or path.startswith(f"{source_folder}/")


def normalize_image_ref(markdown_path, target):
    target = target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    if target.startswith("<"):
        target = target[1:].split(">", 1)[0].strip()
    else:
        target = target.split()[0]
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not target:
        return None

    if target.startswith("/"):
        candidate = target.lstrip("/")
    else:
        candidate = str(PurePosixPath(markdown_path).parent.joinpath(target))

    parts = []
    for part in PurePosixPath(candidate).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)

    normalized = "/".join(parts)
    return normalized if normalized and is_image(normalized) else None


def referenced_images(repo_path, ref, source_folder):
    images = set()
    for markdown_path in list_ai_markdown(repo_path, ref, source_folder):
        content = git_show(repo_path, ref, markdown_path)
        for match in MARKDOWN_IMAGE_RE.finditer(content):
            image_path = normalize_image_ref(markdown_path, match.group(1))
            if image_path:
                images.add(image_path)
        for match in HTML_IMAGE_RE.finditer(content):
            image_path = normalize_image_ref(markdown_path, match.group(1))
            if image_path:
                images.add(image_path)
    return images


def normalize_requested_files(input_file_names, source_folder, source_toc_file):
    paths = []
    for item in input_file_names.split(","):
        path = item.strip().lstrip("/")
        if path.startswith("./"):
            path = path[2:]
        if path.startswith("docs/"):
            path = path[5:]
        if not path:
            continue

        if is_ai_doc_path(path, source_folder, source_toc_file):
            paths.append(path)
        elif "/" in path and is_image(path):
            paths.append(path)
        else:
            paths.append(f"{source_folder}/{path}")
    return dedupe(paths)


def resolve_changed_files(repo_path, base_ref, head_ref, source_folder, source_toc_file):
    changed_files = run_git(repo_path, "diff", "--name-only", "-M", base_ref, head_ref).splitlines()
    paths = [
        path
        for path in changed_files
        if is_ai_doc_path(path, source_folder, source_toc_file)
    ]

    changed_images = [path for path in changed_files if is_image(path)]
    if not changed_images:
        return dedupe(paths)

    referenced = referenced_images(repo_path, base_ref, source_folder)
    referenced.update(referenced_images(repo_path, head_ref, source_folder))

    for path in changed_images:
        if not is_ai_doc_path(path, source_folder, source_toc_file) and path in referenced:
            paths.append(path)
            print(f"Including referenced image change: {path}", file=sys.stderr)
    return dedupe(paths)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-source-path", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--source-folder", required=True)
    parser.add_argument("--source-toc-file", required=True)
    parser.add_argument("--input-file-names", default="")
    return parser.parse_args()


def main():
    args = parse_args()
    source_folder = args.source_folder.strip("/")
    if args.input_file_names.strip():
        paths = normalize_requested_files(
            args.input_file_names,
            source_folder,
            args.source_toc_file,
        )
    else:
        paths = resolve_changed_files(
            args.docs_source_path,
            args.base_ref,
            args.head_ref,
            source_folder,
            args.source_toc_file,
        )
    print(",".join(paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
