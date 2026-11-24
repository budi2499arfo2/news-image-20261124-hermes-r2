#!/usr/bin/env python3
"""Copy the pre-rendered broadsheet to the output directory.

Standard library only. The image is rendered by draw.py at build time
and shipped in this repository as entry.png; this program only copies it,
so two runs always produce identical bytes.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print("entry.png missing from repository", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    if os.path.abspath(src) == os.path.abspath(dst):
        # Output dir is the repository itself: nothing to copy.
        pass
    else:
        shutil.copyfile(src, dst)
    if _sha256(src) != _sha256(dst):
        print("output differs from entry.png", file=sys.stderr)
        return 1
    print("wrote", dst, _sha256(dst)[:12])
    return 0


if __name__ == "__main__":
    sys.exit(main())
