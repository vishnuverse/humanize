"""Tests for issue #1: ordinal() returns wrong suffix for 11, 12, 13."""

from humanize import number


class TestOrdinalTeens:
    """ordinal() should return 'th' for numbers ending in 11, 12, 13."""

    def test_ticket_12(self):
        """From the ticket: ordinal(12) should be '12th'."""
        assert number.ordinal(12) == "12th"

    def test_11(self):
        assert number.ordinal(11) == "11th"

    def test_13(self):
        assert number.ordinal(13) == "13th"

    def test_112(self):
        """Edge: teens inside the hundreds."""
        assert number.ordinal(112) == "112th"

    def test_22(self):
        """Not affected: 22 ends in 2 -> 'nd'."""
        assert number.ordinal(22) == "22nd"

    def test_21(self):
        """Not affected: 21 ends in 1 -> 'st'."""
        assert number.ordinal(21) == "21st"

    def test_23(self):
        """Not affected: 23 ends in 3 -> 'rd'."""
        assert number.ordinal(23) == "23rd"
