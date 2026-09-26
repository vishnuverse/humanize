"""Regression tests for gh#1: ordinal() returns wrong suffix for 11, 12, 13."""
from humanize import ordinal


class TestOrdinalTeens:
    """Test that ordinal() handles teen numbers (11-13) correctly."""

    def test_twelve(self):
        """Ticket example: ordinal(12) should be '12th' not '12nd'."""
        assert ordinal(12) == "12th"

    def test_eleven(self):
        """ordinal(11) should be '11th' not '11st'."""
        assert ordinal(11) == "11th"

    def test_thirteen(self):
        """ordinal(13) should be '13th' not '13rd'."""
        assert ordinal(13) == "13th"

    def test_hundred_teens(self):
        """Edge: 112 (teens inside hundreds) should be '112th'."""
        assert ordinal(112) == "112th"

    def test_thousand_teens(self):
        """Edge: 1013 (teens inside thousands) should be '1013th'."""
        assert ordinal(1013) == "1013th"

    def test_regular_numbers(self):
        """Verify regular numbers still work correctly."""
        assert ordinal(0) == "0th"
        assert ordinal(1) == "1st"
        assert ordinal(2) == "2nd"
        assert ordinal(3) == "3rd"
        assert ordinal(4) == "4th"
        assert ordinal(22) == "22nd"
        assert ordinal(103) == "103rd"
