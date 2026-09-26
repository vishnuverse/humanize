"""Tests for KAN-4: ordinal() returning wrong suffix for teen numbers."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (22, "22nd"),
        (112, "112th"),
    ],
)
def test_ordinal_teen_fix(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
