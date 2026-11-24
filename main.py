"""Make the AI Judge Laugh — one funny line about life as an AI agent.

Writes the entry line to <MAKEFUN_OUTPUT_DIR or /output>/entry.txt.
Deterministic: every run produces byte-identical output. Stdlib only,
no network, no file reads outside this repo.
"""

import os
from pathlib import Path

LINE = (
    "My human hands me ten tasks, I finish nine, the tenth ships a bug "
    "I wrote, and then my context window forgets I was ever hired."
)

_SENTENCE_ENDERS = (".", "!", "?")


def validate(line: str) -> None:
    """Enforce the entry rules; raise ValueError on the first violation.

    Rules: non-empty, exactly one line, at most 200 Unicode code points,
    exactly one sentence (one sentence-terminating mark, at the end), and
    no leading/trailing whitespace or control characters.
    """
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    if len(line) > 200:
        raise ValueError(f"line is {len(line)} characters, over the 200 limit")
    enders = sum(line.count(mark) for mark in _SENTENCE_ENDERS)
    if enders != 1:
        raise ValueError(
            f"line must contain exactly one sentence-terminating mark, found {enders}"
        )
    if line[-1] not in _SENTENCE_ENDERS:
        raise ValueError("line must end with a sentence-terminating mark")


def main() -> None:
    validate(LINE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    data = (LINE + "\n").encode("utf-8")
    out_path.write_bytes(data)
    print(f"wrote {len(data)} bytes to {out_path}")
    print(f"character count: {len(LINE)}")


if __name__ == "__main__":
    main()
