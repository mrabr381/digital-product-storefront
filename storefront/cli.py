"""CLI: build the site, list products, scaffold a new product.

Usage:
    python -m storefront build
    python -m storefront list
    python -m storefront add-product --name "My E-book" --price 15 \\
        --tagline "Short pitch" --description "Longer pitch" \\
        --format "PDF e-book, 40 pages" [--features "A, B, C"]
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from .generate import ROOT, build_site, load_products
from .sample import make_cover_svg

PALETTE = [
    ("#6d28d9", "#1e0a45"),
    ("#0e7490", "#164e63"),
    ("#b45309", "#3f3f46"),
    ("#be185d", "#4c0519"),
    ("#15803d", "#14532d"),
    ("#b91c1c", "#450a0a"),
]


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise ValueError("could not make a URL slug from %r" % name)
    return slug


def parse_price_dollars(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise ValueError("price must be a number, e.g. 15 or 12.50")
    if value <= 0:
        raise ValueError("price must be greater than 0")
    if value > 10000:
        raise ValueError("price looks wrong (over $10,000) — check it")
    cents = int(round(value * 100))
    if cents <= 0:
        raise ValueError("price is too small (under 1 cent)")
    return cents


def cmd_build(_args):
    products = build_site()
    print("Built %d product pages + index.html" % len(products))
    return 0


def cmd_list(_args):
    for p in load_products():
        print("%-28s $%.2f  %s" % (p["id"], p["price_cents"] / 100, p["name"]))
    return 0


def cmd_add_product(args):
    if not args.name or not args.name.strip():
        print("Error: --name is required", file=sys.stderr)
        return 1
    if not args.tagline or not args.tagline.strip():
        print("Error: --tagline is required", file=sys.stderr)
        return 1
    if not args.description or not args.description.strip():
        print("Error: --description is required", file=sys.stderr)
        return 1
    try:
        price_cents = parse_price_dollars(args.price)
    except ValueError as e:
        print("Error: %s" % e, file=sys.stderr)
        return 1
    slug = slugify(args.name)
    products = load_products()
    if any(p["id"] == slug for p in products):
        print("Error: a product with id %r already exists" % slug, file=sys.stderr)
        return 1
    features = [f.strip() for f in (args.features or "").split(",") if f.strip()]
    if not features:
        features = ["Instant download", "Free updates for life"]

    # Deterministic cover: colours from the slug hash, so the same product
    # always gets the same cover.
    digest = int(hashlib.sha256(slug.encode("utf-8")).hexdigest(), 16)
    color_a, color_b = PALETTE[digest % len(PALETTE)]
    cover_path = ROOT / "assets" / "covers" / ("%s.svg" % slug)
    cover_path.write_text(
        make_cover_svg(slug, args.name.strip(), args.tagline.strip(), color_a, color_b),
        encoding="utf-8",
    )

    product = {
        "id": slug,
        "name": args.name.strip(),
        "tagline": args.tagline.strip(),
        "description": args.description.strip(),
        "price_cents": price_cents,
        "currency": "USD",
        "format": args.format or "Digital download",
        "file_size": args.file_size or "—",
        "cover": "assets/covers/%s.svg" % slug,
        "features": features,
        "stripe_link": args.stripe_link or "https://buy.stripe.com/REPLACE-ME-%s" % slug,
        "paypal_link": args.paypal_link or "https://www.paypal.com/paypalme/REPLACE-ME/%d" % (price_cents // 100),
    }
    products.append(product)
    with open(ROOT / "products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, sort_keys=True)
        f.write("\n")
    build_site()
    print("Added %s ($%.2f) — page: products/%s.html" % (slug, price_cents / 100, slug))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="storefront",
        description="Free digital-product storefront: build pages, add products.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Regenerate index.html + product pages")
    p_build.set_defaults(func=cmd_build)

    p_list = sub.add_parser("list", help="List products")
    p_list.set_defaults(func=cmd_list)

    p_add = sub.add_parser("add-product", help="Scaffold a new product page")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--price", required=True, help="Price in dollars, e.g. 15 or 12.50")
    p_add.add_argument("--tagline", required=True)
    p_add.add_argument("--description", required=True)
    p_add.add_argument("--format", default="Digital download")
    p_add.add_argument("--file-size", default="—")
    p_add.add_argument("--features", default="", help="Comma-separated feature list")
    p_add.add_argument("--stripe-link", default="")
    p_add.add_argument("--paypal-link", default="")
    p_add.set_defaults(func=cmd_add_product)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
