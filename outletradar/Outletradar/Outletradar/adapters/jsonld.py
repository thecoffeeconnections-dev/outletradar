"""Generic schema.org adapter.

Most Nordic retailers publish Product/Offer JSON-LD on product pages for Google
Shopping. This adapter discovers product URLs (from listing pages or XML
sitemaps, filtered by a regex such as 'demo|outlet|b-stock') and reads the
JSON-LD of each page. It works for any retailer that does this, which makes it
the default way to add a new source without custom code.
"""
from __future__ import annotations

import json
import re
from typing import Iterator
from urllib.parse import urljoin

from .base import Adapter, register
from . import dom


def extract_products(html: str, base_url: str) -> list[dict]:
    root = dom.parse(html)
    out = []
    for s in root.find_all("script", lambda n: "ld+json" in n.attrs.get("type", "")):
        try:
            data = json.loads(s.raw_text().strip())
        except (json.JSONDecodeError, ValueError):
            continue
        for obj in _walk(data):
            rec = _product_to_record(obj, base_url)
            if rec:
                out.append(rec)
    return out


def _walk(data):
    if isinstance(data, list):
        for d in data:
            yield from _walk(d)
    elif isinstance(data, dict):
        t = data.get("@type")
        types = t if isinstance(t, list) else [t]
        if "Product" in types or "ProductGroup" in types:
            yield data
        for key in ("@graph", "itemListElement", "item", "hasVariant", "mainEntity"):
            if key in data:
                yield from _walk(data[key])


def _first(v):
    return v[0] if isinstance(v, list) and v else v


def _product_to_record(p: dict, base_url: str):
    offers = p.get("offers") or {}
    if isinstance(offers, dict) and offers.get("@type") == "AggregateOffer":
        offers = offers.get("offers") or offers
    offer = _first(offers) if offers else {}
    if not isinstance(offer, dict):
        return None
    price = offer.get("price") or offer.get("lowPrice")
    spec = offer.get("priceSpecification")
    regular = None
    if isinstance(spec, list):
        for sp in spec:
            if isinstance(sp, dict) and "ListPrice" in str(sp.get("priceType", "")):
                regular = sp.get("price")
            elif isinstance(sp, dict) and price is None:
                price = sp.get("price")
    elif isinstance(spec, dict) and price is None:
        price = spec.get("price")
    if price is None or not p.get("name"):
        return None
    cond = str(offer.get("itemCondition") or p.get("itemCondition") or "")
    avail = str(offer.get("availability") or "")
    brand = p.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")
    img = _first(p.get("image"))
    if isinstance(img, dict):
        img = img.get("url") or img.get("contentUrl")
    url = offer.get("url") or p.get("url") or base_url
    return {
        "title": p.get("name"),
        "price": price,
        "regular_price": regular,
        "currency": offer.get("priceCurrency") or (spec.get("priceCurrency") if isinstance(spec, dict) else None),
        "condition_text": " ".join(x for x in [cond.rsplit("/", 1)[-1], p.get("name", "")] if x),
        "schema_condition": cond.rsplit("/", 1)[-1] or None,
        "url": urljoin(base_url, url),
        "image_url": urljoin(base_url, img) if isinstance(img, str) else None,
        "availability_text": avail.rsplit("/", 1)[-1] or None,
        "in_stock": ("InStock" in avail or "LimitedAvailability" in avail) if avail else None,
        "brand": brand if isinstance(brand, str) else None,
        "gtin": p.get("gtin13") or p.get("gtin") or p.get("gtin8"),
        "sku": p.get("sku"),
    }


def links_from_listing(html: str, base_url: str, pattern: str) -> list[str]:
    rx = re.compile(pattern, re.I)
    root = dom.parse(html)
    seen, out = set(), []
    for a in root.find_all("a"):
        href = a.attrs.get("href")
        if href and rx.search(href):
            u = urljoin(base_url, href.split("#")[0])
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out


def links_from_sitemap(xml: str, pattern: str) -> list[str]:
    rx = re.compile(pattern, re.I)
    return [u for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml) if rx.search(u)]


@register("jsonld")
class JsonLdAdapter(Adapter):
    """cfg: listing_urls[] and/or sitemaps[], link_pattern, max_products, pages (template with {page})."""

    def discover(self) -> list[str]:
        pat = self.cfg.get("link_pattern", r"/produ")
        urls: list[str] = []
        for su in self.cfg.get("sitemaps", []):
            xml = self.fetcher.get(su, accept="application/xml,text/xml")
            nested = re.findall(r"<sitemap>\s*<loc>\s*([^<\s]+)", xml)
            for n in nested[: self.cfg.get("max_sitemaps", 20)]:
                if re.search(self.cfg.get("sitemap_pattern", "."), n):
                    urls += links_from_sitemap(self.fetcher.get(n, accept="application/xml"), pat)
            urls += links_from_sitemap(xml, pat)
        for lu in self.cfg.get("listing_urls", []):
            pages = self.cfg.get("pages", 1)
            for i in range(1, pages + 1):
                u = lu.format(page=i) if "{page}" in lu else lu
                urls += links_from_listing(self.fetcher.get(u), u, pat)
                if "{page}" not in lu:
                    break
        return list(dict.fromkeys(urls))[: self.cfg.get("max_products", 300)]

    def records(self) -> Iterator[dict]:
        for url in self.discover():
            try:
                html = self.fetcher.get(url)
            except Exception as e:  # keep going; health report counts failures
                yield {"_error": f"{url}: {e}"}
                continue
            for rec in extract_products(html, url):
                rec.setdefault("url", url)
                yield rec
