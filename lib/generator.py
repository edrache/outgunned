import random
from datetime import datetime

from lib.data import get_by_name, load_available_feats, load_roles, load_tropes


def generate_character(
    name: str | None = None,
    role: str | None = None,
    trope: str | None = None,
    feats: list[str] | None = None,
    book: str = "outgunned",
) -> dict:
    roles = load_roles(book)
    tropes = load_tropes(book)
    all_feats = load_available_feats(book)

    chosen_role = get_by_name(roles, role) if role else random.choice(roles)
    chosen_trope = get_by_name(tropes, trope) if trope else random.choice(tropes)
    chosen_feats = _choose_feats(chosen_role, all_feats, feats)
    chosen_feat_details = [_get_feat_detail(all_feats, feat_name) for feat_name in chosen_feats]

    if name is None:
        prefix = "Killer" if book == "wok" else "Hero"
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"{prefix}_{stamp}"

    return {
        "name": name,
        "book": book,
        "role": chosen_role["name"],
        "role_id": chosen_role["id"],
        "role_description_pl": chosen_role.get("description_pl", ""),
        "trope": chosen_trope["name"],
        "trope_id": chosen_trope["id"],
        "trope_description_pl": chosen_trope.get("description_pl", ""),
        "trope_bonus": chosen_trope.get("bonus", ""),
        "feats": chosen_feats,
        "feat_details": chosen_feat_details,
        "stats": chosen_role.get("stats", {}),
        "skill_points": chosen_role.get("skill_points", []),
        "gear": chosen_role.get("gear", []),
        "generated_at": datetime.now().date().isoformat(),
    }


def _choose_feats(role_data: dict, all_feats: list[dict], requested_feats: list[str] | None) -> list[str]:
    if requested_feats:
        return [get_by_name(all_feats, feat_name)["name"] for feat_name in requested_feats]

    starting_feats = list(role_data.get("starting_feats", []))
    choose_feats = role_data.get("choose_feats", 2)
    if starting_feats:
        return random.sample(starting_feats, min(choose_feats, len(starting_feats)))

    feat_names = [feat["name"] for feat in all_feats]
    return random.sample(feat_names, min(2, len(feat_names)))


def _get_feat_detail(all_feats: list[dict], feat_name: str) -> dict:
    try:
        return get_by_name(all_feats, feat_name)
    except ValueError:
        return {"name": feat_name, "description_pl": "", "effect": ""}
