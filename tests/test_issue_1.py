"""Tests for issue #1: ordinal() returns wrong suffix for 11, 12, 13."""

import humanize


def test_ordinal_11() -> None:
    """11 should be '11th' not '11st'."""
    assert humanize.ordinal(11) == "11th"


def test_ordinal_12() -> None:
    """12 should be '12th' not '12nd'."""
    assert humanize.ordinal(12) == "12th"


def test_ordinal_13() -> None:
    """13 should be '13th' not '13rd'."""
    assert humanize.ordinal(13) == "13th"


def test_ordinal_22() -> None:
    """22 should be '22nd' (regular case, unaffected)."""
    assert humanize.ordinal(22) == "22nd"


def test_ordinal_112() -> None:
    """112 should be '112th' (teens inside hundreds)."""
    assert humanize.ordinal(112) == "112th"


def test_ordinal_111() -> None:
    """111 should be '111th'"""
    assert humanize.ordinal(111) == "111th"


def test_ordinal_113() -> None:
    """113 should be '113th'"""
    assert humanize.ordinal(113) == "113th"
