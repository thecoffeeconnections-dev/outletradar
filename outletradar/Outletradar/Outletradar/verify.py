"""Verification rules. A listing that fails is dropped and counted, never 'fixed' by guessing."""
from __future__ import annotations

from urllib.parse import urlparse

from .models import Listing, COUNTRIES

MAX_DISCOUNT = 90.0      # above this we suspect a parse error or a wrong regular price
MIN_PRICE = 1.0


def check(l: Listing, allowed_hosts: list[str] | None = None) -> str | None:
    """Return None if valid, else a short reason code."""
    if not l.title or len(l.title) < 3:
        return "no_title"
    if l.price is None or l.price < MIN_PRICE:
        return "bad_price"
    if l.country not in COUNTRIES:
        return "bad_country"
    u = urlparse(l.url or "")
    if u.scheme != "https" or not u.netloc:
        return "bad_url"
    if allowed_hosts and not any(u.netloc == h or u.netloc.endswith("." + h) for h in allowed_hosts):
        return "foreign_host"
    if l.regular_price is not None:
        if l.regular_price <= l.price:
            l.regular_price = None          # no proven discount: show price only
        elif l.discount_pct and l.discount_pct > MAX_DISCOUNT:
            return "implausible_discount"
    if l.in_stock is False:
        return "out_of_stock"
    return None
