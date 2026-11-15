from __future__ import annotations

from typing import Iterator

REGISTRY: dict[str, type["Adapter"]] = {}


def register(kind: str):
    def deco(cls):
        REGISTRY[kind] = cls
        cls.kind = kind
        return cls
    return deco


class Adapter:
    kind = "base"

    def __init__(self, cfg: dict, fetcher):
        self.cfg = cfg
        self.fetcher = fetcher

    def records(self) -> Iterator[dict]:  # pragma: no cover - interface
        raise NotImplementedError
