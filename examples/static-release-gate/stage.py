#!/usr/bin/env python3
"""Educational, no-dependencies example of a fail-closed static release gate.

Publishes ONLY paths declared in a manifest. No network, CI token or real private
project is required. Intended as inspectable code for a public DevOps portfolio.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path, PurePosixPath

FORBIDDEN_NAMES = {
    ".env", ".git", ".github", "id_rsa", "package-lock.json",
    "credentials.json", "secret.json", "README.md", "CLAUDE.md",
}
SENSITIVE_CONTENT = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?:sk_live|rk_live|whsec)_[A-Za-z0-9]{12,}"),
    re.compile(rb"ghp_[A-Za-z0-9]{20,}"),
)
MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL = 8 * 1024 * 1024
ALLOWED_SUFFIXES = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg"}


def validate_path(value: str) -> PurePosixPath:
    if "\\" in value or "\x00" in value:
        raise ValueError("Unsupported separators or NUL in asset path")
    path = PurePosixPath(value)
    if (
        not value or value.startswith("/") or
        any(part in {"..", "."} for part in value.split("/")) or
        any(part.startswith(".") for part in path.parts) or
        any(part in FORBIDDEN_NAMES for part in path.parts) or
        path.suffix.lower() not in ALLOWED_SUFFIXES
    ):
        raise ValueError("Unsafe or disallowed public path: " + value)
    return path


def stage_public(source: Path, destination: Path, manifest: list[str]) -> int:
    source = Path(source).resolve()
    destination = Path(destination).absolute()
    if destination == source or source in destination.parents and destination.name != "dist":
        # Only the specific output subdirectory "dist" may live under source.
        raise ValueError("Output must be separate from source (or source/dist)")
    if not isinstance(manifest, list) or not manifest or len(manifest) != len(set(manifest)):
        raise ValueError("Manifest must contain unique paths")
    entries: list[tuple[PurePosixPath, bytes]] = []
    total = 0
    for name in manifest:
        if not isinstance(name, str):
            raise ValueError("Manifest entries must be strings")
        relative = validate_path(name)
        current = source
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Symlink is not publishable: " + name)
        if not current.is_file():
            raise FileNotFoundError("Missing declared public file: " + name)
        if current.stat().st_size > MAX_FILE:
            raise ValueError("File exceeds asset budget: " + name)
        contents = current.read_bytes()
        if any(pattern.search(contents) for pattern in SENSITIVE_CONTENT):
            raise ValueError("Credential-like content in " + name)
        total += len(contents)
        if total > MAX_TOTAL:
            raise ValueError("Bundle exceeds release size limit")
        entries.append((relative, contents))

    # Construct a complete, audited output from scratch. Never copy a directory.
    if destination.exists():
        if destination.is_symlink() or not destination.is_dir():
            raise ValueError("Unsafe existing output directory")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for relative, contents in entries:
        file = destination.joinpath(*relative.parts)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(contents)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage only explicitly public files")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("assets", nargs="+", help="explicit asset paths (never a folder)")
    args = parser.parse_args()
    size = stage_public(args.source, args.destination, args.assets)
    print(f"PASS: {len(args.assets)} public assets staged ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
