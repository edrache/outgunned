import pytest

from lib.data import get_by_name, load_feats, load_roles, load_tropes


def test_load_roles_outgunned_returns_list():
    roles = load_roles("outgunned")
    assert isinstance(roles, list)
    assert len(roles) > 0


def test_load_roles_wok_returns_only_wok_entries():
    roles = load_roles("wok")
    assert roles
    assert all(role["book"] == "wok" for role in roles)


def test_load_roles_invalid_book_raises():
    with pytest.raises(ValueError, match="Unknown book"):
        load_roles("invalid")


def test_load_tropes_outgunned_returns_named_entries():
    tropes = load_tropes("outgunned")
    assert tropes
    assert all("name" in trope for trope in tropes)


def test_load_feats_outgunned_returns_named_entries():
    feats = load_feats("outgunned")
    assert feats
    assert all("name" in feat for feat in feats)


def test_get_by_name_found():
    items = [{"id": "foo", "name": "Foo", "book": "outgunned"}]
    result = get_by_name(items, "Foo")
    assert result["id"] == "foo"


def test_get_by_name_case_insensitive():
    items = [{"id": "foo", "name": "Foo", "book": "outgunned"}]
    result = get_by_name(items, " foo ")
    assert result["id"] == "foo"


def test_get_by_name_not_found_raises():
    with pytest.raises(ValueError, match="not found"):
        get_by_name([], "Missing")
