# Outgunned GM Toolset — Design Spec

**Date:** 2026-03-27
**Status:** Approved

## Overview

A Python CLI toolset to support running Outgunned RPG campaigns (core + World of Killers expansion). Tools are designed to be invoked by AI agents (Codex CLI) as well as directly from the terminal.

## Project Structure

```
Outgunned/
├── AGENTS.md                        # Project context for Codex CLI
├── outgunned.py                     # Main CLI entry point
├── data/
│   ├── roles.json                   # Roles (Outgunned + WoK)
│   ├── tropes.json                  # Tropes (Outgunned + WoK)
│   └── feats.json                   # Feats (Outgunned + WoK)
├── templates/
│   └── character.md.jinja2          # Markdown character sheet template
├── characters/                      # Generated characters
│   └── <name>/
│       ├── character.json
│       ├── character.md
│       └── character_sheet.pdf      # (optional, generated on demand)
├── docs/
│   ├── cheatsheet.md                # Outgunned cheat sheet (Polish descriptions)
│   ├── cheatsheet_wok.md            # World of Killers cheat sheet (Polish descriptions)
│   └── superpowers/specs/           # Design documents
└── PDF/                             # Original PDF files (read-only)
```

## CLI (`outgunned.py`)

Single entry point with subcommands. Invoked as `python outgunned.py <subcommand>`.

### `generate` — character generation

```bash
python outgunned.py generate
python outgunned.py generate --name "John Doe" --role "Hitman" --trope "The Professional" --feats "Quick Draw,Iron Will"
python outgunned.py generate --book wok
```

- `--name`: optional; defaults to `Hero_<timestamp>` (or `Killer_<timestamp>` for WoK)
- `--role`: optional; if omitted — randomly selected from those available for `--book`
- `--trope`: optional; if omitted — randomly selected
- `--feats`: optional; comma-separated list; if omitted — randomly selected per game rules
- `--book`: `outgunned` (default) or `wok`
- Output: `characters/<name>/character.json` + `characters/<name>/character.md`

### `fill-pdf` — fill character sheet PDF

```bash
python outgunned.py fill-pdf characters/john_doe/character.json
```

- Reads `character.json`, maps fields to PDF form fields
- Uses `pypdf` library to fill fillable PDF forms
- Output: `characters/<name>/character_sheet.pdf`
- Handles both sheet types: Outgunned Hero Sheet and WoK Killer Sheet (selected based on `book` field in JSON)

### `cheatsheet` — generate cheat sheet

```bash
python outgunned.py cheatsheet
python outgunned.py cheatsheet --book wok
```

- Generates Markdown with Polish descriptions of all Roles, Tropes, and Feats from `data/` files
- Output: `docs/cheatsheet.md` (Outgunned) or `docs/cheatsheet_wok.md` (WoK)

## Data Format

### `data/roles.json`
```json
[
  {
    "id": "hitman",
    "name": "Hitman",
    "book": "outgunned",
    "description_pl": "Polish description...",
    "stats": {},
    "starting_feats": []
  }
]
```

### `data/tropes.json` and `data/feats.json`
Same structure: `id`, `name`, `book`, `description_pl`, plus type-specific fields.

### `characters/<name>/character.json`
```json
{
  "name": "John Doe",
  "book": "outgunned",
  "role": "Hitman",
  "trope": "The Professional",
  "feats": ["Quick Draw", "Iron Will"],
  "stats": {},
  "generated_at": "2026-03-27"
}
```

## Python Dependencies

- `pypdf` — PDF form filling
- `jinja2` — Markdown templates
- `click` — CLI (subcommands, arguments)

## AGENTS.md

Contains:
- Project description (Outgunned campaign, GM toolset)
- Available CLI commands with examples
- Directory structure overview
- Notes on PDF files (read-only originals in `PDF/`)
- Where to find game rules data (`data/` files)

## Constraints and Decisions

- Game data (roles, tropes, feats) is **hardcoded** in `data/` files — not parsed from PDFs at runtime
- PDF filling only works with fillable PDFs (those in `PDF/` already are fillable)
- PDF field names must be mapped manually after inspecting the file (first `fill-pdf` run may require debugging field names)
- Project does not require package installation — run directly via `python outgunned.py`
- Exact `stats` structure and number of starting feats to be determined from the rulebook (implementation will fill these from `data/`)
- `description_pl` fields in data files and cheat sheet content are intentionally in Polish (GM reference material)
