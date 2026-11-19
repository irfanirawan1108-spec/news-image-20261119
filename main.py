#!/usr/bin/env python3
"""news-image-20261119 entrypoint (Python 3.13, standard library only).

Copies the front-page image held in this repository to the output path
make.fun grades. Deterministic: the same bytes every run, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                   "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
