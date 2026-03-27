from pathlib import Path


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def render_character_md(character: dict, feats_data: list[dict]) -> str:
    try:
        from jinja2 import Environment, FileSystemLoader
    except ModuleNotFoundError:
        return _render_without_jinja2(character, feats_data)

    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template("character.md.jinja2")
    return template.render(character=character, feats_data=feats_data)


def _render_without_jinja2(character: dict, feats_data: list[dict]) -> str:
    lines = [
        f"# {character['name']}",
        "",
        f"**Book:** {character['book']}",
        f"**Generated:** {character['generated_at']}",
        "",
        "## Identity",
        "",
        f"- **Role:** {character['role']}",
        f"- **Trope:** {character['trope']}",
    ]

    if character.get("role_description_pl"):
        lines.extend(["", "## Role Notes", "", character["role_description_pl"]])

    if character.get("trope_description_pl") or character.get("trope_bonus"):
        lines.extend(["", "## Trope Notes", ""])
        if character.get("trope_description_pl"):
            lines.append(character["trope_description_pl"])
        if character.get("trope_bonus"):
            lines.extend(["", f"**Bonus:** {character['trope_bonus']}"])

    if character.get("stats"):
        lines.extend(["", "## Stats", ""])
        for stat_name, value in character["stats"].items():
            lines.append(f"- **{stat_name.title()}:** {value}")

    if character.get("skill_points"):
        lines.extend(["", "## Skills", ""])
        for skill in character["skill_points"]:
            lines.append(f"- {skill}")

    if character.get("gear"):
        lines.extend(["", "## Gear", ""])
        for item in character["gear"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Feats", ""])
    for feat in feats_data:
        lines.extend(
            [
                f"### {feat['name']}",
                "",
                feat.get("description_pl", ""),
                "",
                f"**Effect:** {feat.get('effect', '')}",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"
