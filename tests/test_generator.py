from unittest.mock import patch

import pytest

from lib.generator import generate_character


FAKE_ROLES = [
    {
        "id": "hitman",
        "name": "Hitman",
        "book": "outgunned",
        "description_pl": "Desc",
        "stats": {"brawn": 1},
        "starting_feats": ["Quick Draw", "Iron Will"],
        "choose_feats": 2,
        "skill_points": ["Shoot"],
        "gear": ["Pistol"],
    }
]
FAKE_TROPES = [
    {
        "id": "pro",
        "name": "The Professional",
        "book": "outgunned",
        "description_pl": "Desc",
        "bonus": "Bonus",
    }
]
FAKE_FEATS = [
    {"id": "quick-draw", "name": "Quick Draw", "book": "outgunned", "description_pl": "Desc", "effect": "Fast"},
    {"id": "iron-will", "name": "Iron Will", "book": "outgunned", "description_pl": "Desc", "effect": "Tough"},
]


def _patch_data(fn):
    import functools

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with (
            patch("lib.generator.load_roles", return_value=FAKE_ROLES),
            patch("lib.generator.load_tropes", return_value=FAKE_TROPES),
            patch("lib.generator.load_available_feats", return_value=FAKE_FEATS),
        ):
            return fn(*args, **kwargs)

    return wrapper


@_patch_data
def test_generate_returns_required_keys():
    character = generate_character(book="outgunned")
    for key in ("name", "book", "role", "trope", "feats", "stats", "generated_at"):
        assert key in character


@_patch_data
def test_generate_explicit_role():
    character = generate_character(role="Hitman", book="outgunned")
    assert character["role"] == "Hitman"


@_patch_data
def test_generate_explicit_trope():
    character = generate_character(trope="The Professional", book="outgunned")
    assert character["trope"] == "The Professional"


@_patch_data
def test_generate_explicit_feats():
    character = generate_character(feats=["Quick Draw", "Iron Will"], book="outgunned")
    assert character["feats"] == ["Quick Draw", "Iron Will"]


@_patch_data
def test_generate_random_feat_count_uses_role_configuration():
    character = generate_character(book="outgunned")
    assert len(character["feats"]) == 2


@_patch_data
def test_generate_explicit_name():
    character = generate_character(name="John Doe", book="outgunned")
    assert character["name"] == "John Doe"


@_patch_data
def test_generate_default_name_has_prefix():
    character = generate_character(book="outgunned")
    assert character["name"].startswith("Hero_")


def test_generate_wok_name_prefix():
    with (
        patch("lib.generator.load_roles", return_value=[{**FAKE_ROLES[0], "book": "wok"}]),
        patch("lib.generator.load_tropes", return_value=[{**FAKE_TROPES[0], "book": "wok"}]),
        patch("lib.generator.load_available_feats", return_value=[{**FAKE_FEATS[0], "book": "wok"}]),
    ):
        character = generate_character(book="wok")
        assert character["name"].startswith("Killer_")


@_patch_data
def test_generate_invalid_role_raises():
    with pytest.raises(ValueError):
        generate_character(role="NonExistent", book="outgunned")
