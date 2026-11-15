"""Kjell & Company outlet (https://www.kjell.com/se/outlet).

Outlet pages (…-pNNNNN?outlet=a|b|c) are individual returned units. Their JSON-LD
describes the NEW product (new price, link to the new product page), so the
generic jsonld adapter must not be used here. We read the outlet page itself:
  - outlet price: <meta property="product:price:amount">
  - new price:    text "Ny för 3 149:-"
  - grade:        "Nyskick" / "Mycket bra skick" / "Bra skick"
  - title/image:  og:title / h1, og:image
The listing URL is kept as the product URL so the visitor lands on the outlet unit.
"""
from __future__ import annotations

import re
from typing import Iterator

from .base import Adapter, register
from . import dom
from .jsonld import links_from_listing
from ..normalize import parse_price

GRADES = {"nyskick": "open_box", "mycket bra skick": "returned", "bra skick": "used"}
NEW_RX = re.compile(r"Ny\s+för\s*([\d\s  .]+)\s*(?::-|kr)", re.I)
GRADE_RX = re.compile(r"\b(Mycket bra skick|Bra skick|Nyskick)\b", re.I)
STOCK_RX = re.compile(r"Finns i (\d+) butik(?:er)?", re.I)


def _meta(root, *names):
    for m in root.find_all("meta"):
        k = m.attrs.get("property") or m.attrs.get("name") or ""
        if k in names and m.attrs.get("content"):
            return m.attrs["content"].strip()
    return None


def parse_outlet_page(html: str, url: str) -> dict | None:
    root = dom.parse(html)
    price = parse_price(_meta(root, "product:price:amount", "og:price:amount"))
    if price is None:
        return None
    for s in root.find_all("script") + root.find_all("style"):
        s.children = []
    text = root.get_text(" ")
    h1 = next(iter(root.find_all("h1")), None)
    title = (h1.get_text(" ").strip() if h1 else "") or (_meta(root, "og:title") or "")
    title = re.sub(r"\s*[|\-–]\s*Kjell.*$", "", title).strip()
    if not title:
        return None
    m = NEW_RX.search(text)
    regular = parse_price(m.group(1)) if m else None
    g = GRADE_RX.search(text)
    grade = g.group(1).capitalize() if g else None
    if grade and grade.lower() == "mycket bra skick":
        grade = "Mycket bra skick"
    st = STOCK_RX.search(text)
    return {
        "title": title,
        "price": price,
        "regular_price": regular if regular and regular > price else None,
        "currency": _meta(root, "product:price:currency") or "SEK",
        "condition": GRADES.get((grade or "").lower(), "returned"),
        "condition_text": f"Outlet, skick: {grade}" if grade else "Outlet (returvara)",
        "url": url,
        "image_url": _meta(root, "og:image"),
        "availability_text": f"Finns i {st.group(1)} butik{'er' if st.group(1) != '1' else ''}" if st else None,
    }


@register("kjell_outlet")
class KjellOutletAdapter(Adapter):
    """cfg: listing_urls (with {page}), pages, link_pattern, max_products."""

    def discover(self) -> list[str]:
        pat = self.cfg.get("link_pattern", r"\?outlet=[abc]")
        urls: list[str] = []
        for lu in self.cfg.get("listing_urls", []):
            for i in range(1, self.cfg.get("pages", 1) + 1):
                u = lu.format(page=i)
                found = links_from_listing(self.fetcher.get(u), u, pat)
                if not found:
                    break
                urls += found
        return list(dict.fromkeys(urls))[: self.cfg.get("max_products", 400)]

    def records(self) -> Iterator[dict]:
        for url in self.discover():
            try:
                rec = parse_outlet_page(self.fetcher.get(url), url)
            except Exception as e:
                yield {"_error": f"{url}: {e}"}
                continue
            if rec:
                yield rec
