"""Tests for the storefront cart maths and the sample-product labelling.

Prices are integer cents everywhere (Python side in products.json and
the JS side in assets/store.js), so $19 + $29 + $12 must be exactly
$60.00 — never $59.999999. The JS cart is tested for real via node
(skipped when node is absent); the Python tests cover the same maths
from products.json plus the fee table in the README.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from storefront.generate import format_price, load_products

REPO = Path(__file__).resolve().parent.parent
PRODUCTS = json.loads((REPO / "products.json").read_text())


def gumroad_fee_cents(price_cents):
    """Gumroad's published fee: 10% + $0.50 per sale, in cents."""
    return price_cents // 10 + 50


def test_all_three_sample_products_total_60_dollars():
    assert [p["price_cents"] for p in PRODUCTS] == [1900, 2900, 1200]
    assert sum(p["price_cents"] for p in PRODUCTS) == 6000
    assert format_price(6000) == "$60.00"


def test_quantities_use_integer_cents():
    # 2 x $19 + 1 x $29 + 3 x $12 = $103.00 exactly.
    quantities = {"notion-creator-kit": 2, "moody-film-presets": 1,
                  "first-1000-subscribers": 3}
    total = sum(
        p["price_cents"] * quantities[p["id"]] for p in PRODUCTS
    )
    assert total == 10300
    assert format_price(total) == "$103.00"
    # No float dust: 19 + 29 in cents is exactly 48.00.
    assert format_price(1900 + 2900) == "$48.00"


def test_gumroad_fee_table_matches_readme():
    # README table: $12 -> $1.70 fee / $10.30 kept; $19 -> $2.40 / $16.60;
    # $29 -> $3.40 / $25.60; all three $60 -> $7.50 / $52.50.
    assert gumroad_fee_cents(1200) == 170
    assert gumroad_fee_cents(1900) == 240
    assert gumroad_fee_cents(2900) == 340
    total_fee = sum(gumroad_fee_cents(p["price_cents"]) for p in PRODUCTS)
    assert total_fee == 750
    assert format_price(6000 - total_fee) == "$52.50"


def test_format_price():
    assert format_price(0) == "$0.00"
    assert format_price(5) == "$0.05"
    assert format_price(1999) == "$19.99"


def test_all_products_are_labelled_sample():
    """Every demo product is flagged sample in the data and labelled on
    every generated page, so the store never looks like a fake shop."""
    assert len(PRODUCTS) == 3
    assert all(p.get("sample") is True for p in PRODUCTS)
    index = (REPO / "index.html").read_text()
    assert "Sample product" in index
    for p in PRODUCTS:
        page = (REPO / "products" / ("%s.html" % p["id"])).read_text()
        assert "Sample product" in page
        assert "demo" in page.lower()


def test_load_products_validation(tmp_path):
    good = dict(PRODUCTS[0])
    bad_path = tmp_path / "products.json"
    # Duplicate id.
    bad_path.write_text(json.dumps([good, dict(good)]))
    with pytest.raises(ValueError, match="duplicate"):
        load_products(bad_path)
    # Non-positive price.
    bad_price = dict(good, price_cents=0)
    bad_path.write_text(json.dumps([bad_price]))
    with pytest.raises(ValueError, match="price_cents"):
        load_products(bad_path)
    # Bad id characters.
    bad_id = dict(good, id="Bad ID!")
    bad_path.write_text(json.dumps([bad_id]))
    with pytest.raises(ValueError, match="must be lowercase"):
        load_products(bad_path)


NODE_SCRIPT = """
const s = require(%s);
const products = [
  {id: 'notion-creator-kit', price_cents: 1900},
  {id: 'moody-film-presets', price_cents: 2900},
  {id: 'first-1000-subscribers', price_cents: 1200},
];
const out = {};
let cart = {};
s.addToCart(cart, 'notion-creator-kit', 1);
s.addToCart(cart, 'moody-film-presets', 1);
s.addToCart(cart, 'first-1000-subscribers', 1);
out.all_three_cents = s.cartTotalCents(cart, products);
out.all_three_formatted = s.formatPrice(out.all_three_cents);
out.item_count = s.cartItemCount(cart);
s.addToCart(cart, 'notion-creator-kit', 1);
out.two_notion_plus_rest = s.cartTotalCents(cart, products);
s.setQuantity(cart, 'notion-creator-kit', 0);
out.after_removing_notion = s.cartTotalCents(cart, products);
out.after_removing_count = s.cartItemCount(cart);
out.clamped = s.addToCart({}, 'moody-film-presets', 500)['moody-film-presets'];
const key = s.generateLicenseKey();
out.key_valid = s.isValidLicenseKey(key);
out.bad_key_rejected = !s.isValidLicenseKey('0000-0000-0000-0000');
console.log(JSON.stringify(out));
""" % json.dumps(str(REPO / "assets" / "store.js"))


@pytest.mark.skipif(
    shutil.which("node") is None, reason="JS cart test needs node"
)
def test_cart_js_matches_python_totals():
    """The real cart code in assets/store.js, run in node."""
    proc = subprocess.run(
        ["node", "-e", NODE_SCRIPT],
        capture_output=True, text=True, timeout=60, check=True,
    )
    out = json.loads(proc.stdout)
    assert out["all_three_cents"] == 6000
    assert out["all_three_formatted"] == "$60.00"
    assert out["item_count"] == 3
    assert out["two_notion_plus_rest"] == 7900  # 2x19 + 29 + 12
    assert out["after_removing_notion"] == 4100  # 29 + 12
    assert out["after_removing_count"] == 2
    assert out["clamped"] == 99  # quantities clamp to 1..99
    assert out["key_valid"] is True
    assert out["bad_key_rejected"] is True
