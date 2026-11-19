"""news-image-20261119 — entry point.

Copies the pre-rendered front-page image held in this repository to the
grader's output directory. Standard library only; no network, no clock,
no randomness — running this twice produces a byte-identical file.
The image itself is rendered offline by draw.py (Pillow); this entry
point deliberately does no rendering, because the grader mounts the
repository read-only.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = (
    os.environ.get("MAKEFUN_OUTPUT_DIR")
    or os.environ.get("OUTPUT_DIR")
    or "/output"
)
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
