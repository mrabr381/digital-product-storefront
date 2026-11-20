"""Sample store data — the single source of truth for the demo products.

scripts/make_sample.py regenerates products.json and the cover SVGs from
this file, so the whole sample store is reproducible from text alone.
All three products are fictional; prices are in USD.
"""

SAMPLE_PRODUCTS = [
    {
        "id": "notion-creator-kit",
        "name": "Creator OS — Notion Template",
        "tagline": "Plan, write and ship a month of content from one Notion workspace.",
        "description": "A complete Notion workspace for creators: a 30-day content calendar, an idea bank with a hook library, a publishing checklist, and a simple analytics tracker. Duplicate it into your own Notion in one click and start planning today. Works with a free Notion account.",
        "price_cents": 1900,
        "currency": "USD",
        "format": "Notion template (duplicate link + PDF setup guide)",
        "file_size": "1 Notion workspace + 6-page PDF",
        "cover": "assets/covers/notion-creator-kit.svg",
        "features": [
            "30-day content calendar with status tracking",
            "Idea bank with 50 ready-to-use hooks",
            "Publishing checklist for every video or post",
            "Simple analytics tracker (views, subs, watch time)",
            "Free updates for life",
        ],
        "stripe_link": "https://buy.stripe.com/REPLACE-ME-notion-creator-kit",
        "paypal_link": "https://www.paypal.com/paypalme/REPLACE-ME/19",
    },
    {
        "id": "moody-film-presets",
        "name": "Moody Film — Lightroom Presets",
        "tagline": "12 film-inspired presets for moody, cinematic photos on desktop and mobile.",
        "description": "Twelve Lightroom presets inspired by 35mm film: muted greens, warm skin tones and soft contrast that work on portraits, street and travel shots. Includes desktop (.xmp) and mobile (.dng) versions plus a 10-minute install guide. One purchase, use on as many of your own photos as you like.",
        "price_cents": 2900,
        "currency": "USD",
        "format": "12 × .xmp (desktop) + 12 × .dng (mobile) + PDF guide",
        "file_size": "48 MB download (ZIP)",
        "cover": "assets/covers/moody-film-presets.svg",
        "features": [
            "12 presets: 6 colour, 4 black & white, 2 warm",
            "Desktop (.xmp) and mobile (.dng) versions included",
            "Before/after reference photos for every preset",
            "10-minute install guide (PDF + video link)",
            "Free updates for life",
        ],
        "stripe_link": "https://buy.stripe.com/REPLACE-ME-moody-film-presets",
        "paypal_link": "https://www.paypal.com/paypalme/REPLACE-ME/29",
    },
    {
        "id": "first-1000-subscribers",
        "name": "Your First 1,000 Subscribers — E-book",
        "tagline": "A practical 68-page playbook for growing a new channel from zero.",
        "description": "No hacks, no bought subs: a step-by-step playbook for the first 1,000 subscribers. Covers picking a niche that searches, titles and thumbnails that earn the click, a realistic upload schedule, and the five analytics numbers that actually matter. Includes printable worksheets for each chapter.",
        "price_cents": 1200,
        "currency": "USD",
        "format": "PDF e-book, 68 pages",
        "file_size": "4.2 MB download (PDF)",
        "cover": "assets/covers/first-1000-subscribers.svg",
        "features": [
            "12 chapters, 68 pages, zero fluff",
            "Printable worksheet for every chapter",
            "Real examples from small channels (not gurus)",
            "A 30-day launch plan you can start today",
            "Free updates for life",
        ],
        "stripe_link": "https://buy.stripe.com/REPLACE-ME-first-1000-subscribers",
        "paypal_link": "https://www.paypal.com/paypalme/REPLACE-ME/12",
    },
]

# Cover art: inline SVG (text, so it pushes to GitHub fine). Regenerated
# by scripts/make_sample.py. Keep each cover simple: gradient + shapes + title.
COVER_SVGS = {
    "notion-creator-kit": """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450" role="img" aria-label="Creator OS Notion Template cover">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#6d28d9"/>
      <stop offset="1" stop-color="#1e0a45"/>
    </linearGradient>
  </defs>
  <rect width="600" height="450" fill="url(#g)"/>
  <rect x="90" y="70" width="420" height="300" rx="14" fill="#ffffff" opacity="0.12"/>
  <rect x="115" y="95" width="370" height="42" rx="8" fill="#ffffff" opacity="0.9"/>
  <rect x="115" y="155" width="240" height="16" rx="8" fill="#fbbf24"/>
  <rect x="115" y="185" width="370" height="10" rx="5" fill="#ffffff" opacity="0.55"/>
  <rect x="115" y="205" width="300" height="10" rx="5" fill="#ffffff" opacity="0.55"/>
  <rect x="115" y="225" width="340" height="10" rx="5" fill="#ffffff" opacity="0.55"/>
  <rect x="115" y="265" width="170" height="34" rx="17" fill="#f59e0b"/>
  <rect x="300" y="265" width="170" height="34" rx="17" fill="#ffffff" opacity="0.25"/>
  <text x="300" y="410" text-anchor="middle" font-family="Georgia, serif" font-size="30" fill="#ffffff">Creator OS</text>
  <text x="300" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="#fbbf24" letter-spacing="3">NOTION TEMPLATE</text>
</svg>
""",
    "moody-film-presets": """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450" role="img" aria-label="Moody Film Lightroom Presets cover">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3f3f46"/>
      <stop offset="1" stop-color="#b45309"/>
    </linearGradient>
  </defs>
  <rect width="600" height="450" fill="url(#g)"/>
  <circle cx="300" cy="190" r="110" fill="#f59e0b" opacity="0.85"/>
  <circle cx="300" cy="190" r="110" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.6"/>
  <rect x="120" y="330" width="360" height="6" rx="3" fill="#ffffff" opacity="0.5"/>
  <rect x="180" y="345" width="240" height="6" rx="3" fill="#ffffff" opacity="0.35"/>
  <text x="300" y="100" text-anchor="middle" font-family="Georgia, serif" font-size="30" fill="#ffffff">Moody Film</text>
  <text x="300" y="60" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="#fbbf24" letter-spacing="3">LIGHTROOM PRESETS</text>
  <text x="300" y="410" text-anchor="middle" font-family="Georgia, serif" font-size="20" fill="#ffffff">12 presets · desktop + mobile</text>
</svg>
""",
    "first-1000-subscribers": """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450" role="img" aria-label="Your First 1000 Subscribers e-book cover">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0e7490"/>
      <stop offset="1" stop-color="#164e63"/>
    </linearGradient>
  </defs>
  <rect width="600" height="450" fill="url(#g)"/>
  <rect x="150" y="60" width="300" height="330" rx="10" fill="#ffffff"/>
  <rect x="150" y="60" width="300" height="14" rx="7" fill="#0e7490"/>
  <rect x="180" y="110" width="240" height="18" rx="9" fill="#164e63"/>
  <rect x="180" y="140" width="180" height="18" rx="9" fill="#164e63"/>
  <rect x="180" y="190" width="240" height="8" rx="4" fill="#94a3b8"/>
  <rect x="180" y="210" width="240" height="8" rx="4" fill="#94a3b8"/>
  <rect x="180" y="230" width="200" height="8" rx="4" fill="#94a3b8"/>
  <rect x="180" y="300" width="240" height="40" rx="20" fill="#f59e0b"/>
  <text x="300" y="325" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#1e0a45">68 pages · 12 chapters</text>
  <text x="300" y="425" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#ffffff">Your First 1,000 Subscribers</text>
</svg>
""",
}


def make_cover_svg(product_id, title, subtitle, color_a, color_b):
    """Deterministic generic cover for products added via the CLI.

    Colours are picked by the caller from a fixed palette (hash of the id),
    so the same product always gets the same cover.
    """
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" '
        'viewBox="0 0 600 450" role="img" aria-label="%s cover">\n'
        '  <defs>\n'
        '    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">\n'
        '      <stop offset="0" stop-color="%s"/>\n'
        '      <stop offset="1" stop-color="%s"/>\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        '  <rect width="600" height="450" fill="url(#g)"/>\n'
        '  <rect x="90" y="90" width="420" height="220" rx="14" fill="#ffffff" opacity="0.12"/>\n'
        '  <rect x="115" y="120" width="370" height="16" rx="8" fill="#fbbf24"/>\n'
        '  <rect x="115" y="160" width="370" height="10" rx="5" fill="#ffffff" opacity="0.55"/>\n'
        '  <rect x="115" y="185" width="300" height="10" rx="5" fill="#ffffff" opacity="0.55"/>\n'
        '  <rect x="115" y="210" width="340" height="10" rx="5" fill="#ffffff" opacity="0.55"/>\n'
        '  <rect x="115" y="250" width="170" height="34" rx="17" fill="#f59e0b"/>\n'
        '  <text x="300" y="380" text-anchor="middle" font-family="Georgia, serif" font-size="28" fill="#ffffff">%s</text>\n'
        '  <text x="300" y="60" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#fbbf24" letter-spacing="3">%s</text>\n'
        '</svg>\n' % (_xml_escape(title), color_a, color_b, _xml_escape(title), _xml_escape(subtitle.upper()))
    )


def _xml_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
