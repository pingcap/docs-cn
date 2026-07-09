#!/usr/bin/env python3
"""Resolve source files for the AI docs EN-to-ZH sync workflow."""

import argparse
import io
import re
import subprocess
import sys
import tarfile
from pathlib import PurePosixPath


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico"}
IMAGE_EXTENSION_PATTERN = r"\.(?:png|jpe?g|gif|svg|webp|bmp|ico)"
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_REFERENCE_IMAGE_RE = re.compile(r"!\[([^\]]+)\]\[([^\]]*)\]")
MARKDOWN_LINK_DEFINITION_RE = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(\S.*)$", re.MULTILINE)
IMAGE_DESTINATION_RE = re.compile(rf"^(.+?{IMAGE_EXTENSION_PATTERN}(?:[?#][^\s\"')>]*)?)", re.IGNORECASE)
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


def archive_ai_markdown_contents(repo_path, ref, source_folder):
    """Yield markdown files from source_folder at ref using one git subprocess."""
    try:
        archive_data = subprocess.check_output(
            ["git", "-C", repo_path, "archive", "--format=tar", ref, source_folder],
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return

    with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith(".md"):
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            yield member.name, extracted.read().decode("utf-8", errors="replace")


def is_ai_doc_path(path, source_folder, source_toc_file):
    return path == source_toc_file or path.startswith(f"{source_folder}/")


def normalize_reference_label(label):
    return " ".join(label.strip().lower().split())


def extract_image_destination(target):
    target = target.strip()
    if target.startswith("<"):
        return target[1:].split(">", 1)[0].strip()

    if is_image(target.split("#", 1)[0].split("?", 1)[0].strip()):
        return target

    match = IMAGE_DESTINATION_RE.match(target)
    return match.group(1).strip() if match else target.split()[0]


def normalize_image_ref(markdown_path, target):
    target = target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    target = extract_image_destination(target)
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
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


def images_from_markdown(markdown_path, content):
    images = set()
    for match in MARKDOWN_IMAGE_RE.finditer(content):
        image_path = normalize_image_ref(markdown_path, match.group(1))
        if image_path:
            images.add(image_path)
    for match in HTML_IMAGE_RE.finditer(content):
        image_path = normalize_image_ref(markdown_path, match.group(1))
        if image_path:
            images.add(image_path)

    reference_labels = {
        normalize_reference_label(match.group(2) or match.group(1))
        for match in MARKDOWN_REFERENCE_IMAGE_RE.finditer(content)
    }
    if reference_labels:
        for match in MARKDOWN_LINK_DEFINITION_RE.finditer(content):
            label = normalize_reference_label(match.group(1))
            if label not in reference_labels:
                continue
            image_path = normalize_image_ref(markdown_path, match.group(2))
            if image_path:
                images.add(image_path)
    return images


def referenced_images(repo_path, ref, source_folder):
    images = set()
    for markdown_path, content in archive_ai_markdown_contents(repo_path, ref, source_folder):
        images.update(images_from_markdown(markdown_path, content))
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
        elif is_image(path):
            # Manual image entries are treated as repo-relative paths. Markdown
            # entries without an explicit folder remain relative to source_folder.
            paths.append(path)
        else:
            paths.append(f"{source_folder}/{path}")
    return dedupe(paths)


def resolve_changed_files(repo_path, base_ref, head_ref, source_folder, source_toc_file):
    # A failed diff means the workflow cannot safely determine the sync scope, so
    # let the git error fail the step. Missing source folders at one side of the
    # range are handled inside archive_ai_markdown_contents() as empty content.
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
