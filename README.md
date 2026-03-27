# Outgunned GM Toolset

Python CLI for generating Outgunned RPG characters, rendering Markdown sheets, producing quick-reference cheat sheets, and filling local PDF character forms.

## What It Does

- Generates random or partially specified characters for:
  - `outgunned` (core book)
  - `wok` (World of Killers)
- Saves each generated character as:
  - `characters/<name>/character.json`
  - `characters/<name>/character.md`
- Builds Markdown cheat sheets from the curated game data in `data/`
- Fills local PDF sheets when the original fillable forms are available on disk

## Project Layout

```text
Outgunned/
├── outgunned.py
├── lib/
│   ├── data.py
│   ├── generator.py
│   ├── renderer.py
│   ├── cheatsheet.py
│   └── pdf_filler.py
├── data/
│   ├── roles.json
│   ├── tropes.json
│   ├── feats.json
│   └── pdf_field_maps.json
├── templates/
│   └── character.md.jinja2
├── tests/
├── tools/
│   └── inspect_pdf_fields.py
├── docs/
│   ├── cheatsheet.md
│   └── cheatsheet_wok.md
└── characters/
```

## Requirements

- Python 3.14 tested locally
- Dependencies from `requirements.txt`

Install locally:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## CLI Usage

All commands run through:

```bash
.venv/bin/python outgunned.py <command>
```

### Generate a Character

Random core-book character:

```bash
.venv/bin/python outgunned.py generate
```

Random World of Killers character:

```bash
.venv/bin/python outgunned.py generate --book wok
```

Pinned values:

```bash
.venv/bin/python outgunned.py generate \
  --name "John Doe" \
  --role "The Ace" \
  --trope "Leader" \
  --feats "Full Throttle!,Crazy Stunt" \
  --book outgunned
```

Output:

- `characters/<safe_name>/character.json`
- `characters/<safe_name>/character.md`

### Generate Cheat Sheets

Core:

```bash
.venv/bin/python outgunned.py cheatsheet
```

World of Killers:

```bash
.venv/bin/python outgunned.py cheatsheet --book wok
```

Output:

- `docs/cheatsheet.md`
- `docs/cheatsheet_wok.md`

### Fill a Character Sheet PDF

```bash
.venv/bin/python outgunned.py fill-pdf characters/John_Doe/character.json
```

Output:

- `characters/John_Doe/character_sheet.pdf`

## Local PDF Assets

The repository does **not** include the original rulebook PDFs or fillable character sheets in git history anymore.

To use `fill-pdf`, keep the required source PDFs locally under `PDF/` with these paths:

```text
PDF/OG_Hero Sheet_ENG_Fillable.pdf
PDF/World of Killers/Killer Sheet.pdf
```

The field maps in `data/pdf_field_maps.json` were built against those local filenames.

If the files are missing, `fill-pdf` will return a clear error instead of crashing.

## Data Model Notes

### Roles

Stored in `data/roles.json` with:

- `id`
- `name`
- `book`
- `description_pl`
- `stats`
- `skill_points`
- `starting_feats`
- `choose_feats`
- `gear`

### Tropes

Stored in `data/tropes.json` with:

- `id`
- `name`
- `book`
- `description_pl`
- `bonus`

### Feats

Stored in `data/feats.json` with:

- `id`
- `name`
- `book`
- `description_pl`
- `effect`

### Character Output

Generated JSON includes:

- identity fields such as `name`, `book`, `role`, `trope`
- Polish descriptive fields for role and trope
- selected feats and expanded `feat_details`
- role stats, skills, gear
- `generated_at`

World of Killers roles may reference both core-book feats and expansion feats. The generator accounts for that by loading core feats plus WoK feats when `--book wok` is selected.

## PDF Mapping Workflow

`tools/inspect_pdf_fields.py` is a helper that writes field names into local fillable PDFs so field placement can be inspected visually.

Run it with:

```bash
.venv/bin/python tools/inspect_pdf_fields.py
```

This creates local inspection files in `tools/`, which are ignored by git.

## Tests

Run the full test suite:

```bash
.venv/bin/pytest tests/ -v
```

Current local status during development:

- `29` tests passing

## Notes

- Polish descriptions are intentional and meant for GM reference material.
- `PDF/` is ignored by git on purpose.
- Generated characters in `characters/` are also ignored, except for `.gitkeep`.
