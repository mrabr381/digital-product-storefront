# Free Digital-Product Storefront 🛍️

![No account](https://img.shields.io/badge/account-none%20required-brightgreen.svg)
![Platform fee](https://img.shields.io/badge/platform%20fee-0%25-brightgreen.svg)
![Static site](https://img.shields.io/badge/hosting-GitHub%20Pages%20free-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sell downloads with 0% commission.** A static storefront for digital
products — product pages, a cart, checkout through your own Stripe Payment
Links or PayPal buttons, and demo-grade license keys. No monthly fee, no
per-sale cut, no account, no tracking. Host it free on GitHub Pages.

> **Live demo:** this repo *is* the demo. Enable GitHub Pages on the repo
> (Settings → Pages → Deploy from a branch → `main`, `/ (root)`) and the
> store is live at `https://mrabr381.github.io/digital-product-storefront/`.
> The three sample products below are fictional — swap them for yours.

## Table of contents

- [What it is](#what-it-is)
- [What you keep: Gumroad vs this store](#what-you-keep-gumroad-vs-this-store)
- [Quickstart](#quickstart)
- [Adding a product](#adding-a-product)
- [Going live: Pages + real payments](#going-live-pages--real-payments)
- [How checkout and license keys work](#how-checkout-and-license-keys-work)
- [Project layout](#project-layout)
- [Honest limitations](#honest-limitations)
- [Contributing](#contributing)
- [License](#license)

## What it is

A plain HTML/CSS/JS storefront with no framework and no build step:

- **Product grid + detail pages** — cover art, description, features, format, price.
- **Cart** — add, remove, change quantities. Totals are computed in integer
  cents, so `$19.00 + $29.00` is exactly `$48.00`, never `$47.999999`.
- **Checkout via your own links** — each product has a Stripe Payment Link
  and a PayPal button. Buyers pay you directly; no platform sits in between.
- **License keys (demo-grade)** — a button generates a key in the format
  `XXXX-XXXX-XXXX-XXXX` so you can see what a buyer would receive.
- **A tiny CLI** — `python -m storefront add-product` scaffolds a new
  product page and a matching cover, so you never hand-edit HTML.

Everything is static. There is no server, no database, no API key, and
nothing leaves the buyer's browser except the payment itself (which happens
on Stripe's / PayPal's own site).

## What you keep: Gumroad vs this store

Gumroad charges **10% + $0.50 per sale** (their published fee). This store
charges **0%** — you only pay your payment processor's own fee on top.

| Sale | Gumroad fee (10% + $0.50) | You keep (Gumroad) | You keep (this store) |
|------|---------------------------|--------------------|-----------------------|
| E-book — $12.00 | $1.70 | $10.30 | **$12.00** |
| Notion template — $19.00 | $2.40 | $16.60 | **$19.00** |
| Lightroom presets — $29.00 | $3.40 | $25.60 | **$29.00** |
| All three — $60.00 | $7.50 | $52.50 | **$60.00** |

Maths, checked by hand: 10% of $29.00 is $2.90, plus $0.50 is $3.40;
$29.00 − $3.40 = $25.60. "You keep" here means before your payment
processor's own fee (Stripe / PayPal charge their own percentage on top of
both — that fee is the same either way, so the difference above is real).

## Quickstart

No dependencies — Python 3.10+ only, standard library.

```bash
git clone https://github.com/mrabr381/digital-product-storefront.git
cd digital-product-storefront
python scripts/make_sample.py   # regenerate the sample store (optional)
python -m http.server 8000       # open http://localhost:8000
```

Browse the store, add the three sample products to the cart, change
quantities — the total updates instantly. The cart is stored in your
browser's `localStorage`; clearing it empties the cart.

## Adding a product

```bash
python -m storefront add-product \
  --name "My Preset Pack" \
  --price 15 \
  --tagline "Five presets for golden-hour portraits." \
  --description "Longer pitch goes here. What it is, who it is for, what is inside." \
  --format "5 × .xmp + 5 × .dng + PDF guide" \
  --features "5 presets, Desktop + mobile, Install guide, Free updates"
```

This appends the product to `products.json`, generates a matching cover SVG
(colours picked deterministically from the product name, so the same product
always gets the same cover), and rebuilds `index.html` and
`products/<slug>.html`. Then replace the placeholder checkout links in
`products.json`:

```json
"stripe_link": "https://buy.stripe.com/REPLACE-ME-my-preset-pack",
"paypal_link": "https://www.paypal.com/paypalme/REPLACE-ME/15"
```

Other commands:

```bash
python -m storefront build   # regenerate all pages from products.json
python -m storefront list    # list products and prices
```

## Going live: Pages + real payments

**1. GitHub Pages (2 minutes, free)**

Repo Settings → Pages → Source: *Deploy from a branch* → branch `main`,
folder `/ (root)` → Save. The store is live at
`https://mrabr381.github.io/digital-product-storefront/`.

**2. Stripe Payment Links (free to create, no code)**

Stripe Dashboard → Payment Links → Create payment link → set the product
and price → copy the `https://buy.stripe.com/...` URL into the product's
`stripe_link` in `products.json` → `python -m storefront build` → commit
and push. Each product needs its own link.

**3. PayPal (free to create)**

PayPal → PayPal.Me → create your link, or use a PayPal payment button.
Put the URL in the product's `paypal_link`. Format:
`https://www.paypal.com/paypalme/YOURNAME/15` (amount optional).

**4. Delivering the files**

This store does not host file delivery. The simple honest setup: after a
buyer pays, Stripe / PayPal emails you their address; you email the download
link (host the files on Google Drive, Gumroad-free hosting, or your own
server). For automatic delivery, point the Payment Link's confirmation page
at a download page, or add a small server later — that part is out of scope
for this static store, by design.

## How checkout and license keys work

- **Checkout:** the "Buy with Stripe" / "Buy with PayPal" buttons are plain
  links to the URLs in `products.json`. Until you replace the
  `REPLACE-ME` placeholders, they go nowhere useful — the product page says
  so in a yellow note box.
- **Cart:** the cart is a convenience for browsing totals. There is no
  combined checkout: each product is paid for on its own Payment Link, which
  is how Payment Links work. The cart total is the sum of the listed prices.
- **License keys:** the "Generate demo key" button makes a random key in the
  format `XXXX-XXXX-XXXX-XXXX` (letters/digits, no confusing `0`/`O`/`1`/`I`).
  It is **demo-grade, not DRM** — anyone can generate one, and nothing
  checks it. Real key delivery should come from your email or payment
  processor after a verified payment.

## Project layout

```text
├── index.html                  # storefront home (generated)
├── products/                   # one page per product (generated)
│   ├── notion-creator-kit.html
│   ├── moody-film-presets.html
│   └── first-1000-subscribers.html
├── products.json               # the whole catalogue (edit this)
├── assets/
│   ├── style.css               # plain CSS, no framework
│   ├── store.js                # cart + license keys, no network calls
│   └── covers/*.svg            # cover art (inline SVG = text, pushable)
├── storefront/                 # Python CLI (stdlib only)
│   ├── cli.py                  # build / list / add-product
│   ├── generate.py             # renders index.html + product pages
│   └── sample.py               # sample products + cover art (source of truth)
└── scripts/make_sample.py      # regenerate the sample store from sample.py
```

## Honest limitations

- **No real payment processing in this repo.** Checkout is links only.
  Stripe / PayPal handle the money on their own sites.
- **No automatic file delivery.** See the "Delivering the files" section
  above — delivery is manual (email) unless you add it.
- **License keys are demo-grade.** They are not checked against anything
  and are not copy protection.
- **No combined cart checkout.** Payment Links are per product; the cart
  shows the total but each item is paid for separately.
- **No analytics, no accounts, no order history.** That is the trade-off
  for 0% fees and no server: if you need order tracking, use Stripe's
  dashboard (it logs every Payment Link sale).
- **Sample products are fictional.** The Notion template, presets and
  e-book do not exist as real files — the store demonstrates the flow.
  Replace them with your own products before selling anything.
- **Covers are simple SVG art**, not product photography. Swap in your own
  images (JPG/PNG) by changing the `cover` path in `products.json` — note
  that binary images cannot be pushed with the usual GitHub connector
  workflow; upload them through the GitHub web UI instead.

## Contributing

Issues and pull requests are welcome. Keep the quality promise: no invented
prices or fees, every fee quoted must come from the vendor's own pricing
page, and every new feature must be testable with `python -m http.server`
and `curl`.

## License

MIT — see [LICENSE](LICENSE).
