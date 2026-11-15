"""Sweden second-chance snapshot (returns, demo, open-box), captured 2026-11-15 ~19:15.

All values copied from the retailers' own public pages, with product and image URLs
as published. Run to write 2026-11-15_se_returns.json (ingested by manual_snapshot).
"""
import json
import pathlib

OBS = "2026-11-15T19:15:00+01:00"

# Kjell & Company outlet: returned items graded by Kjell (Nyskick / Mycket bra skick / Bra skick).
KJ = "https://www.kjell.com/se/outlet/"
KJI = "https://www.kjell.com/cdn-cgi/image/width=600,format=auto/globalassets/productimages/"
GRADE = {"A": ("Nyskick", "open_box"), "B": ("Mycket bra skick", "returned"), "C": ("Bra skick", "used")}
# (title, price, grade, path, image file, ref, availability)
KJELL = [
 ("Yale Linus Smartlås L2 Svart", 2835, "A", "sakerhet-overvakning/las/smarta-las/yale-linus-smartlas-l2-svart-p66153?outlet=a", "905030_66153.jpg", "AC56DF564B", "Fri frakt | Finns i 1 butik"),
 ("Eufy Security Hemlarm 5 delar", 1341, "A", "smarta-hem/smarta-larm/eufy-security-hemlarm-5-delar-p51927?outlet=a", "843600_51927.jpg", "BCCB95CE9F", "Fri frakt | Finns i 1 butik"),
 ("TP-Link Tapo D235 Videodörrklocka", 1266, "B", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/tp-link-tapo-d235-videodorrklocka-p66481?outlet=b", "904444_66481.jpg", "EA997832E1", "Fri frakt | Finns i 1 butik"),
 ("TP-Link Tapo D235 Videodörrklocka", 1341, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/tp-link-tapo-d235-videodorrklocka-p66481?outlet=a", "904444_66481.jpg", "EA997832E1", "Fri frakt | Finns i 2 butiker"),
 ("TP-Link Tapo D235 Videodörrklocka", 1192, "C", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/tp-link-tapo-d235-videodorrklocka-p66481?outlet=c", "904444_66481.jpg", "EA997832E1", "Fri frakt | Finns i 1 butik"),
 ("Yale Entrus Borstat Stål", 2601, "A", "sakerhet-overvakning/las/smarta-las/yale-entrus-borstat-stal-p66558?outlet=a", "942980_66558_01.webp", "89B0F74D60", "Fri frakt | Finns i 2 butiker"),
 ("TP-Link Tapo D210 Videodörrklocka", 842, "B", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/tp-link-tapo-d210-videodorrklocka-p66480?outlet=b", "904437_66480.jpg", "FB4F3B54DA", "Fri frakt | Finns i 1 butik"),
 ("Cleverio Smart rök- och värmedetektor", 240, "A", "smarta-hem/smarta-sensorer/smarta-brandvarnare/cleverio-smart-rok-och-varmedetektor-p51328?outlet=a", "767712_51328.jpg", "0FBE15213E", "Finns i 1 butik"),
 ("Philips Hue Essential Smart LED-lampa GU10 345 lm 3-pack", 522, "A", "smarta-hem/philips-hue/philips-hue-ljuskallor/philips-hue-essential-smart-led-lampa-gu10-345-lm-3-pack-p66538?outlet=a", "945265_66538_01.webp", "254B04A564", "Finns i 1 butik"),
 ("Philips Hue Ambiance Smart LED-lampa E14 470 lm 2-pack", 450, "A", "smarta-hem/philips-hue/philips-hue-ljuskallor/philips-hue-ambiance-smart-led-lampa-e14-470-lm-2-pack-p51689?outlet=a", "773988_51689.jpg", "959ADAE32B", "Finns i 4 butiker"),
 ("Danalock V3 Scandi Elektroniskt dörrlås", 1947, "A", "sakerhet-overvakning/las/smarta-las/danalock-v3-scandi-elektroniskt-dorrlas-p51039?outlet=a", "712130_51039_4.jpg", "99B5B2EC3E", "Fri frakt | Finns i 1 butik"),
 ("Aqara Hub M3 Smarta hem-controller", 1557, "A", "smarta-hem/controllers/aqara-hub-m3-smarta-hem-controller-p57869?outlet=a", "901562_57869.jpg", "35DEDAAF3B", "Fri frakt | Finns i 1 butik"),
 ("Yale Larmknappsats", 657, "A", "smarta-hem/smarta-larm/yale-larmknappsats-p67916?outlet=a", "898972_67916.jpg", "D255D74113", "Fri frakt | Finns i 2 butiker"),
 ("Ring Battery Video Doorbell Venetian Bronze", 585, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/ring-battery-video-doorbell-venetian-bronze-p65866?outlet=a", "907583_65866.jpg", "97B42823B2", "Finns i 4 butiker"),
 ("Ring Video Doorbell Wired", 255, "B", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/ring-video-doorbell-wired-p51852?outlet=b", "836374_51852.jpg", "5174402C52", "Finns i 3 butiker"),
 ("Athom Homey Bridge Smarta hem-controller", 680, "B", "smarta-hem/controllers/athom-homey-bridge-smarta-hem-controller-p51900?outlet=b", "827139_51900.jpg", "57B6B6B27A", "Fri frakt | Finns i 3 butiker"),
 ("Eufy Video Doorbell 2K dubbla kameror", 1791, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/eufy-video-doorbell-2k-dubbla-kameror-p60031?outlet=a", "909242_60031.jpg", "4F93BECA61", "Fri frakt | Finns i 1 butik"),
 ("Aqara Roller Shade Driver E1 Gardinkontroll", 637, "B", "smarta-hem/smart-gardinkontroll/aqara-roller-shade-driver-e1-gardinkontroll-p51850?outlet=b", "833218_51850.jpg", "5074B97FCC", "Fri frakt | Finns i 1 butik"),
 ("Arlo Essential Doorbell 2 FHD Trådlös Dörrklocka", 711, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/arlo-essential-doorbell-2-fhd-tradlos-dorrklocka-p65823?outlet=a", "898724_65823_03.jpg", "065B1C5D9A", "Fri frakt | Finns i 1 butik"),
 ("Aqara Smoke Detector Vit", 468, "A", "smarta-hem/smarta-sensorer/aqara-smoke-detector-vit-p56561?outlet=a", "934881_56561_01.jpg", "3D3356AB3B", "Finns i 1 butik"),
 ("Ring Battery Video Doorbell Plus Nickel Silver", 1785, "B", "sakerhet-overvakning/dorrklockor/tradlosa-dorrklockor/ring-battery-video-doorbell-plus-videodorrklocka-nickel-silver-p66873?outlet=b", "941966_66873_01.webp", "330D6EF0EA", "Fri frakt | Finns i 1 butik"),
 ("Philips Hue Luster Klotlampa White and Color Ambiance E14 2-pack", 900, "A", "smarta-hem/philips-hue/philips-hue-ljuskallor/philips-hue-luster-klotlampa-white-and-color-ambiance-e14-470-lm-2-pack-p65638?outlet=a", "889044_65638.jpg", "E697ECC28A", "Fri frakt | Finns i 1 butik"),
 ("Aqara Hub M200 med Matter, Zigbee och Thread", 684, "A", "smarta-hem/controllers/aqara-hub-m200-smart-hub-med-matter-zigbee-och-thread-p56570?outlet=a", "928677_56570_01.jpg", "316A3E8E41", "Fri frakt | Finns i 2 butiker"),
 ("Ring Wired Video Doorbell Pro Retinal 4K", 2520, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/ring-wired-video-doorbell-pro-retinal-4k-p66704?outlet=a", "934809_66704_01.jpg", "C73A3327FE", "Fri frakt | Finns i 2 butiker"),
 ("Reolink D340W 2K Video Dörrklocka", 1096, "B", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/reolink-d340w-2k-video-dorrklocka-p60397?outlet=b", "917786_60397_01.webp", "5F53EEFC50", "Fri frakt | Finns i 1 butik"),
 ("Philips Hue Filament A60 E27 Smart LED-lampa 550 lm", 314, "B", "smarta-hem/philips-hue/philips-hue-ljuskallor/philips-hue-filament-a60-e27-smart-led-lampa-550-lm-p65647?outlet=b", "894701_65647.jpg", "BF91CD7749", "Finns i 1 butik"),
 ("Philips Hue Smart inbyggnadsrelä 2 kanaler", 576, "A", "smarta-hem/philips-hue/philips-hue-tillbehor/philips-hue-smart-inbyggnadsrela-2-kanaler-p66851?outlet=a", "945250_66851_01.webp", "86F9820D71", "Finns i 2 butiker"),
 ("Yale Smart Opener för motordrivna garageportar", 1521, "A", "sakerhet-overvakning/las/smarta-las/yale-smart-opener-for-motordrivna-garageportar-p66156?outlet=a", "905132_66156.jpg", "528FD63F41", "Fri frakt | Finns i 1 butik"),
 ("Yale Smart Video Doorbell", 1530, "B", "sakerhet-overvakning/dorrklockor/fast-montering/yale-smart-video-doorbell-p65942?outlet=b", "897884_65942.jpg", "7E1B92B32F", "Fri frakt | Finns i 1 butik"),
 ("Eufy Video Doorbell C30", 900, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/eufy-video-doorbell-c30-p60041?outlet=a", "916336_60041_01.jpg", "8FB9FB6D90", "Fri frakt | Finns i 1 butik"),
 ("Philips Hue Väggbrytarmodul 1-pack", 493, "B", "smarta-hem/philips-hue/philips-hue-tillbehor/philips-hue-vaggbrytarmodul-1-pack-p51737?outlet=b", "819143_51737.jpg", "2B8BAE9A1B", "Finns i 2 butiker"),
 ("Athom Homey Energy Dongle", 450, "A", "smarta-hem/smarta-sensorer/smarta-energimatare/athom-homey-energy-dongle-p52222?outlet=a", "914205_52222_01.jpg", "ADCD86599D", "Finns i 2 butiker"),
 ("Defunc Home Small Vit", 1596, "B", "ljud-bild/hogtalare/smarta-hogtalare/defunc-home-small-vit-p67854?outlet=b", "916666_67854_01.jpg", "3D68698E0A", "Fri frakt | Finns i 1 butik"),
 ("Philips Hue Color Ambiance Smart LED-lampa E14 470 lm 1-pack", 594, "A", "smarta-hem/philips-hue/philips-hue-ljuskallor/philips-hue-color-ambiance-smart-led-lampa-e14-470-lm-1-pack-p51661?outlet=a", "770770_51661.jpg", "6525BD6F97", "Finns i 1 butik"),
 ("Reolink Smart Video Doorbell med Home Hub", 2070, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/reolink-smart-video-doorbell-med-home-hub-p60396?outlet=a", "909095_60396.webp", "6CB1D72332", "Fri frakt | Finns i 1 butik"),
 ("Arlo Essential Doorbell 2 2K Trådlös dörrklocka", 1791, "A", "sakerhet-overvakning/dorrklockor/smarta-dorrklockor/arlo-essential-doorbell-2-2k-tradlos-dorrklocka-p65824?outlet=a", "898743_65824_04.jpg", "EA2794F100", "Fri frakt | Finns i 1 butik"),
 ("Yale Smart Code Handle Rakt utförande", 1530, "A", "sakerhet-overvakning/las/smarta-las/yale-smart-code-handle-rakt-utforande-p52080?outlet=a", "902885_52080.jpg", "36EC15DAED", "Fri frakt | Finns i 1 butik"),
 ("TP-Link Tapo T310 Smart Termometer och hygrometer", 160, "C", "smarta-hem/smarta-sensorer/smarta-temperatursensorer/tp-link-tapo-t310-smart-termometer-och-hygrometer-p65281?outlet=c", "885176_65281.jpg", "11E2B704D3", "Finns i 1 butik"),
]

# Cremashop (Swedish coffee specialist) outlet: individual items; the shop states these are unused items
# with dented packaging, demo models, briefly tested or warranty-serviced devices.
CREMA_COND = "Outlet-exemplar: oanvänd med skadad förpackning, demo, kort testad eller garantiservad. Se skick på produktsidan."
CS = "https://www.cremashop.se/en/outlet/"
CSI = "https://www.cremashop.se/media/cache/grid_product/content/products/"
# (title, price, regular, outlet id, image path)
CREMA = [
 ("Eureka Mignon Libra 65 All Purpose 16CR Coffee Grinder, Chrome", 6589, 7377, 202, "eureka/mignon-libra-65-all-purpose/13463-e6cb3c6c767730cb3b1bad48f7ef49d3.jpg"),
 ("Wilfa Zense Alux Coffee Maker CM10AB-M125 1,25 l, Black Aluminum", 2029, 2179, 201, "wilfa/zense-alux-manual-drip-stop/13517-ca5f3ef8990c2daf335174ada9abaeee.jpg"),
 ("Wilfa Performance Thermo CM9B-T125 Coffee Maker 1.25 l", 3129, 3279, 200, "wilfa/performamce-thermo/12773-90d68a59c174359836fa81106cc417bd.jpg"),
 ("9Barista Mk.2 Pro Espresso Machine", 7019, 7361, 198, "9barista/mk2-pro-espresso-machine/13570-000441051c5671fa2b2db285c105e350.jpg"),
 ("Eureka Oro Mignon Single Dose Pro Coffee Grinder", 6909, 7019, 197, "eureka-oro/mignon-single-dose-pro/13011-8fd7797b4f0b90a4980f9ae87327dada.jpg"),
 ("Gaggia Classic Evo Pro 2023 Espresso Machine, Brushed Stainless Steel", 5259, 6139, 192, "gaggia/classic/10371-bbbf82ed17c454b91bd1beabadd07a98.jpg"),
 ("Rancilio Silvia Pro X Espresso Machine, Stainless Steel", 16479, 19689, 188, "rancilio/silvia-pro-x-dual/10939-aacc8bb0e0d05b91569842ea615e73e2.jpg"),
 ("Baratza Sette 270 Coffee Grinder", 3279, 3730, 186, "baratza/sette-270/2518.jpg"),
 ("Baratza Vario Coffee Grinder", 3939, 5479, 185, "baratza/vario/2520-7158fd2bb70412467f16e4cef9fe7d0c.jpg"),
 ("Sage Barista Touch Impress Cold SES882BSS Espresso Machine", 12739, 14829, 183, "sage/barista-touch-impress-cold/14480-3a2540ff5e5c1c50e4b05688be27de38.jpg"),
 ("Lelit Victoria PL91T Espresso Machine", 8889, 10939, 174, "lelit/victoria-pl91t/13385-23e02eaa60da0b2d62a9f385b833cd5c.jpg"),
 ("Compak K3 Touch Advanced Coffee Grinder, White", 3059, 5149, 171, "compak/k3-touch-advanced/4461-d6142a27db167a2de2fb6b695a3d56a1.jpg"),
 ("Jura ENA 4 (EB) Automatic Coffee Machine, Full Metropolitan Black", 7459, 8229, 167, "jura/ena-4/10330-201e80c428b0ca28f06f161646b0241f.jpg"),
 ("Eureka Atom Excellence 65 Espresso Coffee Grinder, Black", 10649, 10979, 164, "eureka/atom-excellence-65-espresso-coffee-grinder/11831-8ad2c71c33d5298a6bb71ba63295a793.jpeg"),
 ("Eureka Mignon Zero 16CR Espresso Coffee Grinder, White", 3939, 4060, 159, "eureka/mignon-zero-16cr/10729-afeb95b08f9bafc7eb41ae228a5141b4.jpg"),
 ("Quick Mill Orione Espresso Machine", 8119, 8339, 146, "quick-mill/orione-espresso-machine/13288-5cdb0b33724aa7a74d645fc8802567c1.jpg"),
 ("Lelit Bianca PL162T V3 Espresso Machine, White", 27929, 28040, 145, "lelit/bianca-pl162t/13628-b0e9dc702fc124e0db690a7186a8d053.jpg"),
 ("Fellow Stagg Pour-Over Kettle 1 l, Matte Black", 1039, 1089, 136, "fellow/stagg-pour-over-kettle/2573.jpg"),
 ("Sage The Oracle Touch SES990BSS Espresso Coffee Maker, Brushed Steel", 23099, 26379, 132, "sage/the-oracle-touch/2994.jpg"),
 ("Nivona NICR 970 CafeRomatica Fully Automatic Coffee Machine, Grey", 13729, 16479, 123, "nivona/nicr-960-and-970/4733-b5916c63583033311e32d01e2c0f4985.jpg"),
 ("Goat Story GINA Basic Coffee Maker, Black", 1189, 1530, 106, "goat-story/gina-basic-coffee-maker/11328-9dac84678125bca8018508b76b7f6b37.jpg"),
 ("Fellow Clyde Electric Kettle 1.5 l, Matte Black", 1079, 1369, 98, "fellow/clyde-electric-kettle/12910-f15d55cea662df5c960a86eefd80dd63.jpg"),
 ("Quick Mill Carola PID Espresso Machine", 10429, 12629, 97, "quick-mill/carola-pid-0960-espresso-machine/13291-d2235461b90ee09f8d8ab3cff33dc5c7.jpg"),
 ("GSI Outdoors Enamel Tea Kettle, Blue", 419, 599, 86, "gsi/tea-kettle/9721-26a1a00212f3c1eedd1db1f0f752af79.jpg"),
 ("CASO Perfect Cup 1000 Pro Hot Water Dispenser 4 l", 969, 2179, 47, "caso/perfect-cup-1000-pro-dispenser/11440-502ee2c21ddedf4f54f6076dabb24b56.jpg"),
]

# Inet Fyndhörnan: verified on the product page (several other items had already sold).
INET = [
 ("Philips Hue HDMI Sync Box 4K", 1390, 1729, "x256244/philips-hue-hdmi-sync-box-4k", "6603678_ovq3ug.jpg",
  "Öppnad förpackning, komplett med alla tillbehör.", "open_box", "Inet Göteborg Sisjön", "tv_audio"),
 ("Wacom Cintiq 24 Touch (2025)", 18999, 20190, "x255826/wacom-cintiq-24-touch-2025", "6612515_5n7rkb.jpg",
  "Öppnad förpackning, komplett med alla tillbehör.", "open_box", "Inet Stockholm Sveavägen", "computers"),
 ("LG NS90TY Soundbar", 9510, 9990, "x256254/lg-ns90ty-soundbar", "6306270_0.jpg",
  "Ersättningsprodukt från tillverkaren, komplett med alla tillbehör. Bruksslitage på vissa delar, endast kosmetiska skador.",
  "manufacturer_replacement", "Inet Göteborg Sisjön", "tv_audio"),
]


def build():
    out = []
    for t, p, g, path, img, ref, av in KJELL:
        label, cond = GRADE[g]
        out.append(dict(source="kjell_se", retailer="Kjell & Company", country="SE", currency="SEK", title=t,
                        price=p, regular_price=None, category="smart_home", condition=cond,
                        condition_text=f"Outlet, skick: {label}", grade=label,
                        url=KJ + path, url_kind="product", image_url=f"{KJI}{img}?ref={ref}",
                        availability_text=av, list_url=KJ + "smarta-hem", observed_at=OBS))
    for t, p, r, oid, img in CREMA:
        out.append(dict(source="cremashop_se", retailer="Cremashop", country="SE", currency="SEK", title=t,
                        price=p, regular_price=r, category="coffee", condition="demo", condition_text=CREMA_COND,
                        url=f"{CS}{oid}", url_kind="product", image_url=CSI + img,
                        availability_text="Ett exemplar, leverans i Sverige", list_url=CS[:-1], observed_at=OBS))
    for t, p, r, path, img, ctext, cond, store, cat in INET:
        out.append(dict(source="inet_se", retailer="Inet", country="SE", currency="SEK", title=t,
                        price=p, regular_price=r, category=cat, condition=cond, condition_text=ctext,
                        url="https://www.inet.se/produkt/" + path, url_kind="product",
                        image_url="https://cdn.inet.se/product/688x386/" + img, store=store,
                        availability_text=f"1 st i {store}, kan även skickas", list_url="https://www.inet.se/fyndhornan",
                        observed_at="2026-11-15T19:05:00+01:00"))
    return out


if __name__ == "__main__":
    p = pathlib.Path(__file__).with_suffix(".json")
    d = build()
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(d)} records to {p.name}")
