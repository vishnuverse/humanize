"""Tests for KAN-4: ordinal() returning wrong suffix for 11/12/13."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
    ],
)
def test_kan_4_ordinal_teens(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
