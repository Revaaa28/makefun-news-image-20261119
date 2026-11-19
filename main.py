#!/usr/bin/env python3
"""make.fun entry: news-image-20261119.

Copies the shipped entry.png (the world news of Thursday 19 November 2026
in one image) into the output directory, byte for byte. The picture itself
is drawn by tools/render.py; this program only places the file.
"""

import os
import shutil
from pathlib import Path

OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
IMAGE_NAME = "entry.png"


def main():
    src = Path(__file__).resolve().parent / IMAGE_NAME
    out_dir = Path(os.environ.get(OUTPUT_ENV, DEFAULT_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / IMAGE_NAME
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
