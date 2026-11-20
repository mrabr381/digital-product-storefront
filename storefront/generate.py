"""Render the static storefront from products.json.

No build step for visitors: the generated pages are plain HTML/CSS/JS.
Run `python -m storefront build` after editing products.json or adding
a product. All output is deterministic (same input -> same bytes).
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_products(path=None):
    path = Path(path) if path else ROOT / "products.json"
    with open(path, encoding="utf-8") as f:
        products = json.load(f)
    if not isinstance(products, list):
        raise ValueError("products.json must contain a list of products")
    seen = set()
    for p in products:
        for field in ("id", "name", "tagline", "description", "price_cents", "cover"):
            if field not in p or p[field] in ("", None):
                raise ValueError("product %r is missing field %r" % (p.get("id"), field))
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(p["id"])):
            raise ValueError("product id %r must be lowercase letters, digits, hyphens" % p["id"])
        if p["id"] in seen:
            raise ValueError("duplicate product id %r" % p["id"])
        seen.add(p["id"])
        if not isinstance(p["price_cents"], int) or p["price_cents"] <= 0:
            raise ValueError("product %r price_cents must be a positive integer" % p["id"])
    return products


def format_price(cents, currency="USD"):
    symbol = "$" if currency == "USD" else currency + " "
    return "%s%.2f" % (symbol, cents / 100)


def _esc(text):
    return html.escape(str(text), quote=True)


def _products_js(products):
    """Minimal product data for the cart script (id, name, price, currency)."""
    slim = [
        {"id": p["id"], "name": p["name"], "price_cents": p["price_cents"],
         "currency": p.get("currency", "USD")}
        for p in products
    ]
    return json.dumps(slim, sort_keys=True)


def _shell(title, body, products):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header>
  <div class="wrap">
    <h1><a href="/">The Sample Store</a></h1>
    <nav><a href="/">Products</a> <a href="#cart">Cart (<span id="cart-count">0</span>)</a></nav>
  </div>
</header>
<main>
%s
</main>
<footer>
  <p>The Sample Store — a demo storefront. 0%% platform commission: you keep
  every sale minus only your payment processor's own fee. Checkout links are
  placeholders until the seller adds their own Stripe Payment Links / PayPal buttons.</p>
  <p>Built with the free digital-product storefront. No tracking, no cookies, no accounts.</p>
</footer>
<script>window.STOREFRONT_PRODUCTS = %s;</script>
<script src="/assets/store.js"></script>
</body>
</html>
""" % (_esc(title), body, _products_js(products))


def _cart_section():
    return """<section class="cart" id="cart">
  <h2>Your cart</h2>
  <p id="cart-empty">Your cart is empty.</p>
  <table id="cart-table" style="display: none">
    <thead><tr><th>Product</th><th>Qty</th><th>Price</th><th></th></tr></thead>
    <tbody id="cart-items"></tbody>
  </table>
  <p class="total">Total: <span id="cart-total">$0.00</span></p>
  <p>Checkout is handled by your own payment links — open a product and pay
  with Stripe or PayPal. No account here, no platform fee, no tracking.</p>
</section>
"""


def _sample_badge(p):
    """Sample products are labelled on every card and page, so the demo
    store never looks like a fake shop. Real products added later have
    no 'sample' flag and get no badge."""
    if not p.get("sample"):
        return ""
    return """<p class="sample-badge">Sample product — demo only, not for sale.</p>"""


def render_index(products):
    cards = []
    for p in products:
        cards.append("""<article class="card">
  <img src="/%s" alt="%s cover" width="600" height="450">
  <div class="card-body">
    <h3>%s</h3>
    %s
    <p>%s</p>
    <p class="price">%s</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/products/%s.html">View</a>
      <button class="btn" data-add="%s">Add to cart</button>
    </div>
  </div>
</article>""" % (
            _esc(p["cover"]), _esc(p["name"]), _esc(p["name"]),
            _sample_badge(p), _esc(p["tagline"]),
            format_price(p["price_cents"], p.get("currency", "USD")),
            _esc(p["id"]), _esc(p["id"]),
        ))
    body = """<section class="hero">
  <h2>Sell downloads. Keep 100%% of the sale.</h2>
  <p>No monthly fee, no per-sale commission. This store runs on free static
  hosting and your own Stripe / PayPal links — the only fee is your payment
  processor's own charge. Three sample products below; swap them for yours
  with <code>python -m storefront add-product</code>.</p>
</section>
<section class="grid">
%s
</section>
%s""" % ("\n".join(cards), _cart_section())
    return _shell("The Sample Store — digital products, 0% commission", body, products)


def render_product(p, products):
    features = "\n".join("    <li>%s</li>" % _esc(f) for f in p.get("features", []))
    body = """<article class="product">
  <div><img src="/%s" alt="%s cover" width="600" height="450"></div>
  <div>
    <h2>%s</h2>
    %s
    <p><em>%s</em></p>
    <p>%s</p>
    <ul class="features">
%s
    </ul>
    <p><strong>Format:</strong> %s<br><strong>Size:</strong> %s</p>
    <p class="price">%s</p>
    <div class="btn-row">
      <button class="btn" data-add="%s">Add to cart</button>
      <a class="btn btn-secondary" href="%s">Buy with Stripe</a>
      <a class="btn btn-secondary" href="%s">Buy with PayPal</a>
    </div>
    <div class="note">
      <p><strong>Demo checkout links.</strong> These buttons point at
      placeholder Stripe / PayPal links — replace <code>stripe_link</code> and
      <code>paypal_link</code> in <code>products.json</code> with your own
      Payment Links to take real payments.</p>
    </div>
    <h3>License key (demo)</h3>
    <p>Keys are <strong>demo-grade, not DRM</strong>: this button generates a
    key in the store's format so you can see what a buyer would receive.
    Real delivery should come from your email / payment processor.</p>
    <p><button class="btn btn-secondary" id="demo-key-btn">Generate demo key</button></p>
    <p class="keybox" id="demo-key-out">No key generated yet.</p>
  </div>
</article>
<p><a href="/">&larr; Back to all products</a></p>
%s""" % (
        _esc(p["cover"]), _esc(p["name"]), _esc(p["name"]),
        _sample_badge(p), _esc(p["tagline"]),
        _esc(p["description"]), features,
        _esc(p.get("format", "Digital download")),
        _esc(p.get("file_size", "—")),
        format_price(p["price_cents"], p.get("currency", "USD")),
        _esc(p["id"]), _esc(p.get("stripe_link", "#")), _esc(p.get("paypal_link", "#")),
        _cart_section(),
    )
    return _shell("%s — The Sample Store" % p["name"], body, products)


def build_site(root=None):
    root = Path(root) if root else ROOT
    products = load_products(root / "products.json")
    (root / "index.html").write_text(render_index(products), encoding="utf-8")
    products_dir = root / "products"
    products_dir.mkdir(exist_ok=True)
    # Remove stale product pages (a product deleted from products.json
    # must not leave a live page behind).
    for old in products_dir.glob("*.html"):
        if old.stem not in {p["id"] for p in products}:
            old.unlink()
    for p in products:
        (products_dir / ("%s.html" % p["id"])).write_text(
            render_product(p, products), encoding="utf-8")
    return products
