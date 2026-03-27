import json
import re
import sys
from pathlib import Path

import click

from lib.cheatsheet import generate_cheatsheet
from lib.data import get_by_name, load_available_feats
from lib.generator import generate_character
from lib.pdf_filler import fill_pdf
from lib.renderer import render_character_md


@click.group()
def cli() -> None:
    """Outgunned GM Toolset."""


@cli.command()
@click.option("--name", default=None, help="Character name")
@click.option("--role", default=None, help="Role name")
@click.option("--trope", default=None, help="Trope name")
@click.option("--feats", default=None, help="Comma-separated feat names")
@click.option(
    "--book",
    default="outgunned",
    type=click.Choice(["outgunned", "wok"]),
    help="Rulebook (outgunned or wok)",
)
def generate(name: str | None, role: str | None, trope: str | None, feats: str | None, book: str) -> None:
    """Generate a character and save it to characters/<name>/."""
    feat_list = [item.strip() for item in feats.split(",") if item.strip()] if feats else None

    try:
        character = generate_character(name=name, role=role, trope=trope, feats=feat_list, book=book)
        feats_data = _resolve_feats_data(book, character["feats"])
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1) from exc

    safe_name = re.sub(r"[^\w.-]+", "_", character["name"]).strip("_") or "character"
    output_dir = Path("characters") / safe_name
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "character.json"
    json_path.write_text(json.dumps(character, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    markdown_path = output_dir / "character.md"
    markdown_path.write_text(render_character_md(character, feats_data), encoding="utf-8")

    click.echo("Character generated:")
    click.echo(f"  JSON: {json_path}")
    click.echo(f"  Markdown: {markdown_path}")


@cli.command("fill-pdf")
@click.argument("character_json", type=click.Path(exists=True, path_type=Path))
def fill_pdf_cmd(character_json: Path) -> None:
    """Fill a character sheet PDF from CHARACTER_JSON."""
    with character_json.open(encoding="utf-8") as handle:
        character = json.load(handle)

    output_path = character_json.parent / "character_sheet.pdf"

    try:
        fill_pdf(character, output_path)
    except (RuntimeError, ValueError) as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1) from exc

    click.echo(f"PDF filled: {output_path}")


@cli.command()
@click.option(
    "--book",
    default="outgunned",
    type=click.Choice(["outgunned", "wok"]),
    help="Rulebook (outgunned or wok)",
)
def cheatsheet(book: str) -> None:
    """Generate a Markdown cheat sheet for all roles, tropes, and feats."""
    content = generate_cheatsheet(book)
    filename = "cheatsheet.md" if book == "outgunned" else f"cheatsheet_{book}.md"
    output_path = Path("docs") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    click.echo(f"Cheat sheet written: {output_path}")


def _resolve_feats_data(book: str, feat_names: list[str]) -> list[dict]:
    all_feats = load_available_feats(book)
    feats_data = []
    for feat_name in feat_names:
        try:
            feats_data.append(get_by_name(all_feats, feat_name))
        except ValueError:
            feats_data.append({"name": feat_name, "description_pl": "", "effect": ""})
    return feats_data


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit(130)
