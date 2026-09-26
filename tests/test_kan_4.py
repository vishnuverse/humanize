import pytest

import humanize


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (12, "12th"),
        (11, "11th"),
        (13, "13th"),
        (22, "22nd"),
        (112, "112th"),
    ],
)
def test_ordinal_teen_suffixes(value, expected):
    assert humanize.ordinal(value) == expected
