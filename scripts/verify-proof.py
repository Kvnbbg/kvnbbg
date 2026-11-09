#!/usr/bin/env python3
"""Public proof integrity check. No network, credentials or private repo access."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "engineering-proof.md"

def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("Public proof document is missing")
    else:
        text = DOC.read_text(encoding="utf-8")
        for required in (
            "Engineering Proof of Work",
            "9 November 2026",
            "Private project",
            "execution **not confirmed**",
            "## Case study 01",
            "## Case study 02",
            "## Acceptance criteria",
            "## Privacy, scope and reuse",
            "https://github.com/Kvnbbg/kvnbbg/actions/workflows/engineering-proof.yml",
        ):
            if required not in text:
                errors.append(f"Missing mandatory statement: {required}")
        # Publishing direct private PR links exposes unverifiable URLs and
        # may mislead an external reviewer, so the public report is sanitized.
        forbidden = (
            r"https?://github[.]com/Kvnbbg/french-dev-ai-tools/(pull|issues|actions)/",
            r"https?://api[.]github[.]com/repos/Kvnbbg/french-dev-ai-tools",
            r"(?i)(sk_live_|whsec_|ghp_[a-zA-Z0-9]{20,}|supabase_service_role)",
            r"(?i)CI\s*:\s*(passing|green|all tests passed)",
        )
        for pattern in forbidden:
            if re.search(pattern, text):
                errors.append(f"Public disclosure or unsupported success claim matching {pattern}")
        if not (ROOT / ".github" / "workflows" / "engineering-proof.yml").is_file():
            errors.append("Documented public workflow is missing")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: public engineering evidence has mandatory disclosures and references")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
