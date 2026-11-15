"""Inet Fyndhörnan (https://www.inet.se/fyndhornan).

The listing is server-rendered: each card holds title, 'Fyndvara: <condition>',
stock count, regular price and fynd price. We parse cards structurally (anchor
to /produkt/ + nearest ancestor that carries both prices) so small markup
changes don't break it, and fall back to embedded JSON (Next.js data) or
JSON-LD when present.
"""
from __future__ import annotations

import json
import re
from typing import Iterator
from urllib.parse import urljoin

from .base import Adapter, register
from . import dom
from .jsonld import extract_products
from ..normalize import parse_price

PRICE_RX = re.compile(r"(\d{1,3}(?:[   ]\d{3})*|\d+)\s*kr", re.I)
COND_RX = re.compile(r"Fyndvara:\s*(.+?)(?=(?:\d(?:[,.]\d)? av 5 stjärnor)|\d+ st|$)", re.I)


def parse_cards(html: str, base_url: str) -> list[dict]:
    root = dom.parse(html)
    out, seen = [], set()
    for a in root.find_all("a", lambda n: "/produkt/" in n.attrs.get("href", "")):
        url = urljoin(base_url, a.attrs["href"].split("?")[0])
        if url in seen:
            continue
        card, node = None, a
        for _ in range(8):
            node = node.parent
            if node is None:
                break
            hrefs = {n.attrs.get("href", "").split("?")[0] for n in node.find_all("a", lambda n: "/produkt/" in n.attrs.get("href", ""))}
            if len(hrefs) > 1:
                break  # climbed past the card into the list
            txt = node.get_text()
            if len(PRICE_RX.findall(txt)) >= 1 and "Fyndvara" in txt:
                card = node
                break
            if len(txt) > 1500:
                break
        if card is None:
            continue
        txt = card.get_text()
        prices = [parse_price(p) for p in PRICE_RX.findall(txt)]
        prices = [p for p in prices if p]
        if not prices:
            continue
        title = a.attrs.get("title") or a.get_text()
        if not title or len(title) < 3:
            h = card.find_all(None, lambda n: n.tag in ("h2", "h3", "h4"))
            title = h[0].get_text() if h else None
        if not title:
            continue
        title = re.sub(r"^[−-]\d+%\s*", "", title).strip()
        m = COND_RX.search(txt)
        img = card.find_all("img")
        img_url = None
        if img:
            src = img[0].attrs.get("src") or img[0].attrs.get("data-src") or (img[0].attrs.get("srcset") or "").split(" ")[0]
            img_url = urljoin(base_url, src) if src else None
        stock = re.search(r"(\d+)\s*st\b", txt)
        seen.add(url)
        out.append({
            "title": title,
            "price": min(prices),
            "regular_price": max(prices) if len(prices) > 1 and max(prices) > min(prices) else None,
            "currency": "SEK",
            "condition_text": m.group(1).strip() if m else None,
            "url": url,
            "image_url": img_url,
            "availability_text": f"{stock.group(1)} st i lager" if stock else None,
            "in_stock": True,
        })
    return out


def parse_embedded_json(html: str, base_url: str) -> list[dict]:
    m = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return []
    out = []

    def walk(o):
        if isinstance(o, dict):
            name = o.get("name") or o.get("title")
            price = o.get("price")
            if isinstance(price, dict):
                price = price.get("price") or price.get("value")
            url = o.get("url") or o.get("href")
            if name and price and url and "/produkt/" in str(url):
                out.append({"title": name, "price": price, "regular_price": o.get("listPrice") or o.get("ordinaryPrice"),
                            "currency": "SEK", "url": urljoin(base_url, url),
                            "condition_text": o.get("conditionDescription") or o.get("description")})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    return out


@register("inet")
class InetAdapter(Adapter):
    def records(self) -> Iterator[dict]:
        base = self.cfg.get("url", "https://www.inet.se/fyndhornan")
        seen = set()
        for page in range(1, self.cfg.get("max_pages", 40) + 1):
            url = base if page == 1 else f"{base}?page={page}"
            html = self.fetcher.get(url)
            recs = parse_cards(html, url) or parse_embedded_json(html, url) or extract_products(html, url)
            new = [r for r in recs if r["url"] not in seen]
            if not new:
                break  # pagination exhausted (or same page served again)
            for r in new:
                seen.add(r["url"])
                r["url_kind"] = "product"
                yield r
