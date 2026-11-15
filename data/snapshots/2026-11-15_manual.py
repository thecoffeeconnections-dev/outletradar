"""Manual capture of real listings observed on 2026-11-15 (Europe/Stockholm).

Captured by reading the public retailer pages listed in each record. No values
are invented: titles, prices and condition texts are copied from the pages.
Running this file writes 2026-11-15_manual.json, which the pipeline ingests
through the `manual_snapshot` adapter. Live adapters replace this data as soon
as the scheduled crawler has network access.
"""
import json
import pathlib

OBSERVED = "2026-11-15T17:30:00+01:00"
INET_LIST = "https://www.inet.se/fyndhornan"
INET_SHIP = "Online, leverans med PostNord eller köp i butik (se lagersaldo på produktsidan)"

# Inet Fyndhörnan, page view with direct product links: (title, now, regular, condition, url-slug)
inet_with_links = [
    ("Philips Hue HDMI Sync Box 4K", 1390, 1729, "Öppnad förpackning, komplett med alla tillbehör.", "x256244/philips-hue-hdmi-sync-box-4k"),
    ("Aqara Rökdetektor", 429, 519, "Öppnad förpackning, komplett med alla tillbehör.", "x256229/aqara-rokdetektor"),
    ("Aqara Rökdetektor", 429, 519, "Öppnad förpackning, komplett med alla tillbehör.", "x256228/aqara-rokdetektor"),
    ("Aqara Rökdetektor", 429, 519, "Öppnad förpackning, komplett med alla tillbehör.", "x256227/aqara-rokdetektor"),
    ("Gigabyte X870 Gaming WIFI6", 2370, 2490, "Öppnad förpackning, komplett med alla tillbehör.", "x255917/gigabyte-x870-gaming-wifi6"),
    ("DELTACO HD kabinett 3.5\" SATA 6Gb/s till USB 3.0 Aluminium Svart", 330, 349, "Öppnad förpackning, komplett med alla tillbehör.", "x256241/deltaco-hd-kabinett-3-5-sata-6gb-s-till-usb-3-0-aluminium-svart"),
    ("nuki Keypad 2 NFC", 1790, 2299, "Öppnad förpackning, komplett med alla tillbehör. Klister för fästning är använt", "x256247/nuki-keypad-2-nfc"),
    ("Holdit iPhone 17 Pro Max/18 Pro Max Silicone Case Svart", 149, 199, "Öppnad förpackning, komplett med alla tillbehör.", "x256220/holdit-iphone-17-pro-max-18-pro-max-silicone-case-svart"),
    ("Arozzi Nova 25\" E-Sport Black IPS FHD 400Hz", 2840, 2990, "Öppnad förpackning, komplett med alla tillbehör.", "x256272/arozzi-nova-25-e-sport-black-ips-fhd-400hz"),
    ("ZOWIE 24\" XL2566X+ DyAc 2 400 Hz e-Sports Monitor", 8499, 8990, "Öppnad förpackning, komplett med alla tillbehör.", "x256252/zowie-24-xl2566x-dyac-2-400-hz-e-sports-monitor"),
    ("Anker Prime 250W GaN Desktop Charger", 2080, 2190, "Öppnad förpackning, komplett med alla tillbehör.", "x256422/anker-prime-250w-gan-desktop-charger"),
    ("Kingston 32GB (2x16GB) DDR5 5600MHz CL40 FURY Beast RGB", 7410, 7790, "Öppnad förpackning, komplett med alla tillbehör.", "x256416/kingston-32gb-2x16gb-ddr5-5600mhz-cl40-fury-beast-rgb"),
    ("Moza - SR-P2 - Clutch", 549, 649, "Öppnad förpackning, komplett med alla tillbehör.", "x256192/moza-sr-p2-clutch"),
    ("Gigabyte X670E Aorus Xtreme", 8570, 8999, "Ersättningsprodukt från tillverkaren. Endast moderkort. Saknar samtliga tillbehör", "x256430/gigabyte-x670e-aorus-xtreme"),
    ("ASUS TUF Gaming B650-E WIFI", 1999, 2190, "Ersättningsprodukt från tillverkaren, komplett med alla tillbehör", "x255450/asus-tuf-gaming-b650-e-wifi"),
    ("Logitech M330 Silent Plus Svart", 399, 499, "Öppnad förpackning, komplett med alla tillbehör.", "x254673/logitech-m330-silent-plus-svart"),
    ("AMD Ryzen 7 9700X 3.8 GHz 40MB", 3510, 3690, "Öppnad förpackning, komplett med alla tillbehör. Spår av kylpasta kan förekomma.", "x256290/amd-ryzen-7-9700x-3-8-ghz-40mb"),
    ("Realme GT 8 Pro (16+512GB) Urban Blue", 9499, 13490, "Öppnad förpackning, komplett med alla tillbehör.", "x255849/realme-gt-8-pro-16-512gb-urban-blue"),
    ("Belkin USB-C Hub 5 Portar Silver", 470, 499, "Öppnad förpackning, komplett med alla tillbehör", "x256316/belkin-usb-c-hub-5-portar-silver"),
    ("Corsair Gaming Galleon 100 SD", 3599, 3890, "Öppnad förpackning, komplett med alla tillbehör.", "x256235/corsair-gaming-galleon-100-sd"),
    ("TP-Link Archer C24 AC750", 299, 359, "Öppnad förpackning, komplett med alla tillbehör.", "x256134/tp-link-archer-c24-ac750"),
    ("Gigabyte 32\" MO32U24 OLED 4K 240 Hz", 9999, 11120, None, "x256287/gigabyte-32-mo32u24-oled-4k-240-hz"),
    ("ASUS TUF Gaming B650-E WIFI", 2080, 2190, "Öppnad förpackning, komplett med alla tillbehör.", "x256372/asus-tuf-gaming-b650-e-wifi"),
    ("DELTACO HDMI-kabel 2.0 ha-ha Aktiv Svart 5 m", 399, 599, "Öppnad förpackning, komplett med alla tillbehör.", "x254763/deltaco-hdmi-kabel-2-0-ha-ha-aktiv-svart-5-m"),
    ("Moza - SR-P2 Two Pedal set Throttle + Break", 1790, 1999, "Öppnad förpackning, komplett med alla tillbehör.", "x256191/moza-sr-p2-two-pedal-set-throttle-break"),
    ("ASUS Prime B760M-A WIFI", 1700, 1790, "Öppnad förpackning, komplett med alla tillbehör.", "x256421/asus-prime-b760m-a-wifi"),
    ("8bitdo Ultimate 3-mode Xbox Vit", 599, 699, "Öppnad förpackning, komplett med alla tillbehör.", "x253934/8bitdo-ultimate-3-mode-xbox-vit"),
    ("Keychron G6 HE 8K Black", 1199, 1290, "Öppnad förpackning, komplett med alla tillbehör", "x256315/keychron-g6-he-8k-black"),
    ("Logitech M330 Silent Plus Svart", 470, 499, "Öppnad förpackning, komplett med alla tillbehör.", "x256404/logitech-m330-silent-plus-svart"),
    ("Wacom Cintiq 24 Touch (2025)", 17999, 20190, "Öppnad förpackning, komplett med alla tillbehör.", "x255826/wacom-cintiq-24-touch-2025"),
    ("Elgato Wave DX", 1180, 1245, "Öppnad förpackning, komplett med alla tillbehör.", "x256409/elgato-wave-dx"),
    ("ASUS Prime B860M-K", 1499, 1999, "Öppnad förpackning, komplett med alla tillbehör", "x254480/asus-prime-b860m-k"),
    ("ASUS ROG Strix Z790-E Gaming WIFI II", 7299, 7789, "Saknar förpackning och tillbehör, i övrigt komplett.", "x254823/asus-rog-strix-z790-e-gaming-wifi-ii"),
    ("Sony Playstation 5 Slim Cover Rythm Blue", 549, 799, "Öppnad förpackning, komplett med alla tillbehör.", "x254598/sony-playstation-5-slim-cover-rythm-blue"),
    ("Corsair K70 Core TKL Wireless MLX Red", 1399, 1749, "Öppnad förpackning, komplett med alla tillbehör.", "x255914/corsair-k70-core-tkl-wireless-mlx-red"),
    ("MSI B550-A Pro", 1510, 1589, "Öppnad förpackning, komplett med alla tillbehör.", "x256420/msi-b550-a-pro"),
    ("Fairbuds XL (2025) Grön", 2399, 2849, "Öppnad förpackning, komplett med alla tillbehör.", "x255766/fairbuds-xl-2025-gron"),
    ("LG NS90TY Soundbar", 9510, 9990, "Ersättningsprodukt från tillverkaren, komplett med alla tillbehör. Bruksslitage på vissa delar, endast kosmetiska skador.", "x256254/lg-ns90ty-soundbar"),
    ("WLMouse Beast G Mini - Black", 799, 999, "Öppnad förpackning, komplett med alla tillbehör.", "x256328/wlmouse-beast-g-mini-black"),
    ("Seasonic Core GC 650W ATX3.1", 749, 949, "Öppnad förpackning, komplett med alla tillbehör.", "x256248/seasonic-core-gc-650w-atx3-1"),
    ("ASUS 27\" ROG Swift PG27AQWP-W OLED QHD 540/720 Hz Dual Mode", 11999, 12990, "Öppnad förpackning, komplett med alla tillbehör.", "x256301/asus-27-rog-swift-pg27aqwp-w-oled-qhd-540-720-hz-dual-mode"),
    ("Ultrahuman Ring AIR (Size 11) Raw Titanium", 3499, 4288, "Ersättningsprodukt från tillverkaren, komplett med alla tillbehör.", "x255705/ultrahuman-ring-air-size-11-raw-titanium"),
    ("Gigabyte B860M D3HP", 1610, 1699, "Öppnad förpackning, komplett med alla tillbehör.", "x255933/gigabyte-b860m-d3hp"),
    ("GameSir G7 Pro 8K - Aimlabs Edition", 999, 1199, "Öppnad förpackning, komplett med alla tillbehör", "x255032/gamesir-g7-pro-8k-aimlabs-edition"),
    ("PLAUD NotePin AI Voice recorder Silver", 1499, 1999, "Öppnad förpackning, saknar förpackning och samtliga tillbehör. Endast enhet och laddare.", "x253469/plaud-notepin-ai-voice-recorder-silver"),
    ("Aqara G5 Pro Camera Hub PoE Grå", 1590, 1949, "Öppnad förpackning, saknar samtliga tillbehör", "x256175/aqara-g5-pro-camera-hub-poe-gra"),
    ("ASUS ROG Harpe Ace Aim Lab Edition Wireless", 649, 1590, "Demoexemplar, komplett med alla tillbehör", "x253366/asus-rog-harpe-ace-aim-lab-edition-wireless"),
    ("Pulsar Zywoo The Chosen Gen 2 Medium Pink", 1499, 1790, "Öppnad förpackning, komplett med alla tillbehör.", "x255994/pulsar-zywoo-the-chosen-gen-2-medium-pink"),
    ("Bose SoundLink Max Svart", 3999, 4790, "Ersättningsprodukt från tillverkaren, komplett med alla tillbehör", "x255532/bose-soundlink-max-svart"),
    ("SteelSeries Apex Pro Gen 3", 2699, 2999, "Demoexemplar, komplett med alla tillbehör, små repor på displayen.", "x256196/steelseries-apex-pro-gen-3"),
    ("Samsung Galaxy Tab A11+ Keyboard Cover Case Slim", 499, 649, "Öppnad förpackning, komplett med alla tillbehör.", "x256308/samsung-galaxy-tab-a11-keyboard-cover-case-slim"),
    ("MSI B840 Gaming Plus WIFI", 1799, 2199, "Öppnad förpackning, komplett med alla tillbehör.", "x254535/msi-b840-gaming-plus-wifi"),
    ("Apple iPhone 18 Pro Max (2TB) Silver", 31999, 35489, "Öppnad förpackning, komplett med alla tillbehör.", "x255878/apple-iphone-18-pro-max-2tb-silver"),
    ("Anker Thunderbolt 5 Dockningsstation", 4280, 4499, "Öppnad förpackning, komplett med alla tillbehör.", "x256344/anker-thunderbolt-5-dockningsstation"),
    ("Gigabyte X870 Gaming WIFI6", 1999, 2490, "Öppnad förpackning, saknar Wi-Fi antenn, i övrigt komplett med alla tillbehör", "x253056/gigabyte-x870-gaming-wifi6"),
    ("BenQ TH575i Google TV", 6499, 6990, "Öppnad förpackning, komplett med alla tillbehör.", "x256048/benq-th575i-google-tv"),
    ("ASUS ROG Keris II Origin Svart", 1299, 1790, "Öppnad förpackning, komplett med alla tillbehör.", "x253877/asus-rog-keris-ii-origin-svart"),
    ("SteelSeries Aerox 5 Wireless", 1499, 1699, "Öppnad förpackning, komplett med alla tillbehör.", "x256376/steelseries-aerox-5-wireless"),
    ("Gigabyte B650 Aorus Elite AX", 2499, 2699, "Öppnad förpackning, endast moderkort och kartong. Spår av användning förekommer, som t.ex. repor och skavmärken.", "x255534/gigabyte-b650-aorus-elite-ax"),
    ("Razer Huntsman V2 Clicky Purple", 1899, 2099, "Demoexemplar, komplett med alla tillbehör", "x256246/razer-huntsman-v2-clicky-purple"),
]

# Inet Fyndhörnan first page: listing text was readable but product hrefs were not
# exposed to the reader, so these link to Inet's own search for the exact title.
# (Glorious Model O Wireless Vit is left out: its two prices were ambiguous.)
inet_without_links = [
    ("PNY GeForce RTX 5080 16GB ARGB OC", 15990, 16799, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Sapphire Radeon RX 9070 XT 16GB Nitro+", 8560, 8990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("LG 27\" UltraGear 27GS85Q Nano IPS QHD 200 Hz", 4080, 4290, "Öppnad förpackning, komplett med alla tillbehör"),
    ("AMD Ryzen 9 7950X3D 4.2 GHz 145MB", 6999, 9499, "Saknar förpackning, endast CPU."),
    ("Acer 34\" Nitro XV345CURV3 VA WQHD (1000R) 180 Hz USB-C", 3299, 3990, "Demoexemplar, komplett med alla tillbehör"),
    ("Taurus Hardcore Gaming RTX 4070 Super - 7800X3D", 17999, 22999, "Öppnad förpackning, komplett med alla tillbehör"),
    ("ASUS 27\" ROG Swift PG27AQN IPS QHD 360 Hz G-Sync", 8999, 15990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Nintendo Switch 2 Pro Controller", 950, 999, "Öppnad förpackning, komplett med alla tillbehör."),
    ("ASUS 24\" ROG Swift Pro PG248QP Esports-TN 540 Hz G-Sync", 8999, 12990, "Öppnad förpackning, komplett med alla tillbehör"),
    ("Taurus Endgame RTX 5080 - 9800X3D", 28999, 34999, "Demoexemplar, komplett med alla tillbehör"),
    ("Intel Arc B580 12GB Limited Edition", 2790, 3290, "Öppnad förpackning, komplett med alla tillbehör."),
    ("ASUS GeForce RTX 4090 24GB ROG Strix Gaming OC", 24999, 26490, "Saknar förpackning, i övrigt komplett med alla tillbehör"),
    ("ASUS Vivobook 15X OLED D1505 - Ryzen 7 | 16GB | 1TB", 7799, 11990, "Öppnad förpackning, komplett med alla tillbehör"),
    ("ASUS 32\" ROG Swift PG32UCDMZ OLED 4K 240 Hz", 11299, 14990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Sony Playstation 5 DualSense Edge", 2090, 2489, "Öppnad förpackning, komplett med alla tillbehör"),
    ("Sony Inzone H9 Vit", 1499, 3449, "Öppnad förpackning, komplett med alla tillbehör. Skadad kartong"),
    ("ASUS 32\" ROG Swift PG32UCDP OLED 4K 240/480 Hz Dual Mode USB-C", 9999, 11990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("ASUS ROG Flow Z13 - Ryzen AI Max+ | 32GB | 1TB", 23999, 29990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("MSI Stealth 15 OLED - i7 | 16GB | 1TB | RTX 4060", 14999, 19990, "Öppnad förpackning, komplett med alla tillbehör, Tydliga repor på lock, mindre synliga repor här och där på chassit."),
    ("eblaztr PC Case", 2799, 4499, "Öppnad förpackning, komplett med alla tillbehör."),
    ("MSI Cyborg 15 - i5 | 16GB | 512GB | RTX 3050", 8999, 11990, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Dell 27\" Alienware AW2725QF IPS 4K 180/360 Hz Dual Mode", 5499, 7990, "Spår av användning förekommer, defekta pixlar."),
    ("Razer Huntsman Mini Clicky Svart", 899, 1399, "Demoexemplar, komplett med alla tillbehör. Använt skick"),
    ("Apple MacBook Air (2025) - 13,6\" | M4 | 16GB | 256GB | Himmelsblå", 12499, 13489, "Öppnad förpackning, komplett med alla tillbehör"),
    ("Samsung Galaxy Tab S10 Ultra (12+256GB) Moonstone Gray", 6799, 16690, "Öppnad förpackning, komplett med alla tillbehör"),
    ("ASUS TUF F15 - i7 | 16GB | 1TB | RTX 4070", 15999, 19989, "Ej originalförpackning, saknar tillbehör. Endast dator och laddare."),
    ("AMD Ryzen 9 9900X3D 4.4GHz 140MB", 6199, 6679, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Lenovo LOQ - i5 | 16GB | 1TB | RTX 4060 Ti", 11499, 11990, "Öppnad förpackning, komplett med alla tillbehör"),
    ("Sony Playstation 5 Pro", 9490, 9789, "Öppnad förpackning, komplett med alla tillbehör."),
    ("Fractal Design Refine Alcantara Dark", 8990, 10489, "Öppnad förpackning, komplett med alla tillbehör."),
]

# Thomann (ships to Denmark), B-stock product pages; prices DKK incl. VAT.
thomann_dk = [
    ("Brennenstuhl Power Distributor BSV3 B-Stock", 1299, 1419, "https://www.thomann.dk/brennenstuhl_power_distributor_bsv3_b_stock.htm"),
    ("T-Rex Fuel Tank Classic B-Stock", 866, 939, "https://www.thomann.dk/t_rex_fuel_tank_classic_b_stock.htm"),
    ("Adam Hall PROPORT 4 B-Stock", 362, 389, "https://www.thomann.dk/adam_hall_proport_4_b_stock.htm"),
    ("Showgear PowerCore 32.12p B-Stock", 7899, 8666, "https://www.thomann.dk/showgear_powercore_3212p_b_stock.htm"),
    ("Botex Power box BO-6-S2-16 C B-Stock", 555, 599, "https://www.thomann.dk/botex_power_box_bo_6_s2_16_c_b_stock_650418.htm"),
    ("Showgear PowerCore 32.9s B-Stock", 6444, 7599, "https://www.thomann.dk/showgear_powercore_329s_b_stock.htm"),
]


def build():
    out = []
    for t, p, r, c, slug in inet_with_links:
        out.append(dict(source="inet_se", retailer="Inet", country="SE", currency="SEK", title=t,
                        price=p, regular_price=r, condition_text=c,
                        url=f"https://www.inet.se/produkt/{slug}", url_kind="product",
                        availability_text=INET_SHIP, list_url=INET_LIST, observed_at=OBSERVED))
    for t, p, r, c in inet_without_links:
        from urllib.parse import quote
        out.append(dict(source="inet_se", retailer="Inet", country="SE", currency="SEK", title=t,
                        price=p, regular_price=r, condition_text=c,
                        url=f"https://www.inet.se/hitta?q={quote(t)}", url_kind="search",
                        availability_text=INET_SHIP, list_url=INET_LIST, observed_at=OBSERVED))
    for t, p, r, u in thomann_dk:
        out.append(dict(source="thomann_dk", retailer="Thomann", country="DK", currency="DKK", title=t,
                        price=p, regular_price=r,
                        condition_text="B-stock med fuld garanti. Returvare hhv. med lette brugsspor",
                        url=u, url_kind="product", availability_text="På lager, levering til Danmark",
                        list_url=u, observed_at=OBSERVED))
    # Elkjøp Norway outlet (store stock in Kongsvinger). Product pages not exposed: link the outlet page.
    for t, p, r in [("Apple Mini DisplayPort-til-VGA", 1599, 1999),
                    ("Electrolux mikrobølgeovn KMFE171TEX innebygd", 3399, 3999)]:
        out.append(dict(source="elkjop_no", retailer="Elkjøp", country="NO", currency="NOK", title=t,
                        price=p, regular_price=r, condition_text="Som ny - Komplett i originalemballasje",
                        url="https://elkjop.no/outlet/outlet-elkjop-vinje", url_kind="listing",
                        availability_text="Kan kjøpes på nett | På lager i 1 butikk(er)",
                        store="Elkjøp Kongsvinger", list_url="https://elkjop.no/outlet/outlet-elkjop-vinje",
                        observed_at=OBSERVED))
    # Proshop Denmark demo product page (no regular price shown on the captured page).
    out.append(dict(source="proshop_dk", retailer="Proshop", country="DK", currency="DKK", title="Razor Pro-X *DEMO*",
                    price=554, regular_price=None,
                    condition_text="Demovare. Samme reklamations- og fortrydelsesret som nye varer",
                    url="https://www.proshop.dk/Skating-Cykler/Razor-Pro-X-DEMO/3446145d", url_kind="product",
                    availability_text="På lager", list_url="https://www.proshop.dk/Demo-produkter",
                    observed_at=OBSERVED))
    return out


if __name__ == "__main__":
    path = pathlib.Path(__file__).with_suffix(".json")
    data = build()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(data)} records to {path.name}")
