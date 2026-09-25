"""Issue #1: ordinal(12) returns '12nd' instead of '12th'."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (11, "11th"),   # ticket mentions 11 looks wrong too
        (12, "12th"),   # ticket's exact input
        (13, "13th"),   # ticket mentions 13 looks wrong too
        (22, "22nd"),   # edge: ends in 2 but not a teen
        (112, "112th"), # edge: ends in 12 but in the hundreds
        (111, "111th"), # edge: ends in 11 but in the hundreds
        (113, "113th"), # edge: ends in 13 but in the hundreds
    ],
)
def test_ordinal_teens(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
