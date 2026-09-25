"""Tests for issue #1: ordinal() returns wrong suffix for 11, 12, 13."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (22, "22nd"),
        (101, "101st"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
    ],
)
def test_ordinal_issue_1(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
