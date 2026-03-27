from unittest.mock import patch

from lib.cheatsheet import generate_cheatsheet


FAKE_ROLES = [{"name": "Hitman", "description_pl": "Zawodowy zabojca.", "book": "outgunned"}]
FAKE_TROPES = [{"name": "The Professional", "description_pl": "Zimna krew.", "book": "outgunned"}]
FAKE_FEATS = [{"name": "Quick Draw", "description_pl": "Szybki strzal.", "effect": "Fast draw", "book": "outgunned"}]


def _patch_loaders(fn):
    import functools

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with (
            patch("lib.cheatsheet.load_roles", return_value=FAKE_ROLES),
            patch("lib.cheatsheet.load_tropes", return_value=FAKE_TROPES),
            patch("lib.cheatsheet.load_feats", return_value=FAKE_FEATS),
        ):
            return fn(*args, **kwargs)

    return wrapper


@_patch_loaders
def test_cheatsheet_contains_roles_section():
    markdown = generate_cheatsheet("outgunned")
    assert "## Roles" in markdown


@_patch_loaders
def test_cheatsheet_contains_role_name():
    markdown = generate_cheatsheet("outgunned")
    assert "Hitman" in markdown


@_patch_loaders
def test_cheatsheet_contains_polish_description():
    markdown = generate_cheatsheet("outgunned")
    assert "Zawodowy zabojca" in markdown


@_patch_loaders
def test_cheatsheet_contains_tropes_section():
    markdown = generate_cheatsheet("outgunned")
    assert "## Tropes" in markdown


@_patch_loaders
def test_cheatsheet_contains_feats_section():
    markdown = generate_cheatsheet("outgunned")
    assert "## Feats" in markdown


@_patch_loaders
def test_cheatsheet_contains_feat_effect():
    markdown = generate_cheatsheet("outgunned")
    assert "Fast draw" in markdown
