"""news-image-20261119 — entry point.

Ships the pre-rendered front page (entry.png, drawn offline by
render.py) to the grader's output directory. Standard library only;
no network, no clock, no randomness. The copy is byte-for-byte, so
running this twice always produces identical output.
"""

import hashlib
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "entry.png"

DEST_DIR = pathlib.Path(
    os.environ.get("MAKEFUN_OUTPUT_DIR")
    or os.environ.get("OUTPUT_DIR")
    or "/output"
)
DEST = DEST_DIR / "entry.png"


def run() -> None:
    payload = SOURCE.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(payload)
    check = DEST.read_bytes()
    if hashlib.sha256(check).hexdigest() != digest:
        raise RuntimeError("entry.png did not copy cleanly")
    if len(check) > 1_048_576:
        raise RuntimeError("entry.png exceeds the 1 MiB limit")


if __name__ == "__main__":
    run()
