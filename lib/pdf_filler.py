import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"


def fill_pdf(character: dict, output_path: Path) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ModuleNotFoundError as exc:
        raise RuntimeError("Missing dependency: pypdf. Install requirements before using fill-pdf.") from exc

    field_maps_path = DATA_DIR / "pdf_field_maps.json"
    if not field_maps_path.exists():
        raise ValueError("PDF field mapping file is missing: data/pdf_field_maps.json")

    with field_maps_path.open(encoding="utf-8") as handle:
        all_maps = json.load(handle)

    book = character["book"]
    if book not in all_maps:
        raise ValueError(f"No PDF field mapping configured for book: {book}")

    book_map = all_maps[book]
    if not book_map.get("text") and not book_map.get("stats"):
        raise ValueError(f"PDF field mapping for {book!r} is empty.")

    pdf_path = ROOT_DIR / book_map["pdf_path"]
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    field_values: dict[str, str] = {}

    for field_name, key in book_map.get("text", {}).items():
        value = _resolve_character_value(character, key)
        if value not in (None, ""):
            field_values[field_name] = str(value)

    for field_name, stat_key in book_map.get("stats", {}).items():
        value = character.get("stats", {}).get(stat_key)
        if value not in (None, ""):
            field_values[field_name] = str(value)

    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values, auto_regenerate=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)


def _resolve_character_value(character: dict, key: str) -> str | None:
    if key.startswith("feat_") and key.endswith("_effect"):
        feat_index = int(key.split("_", maxsplit=2)[1]) - 1
        feat_details = character.get("feat_details", [])
        if feat_index < len(feat_details):
            return feat_details[feat_index].get("effect")
        return None

    if key.startswith("feat_"):
        feat_index = int(key.split("_", maxsplit=1)[1]) - 1
        feats = character.get("feats", [])
        return feats[feat_index] if feat_index < len(feats) else None

    if key.startswith("gear_"):
        gear_index = int(key.split("_", maxsplit=1)[1]) - 1
        gear = character.get("gear", [])
        return gear[gear_index] if gear_index < len(gear) else None

    if key.startswith("storage_"):
        storage_index = int(key.split("_", maxsplit=1)[1]) - 1
        storage = character.get("storage", [])
        return storage[storage_index] if storage_index < len(storage) else None

    return character.get(key)
