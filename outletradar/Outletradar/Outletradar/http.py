"""Polite HTTP client: robots.txt, per-host rate limiting, retries, conditional GET cache."""
from __future__ import annotations

import gzip
import hashlib
import json
import time
import urllib.error
import urllib.request
import urllib.robotparser
from pathlib import Path
from urllib.parse import urlparse

USER_AGENT = "OutletRadarBot/0.1 (+https://outletradar.se)"


class Fetcher:
    def __init__(self, cache_dir: Path, min_interval: float = 3.0, timeout: float = 30.0, respect_robots: bool = True):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.min_interval = min_interval
        self.timeout = timeout
        self.respect_robots = respect_robots
        self._last: dict[str, float] = {}
        self._robots: dict[str, urllib.robotparser.RobotFileParser] = {}
        self._meta_path = self.cache_dir / "_meta.json"
        self._meta = json.loads(self._meta_path.read_text()) if self._meta_path.exists() else {}

    # -- robots ---------------------------------------------------------------
    def allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        host = urlparse(url)
        base = f"{host.scheme}://{host.netloc}"
        rp = self._robots.get(base)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            try:
                req = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    rp.parse(r.read().decode("utf-8", "replace").splitlines())
            except urllib.error.HTTPError as e:
                # 4xx: no robots file means allowed; 5xx: be conservative
                rp.parse([] if 400 <= e.code < 500 else ["User-agent: *", "Disallow: /"])
            except Exception:
                rp.parse(["User-agent: *", "Disallow: /"])
            self._robots[base] = rp
        return rp.can_fetch(USER_AGENT, url)

    # -- fetch ----------------------------------------------------------------
    def _throttle(self, host: str):
        wait = self.min_interval - (time.monotonic() - self._last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        self._last[host] = time.monotonic()

    def get(self, url: str, accept: str = "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8", retries: int = 2) -> str:
        if not self.allowed(url):
            raise PermissionError(f"robots.txt disallows {url}")
        host = urlparse(url).netloc
        headers = {"User-Agent": USER_AGENT, "Accept": accept, "Accept-Encoding": "gzip",
                   "Accept-Language": "sv-SE,sv;q=0.9,da;q=0.8,nb;q=0.8,en;q=0.7"}
        meta = self._meta.get(url, {})
        cache_file = self.cache_dir / (hashlib.sha1(url.encode()).hexdigest() + ".body")
        if meta.get("etag") and cache_file.exists():
            headers["If-None-Match"] = meta["etag"]
        if meta.get("last_modified") and cache_file.exists():
            headers["If-Modified-Since"] = meta["last_modified"]
        err = None
        for attempt in range(retries + 1):
            self._throttle(host)
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    raw = r.read()
                    if r.headers.get("Content-Encoding") == "gzip":
                        raw = gzip.decompress(raw)
                    charset = r.headers.get_content_charset() or "utf-8"
                    body = raw.decode(charset, "replace")
                    cache_file.write_text(body, encoding="utf-8")
                    self._meta[url] = {"etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified")}
                    self._save_meta()
                    return body
            except urllib.error.HTTPError as e:
                if e.code == 304 and cache_file.exists():
                    return cache_file.read_text(encoding="utf-8")
                if e.code in (429, 500, 502, 503, 504):
                    err = e
                    time.sleep(5 * (attempt + 1))
                    continue
                raise
            except (urllib.error.URLError, TimeoutError) as e:
                err = e
                time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"GET failed for {url}: {err}")

    def _save_meta(self):
        self._meta_path.write_text(json.dumps(self._meta))
