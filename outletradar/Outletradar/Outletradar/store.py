"""SQLite persistence: current listings, price history, run log. Zero-cost, file-based."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS listing (
  id TEXT PRIMARY KEY, source TEXT, data TEXT,
  first_seen TEXT, last_seen TEXT, active INTEGER DEFAULT 1, misses INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS price (id TEXT, at TEXT, price REAL, PRIMARY KEY (id, at));
CREATE TABLE IF NOT EXISTS run (
  at TEXT, source TEXT, ok INTEGER, fetched INTEGER, kept INTEGER, dropped TEXT, error TEXT
);
CREATE INDEX IF NOT EXISTS listing_active ON listing(active, source);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Store:
    def __init__(self, path: Path):
        self.db = sqlite3.connect(str(path))
        self.db.executescript(SCHEMA)

    def upsert(self, listing_public: dict, seen_at: str):
        lid, src = listing_public["id"], listing_public["source"]
        row = self.db.execute("SELECT data, first_seen FROM listing WHERE id=?", (lid,)).fetchone()
        last_price = None
        if row:
            last_price = json.loads(row[0]).get("price")
            self.db.execute("UPDATE listing SET data=?, last_seen=?, active=1, misses=0 WHERE id=?",
                            (json.dumps(listing_public, ensure_ascii=False), seen_at, lid))
        else:
            self.db.execute("INSERT INTO listing VALUES (?,?,?,?,?,1,0)",
                            (lid, src, json.dumps(listing_public, ensure_ascii=False), seen_at, seen_at))
        if last_price != listing_public["price"]:
            self.db.execute("INSERT OR REPLACE INTO price VALUES (?,?,?)", (lid, seen_at, listing_public["price"]))

    def mark_missing(self, source: str, seen_ids: set[str], max_misses: int = 2):
        """Listings a healthy run did not see are retired after `max_misses` runs (sold or removed)."""
        for (lid,) in self.db.execute("SELECT id FROM listing WHERE source=? AND active=1", (source,)).fetchall():
            if lid not in seen_ids:
                self.db.execute("UPDATE listing SET misses=misses+1 WHERE id=?", (lid,))
        self.db.execute("UPDATE listing SET active=0 WHERE source=? AND misses>=?", (source, max_misses))

    def log_run(self, source, ok, fetched, kept, dropped: dict, error=None):
        self.db.execute("INSERT INTO run VALUES (?,?,?,?,?,?,?)",
                        (now_iso(), source, int(ok), fetched, kept, json.dumps(dropped), error))

    def active(self) -> list[dict]:
        out = []
        for lid, data, first_seen, last_seen in self.db.execute(
                "SELECT id, data, first_seen, last_seen FROM listing WHERE active=1"):
            d = json.loads(data)
            d["first_seen"], d["last_seen"] = first_seen, last_seen
            hist = self.db.execute("SELECT at, price FROM price WHERE id=? ORDER BY at", (lid,)).fetchall()
            if len(hist) > 1:
                d["history"] = [list(h) for h in hist[-20:]]
            out.append(d)
        return out

    def health(self) -> list[dict]:
        q = """SELECT source, at, ok, fetched, kept, dropped, error FROM run r
               WHERE at = (SELECT MAX(at) FROM run WHERE source=r.source)"""
        return [dict(zip(("source", "at", "ok", "fetched", "kept", "dropped", "error"), r)) for r in self.db.execute(q)]

    def commit(self):
        self.db.commit()
