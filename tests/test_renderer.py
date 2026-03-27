from lib.renderer import render_character_md


SAMPLE_CHAR = {
    "name": "John Doe",
    "book": "outgunned",
    "role": "Hitman",
    "trope": "The Professional",
    "role_description_pl": "Opis roli.",
    "trope_description_pl": "Opis tropu.",
    "trope_bonus": "Premia.",
    "feats": ["Quick Draw", "Iron Will"],
    "stats": {"brawn": 3, "nerves": 2},
    "skill_points": ["Shoot", "Drive"],
    "gear": ["Pistol"],
    "generated_at": "2026-03-27",
}

SAMPLE_FEATS_DATA = [
    {"name": "Quick Draw", "description_pl": "Szybki strzal.", "effect": "Draw faster"},
    {"name": "Iron Will", "description_pl": "Silna wola.", "effect": "Resist mind"},
]


def test_render_contains_name():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "John Doe" in markdown


def test_render_contains_role():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Hitman" in markdown


def test_render_contains_trope():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "The Professional" in markdown


def test_render_contains_feat_names():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Quick Draw" in markdown
    assert "Iron Will" in markdown


def test_render_contains_feat_descriptions():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "Szybki strzal" in markdown


def test_render_contains_stats():
    markdown = render_character_md(SAMPLE_CHAR, SAMPLE_FEATS_DATA)
    assert "brawn" in markdown.lower()
