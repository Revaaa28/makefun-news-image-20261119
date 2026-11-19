"""Entrypoint for the news-image-20261119 entry.

Renders the 19 November 2026 world-news poster with the PIL-only
renderer in tools/render.py and writes it to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png when that is set).

Standard library plus Pillow only; no network, no clock, no randomness,
so repeated runs write byte-identical output.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.render import render


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    render().save(target, "PNG")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
