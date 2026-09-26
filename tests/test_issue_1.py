"""Test for issue #1: ordinal() returns wrong suffix for 11, 12, 13."""

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
        (111, "111th"),
        (113, "113th"),
    ],
)
def test_ordinal_issue1(test_input: int, expected: str) -> None:
    assert humanize.ordinal(test_input) == expected
