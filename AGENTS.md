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
