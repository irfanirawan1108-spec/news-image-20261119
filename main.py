"""news-image-20261119 — entry point.

Renders the front page with draw.py and writes the PNG to /output/entry.png.
Standard library only; no network, no clock, no randomness — running this
twice produces a byte-identical file.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import draw  # noqa: E402


def main():
    draw.main()
    src = os.path.join(HERE, "entry.png")
    dst_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(dst_dir, "entry.png"))


if __name__ == "__main__":
    main()
