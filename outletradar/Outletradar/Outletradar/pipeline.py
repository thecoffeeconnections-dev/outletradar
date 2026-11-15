"""Run all enabled sources -> normalise -> verify -> persist -> export static JSON."""
from __future__ import annotations

import json
import os
import sys
import traceback
from collections import Counter
from pathlib import Path

from .adapters import REGISTRY
from .http import Fetcher
from .models import Listing, CURRENCIES
from .normalize import classify_category, classify_condition, clean_title, guess_brand, parse_price
from .store import Store, now_iso
from .verify import check

ROOT = Path(__file__).resolve().parent.parent


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def build_listing(rec: dict, cfg: dict, stores: dict, run_at: str) -> Listing:
    country = rec.get("country") or cfg["country"]
    price = parse_price(rec.get("price"))
    title = clean_title(rec.get("title", ""))
    cond_text = rec.get("condition_text")
    l = Listing(
        source=rec.get("source") or cfg["id"],
        retailer=rec.get("retailer") or cfg["retailer"],
        country=country,
        currency=(rec.get("currency") or cfg.get("currency") or CURRENCIES.get(country, "SEK")).upper(),
        title=title,
        price=price,
        regular_price=parse_price(rec.get("regular_price")),
        url=rec.get("url"),
        url_kind=rec.get("url_kind", "product"),
        observed_at=rec.get("observed_at") or run_at,
        condition_text=cond_text,
        condition=rec.get("condition") or classify_condition(cond_text, rec.get("schema_condition"), title, cfg.get("default_condition_hint")),
        category=rec.get("category") or classify_category(title, rec.get("category_hint")),
        brand=rec.get("brand") or guess_brand(title),
        image_url=rec.get("image_url"),
        availability_text=rec.get("availability_text"),
        in_stock=rec.get("in_stock"),
        store=rec.get("store"),
        delivery=rec.get("delivery", cfg.get("delivery", True)),
        gtin=rec.get("gtin"),
        sku=rec.get("sku"),
        affiliate_url=rec.get("affiliate_url"),
    )
    if l.condition == "unknown" and cfg.get("default_condition"):
        l.condition = cfg["default_condition"]
    st = stores.get(l.store or "")
    if st:
        l.lat, l.lon = st["lat"], st["lon"]
    return l


def run(config_path: Path, db_path: Path, out_dir: Path, only: list[str] | None = None, offline: bool = False) -> dict:
    cfg_all = load_json(config_path)
    stores = load_json(ROOT / "data/sources/stores.json")
    fetcher = Fetcher(ROOT / ".cache", min_interval=cfg_all.get("min_interval_s", 3.0))
    store = Store(db_path)
    run_at = now_iso()
    summary = {}
    for cfg in cfg_all["sources"]:
        if not cfg.get("enabled", True) or (only and cfg["id"] not in only):
            continue
        if offline and cfg["adapter"] != "manual_snapshot":
            continue
        adapter = REGISTRY[cfg["adapter"]](cfg, fetcher)
        fetched, kept, dropped, seen, err = 0, 0, Counter(), set(), None
        try:
            for rec in adapter.records():
                if "_error" in rec:
                    dropped["fetch_error"] += 1
                    err = rec["_error"]
                    continue
                fetched += 1
                try:
                    l = build_listing(rec, cfg, stores, run_at)
                except Exception:
                    dropped["parse_error"] += 1
                    continue
                reason = check(l, cfg.get("allowed_hosts"))
                if reason:
                    dropped[reason] += 1
                    continue
                pub = l.to_public()
                store.upsert(pub, l.observed_at if cfg["adapter"] == "manual_snapshot" else run_at)
                seen.add(pub["id"])
                kept += 1
            ok = fetched > 0 and err is None
        except Exception as e:  # source down / layout changed: keep previous data, report it
            ok, err = False, f"{type(e).__name__}: {e}"
            traceback.print_exc(file=sys.stderr)
        if ok and cfg["adapter"] != "manual_snapshot":
            store.mark_missing(cfg["id"], seen)
        store.log_run(cfg["id"], ok, fetched, kept, dict(dropped), err)
        summary[cfg["id"]] = {"ok": ok, "fetched": fetched, "kept": kept, "dropped": dict(dropped), "error": err}
        print(f"[{cfg['id']}] ok={ok} fetched={fetched} kept={kept} dropped={dict(dropped)} {err or ''}")
    store.commit()
    export(store, out_dir, cfg_all, run_at)
    return summary


def export(store: Store, out_dir: Path, cfg_all: dict, run_at: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    listings = store.active()
    listings.sort(key=lambda d: (-(d.get("discount_pct") or 0), d["price"]))
    (out_dir / "listings.json").write_text(json.dumps(listings, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    meta = {
        "generated_at": run_at,
        "count": len(listings),
        "by_country": dict(Counter(l["country"] for l in listings)),
        "by_retailer": dict(Counter(l["retailer"] for l in listings)),
        "sources": [
            {k: s.get(k) for k in ("id", "retailer", "country", "adapter", "enabled", "status_note")}
            for s in cfg_all["sources"]
        ],
        "health": store.health(),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(prog="fyndradar")
    ap.add_argument("--config", default=str(ROOT / "data/sources/sources.json"))
    ap.add_argument("--db", default=os.environ.get("FYNDRADAR_DB", str(ROOT / "data/fyndradar.sqlite")))
    ap.add_argument("--out", default=str(ROOT / "public/data"))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--offline", action="store_true", help="only manual snapshots (no network)")
    a = ap.parse_args(argv)
    run(Path(a.config), Path(a.db), Path(a.out), a.only, a.offline)


if __name__ == "__main__":
    main()
