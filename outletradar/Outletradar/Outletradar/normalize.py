"""Normalisation: prices, condition, category, brand. Multilingual (sv/da/no/en)."""
from __future__ import annotations

import re
from typing import Optional

_PRICE_RE = re.compile(r"(\d{1,3}(?:[  . ]\d{3})+|\d+)(?:[,.](\d{1,2}|-))?")


def parse_price(text) -> Optional[float]:
    """Parse Nordic price strings: '1 299 kr', '1.299,00 kr.', '1599,-', '12 990:-', 1299."""
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).strip()
    if not s:
        return None
    m = _PRICE_RE.search(s)
    if not m:
        return None
    whole = re.sub(r"[  . ]", "", m.group(1))
    dec = m.group(2)
    # '1.299' style thousand separator vs '12.50' decimal: thousands groups are 3 digits
    try:
        value = float(whole)
    except ValueError:
        return None
    if dec and dec != "-":
        value += float("0." + dec)
    return value


# Ordered: first match wins, so specific phrases come before generic ones.
_CONDITION_RULES = [
    ("refurbished", r"refurb|renoverad|renoveret|rekonditioner|istandsat|certifierad begagnad|certified pre-owned"),
    ("manufacturer_replacement", r"ersättningsprodukt|erstatningsprodukt|replacement product"),
    ("demo", r"\bdemo|demoex|demovar|utställning|udstilling|utstilling|visningsex|display unit|ex-display"),
    ("returned", r"\bb-?stock\b|b-?vare"),
    ("used", r"spår av (an)?vändning|bruksspår|brugsspor|bruksslitage|repor|ridser|riper|defekt|använt skick|used|brugt|brukt|begagnad"),
    ("damaged_packaging", r"skadad (förpackning|kartong)|fraktskadad|beskadiget emballage|skadet emballasje|damaged (box|packaging)"),
    ("returned", r"saknar (original)?förpackning|ej (i )?originalförpackning|retur|återköp|returvare|returned|öppet köp"),
    ("open_box", r"öppnad förpackning|åbnet emballage|åpnet emballasje|som ny|open[- ]?box|b-?stock|b-?vare|fyndvara"),
    ("clearance", r"outlet|restlager|utförsäljning|udsalg|sidste på lager|clearance|lageroprydning"),
]
_COND_COMPILED = [(c, re.compile(p, re.I)) for c, p in _CONDITION_RULES]


def classify_condition(*texts: Optional[str]) -> str:
    blob = " ".join(t for t in texts if t)
    if not blob:
        return "unknown"
    # 'used' should not override an explicit 'demo/replacement' label when the
    # only wear signal is minor; keep rule order but special-case open_box+used.
    for cond, rx in _COND_COMPILED:
        if rx.search(blob):
            return cond
    return "unknown"


_CATEGORY_RULES = [
    ("computers", r"macbook|laptop|bärbar|bærbar|notebook|vivobook|zenbook|stealth 15|cyborg|tuf f15|loq|flow z13|inet system|taurus .*(rtx|gaming)|utförsäljningsdator|stationär dator|\bpc\b"),
    ("components", r"geforce|radeon|rtx \d|rx \d|arc b\d|ryzen|core i\d|\bcpu\b|moderkort|motherboard|b650|b760|b860|x870|x670|z790|b840|b550|ddr[45]|psu|atx3|seasonic|nh-l12|noctua|chassi|pc case|kabinett|refine alcantara"),
    ("monitors", r"monitor|skärm|skærm|skjerm|\d{2}\" .*(ips|oled|va|tn|hz)|rog swift|ultragear|alienware|zowie|nitro x|arozzi nova"),
    ("phones_tablets", r"iphone|galaxy (s|a|z|tab)|pixel \d|realme|oneplus|xiaomi|ipad|surfplatta|tablet|tab s\d|boox|kobo|e-?reader|case|fodral|cover"),
    ("gaming", r"playstation|ps5|xbox|nintendo|switch 2|controller|handkontroll|dualsense|8bitdo|gamesir|moza|racing|ratt|pedal"),
    ("peripherals", r"mus\b|mouse|tangentbord|keyboard|keychron|huntsman|apex pro|k70|galleon|harpe|aerox|zywoo|wlmouse|keris|m330|mx keys|mx master|deskpad|wacom|cintiq|webcam"),
    ("audio", r"headset|hörlur|høretelefon|hodetelefon|buds|soundbar|högtalare|højttaler|speaker|soundlink|inzone|fairbuds|a-spire|wave dx|mikrofon|microphone|plaud"),
    ("tv_projectors", r"\btv\b|projektor|projector|benq th|oled\d{2}|hdmi sync|govee|bakbelysning"),
    ("smart_home", r"aqara|nuki|hue|smart|rökdetektor|kamera hub|camera hub"),
    ("networking", r"router|archer|wifi|mesh|switch \d+ port|antenn|5g lte"),
    ("appliances", r"mikrobølgeovn|mikrovågsugn|kylskåp|køleskab|kjøleskap|tvättmaskin|vaskemaskin|dammsugare|støvsuger|kaffemaskin|vitvar|hvidevar|hvitevar"),
    ("cables_power", r"kabel|cable|hub|dock|dockningsstation|laddare|charger|gan|power distributor|power box|powercore|proport|stikdåse|fuel tank|pdu|displayport-til|usb-c"),
    ("wearables", r"ring air|smartklocka|smartwatch|watch|klokke"),
    ("sport_outdoor", r"løbehjul|sparkcykel|scooter|cykel|sykkel|razor"),
]
_CAT_COMPILED = [(c, re.compile(p, re.I)) for c, p in _CATEGORY_RULES]


def classify_category(title: str, hint: Optional[str] = None) -> str:
    blob = f"{title} {hint or ''}"
    for cat, rx in _CAT_COMPILED:
        if rx.search(blob):
            return cat
    return "other"


_KNOWN_BRANDS = [
    "Apple", "Samsung", "Sony", "LG", "ASUS", "MSI", "Gigabyte", "AMD", "Intel", "Logitech", "Corsair",
    "SteelSeries", "Razer", "Kingston", "Anker", "Belkin", "Bose", "Philips", "Aqara", "nuki", "BenQ",
    "Dell", "Acer", "Lenovo", "HP", "Microsoft", "Nintendo", "PNY", "Sapphire", "PowerColor", "Wacom",
    "Elgato", "Keychron", "Seasonic", "Noctua", "Fractal Design", "TP-Link", "DELTACO", "Realme",
    "Ultrahuman", "Electrolux", "Brennenstuhl", "Showgear", "Botex", "Adam Hall", "T-Rex", "Razor",
    "Holdit", "ZOWIE", "Arozzi", "Moza", "8bitdo", "GameSir", "PLAUD", "Pulsar", "WLMouse", "Fairbuds",
    "Govee", "AceZone", "Taurus", "Inet", "Xiaomi", "OnePlus", "Google", "Garmin", "Dyson", "Bosch",
]
_BRAND_RX = re.compile(r"^(?:%s)\b" % "|".join(re.escape(b) for b in sorted(_KNOWN_BRANDS, key=len, reverse=True)), re.I)


def guess_brand(title: str) -> Optional[str]:
    m = _BRAND_RX.match(title.strip())
    if not m:
        return None
    hit = m.group(0).lower()
    for b in _KNOWN_BRANDS:
        if b.lower() == hit:
            return b
    return m.group(0)


def clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", title or "").strip()
