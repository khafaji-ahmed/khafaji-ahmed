#!/usr/bin/env bash
# Rebuild the ASCII portrait from the source photo.
#
# Tuned for this avatar (soft-shaded 3D render whose clothing is darker than
# the skin, on a flat gray backdrop):
#   rembg     proper segmentation; colour-keying at any tolerance bleeds into
#             the shading, which sits within ~12 levels of the backdrop
#   --clahe 0 CLAHE amplifies the render's soft shading into noise
#   --white 55 anchors the white point on the subject
#   --gamma 0.9 lifts highlights so the lit side of the face stays bright
#
# Usage: scripts/portrait.sh [photo]   (defaults to source-photo.png)
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="${1:-source-photo.png}"
.venv/bin/python scripts/prep_photo.py "$SRC" --clahe 0 --white 55 --gamma 0.9
.venv/bin/python scripts/make_ascii_svg.py
echo "done: commit avi-ascii.svg when you like the result"
