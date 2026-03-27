"""Helper for discovering PDF form fields by filling each field with its own name."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "tools"


def fill_for_inspection(source_path: Path, output_path: Path) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ModuleNotFoundError as exc:
        raise RuntimeError("Missing dependency: pypdf. Install requirements before inspecting PDF fields.") from exc

    reader = PdfReader(str(source_path))
    writer = PdfWriter()
    writer.append(reader)

    fields = reader.get_fields() or {}
    field_values: dict[str, str] = {}

    for field_name, field_data in fields.items():
        field_type = field_data.get("/FT")
        if field_type == "/Tx":
            field_values[field_name] = field_name

    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values, auto_regenerate=False)

    with output_path.open("wb") as handle:
        writer.write(handle)

    print(f"Written: {output_path}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    jobs = [
        (
            ROOT_DIR / "PDF" / "OG_Hero Sheet_ENG_Fillable.pdf",
            OUTPUT_DIR / "hero_sheet_inspected.pdf",
        ),
        (
            ROOT_DIR / "PDF" / "World of Killers" / "Killer Sheet.pdf",
            OUTPUT_DIR / "killer_sheet_inspected.pdf",
        ),
    ]

    for source_path, output_path in jobs:
        fill_for_inspection(source_path, output_path)


if __name__ == "__main__":
    main()
