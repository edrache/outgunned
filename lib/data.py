import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
VALID_BOOKS = {"outgunned", "wok"}


def _load(filename: str, book: str) -> list[dict]:
    if book not in VALID_BOOKS:
        valid = ", ".join(sorted(VALID_BOOKS))
        raise ValueError(f"Unknown book: {book!r}. Must be one of: {valid}")

    path = DATA_DIR / filename
    with path.open(encoding="utf-8") as handle:
        items = json.load(handle)

    return [item for item in items if item["book"] == book]


def load_roles(book: str) -> list[dict]:
    return _load("roles.json", book)


def load_tropes(book: str) -> list[dict]:
    return _load("tropes.json", book)


def load_feats(book: str) -> list[dict]:
    return _load("feats.json", book)


def load_available_feats(book: str) -> list[dict]:
    feats = load_feats("outgunned")
    if book == "wok":
        feats.extend(load_feats("wok"))
    return feats


def get_by_name(items: list[dict], name: str) -> dict:
    normalized_name = name.strip().lower()
    for item in items:
        if item["name"].strip().lower() == normalized_name:
            return item

    available = ", ".join(sorted(item["name"] for item in items))
    raise ValueError(f"{name!r} not found. Available: {available}")
