#!/usr/bin/env python3
"""Publish the one-sentence entry for the make.fun bounty
"One Sentence for a Traveler from 1800".

The sentence lives in ``entry.txt`` next to this file. This program
reads it, checks it against the bounty gate (UTF-8 text, a single
line, 1 to 200 characters, not only white space), writes the exact
text to ``entry.txt`` in the output directory, and reads it back to
confirm the published bytes match. Standard library only: no network
access, no clock reads, no randomness, so two runs always produce
identical output.

The output directory is ``$MAKEFUN_OUTPUT_DIR`` when set, else
``/output``.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 200


def load_sentence() -> str:
    here = Path(__file__).resolve().parent
    text = (here / "entry.txt").read_text(encoding="utf-8")
    return text.strip()


def validate(text: str) -> None:
    if not text or text.isspace():
        raise SystemExit("entry is empty or only white space")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main() -> int:
    text = load_sentence()
    validate(text)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(text, encoding="utf-8")
    published = out_path.read_text(encoding="utf-8")
    if published != text:
        raise SystemExit("published entry does not match entry.txt")
    print(f"Wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
