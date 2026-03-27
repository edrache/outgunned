from lib.data import load_feats, load_roles, load_tropes


def generate_cheatsheet(book: str) -> str:
    roles = load_roles(book)
    tropes = load_tropes(book)
    feats = load_feats(book)

    lines = [f"# Outgunned Cheat Sheet - {book.upper()}", ""]

    lines.extend(["## Roles", ""])
    for role in roles:
        lines.append(f"### {role['name']}")
        lines.append("")
        lines.append(role.get("description_pl", ""))
        if role.get("stats"):
            stats_line = ", ".join(f"{key}: {value}" for key, value in role["stats"].items())
            lines.extend(["", f"**Stats:** {stats_line}"])
        if role.get("skill_points"):
            lines.extend(["", f"**Skills:** {', '.join(role['skill_points'])}"])
        if role.get("starting_feats"):
            lines.extend(["", f"**Feat Pool:** {', '.join(role['starting_feats'])}"])
        if role.get("gear"):
            lines.extend(["", f"**Gear:** {', '.join(role['gear'])}"])
        lines.extend(["", ""])

    lines.extend(["## Tropes", ""])
    for trope in tropes:
        lines.append(f"### {trope['name']}")
        lines.append("")
        lines.append(trope.get("description_pl", ""))
        if trope.get("bonus"):
            lines.extend(["", f"**Bonus:** {trope['bonus']}"])
        lines.extend(["", ""])

    lines.extend(["## Feats", ""])
    for feat in feats:
        lines.append(f"### {feat['name']}")
        lines.append("")
        lines.append(feat.get("description_pl", ""))
        if feat.get("effect"):
            lines.extend(["", f"**Effect:** {feat['effect']}"])
        lines.extend(["", ""])

    return "\n".join(lines).rstrip() + "\n"
