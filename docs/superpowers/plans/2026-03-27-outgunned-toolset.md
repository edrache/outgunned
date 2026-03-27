# Outgunned GM Toolset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI (`outgunned.py`) for generating Outgunned RPG characters (JSON + Markdown) and filling character sheet PDFs on demand.

**Architecture:** Single `outgunned.py` entry point using Click subcommands; game logic split across focused modules in `lib/`; game data hardcoded in `data/*.json`; PDF field mapping stored in `data/pdf_field_maps.json` (discovered via helper script).

**Tech Stack:** Python 3, Click, Jinja2, pypdf, pytest

---

## File Map

| File | Responsibility |
|------|---------------|
| `outgunned.py` | CLI entry point — Click group + subcommand wiring only |
| `lib/__init__.py` | Empty |
| `lib/data.py` | Load and query `data/*.json`; filter by book |
| `lib/generator.py` | Build character dict from name/role/trope/feats/book |
| `lib/renderer.py` | Render character dict → Markdown via Jinja2 |
| `lib/pdf_filler.py` | Fill PDF form fields from character dict |
| `lib/cheatsheet.py` | Build cheat sheet Markdown from data files |
| `data/roles.json` | Role definitions (id, name, book, description_pl, stats, starting_feats) |
| `data/tropes.json` | Trope definitions (id, name, book, description_pl) |
| `data/feats.json` | Feat definitions (id, name, book, description_pl) |
| `data/pdf_field_maps.json` | PDF field name → character key mappings per book |
| `templates/character.md.jinja2` | Markdown template for character sheet |
| `requirements.txt` | Python dependencies |
| `AGENTS.md` | Project context for Codex CLI |
| `tests/test_data.py` | Tests for lib/data.py |
| `tests/test_generator.py` | Tests for lib/generator.py |
| `tests/test_renderer.py` | Tests for lib/renderer.py |
| `tests/test_cheatsheet.py` | Tests for lib/cheatsheet.py |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `AGENTS.md`
- Create: `lib/__init__.py`
- Create: `tests/__init__.py`
- Create: `characters/.gitkeep`

- [ ] **Step 1: Create requirements.txt**

```
click>=8.0
jinja2>=3.0
pypdf>=4.0
pytest>=7.0
```

- [ ] **Step 2: Create lib/__init__.py and tests/__init__.py**

Both files are empty. Create them:
```bash
mkdir -p lib tests characters templates data
touch lib/__init__.py tests/__init__.py characters/.gitkeep
```

- [ ] **Step 3: Create AGENTS.md**

```markdown
# Outgunned GM Toolset

Python CLI for running Outgunned RPG campaigns (core + World of Killers expansion).

## Commands

Generate a random character:
    python outgunned.py generate

Generate with specific options:
    python outgunned.py generate --name "John Doe" --role "Hitman" --trope "The Professional" --feats "Quick Draw,Iron Will" --book outgunned

Generate a World of Killers character:
    python outgunned.py generate --book wok

Fill a character sheet PDF (on demand):
    python outgunned.py fill-pdf characters/john_doe/character.json

Generate cheat sheet:
    python outgunned.py cheatsheet
    python outgunned.py cheatsheet --book wok

## Directory Structure

    data/           Game data: roles.json, tropes.json, feats.json, pdf_field_maps.json
    characters/     Generated characters — one subdirectory per character
    templates/      Jinja2 templates for Markdown output
    PDF/            Original PDF files — READ ONLY, never modify
    docs/           Documentation and cheat sheets

## Output Format

Each generated character produces:
- characters/<name>/character.json  — machine-readable character data
- characters/<name>/character.md    — human-readable character sheet

## Books

- outgunned  — Outgunned Core Rulebook
- wok        — World of Killers expansion

## Data Files

- data/roles.json   — Available roles per book
- data/tropes.json  — Available tropes per book
- data/feats.json   — Available feats per book

Each entry has: id, name, book, description_pl (Polish description for GM reference)

## Running Tests

    pytest tests/ -v
```

- [ ] **Step 4: Verify structure**

```bash
ls -la lib/ tests/ data/ characters/ templates/
```

Expected: directories exist, `lib/__init__.py` and `tests/__init__.py` are present.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt AGENTS.md lib/__init__.py tests/__init__.py characters/.gitkeep
git commit -m "chore: project scaffolding for Outgunned GM toolset"
```

---

## Task 2: Populate Game Data from Rulebook

**Files:**
- Create: `data/roles.json`
- Create: `data/tropes.json`
- Create: `data/feats.json`

Read `PDF/Outgunned_Corebook_ENG_2.0.pdf` and `PDF/World of Killers/Outgunned_WorldOfKillers.pdf` to extract all Roles, Tropes, and Feats. Populate the JSON files using the schema below.

- [ ] **Step 1: Create data/roles.json from Outgunned Corebook**

Read the corebook PDF. Find the section listing all Roles (character archetypes). For each Role, record its name, stats bonuses, starting feats, and write a Polish description (2-3 sentences for GM reference).

Schema:
```json
[
  {
    "id": "slug-from-name",
    "name": "Role Name",
    "book": "outgunned",
    "description_pl": "Opis po polsku dla MG.",
    "stats": {
      "action": 0,
      "stealth": 0,
      "social": 0,
      "technical": 0,
      "willpower": 0,
      "perception": 0
    },
    "starting_feats": ["Feat Name"]
  }
]
```

Add WoK roles at the bottom with `"book": "wok"`.

- [ ] **Step 2: Create data/tropes.json**

Read both PDFs. Find all Tropes. For each Trope:

```json
[
  {
    "id": "slug-from-name",
    "name": "Trope Name",
    "book": "outgunned",
    "description_pl": "Opis po polsku dla MG.",
    "bonus": "Brief description of mechanical bonus (English)"
  }
]
```

- [ ] **Step 3: Create data/feats.json**

Read both PDFs. Find all Feats. For each Feat:

```json
[
  {
    "id": "slug-from-name",
    "name": "Feat Name",
    "book": "outgunned",
    "description_pl": "Opis po polsku dla MG.",
    "effect": "Mechanical effect summary (English)"
  }
]
```

- [ ] **Step 4: Verify JSON is valid**

```bash
python3 -c "
import json
for f in ['data/roles.json', 'data/tropes.json', 'data/feats.json']:
    data = json.load(open(f))
    books = set(e['book'] for e in data)
    print(f'{f}: {len(data)} entries, books={books}')
"
```

Expected: all three files parse without error, each has at least 1 entry for `outgunned`.

- [ ] **Step 5: Commit**

```bash
git add data/roles.json data/tropes.json data/feats.json
git commit -m "feat: add game data for Outgunned and WoK"
```

---

## Task 3: Data Loader (`lib/data.py`)

**Files:**
- Create: `lib/data.py`
- Create: `tests/test_data.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_data.py`:

```python
import pytest
from lib.data import load_roles, load_tropes, load_feats, get_by_name

def test_load_roles_outgunned_returns_list():
    roles = load_roles("outgunned")
    assert isinstance(roles, list)
    assert len(roles) > 0

def test_load_roles_wok_returns_only_wok():
    roles = load_roles("wok")
    assert all(r["book"] == "wok" for r in roles)

def test_load_roles_invalid_book_raises():
    with pytest.raises(ValueError, match="Unknown book"):
        load_roles("invalid")

def test_load_tropes_outgunned():
    tropes = load_tropes("outgunned")
    assert len(tropes) > 0
    assert all("name" in t for t in tropes)

def test_load_feats_outgunned():
    feats = load_feats("outgunned")
    assert len(feats) > 0
    assert all("name" in f for f in feats)

def test_get_by_name_found(tmp_path):
    items = [{"id": "foo", "name": "Foo", "book": "outgunned"}]
    result = get_by_name(items, "Foo")
    assert result["id"] == "foo"

def test_get_by_name_case_insensitive():
    items = [{"id": "foo", "name": "Foo", "book": "outgunned"}]
    result = get_by_name(items, "foo")
    assert result["id"] == "foo"

def test_get_by_name_not_found_raises():
    with pytest.raises(ValueError, match="not found"):
        get_by_name([], "Missing")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_data.py -v
```

Expected: `ImportError` or `ModuleNotFoundError` for `lib.data`.

- [ ] **Step 3: Implement lib/data.py**

```python
import json
import pathlib

_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
_VALID_BOOKS = {"outgunned", "wok"}


def _load(filename: str, book: str) -> list[dict]:
    if book not in _VALID_BOOKS:
        raise ValueError(f"Unknown book: {book!r}. Must be one of {_VALID_BOOKS}")
    path = _DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [entry for entry in data if entry["book"] == book]


def load_roles(book: str) -> list[dict]:
    return _load("roles.json", book)


def load_tropes(book: str) -> list[dict]:
    return _load("tropes.json", book)


def load_feats(book: str) -> list[dict]:
    return _load("feats.json", book)


def get_by_name(items: list[dict], name: str) -> dict:
    name_lower = name.lower()
    for item in items:
        if item["name"].lower() == name_lower:
            return item
    available = [i["name"] for i in items]
    raise ValueError(f"{name!r} not found. Available: {available}")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_data.py -v
```

Expected: all 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/data.py tests/test_data.py
git commit -m "feat: add data loader for roles, tropes, feats"
```

---

## Task 4: Character Generator (`lib/generator.py`)

**Files:**
- Create: `lib/generator.py`
- Create: `tests/test_generator.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_generator.py`:

```python
import pytest
from unittest.mock import patch
from lib.generator import generate_character

# Minimal fake data for isolation
FAKE_ROLES = [{"id": "hitman", "name": "Hitman", "book": "outgunned",
               "description_pl": "Desc", "stats": {"action": 2}, "starting_feats": ["Quick Draw"]}]
FAKE_TROPES = [{"id": "pro", "name": "The Professional", "book": "outgunned",
                "description_pl": "Desc"}]
FAKE_FEATS = [
    {"id": "quick-draw", "name": "Quick Draw", "book": "outgunned", "description_pl": "Desc", "effect": "Fast"},
    {"id": "iron-will", "name": "Iron Will", "book": "outgunned", "description_pl": "Desc", "effect": "Tough"},
]


def _patch_data(fn):
    """Decorator that patches all data loaders with fake data."""
    import functools
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with patch("lib.generator.load_roles", return_value=FAKE_ROLES), \
             patch("lib.generator.load_tropes", return_value=FAKE_TROPES), \
             patch("lib.generator.load_feats", return_value=FAKE_FEATS):
            return fn(*args, **kwargs)
    return wrapper


@_patch_data
def test_generate_returns_required_keys():
    char = generate_character(book="outgunned")
    for key in ("name", "book", "role", "trope", "feats", "stats", "generated_at"):
        assert key in char, f"Missing key: {key}"


@_patch_data
def test_generate_explicit_role():
    char = generate_character(role="Hitman", book="outgunned")
    assert char["role"] == "Hitman"


@_patch_data
def test_generate_explicit_trope():
    char = generate_character(trope="The Professional", book="outgunned")
    assert char["trope"] == "The Professional"


@_patch_data
def test_generate_explicit_feats():
    char = generate_character(feats=["Quick Draw", "Iron Will"], book="outgunned")
    assert "Quick Draw" in char["feats"]
    assert "Iron Will" in char["feats"]


@_patch_data
def test_generate_random_fills_all_fields():
    char = generate_character(book="outgunned")
    assert char["role"] != ""
    assert char["trope"] != ""
    assert isinstance(char["feats"], list)


@_patch_data
def test_generate_explicit_name():
    char = generate_character(name="John Doe", book="outgunned")
    assert char["name"] == "John Doe"


@_patch_data
def test_generate_default_name_has_prefix():
    char = generate_character(book="outgunned")
    assert char["name"].startswith("Hero_")


@_patch_data
def test_generate_wok_name_prefix():
    with patch("lib.generator.load_roles", return_value=[{**FAKE_ROLES[0], "book": "wok"}]), \
         patch("lib.generator.load_tropes", return_value=[{**FAKE_TROPES[0], "book": "wok"}]), \
         patch("lib.generator.load_feats", return_value=[{**FAKE_FEATS[0], "book": "wok"}, {**FAKE_FEATS[1], "book": "wok"}]):
        char = generate_character(book="wok")
        assert char["name"].startswith("Killer_")


@_patch_data
def test_generate_invalid_role_raises():
    with pytest.raises(ValueError):
        generate_character(role="NonExistent", book="outgunned")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_generator.py -v
```

Expected: `ImportError` for `lib.generator`.

- [ ] **Step 3: Implement lib/generator.py**

```python
import random
from datetime import date
from lib.data import load_roles, load_tropes, load_feats, get_by_name


def generate_character(
    name: str | None = None,
    role: str | None = None,
    trope: str | None = None,
    feats: list[str] | None = None,
    book: str = "outgunned",
) -> dict:
    roles = load_roles(book)
    tropes = load_tropes(book)
    all_feats = load_feats(book)

    chosen_role = get_by_name(roles, role) if role else random.choice(roles)
    chosen_trope = get_by_name(tropes, trope) if trope else random.choice(tropes)

    if feats:
        chosen_feats = [get_by_name(all_feats, f)["name"] for f in feats]
    else:
        # Random feats: start with role's starting feats, fill rest randomly
        starting = chosen_role.get("starting_feats", [])
        pool = [f for f in all_feats if f["name"] not in starting]
        extra = random.sample(pool, min(2, len(pool)))
        chosen_feats = starting + [f["name"] for f in extra]

    if name is None:
        prefix = "Killer" if book == "wok" else "Hero"
        name = f"{prefix}_{date.today().strftime('%Y%m%d')}_{random.randint(100, 999)}"

    return {
        "name": name,
        "book": book,
        "role": chosen_role["name"],
        "trope": chosen_trope["name"],
        "feats": chosen_feats,
        "stats": chosen_role.get("stats", {}),
        "generated_at": date.today().isoformat(),
    }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_generator.py -v
```

Expected: all 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/generator.py tests/test_generator.py
git commit -m "feat: add character generator"
```

---

## Task 5: Markdown Template and Renderer (`lib/renderer.py`)

**Files:**
- Create: `templates/character.md.jinja2`
- Create: `lib/renderer.py`
- Create: `tests/test_renderer.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_renderer.py`:

```python
from lib.renderer import render_character_md

SAMPLE_CHAR = {
    "name": "John Doe",
    "book": "outgunned",
    "role": "Hitman",
    "trope": "The Professional",
    "feats": ["Quick Draw", "Iron Will"],
    "stats": {"action": 3, "stealth": 2},
    "generated_at": "2026-03-27",
}

SAMPLE_FEATS_DATA = [
    {"name": "Quick Draw", "description_pl": "Szybki strzał.", "effect": "Draw faster"},
    {"name": "Iron Will", "description_pl": "Silna wola.", "effect": "Resist mind"},
]


def test_render_contains_name():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "John Doe" in md


def test_render_contains_role():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Hitman" in md


def test_render_contains_trope():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "The Professional" in md


def test_render_contains_feat_names():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Quick Draw" in md
    assert "Iron Will" in md


def test_render_contains_feat_descriptions():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Szybki strzał" in md


def test_render_contains_stats():
    md = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "action" in md.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_renderer.py -v
```

Expected: `ImportError` for `lib.renderer`.

- [ ] **Step 3: Create templates/character.md.jinja2**

```jinja2
# {{ character.name }}

**Book:** {{ character.book }}
**Generated:** {{ character.generated_at }}

---

## Identity

| Field | Value |
|-------|-------|
| Role | {{ character.role }} |
| Trope | {{ character.trope }} |

---

## Stats

{% for stat, value in character.stats.items() -%}
- **{{ stat | title }}:** {{ value }}
{% endfor %}

---

## Feats

{% for feat in feats_data -%}
### {{ feat.name }}

*{{ feat.description_pl }}*

**Effect:** {{ feat.effect }}

{% endfor %}
```

- [ ] **Step 4: Implement lib/renderer.py**

```python
import pathlib
from jinja2 import Environment, FileSystemLoader

_TEMPLATES_DIR = pathlib.Path(__file__).parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), keep_trailing_newline=True)


def render_character_md(character: dict, feats_data: list[dict]) -> str:
    template = _env.get_template("character.md.jinja2")
    return template.render(character=character, feats_data=feats_data)
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_renderer.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add templates/character.md.jinja2 lib/renderer.py tests/test_renderer.py
git commit -m "feat: add Markdown renderer for character sheets"
```

---

## Task 6: `generate` CLI Command

**Files:**
- Create: `outgunned.py`

- [ ] **Step 1: Create outgunned.py with generate command**

```python
import json
import pathlib
import re
import sys

import click

from lib.data import load_feats, get_by_name
from lib.generator import generate_character
from lib.renderer import render_character_md


@click.group()
def cli():
    """Outgunned GM Toolset."""


@cli.command()
@click.option("--name", default=None, help="Character name")
@click.option("--role", default=None, help="Role name")
@click.option("--trope", default=None, help="Trope name")
@click.option("--feats", default=None, help="Comma-separated feat names")
@click.option("--book", default="outgunned", type=click.Choice(["outgunned", "wok"]),
              help="Rulebook (outgunned or wok)")
def generate(name, role, trope, feats, book):
    """Generate a character and save to characters/<name>/."""
    feat_list = [f.strip() for f in feats.split(",")] if feats else None

    try:
        character = generate_character(name=name, role=role, trope=trope,
                                       feats=feat_list, book=book)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Resolve feats data for Markdown (only feats the character has)
    all_feats = load_feats(book)
    feats_data = []
    for feat_name in character["feats"]:
        try:
            feats_data.append(get_by_name(all_feats, feat_name))
        except ValueError:
            feats_data.append({"name": feat_name, "description_pl": "", "effect": ""})

    # Create output directory
    safe_name = re.sub(r"[^\w\-]", "_", character["name"])
    out_dir = pathlib.Path("characters") / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON
    json_path = out_dir / "character.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(character, f, indent=2, ensure_ascii=False)

    # Write Markdown
    md_path = out_dir / "character.md"
    md_path.write_text(render_character_md(character, feats_data), encoding="utf-8")

    click.echo(f"Character generated:")
    click.echo(f"  JSON: {json_path}")
    click.echo(f"  Markdown: {md_path}")


if __name__ == "__main__":
    cli()
```

- [ ] **Step 2: Test generate command manually**

```bash
python outgunned.py generate --name "Test Hero" --book outgunned
```

Expected: output shows paths to two files, both files exist in `characters/Test_Hero/`.

- [ ] **Step 3: Verify JSON structure**

```bash
python3 -c "import json; print(json.dumps(json.load(open('characters/Test_Hero/character.json')), indent=2))"
```

Expected: JSON with keys `name`, `book`, `role`, `trope`, `feats`, `stats`, `generated_at`.

- [ ] **Step 4: Verify Markdown**

```bash
cat characters/Test_Hero/character.md
```

Expected: readable Markdown with character name, role, trope, feats with Polish descriptions.

- [ ] **Step 5: Commit**

```bash
git add outgunned.py
git commit -m "feat: add generate CLI command"
```

---

## Task 7: PDF Field Discovery and Mapping

**Files:**
- Create: `data/pdf_field_maps.json`
- Create: `tools/inspect_pdf_fields.py` (helper script, not part of CLI)

The Hero Sheet and Killer Sheet use Italian-named numbered form fields (`Campo testo NNN` for text, `Casella di controllo NNN` for checkboxes). There are no tooltips. This task maps field numbers to character data keys by visual inspection.

- [ ] **Step 1: Create tools/inspect_pdf_fields.py**

```bash
mkdir -p tools
```

```python
"""Fill all PDF fields with their own names to identify them visually."""
import sys
import pathlib
from pypdf import PdfReader, PdfWriter

def fill_for_inspection(src_path: str, out_path: str) -> None:
    reader = PdfReader(src_path)
    writer = PdfWriter()
    writer.append(reader)

    fields = reader.get_fields() or {}
    # For text fields: write the field name; for checkboxes: check them
    text_values = {}
    for name, field in fields.items():
        ft = field.get("/FT")
        if ft == "/Tx":
            # Use short label (last word of field name)
            text_values[name] = name.split()[-1]
        elif ft == "/Btn":
            text_values[name] = "/Yes"

    for page in writer.pages:
        writer.update_page_form_field_values(page, text_values, auto_regenerate=False)

    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"Written: {out_path}")

if __name__ == "__main__":
    fill_for_inspection(
        "PDF/OG_Hero Sheet_ENG_Fillable.pdf",
        "tools/hero_sheet_inspected.pdf"
    )
    fill_for_inspection(
        "PDF/World of Killers/Killer Sheet.pdf",
        "tools/killer_sheet_inspected.pdf"
    )
```

- [ ] **Step 2: Run the inspection script**

```bash
python tools/inspect_pdf_fields.py
```

Expected: `tools/hero_sheet_inspected.pdf` and `tools/killer_sheet_inspected.pdf` created.

- [ ] **Step 3: Open both PDFs and map fields**

Open `tools/hero_sheet_inspected.pdf` and `tools/killer_sheet_inspected.pdf`. Each text field shows its own number. Each checked box is visible. Record which field number corresponds to which character data (name, role, trope, each feat slot, each stat, etc.).

- [ ] **Step 4: Create data/pdf_field_maps.json**

After visual inspection, create the mapping. Use this structure:

```json
{
  "outgunned": {
    "text": {
      "Campo testo 40": "name",
      "Campo testo 41": "role",
      "Campo testo 42": "trope",
      "Campo testo 48": "feat_1",
      "Campo testo 52": "feat_2",
      "Campo testo 54": "feat_3"
    },
    "stats": {
      "Campo testo 45": "action",
      "Campo testo 46": "stealth",
      "Campo testo 47": "social"
    },
    "pdf_path": "PDF/OG_Hero Sheet_ENG_Fillable.pdf"
  },
  "wok": {
    "text": {
      "Campo testo 1012": "name",
      "Campo testo 1013": "role",
      "Campo testo 1014": "trope",
      "Campo testo 1016": "feat_1",
      "Campo testo 1018": "feat_2"
    },
    "stats": {},
    "pdf_path": "PDF/World of Killers/Killer Sheet.pdf"
  }
}
```

**IMPORTANT:** Replace the field numbers above with the actual ones you observed in step 3. The numbers shown here are placeholders — the real mapping comes from your visual inspection.

- [ ] **Step 5: Validate JSON**

```bash
python3 -c "import json; m = json.load(open('data/pdf_field_maps.json')); print('outgunned fields:', len(m['outgunned']['text'])); print('wok fields:', len(m['wok']['text']))"
```

Expected: both books have at least 3 mapped text fields.

- [ ] **Step 6: Commit**

```bash
git add tools/inspect_pdf_fields.py data/pdf_field_maps.json
git commit -m "feat: add PDF field mapping for Hero Sheet and Killer Sheet"
```

---

## Task 8: PDF Filler (`lib/pdf_filler.py`)

**Files:**
- Create: `lib/pdf_filler.py`

No unit tests for this module — it depends on real PDF files which aren't suitable for unit testing. Integration is verified by manual inspection of the output PDF.

- [ ] **Step 1: Implement lib/pdf_filler.py**

```python
import json
import pathlib
from pypdf import PdfReader, PdfWriter

_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
_PDF_DIR = pathlib.Path(__file__).parent.parent / "PDF"


def fill_pdf(character: dict, output_path: pathlib.Path) -> None:
    """Fill a character sheet PDF from a character dict and save to output_path."""
    book = character["book"]

    maps_path = _DATA_DIR / "pdf_field_maps.json"
    with open(maps_path, encoding="utf-8") as f:
        all_maps = json.load(f)

    if book not in all_maps:
        raise ValueError(f"No PDF field map for book: {book!r}")

    book_map = all_maps[book]
    pdf_path = _PDF_DIR / pathlib.Path(book_map["pdf_path"]).relative_to("PDF")

    # Build field values dict
    field_values: dict[str, str] = {}

    for field_name, char_key in book_map.get("text", {}).items():
        value = _resolve_char_key(character, char_key)
        if value is not None:
            field_values[field_name] = str(value)

    for field_name, stat_key in book_map.get("stats", {}).items():
        value = character.get("stats", {}).get(stat_key)
        if value is not None:
            field_values[field_name] = str(value)

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values, auto_regenerate=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)


def _resolve_char_key(character: dict, key: str) -> str | None:
    """Resolve a character key like 'feat_1', 'feat_2', 'name', 'role', etc."""
    if key.startswith("feat_"):
        idx = int(key.split("_")[1]) - 1
        feats = character.get("feats", [])
        return feats[idx] if idx < len(feats) else None
    return character.get(key)
```

- [ ] **Step 2: Wire fill-pdf command into outgunned.py**

Add this import at the top of `outgunned.py` (after existing imports):
```python
from lib.pdf_filler import fill_pdf
```

Add this command after the `generate` command:
```python
@cli.command("fill-pdf")
@click.argument("character_json", type=click.Path(exists=True))
def fill_pdf_cmd(character_json):
    """Fill a character sheet PDF from CHARACTER_JSON file."""
    char_path = pathlib.Path(character_json)
    with open(char_path, encoding="utf-8") as f:
        character = json.load(f)

    out_path = char_path.parent / "character_sheet.pdf"
    try:
        fill_pdf(character, out_path)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    click.echo(f"PDF filled: {out_path}")
```

- [ ] **Step 3: Test fill-pdf command**

First generate a character, then fill its PDF:
```bash
python outgunned.py generate --name "PDF Test" --book outgunned
python outgunned.py fill-pdf characters/PDF_Test/character.json
```

Expected: `characters/PDF_Test/character_sheet.pdf` created.

- [ ] **Step 4: Verify output PDF manually**

Open `characters/PDF_Test/character_sheet.pdf` and confirm that character data (name, role, trope, feats) appears in the correct fields.

- [ ] **Step 5: Commit**

```bash
git add lib/pdf_filler.py outgunned.py
git commit -m "feat: add PDF filler and fill-pdf command"
```

---

## Task 9: Cheat Sheet Generator (`lib/cheatsheet.py`)

**Files:**
- Create: `lib/cheatsheet.py`
- Create: `tests/test_cheatsheet.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_cheatsheet.py`:

```python
from unittest.mock import patch
from lib.cheatsheet import generate_cheatsheet

FAKE_ROLES = [{"name": "Hitman", "description_pl": "Zawodowy zabójca.", "book": "outgunned"}]
FAKE_TROPES = [{"name": "The Professional", "description_pl": "Zimna krew.", "book": "outgunned"}]
FAKE_FEATS = [{"name": "Quick Draw", "description_pl": "Szybki strzał.", "effect": "Fast draw", "book": "outgunned"}]


def _patch_loaders(fn):
    import functools
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with patch("lib.cheatsheet.load_roles", return_value=FAKE_ROLES), \
             patch("lib.cheatsheet.load_tropes", return_value=FAKE_TROPES), \
             patch("lib.cheatsheet.load_feats", return_value=FAKE_FEATS):
            return fn(*args, **kwargs)
    return wrapper


@_patch_loaders
def test_cheatsheet_contains_roles_section():
    md = generate_cheatsheet("outgunned")
    assert "## Roles" in md


@_patch_loaders
def test_cheatsheet_contains_role_name():
    md = generate_cheatsheet("outgunned")
    assert "Hitman" in md


@_patch_loaders
def test_cheatsheet_contains_polish_description():
    md = generate_cheatsheet("outgunned")
    assert "Zawodowy zabójca" in md


@_patch_loaders
def test_cheatsheet_contains_tropes_section():
    md = generate_cheatsheet("outgunned")
    assert "## Tropes" in md


@_patch_loaders
def test_cheatsheet_contains_feats_section():
    md = generate_cheatsheet("outgunned")
    assert "## Feats" in md


@_patch_loaders
def test_cheatsheet_contains_feat_effect():
    md = generate_cheatsheet("outgunned")
    assert "Fast draw" in md
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_cheatsheet.py -v
```

Expected: `ImportError` for `lib.cheatsheet`.

- [ ] **Step 3: Implement lib/cheatsheet.py**

```python
from lib.data import load_roles, load_tropes, load_feats


def generate_cheatsheet(book: str) -> str:
    roles = load_roles(book)
    tropes = load_tropes(book)
    feats = load_feats(book)

    lines = [f"# Outgunned Cheat Sheet — {book.upper()}\n"]

    lines.append("## Roles\n")
    for role in roles:
        lines.append(f"### {role['name']}\n")
        lines.append(f"{role['description_pl']}\n")

    lines.append("## Tropes\n")
    for trope in tropes:
        lines.append(f"### {trope['name']}\n")
        lines.append(f"{trope['description_pl']}\n")

    lines.append("## Feats\n")
    for feat in feats:
        lines.append(f"### {feat['name']}\n")
        lines.append(f"{feat['description_pl']}\n")
        lines.append(f"**Effect:** {feat.get('effect', '')}\n")

    return "\n".join(lines)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_cheatsheet.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 5: Wire cheatsheet command into outgunned.py**

Add this import at the top of `outgunned.py`:
```python
from lib.cheatsheet import generate_cheatsheet
```

Add this command:
```python
@cli.command()
@click.option("--book", default="outgunned", type=click.Choice(["outgunned", "wok"]),
              help="Rulebook (outgunned or wok)")
def cheatsheet(book):
    """Generate a Markdown cheat sheet for all roles, tropes, and feats."""
    md = generate_cheatsheet(book)
    suffix = "" if book == "outgunned" else f"_{book}"
    out_path = pathlib.Path("docs") / f"cheatsheet{suffix}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    click.echo(f"Cheat sheet written: {out_path}")
```

- [ ] **Step 6: Test cheatsheet command**

```bash
python outgunned.py cheatsheet
python outgunned.py cheatsheet --book wok
```

Expected: `docs/cheatsheet.md` and `docs/cheatsheet_wok.md` created, each containing Polish descriptions of all roles, tropes, and feats.

- [ ] **Step 7: Run all tests**

```bash
pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 8: Commit**

```bash
git add lib/cheatsheet.py tests/test_cheatsheet.py outgunned.py
git commit -m "feat: add cheat sheet generator and cheatsheet command"
```

---

## Final Verification

- [ ] **Run full test suite**

```bash
pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Smoke test all three commands**

```bash
python outgunned.py generate --name "Final Test" --book outgunned
python outgunned.py fill-pdf characters/Final_Test/character.json
python outgunned.py cheatsheet
python outgunned.py cheatsheet --book wok
```

Expected: no errors, all output files exist.

- [ ] **Verify help text**

```bash
python outgunned.py --help
python outgunned.py generate --help
python outgunned.py fill-pdf --help
python outgunned.py cheatsheet --help
```

Expected: all commands show usage instructions.
