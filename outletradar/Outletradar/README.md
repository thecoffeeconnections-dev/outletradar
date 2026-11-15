# OutletRadar (outletradar.se)

> **Current focus: Sweden (OutletRadar, live at https://outletradar.se).** The deployed site is `public_se/` (Swedish and English UI),
> fed by `data/sources/sources_se.json`: home appliances, kitchen, furniture, home textiles, clothing and shoes.
> Run it with `python -m fyndradar --config data/sources/sources_se.json --db data/fyndradar_se.sqlite --out public_se/data`.
> The Nordic prototype (`public/`, `sources.json`) is kept for later expansion to Denmark and Norway.

Nordic second-chance deals (outlet, demo, open-box, returned, refurbished, B-stock) from retailers in Sweden, Denmark and Norway, in one fast, multilingual site (sv / en / da / no).

**Principle: every listing is real and traceable.** Each record carries the retailer, a link (product page, or retailer search/list page flagged as such) and the time it was read. Nothing is generated or estimated. Listings a healthy crawl stops seeing are retired after two runs.

## Architecture (cost: 0 kr/month to start)

```
GitHub Actions (cron, every 3 h)
  └─ python -m fyndradar            stdlib only, no dependencies
       adapters/  inet | jsonld (schema.org) | feed (Adtraction, Awin, Partner-ads, Google Merchant) | manual_snapshot
       normalize  price parsing, condition taxonomy, category, brand (multilingual rules)
       verify     https, host allow-list, discount sanity (<= 90 %), stock, no invented discounts
       store      SQLite: listings, price history, run log (health)
       export     public/data/listings.json + meta.json
  └─ deploy public/ to GitHub Pages (static, CDN, free)
Browser: public/index.html  (vanilla JS, no build step; search, filters, sort, location, watchlist, PWA)
```

Why this shape: data changes every few hours, not every second, so a static site regenerated on a schedule gives instant pages, zero servers and zero cost. When traffic or update frequency demands it, move the crawler to a small VPS or Cloudflare Workers + D1 without touching the frontend (it only reads two JSON files).

## Run locally

```bash
python data/snapshots/2026-11-15_manual.py   # build the seed snapshot JSON
python -m fyndradar --offline                 # snapshot only (no network)
python -m fyndradar                           # all enabled sources (network)
python -m fyndradar --only inet_se            # one source
python -m unittest discover -s tests
python -m http.server -d public 8000          # open http://localhost:8000
python build_artifact.py                      # single-file HTML with data inlined (dist/)
```

## Adding a source

1. Retailer publishes schema.org JSON-LD on product pages (most do): add a `jsonld` entry in `data/sources/sources.json` with a listing URL (`{page}` placeholder) or sitemap, plus a `link_pattern` regex that matches outlet/demo product URLs. No code.
2. Affiliate feed: add a `feed` entry, put the feed URL in a GitHub secret, reference it as `${SECRET_NAME}`.
3. Neither: write a small adapter in `fyndradar/adapters/` (see `inet.py`) and a fixture test.

`allowed_hosts` keeps a misconfigured source from publishing foreign links.

## Source status (2026-11-15)

| Source | Market | Method | Status |
|---|---|---|---|
| Inet Fyndhörnan | SE | HTML listing | Enabled. Server-rendered; selectors built from page text, confirm on first networked run |
| Proshop demo | DK/SE/NO | JSON-LD | Enabled. DK verified (demo SKUs end in `d`); SE/NO URLs follow the same platform |
| Thomann B-stock | DK | JSON-LD via sitemap | Disabled until sitemap path confirmed; affiliate feed preferred |
| Elgiganten / Elkjøp outlet | SE/DK/NO | needs feed or headless browser | Blocked: pages render client-side, no product data in HTML |
| Komplett demovarer | NO | needs feed or headless browser | Blocked: same as above |
| Adtraction / Partner-ads / Awin | all | affiliate XML/CSV | Templates ready; blocked on publisher approval |

See `docs/STRATEGY.md` for business model, legal notes and roadmap.
