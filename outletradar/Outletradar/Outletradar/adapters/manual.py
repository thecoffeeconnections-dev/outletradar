"""Ingest manually captured snapshots (data/snapshots/*.json).

Used to seed the site with real, source-linked listings before live crawling is
enabled. Each record keeps its own observed_at so the UI can show its age.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from .base import Adapter, register


@register("manual_snapshot")
class ManualSnapshot(Adapter):
    def records(self) -> Iterator[dict]:
        base = Path(self.cfg["path"])
        if not base.is_absolute():
            base = Path(__file__).resolve().parents[2] / base
        for p in sorted(base.glob(self.cfg.get("glob", "*.json"))):
            for rec in json.loads(p.read_text(encoding="utf-8")):
                if self.cfg.get("source_filter") and rec.get("source") not in self.cfg["source_filter"]:
                    continue
                yield rec
