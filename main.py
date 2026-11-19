"""Entrypoint for the news-image-20261119 entry.

The poster image (entry.png) ships inside this repository, so this
program simply copies it to the grader's output location:
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when that
environment variable is set).

Standard library only — no Pillow, no network, no clock, no
randomness — so repeated runs write byte-identical output.
"""

import os
from pathlib import Path

CHUNK_SIZE = 64 * 1024


def copy_verified(source: Path, target: Path) -> int:
    """Stream source to target in chunks; return the bytes written.

    Raises SystemExit if the number of bytes copied does not match
    the source size, so a truncated write can never pass silently.
    """
    expected = source.stat().st_size
    written = 0
    with source.open("rb") as src, target.open("wb") as dst:
        while chunk := src.read(CHUNK_SIZE):
            dst.write(chunk)
            written += len(chunk)
    if written != expected:
        raise SystemExit(
            f"error: copied {written} bytes but {source} is {expected} bytes"
        )
    return written


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    written = copy_verified(source, target)
    print(f"wrote {target} ({written} bytes)")


if __name__ == "__main__":
    main()
