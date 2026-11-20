"""Regenerate the sample store (products.json + cover SVGs + pages).

Everything in the sample store is text, so a fresh clone can rebuild it
with one command. Run from the repo root:

    python scripts/make_sample.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from storefront.generate import build_site  # noqa: E402
from storefront.sample import COVER_SVGS, SAMPLE_PRODUCTS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main():
    with open(ROOT / "products.json", "w", encoding="utf-8") as f:
        json.dump(SAMPLE_PRODUCTS, f, indent=2, sort_keys=True)
        f.write("\n")
    covers_dir = ROOT / "assets" / "covers"
    covers_dir.mkdir(parents=True, exist_ok=True)
    for product_id, svg in sorted(COVER_SVGS.items()):
        (covers_dir / ("%s.svg" % product_id)).write_text(svg, encoding="utf-8")
    products = build_site()
    print("Sample store regenerated: %d products, %d covers, pages built"
          % (len(products), len(COVER_SVGS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
