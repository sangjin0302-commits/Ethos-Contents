#!/usr/bin/env python3
"""Consent-bound push requests; publish separate results, never edit manuscripts."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

try:
    from scripts import human_proofreader_mcp as hp
except ImportError:
    import human_proofreader_mcp as hp

BRANCH_PREFIX = "proofreader/request/"
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{2,63}\Z")
SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
ROOT_KEYS = {"version", "request_id", "base_commit", "source_sha256", "consent", "mode", "genre", "depth", "preserve", "instructions"}
CONSENT_KEYS = {"public_repository", "external_processing", "no_private_data", "authorization"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request_id(branch: str) -> str:
    if not branch.startswith(BRANCH_PREFIX):
        raise ValueError("Only proofreader/request/<id> branches may execute requests")
    value = branch[len(BRANCH_PREFIX):]
    if not ID_PATTERN.fullmatch(value):
        raise ValueError("Invalid request id")
    return value


def safe_read(root: Path, relative: Path, limit: int) -> bytes:
    """No symlinks, traversal, huge files or directory substitutions."""
    path = root
    for part in relative.parts:
        if part in ("..", "."):
            raise ValueError("Unsafe path")
        path /= part
        if path.is_symlink():
            raise ValueError("Symlinks are not request inputs")
    if not path.is_file() or path.stat().st_size > limit:
        raise ValueError("Missing or oversized request input")
    return path.read_bytes()


def load_request(root: Path, branch: str) -> tuple[dict, str, bytes]:
    rid = request_id(branch)
    folder = Path("_proofreader/requests") / rid
    raw = safe_read(root, folder / "request.json", 40_000)
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) - ROOT_KEYS:
        raise ValueError("Unknown request fields")
    if type(data.get("version")) is not int or data["version"] != 1 or data.get("request_id") != rid:
        raise ValueError("Request version/id mismatch")
    if not SHA_PATTERN.fullmatch(str(data.get("base_commit", ""))):
        raise ValueError("An exact base commit is required")
    consent = data.get("consent")
    if not isinstance(consent, dict) or set(consent) != CONSENT_KEYS:
        raise ValueError("Explicit public-repository and external-processing consent is required")
    if any(consent.get(key) is not True for key in CONSENT_KEYS - {"authorization"}):
        raise ValueError("Consent must be literal true, not a string or inferred value")
    if not isinstance(consent.get("authorization"), str) or not 1 <= len(consent["authorization"].strip()) <= 1000:
        raise ValueError("Record the user's authorization without private details")
    if data.get("mode") not in ("readability", "read_through", "proofread"):
        raise ValueError("Unsupported mode")
    if data.get("genre", "블로그") not in ("칼럼", "리포트", "블로그", "뉴스레터", "공적", "에세이", "자동"):
        raise ValueError("Unsupported genre")
    if data.get("depth", "standard") not in ("light", "standard"):
        raise ValueError("Request bridge supports light or standard only")
    text_bytes = safe_read(root, folder / "source.md", 80_000)
    if sha256(text_bytes) != data.get("source_sha256"):
        raise ValueError("Source SHA-256 mismatch: do not transmit a changed manuscript")
    text = text_bytes.decode("utf-8")
    if not text.strip() or len(text.encode("utf-16-le")) // 2 > 20_000:
        raise ValueError("Source must contain 1..20000 UTF-16 code units")
    protected = data.get("preserve", [])
    if not isinstance(protected, list) or len(protected) > 100 or any(
        not isinstance(p, str) or not p or len(p) > 2000 or p not in text for p in protected
    ):
        raise ValueError("Every preservation string must exist in this exact source")
    if len(set(protected)) != len(protected):
        raise ValueError("Duplicate preservation strings")
    if not isinstance(data.get("instructions", ""), str) or len(data.get("instructions", "")) > 4000:
        raise ValueError("Instructions must be a string of at most 4000 characters")
    return data, text, raw


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8").strip()


def verify_tree(root: Path, data: dict, commit: str) -> None:
    if not SHA_PATTERN.fullmatch(commit) or git(root, "rev-parse", "HEAD") != commit:
        raise ValueError("Checkout does not match the triggering commit")
    git(root, "merge-base", "--is-ancestor", data["base_commit"], "origin/main")
    folder = f"_proofreader/requests/{data['request_id']}/"
    changed = set(git(root, "diff", "--name-only", data["base_commit"], commit).splitlines())
    if changed != {folder + "source.md", folder + "request.json"}:
        raise ValueError("A request commit may change only its source.md and request.json")


def process(root: Path, branch: str, commit: str, run_url: str, verify: bool = True) -> dict:
    rid = request_id(branch)
    result = root / "_proofreader/results" / rid
    if result.exists() or result.is_symlink() or (root / "_proofreader").is_symlink() or (root / "_proofreader/results").is_symlink():
        raise ValueError("Results already exist or the output path is unsafe; use a new request id")
    result.mkdir(parents=True)
    summary = {"version": 1, "request_id": rid, "request_commit": commit,
               "run_url": run_url, "status": "invalid_request", "external_attempted": False,
               "publication_approved": False, "semantic_review": "pending",
               "completed_at_utc": None}
    source = None
    try:
        data, text, raw = load_request(root, branch)
        if verify:
            verify_tree(root, data, commit)
        if os.environ.get("ETHOS_UPSTAGE_API_KEY") or os.environ.get("ETHOS_OPENROUTER_API_KEY"):
            raise ValueError("Request workflow never uses personal paid API keys")
        source = root / "_proofreader/requests" / rid / "source.md"
        summary.update(source_sha256=data["source_sha256"], request_sha256=sha256(raw), input_chars=len(text), mode=data["mode"])
        (result / "original.md").write_bytes(source.read_bytes())
        args = {"text": text}
        if data["mode"] != "readability":
            args["genre"] = data.get("genre", "블로그")
        if data["mode"] == "proofread":
            args.update(strength="보수", depth=data.get("depth", "standard"),
                        audience="한국어 비전문가 독자", preserve=data.get("preserve", []),
                        instructions="주체·의무/재량·조건·예외·수치·인용·출처·서비스 범위를 보존하세요. 새 사실이나 경험을 추가하지 마세요. " + data.get("instructions", ""))
        summary.update(status="remote_error", external_attempted=True)
        report = hp.call_remote(hp.DEFAULT_URL, data["mode"], args)
        (result / "report.md").write_text(report, encoding="utf-8")
        summary["status"] = "succeeded"
        if data["mode"] == "proofread":
            summary["status"] = "gate_rejected"
            proposed = hp.extract_polished(report)
            (result / "proposal.md").write_text(proposed, encoding="utf-8")
            local_ok, local_note = hp.local_compare(text, proposed)
            remote_ok, remote_note = hp.remote_review_gate(report, "proofread")
            preserve_ok = all(text.count(p) == proposed.count(p) for p in data.get("preserve", []))
            summary.update(local_gate=local_ok, remote_gate=remote_ok, preserve_gate=preserve_ok,
                           proposal_sha256=sha256(proposed.encode("utf-8")))
            (result / "review.md").write_text(remote_note + "\n\n" + local_note + f"\n\n보존 지정 대조: {preserve_ok}\n법률 의미 검토와 발행 승인은 별도입니다.\n", encoding="utf-8")
            diff = difflib.unified_diff(text.splitlines(True), proposed.splitlines(True), fromfile="original.md", tofile="proposal.md")
            (result / "changes.diff").write_text("".join(diff), encoding="utf-8")
            if local_ok and remote_ok and preserve_ok:
                summary["status"] = "succeeded"
    except (ValueError, UnicodeError, OSError, subprocess.CalledProcessError, hp.ProofreaderError) as exc:
        # Do not copy a provider's error body or a manuscript to the Actions log.
        summary["error_type"] = type(exc).__name__
        if not summary["external_attempted"]:
            summary["error"] = "요청 형식·동의·입력 지문·변경 범위를 확인하세요. 외부 전송은 하지 않았습니다."
        else:
            summary["error"] = "외부 호출 또는 응답 검사가 완료되지 않았습니다. 원문은 유지되며 재호출은 자동으로 하지 않습니다."
    finally:
        if source is not None:
            summary["source_unchanged"] = sha256(source.read_bytes()) == summary["source_sha256"]
            if not summary["source_unchanged"]:
                summary["status"] = "source_changed"
        summary["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
        (result / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    branch = os.environ.get("GITHUB_REF_NAME", "")
    commit = os.environ.get("GITHUB_SHA", "")
    try:
        summary = process(args.root.resolve(), branch, commit,
                          f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}")
        print(json.dumps(summary, ensure_ascii=False))
        return 0 if summary["status"] == "succeeded" else 2
    except (ValueError, OSError) as exc:
        print(f"Request not executed: {type(exc).__name__}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
