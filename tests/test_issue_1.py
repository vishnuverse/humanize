"""Issue #1: ordinal(12) returns '12nd' instead of '12th'."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (12, "12th"),
        (11, "11th"),
        (13, "13th"),
        (22, "22nd"),
        (112, "112th"),
        (111, "111th"),
        (113, "113th"),
        (101, "101st"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
    ],
)
def test_ordinal_issue_1(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
