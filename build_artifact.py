"""Inline current data into one self-contained HTML file.
Usage: python build_artifact.py [public_dir] [out_file]"""
import json, pathlib, sys
root = pathlib.Path(__file__).parent
src = root / (sys.argv[1] if len(sys.argv) > 1 else "public")
out = root / (sys.argv[2] if len(sys.argv) > 2 else "dist/outletradar.html")
html = (src / "index.html").read_text(encoding="utf-8")
data = {"listings": json.loads((src / "data/listings.json").read_text(encoding="utf-8")),
        "meta": json.loads((src / "data/meta.json").read_text(encoding="utf-8"))}
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = html.replace('<link rel="manifest" href="manifest.webmanifest">', "")
html = html.replace("<script>\n(() => {", f"<script>window.__FR_DATA__={blob};</script>\n<script>\n(() => {{", 1)
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print("wrote", out, len(html) // 1024, "KiB")
