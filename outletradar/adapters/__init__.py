"""Source adapters. Each adapter turns one retailer/feed into raw record dicts.

Raw record keys (all optional except title/price/url):
  title, price, regular_price, currency, condition_text, url, url_kind,
  image_url, availability_text, in_stock, store, brand, gtin, sku, category_hint
"""
from .base import Adapter, REGISTRY, register  # noqa: F401
from . import jsonld, inet, feeds, manual, kjell  # noqa: F401  (registers adapters)
