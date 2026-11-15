"""Affiliate product feeds: the clean, contractual data path.

Supported formats:
  - adtraction  : Adtraction XML feed (API v3 or feed URL from the partner UI)
  - google      : Google Merchant / RSS 2.0 with g: namespace (many retailers expose this)
  - awin_csv    : Awin 'Create-a-Feed' CSV
  - partnerads  : Partner-ads (DK) XML feed

Feeds contain the whole catalogue, so we keep only second-chance offers:
condition != new, or outlet/demo keywords in title/category/labels, or
(optionally) a sale price at least `min_discount_pct` below the regular price.
"""
from __future__ import annotations

import csv
import io
import re
import xml.etree.ElementTree as ET
from typing import Iterator

from .base import Adapter, register
from ..normalize import parse_price

SECOND_CHANCE_RX = re.compile(
    r"outlet|demo|b-?vare|b-?stock|b-?grade|fyndvar|fynd\b|begagn|refurb|renover|returvar|retur\b|open[- ]?box|"
    r"öppnad förpackning|brugt|brukt|used|udstillingsmodel|utstillingsmodell|ex-display|2nd ?hand|second hand",
    re.I,
)

ALIASES = {
    "title": ["name", "title", "productname", "product_name", "produktnavn", "g:title"],
    "price": ["price", "search_price", "saleprice", "sale_price", "nypris", "g:sale_price", "g:price", "store_price"],
    "regular_price": ["originalprice", "original_price", "rrp_price", "regularprice", "glpris", "listprice", "g:price", "product_price_old"],
    "url": ["trackingurl", "aw_deep_link", "deeplink", "vareurl", "link", "g:link", "producturl", "product_url"],
    "product_url": ["producturl", "merchant_deep_link", "product_url", "g:link", "link"],
    "image_url": ["imageurl", "image_url", "merchant_image_url", "aw_image_url", "billedurl", "g:image_link", "image"],
    "currency": ["currency", "valuta"],
    "condition": ["condition", "g:condition", "stand", "tilstand"],
    "category": ["category", "categories", "merchant_category", "kategorinavn", "g:product_type", "g:google_product_category"],
    "brand": ["brand", "brand_name", "brandname", "manufacturer", "g:brand", "producent"],
    "in_stock": ["instock", "in_stock", "stock_status", "g:availability", "lagerantal", "availability"],
    "gtin": ["ean", "gtin", "g:gtin"],
    "sku": ["sku", "aw_product_id", "id", "g:id", "varenummer"],
    "labels": ["custom_label_0", "g:custom_label_0", "custom_label_1", "g:custom_label_1"],
}


def _pick(row: dict, field: str):
    for k in ALIASES[field]:
        v = row.get(k)
        if v not in (None, ""):
            return v
    return None


def _norm_keys(d: dict) -> dict:
    return {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in d.items() if k}


def iter_xml_items(xml_text: str) -> Iterator[dict]:
    """Yield one flat dict per product element, namespace prefixes kept as 'g:'."""
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    item_tags = {"product", "item", "entry", "produkt", "offer"}
    for el in root.iter():
        local = el.tag.split("}")[-1].lower()
        if local in item_tags and len(el):
            row = {}
            for c in el:
                tag = c.tag
                if tag.startswith("{http://base.google.com/ns/1.0}"):
                    tag = "g:" + tag.split("}")[1]
                else:
                    tag = tag.split("}")[-1]
                row[tag.lower()] = (c.text or "").strip()
            yield row


def row_to_record(row: dict) -> dict | None:
    row = _norm_keys(row)
    title, price = _pick(row, "title"), parse_price(_pick(row, "price"))
    reg = parse_price(_pick(row, "regular_price"))
    if reg is not None and price is not None and reg < price:
        reg = None
    if not title or not price:
        return None
    stock_raw = str(_pick(row, "in_stock") or "").lower()
    in_stock = None
    if stock_raw:
        in_stock = stock_raw not in ("0", "false", "no", "out of stock", "out_of_stock", "nej", "nei")
    return {
        "title": title,
        "price": price,
        "regular_price": reg,
        "currency": (_pick(row, "currency") or "").upper() or _currency_from_price(_pick(row, "price")),
        "condition_text": " ".join(str(x) for x in [_pick(row, "condition"), _pick(row, "labels")] if x) or None,
        "schema_condition": (_pick(row, "condition") or "").lower() or None,
        "url": _pick(row, "url"),
        "product_url": _pick(row, "product_url"),
        "image_url": _pick(row, "image_url"),
        "category_hint": _pick(row, "category"),
        "brand": _pick(row, "brand"),
        "in_stock": in_stock,
        "gtin": _pick(row, "gtin"),
        "sku": _pick(row, "sku"),
    }


def _currency_from_price(s):
    m = re.search(r"\b(SEK|DKK|NOK|EUR)\b", str(s or ""), re.I)
    return m.group(1).upper() if m else None


def is_second_chance(rec: dict, min_discount_pct: float | None) -> bool:
    cond = (rec.get("schema_condition") or "").lower()
    if cond and cond not in ("new", "ny", "newcondition", "ny vare"):
        return True
    blob = " ".join(str(rec.get(k) or "") for k in ("title", "category_hint", "condition_text", "url", "product_url"))
    if SECOND_CHANCE_RX.search(blob):
        return True
    if min_discount_pct and rec.get("regular_price"):
        return (rec["regular_price"] - rec["price"]) / rec["regular_price"] * 100 >= min_discount_pct
    return False


@register("feed")
class FeedAdapter(Adapter):
    """cfg: format (adtraction|google|awin_csv|partnerads), url (may contain ${ENV} tokens), min_discount_pct."""

    def records(self) -> Iterator[dict]:
        import os
        missing = [t for t in re.findall(r"\$\{(\w+)\}", self.cfg["url"]) if not os.environ.get(t)]
        if missing:
            yield {"_error": f"missing credentials: set {', '.join(missing)}"}
            return
        url = re.sub(r"\$\{(\w+)\}", lambda m: os.environ[m.group(1)], self.cfg["url"])
        body = self.fetcher.get(url, accept="application/xml,text/csv,*/*")
        fmt = self.cfg.get("format", "google")
        rows = csv.DictReader(io.StringIO(body)) if fmt == "awin_csv" else iter_xml_items(body)
        mdp = self.cfg.get("min_discount_pct")
        for row in rows:
            rec = row_to_record(row)
            if rec and is_second_chance(rec, mdp):
                rec["affiliate_url"] = rec.pop("url")
                rec["url"] = rec.pop("product_url") or rec["affiliate_url"]
                rec["url_kind"] = "product"
                yield rec
