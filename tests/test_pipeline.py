"""Unit tests. Fixtures under tests/fixtures are synthetic markup for parser tests only;
they never reach the published data."""
import json
import tempfile
import unittest
from pathlib import Path

from outletradar.adapters.feeds import iter_xml_items, row_to_record, is_second_chance
from outletradar.adapters.inet import parse_cards
from outletradar.adapters.jsonld import extract_products, links_from_listing
from outletradar.models import Listing
from outletradar.normalize import classify_category, classify_condition, parse_price, guess_brand
from outletradar.store import Store
from outletradar.verify import check

FIX = Path(__file__).parent / "fixtures"


class Normalize(unittest.TestCase):
    def test_prices(self):
        cases = {"1 299 kr": 1299, "1.299,00 kr.": 1299, "1599,-": 1599, "12 990:-": 12990,
                 "554,00 kr.": 554, "Hinta 100.00€": 100, "4 999 kr": 4999, "1299.00 SEK": 1299}
        for s, v in cases.items():
            self.assertEqual(parse_price(s), v, s)
        self.assertIsNone(parse_price(""))

    def test_condition(self):
        self.assertEqual(classify_condition("Öppnad förpackning, komplett med alla tillbehör."), "open_box")
        self.assertEqual(classify_condition("Demoexemplar, komplett med alla tillbehör"), "demo")
        self.assertEqual(classify_condition("Ersättningsprodukt från tillverkaren"), "manufacturer_replacement")
        self.assertEqual(classify_condition("Spår av användning förekommer, defekta pixlar."), "used")
        self.assertEqual(classify_condition("Skadad förpackning, komplett"), "damaged_packaging")
        self.assertEqual(classify_condition("Som ny - Komplett i originalemballasje"), "open_box")
        self.assertEqual(classify_condition("B-stock med fuld garanti"), "returned")
        self.assertEqual(classify_condition("Refurbished Grade A"), "refurbished")
        self.assertEqual(classify_condition(None), "unknown")

    def test_category_brand(self):
        self.assertEqual(classify_category("ASUS 27\" ROG Swift PG27AQN IPS QHD 360 Hz G-Sync"), "monitors")
        self.assertEqual(classify_category("Sapphire Radeon RX 9070 XT 16GB Nitro+"), "components")
        self.assertEqual(classify_category("Apple MacBook Air (2025)"), "computers")
        self.assertEqual(classify_category("Electrolux mikrobølgeovn KMFE171TEX"), "appliances")
        self.assertEqual(guess_brand("Fractal Design Refine Alcantara Dark"), "Fractal Design")


class Parsers(unittest.TestCase):
    def test_inet_cards(self):
        recs = parse_cards((FIX / "inet_listing.html").read_text(encoding="utf-8"), "https://www.inet.se/fyndhornan")
        self.assertEqual(len(recs), 2)
        a = recs[0]
        self.assertEqual(a["title"], "LG 27\" 27UP850K IPS 4K USB-C")
        self.assertEqual((a["price"], a["regular_price"]), (4999, 5490))
        self.assertTrue(a["url"].startswith("https://www.inet.se/produkt/"))
        self.assertIn("Öppnad förpackning", a["condition_text"])
        self.assertEqual(a["image_url"], "https://cdn.inet.se/product/img/1.jpg")

    def test_jsonld(self):
        html = (FIX / "product_jsonld.html").read_text(encoding="utf-8")
        p = extract_products(html, "https://www.proshop.dk/x/y/123d")[0]
        self.assertEqual(p["price"], "443.20")
        self.assertEqual(p["currency"], "DKK")
        self.assertEqual(p["schema_condition"], "UsedCondition")
        self.assertTrue(p["in_stock"])
        links = links_from_listing('<a href="/A/B-DEMO/111d">x</a><a href="/A/C/222">y</a>', "https://www.proshop.dk/Demo", r"DEMO/\d+d$")
        self.assertEqual(links, ["https://www.proshop.dk/A/B-DEMO/111d"])

    def test_google_feed(self):
        rows = list(iter_xml_items((FIX / "google_feed.xml").read_text(encoding="utf-8")))
        recs = [row_to_record(r) for r in rows]
        kept = [r for r in recs if is_second_chance(r, 25)]
        self.assertEqual([r["title"] for r in kept], ["Kaffekvarn DEMO", "Robotdammsugare"])
        self.assertEqual(kept[1]["regular_price"], 4990)

    def test_adtraction_feed(self):
        rows = list(iter_xml_items((FIX / "adtraction_feed.xml").read_text(encoding="utf-8")))
        r = row_to_record(rows[0])
        self.assertEqual((r["price"], r["regular_price"], r["currency"]), (2490, 3990, "SEK"))
        self.assertTrue(r["url"].startswith("https://track.adtraction.com/"))
        self.assertTrue(is_second_chance(r, None))  # 'Outlet' in category


class VerifyAndStore(unittest.TestCase):
    def mk(self, **kw):
        base = dict(source="t", retailer="T", country="SE", currency="SEK", title="Test product",
                    price=100, url="https://ex.se/p/1", observed_at="2026-11-15T00:00:00+00:00")
        base.update(kw)
        return Listing(**base)

    def test_verify(self):
        self.assertIsNone(check(self.mk(regular_price=200)))
        self.assertEqual(check(self.mk(url="http://ex.se")), "bad_url")
        self.assertEqual(check(self.mk(regular_price=5000)), "implausible_discount")
        l = self.mk(regular_price=90)
        self.assertIsNone(check(l))
        self.assertIsNone(l.regular_price)  # no fake discount
        self.assertEqual(check(self.mk(), ["other.se"]), "foreign_host")

    def test_store_retire_and_history(self):
        with tempfile.TemporaryDirectory() as d:
            s = Store(Path(d) / "t.db")
            a = self.mk().to_public()
            s.upsert(a, "t1"); s.mark_missing("t", {a["id"]})
            a2 = dict(a, price=80); s.upsert(a2, "t2"); s.mark_missing("t", {a["id"]})
            self.assertEqual(s.active()[0]["history"], [["t1", 100], ["t2", 80]])
            s.mark_missing("t", set()); self.assertEqual(len(s.active()), 1)
            s.mark_missing("t", set()); self.assertEqual(len(s.active()), 0)


class Snapshot(unittest.TestCase):
    def test_snapshot_records_are_sourced(self):
        data = json.loads((Path(__file__).parents[1] / "data/snapshots/2026-11-15_manual.json").read_text(encoding="utf-8"))
        self.assertGreater(len(data), 50)
        for r in data:
            self.assertTrue(r["url"].startswith("https://"))
            self.assertTrue(r["observed_at"].startswith("2026-11-15"))
            if r["regular_price"]:
                self.assertGreater(r["regular_price"], r["price"])


if __name__ == "__main__":
    unittest.main()
