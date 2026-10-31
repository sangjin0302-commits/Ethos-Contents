"""Validate optional writing/design sources without downloading or executing them."""
from __future__ import annotations

import argparse
import configparser
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCK = "vendor/writing-design/sources.json"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True,
        capture_output=True, text=True, encoding="utf-8", timeout=15,
    )
    return result.stdout.strip()


def local_path(root: Path, value: str) -> Path:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value:
        raise ValueError(f"Unsafe relative path: {value}")
    target = (root / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {value}")
    return target


def validate(root: Path = ROOT, require_checkout: bool = False) -> list[str]:
    """Return errors. An uninitialized optional checkout is allowed by default."""
    root = root.resolve()
    data = json.loads((root / LOCK).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported source lock schema")
    modules = configparser.ConfigParser(interpolation=None)
    modules.read(root / ".gitmodules", encoding="utf-8")
    errors: list[str] = []
    seen: set[str] = set()
    for source in data["sources"]:
        path, sha, url = source["path"], source["commit"], source["url"]
        checkout = local_path(root, path)
        if not path.startswith("vendor/") or path in seen:
            raise ValueError(f"Duplicate or non-vendor source: {path}")
        seen.add(path)
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ValueError(f"Source is not commit-pinned: {path}")
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", url):
            raise ValueError(f"Unexpected upstream URL: {path}")
        section = f'submodule "{path}"'
        if not modules.has_section(section):
            errors.append(f"Missing .gitmodules entry: {path}")
        elif modules[section].get("path") != path or modules[section].get("url") != url:
            errors.append(f"Submodule configuration differs: {path}")
        if git(root, "ls-files", "--stage", "--", path).split() != ["160000", sha, "0", path]:
            errors.append(f"Gitlink differs from pinned commit: {path}")
        initialized = (checkout / ".git").exists()
        if require_checkout and not initialized:
            errors.append(f"Uninitialized optional source: {path}")
        if initialized:
            if git(checkout, "rev-parse", "HEAD") != sha:
                errors.append(f"Checkout differs from pin: {path}")
            if not (checkout / "LICENSE").is_file():
                errors.append(f"Missing upstream license: {path}")
            for entry in source["entries"]:
                file = local_path(checkout, entry["path"])
                if not file.is_file():
                    errors.append(f"Missing upstream skill: {path}/{entry['path']}")
                    continue
                # Git normalizes checkout line endings (including Windows CRLF).
                digest = git(checkout, "hash-object", f"--path={entry['path']}", "--", str(file))
                if digest != entry["blob_sha"]:
                    errors.append(f"Upstream skill bytes changed: {path}/{entry['path']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-checkout", action="store_true", help="Also require initialized upstream files")
    args = parser.parse_args()
    try:
        errors = validate(require_checkout=args.require_checkout)
    except (OSError, ValueError, KeyError, configparser.Error, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        print("FAIL:\n" + "\n".join(errors))
        return 1
    scope = "pins and initialized files" if args.require_checkout else "pins; upstream execution not tested"
    print(f"PASS: writing/design sources ({scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
