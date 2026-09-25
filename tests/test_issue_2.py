"""Tests for GitHub issue #2: intcomma drops the minus sign for negative strings."""

from humanize import intcomma


class TestIntcommaNegativeStrings:
    """intcomma with negative string inputs."""

    def test_negative_string_ticket(self):
        """Ticket example: '-1234567' as a string."""
        assert intcomma("-1234567") == "-1,234,567"

    def test_negative_string_small(self):
        """Small negative integer as string."""
        assert intcomma("-100") == "-100"

    def test_negative_string_thousands(self):
        """Negative integer with thousands as string."""
        assert intcomma("-100000") == "-100,000"

    def test_zero_string(self):
        """Zero as string should work."""
        assert intcomma("0") == "0"

    def test_positive_string(self):
        """Regular positive string still works."""
        assert intcomma("1234") == "1,234"
