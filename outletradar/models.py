"""Core data model for FyndRadar listings."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from typing import Optional

# Condition taxonomy shared by every adapter. Ordered from best to worst.
CONDITIONS = (
    "open_box",          # opened packaging, unused / complete
    "demo",              # display or demo unit
    "returned",          # customer return, checked
    "manufacturer_replacement",
    "refurbished",       # professionally refurbished
    "damaged_packaging",
    "used",              # visible wear or incomplete
    "clearance",         # new, last units / outlet price
    "last_chance",       # being discontinued, current price only
    "unknown",
)

COUNTRIES = ("SE", "DK", "NO")
CURRENCIES = {"SE": "SEK", "DK": "DKK", "NO": "NOK"}


@dataclass
class Listing:
    source: str                     # adapter id, e.g. "inet_se"
    retailer: str                   # display name
    country: str                    # SE / DK / NO (market the offer is sold in)
    currency: str
    title: str
    price: float
    url: str
    observed_at: str                # ISO-8601 time the data was read
    regular_price: Optional[float] = None
    condition: str = "unknown"
    condition_text: Optional[str] = None
    category: str = "other"
    brand: Optional[str] = None
    image_url: Optional[str] = None
    url_kind: str = "product"       # product | search | listing
    availability_text: Optional[str] = None
    in_stock: Optional[bool] = None
    store: Optional[str] = None     # physical store holding the unit, if any
    lat: Optional[float] = None
    lon: Optional[float] = None
    delivery: bool = True
    gtin: Optional[str] = None
    sku: Optional[str] = None
    affiliate_url: Optional[str] = None
    extra: dict = field(default_factory=dict)

    @property
    def discount_pct(self) -> Optional[float]:
        if self.regular_price and self.regular_price > self.price > 0:
            return round(100.0 * (self.regular_price - self.price) / self.regular_price, 1)
        return None

    @property
    def id(self) -> str:
        """Stable id: one physical offer at one retailer.

        Unique units (e.g. Inet's x256229 vs x256228) keep their own URL, so the
        URL is the primary key; search/listing links fall back to title+price.
        """
        if self.url_kind == "product":
            key = f"{self.source}|{self.url}"
        else:
            key = f"{self.source}|{self.title.lower()}|{self.price}"
        return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]

    def to_public(self) -> dict:
        d = asdict(self)
        d.pop("extra", None)
        d["id"] = self.id
        d["discount_pct"] = self.discount_pct
        d["link"] = self.affiliate_url or self.url
        return {k: v for k, v in d.items() if v is not None}
