from humanize import number


class TestOrdinalIssue1:
    """Tests for issue #1: ordinal(12) returning '12nd' instead of '12th'."""

    def test_ordinal_11(self):
        assert number.ordinal(11) == "11th"

    def test_ordinal_12(self):
        assert number.ordinal(12) == "12th"

    def test_ordinal_13(self):
        assert number.ordinal(13) == "13th"

    def test_ordinal_22_still_works(self):
        assert number.ordinal(22) == "22nd"

    def test_ordinal_112_edge(self):
        assert number.ordinal(112) == "112th"

    def test_ordinal_3_still_works(self):
        assert number.ordinal(3) == "3rd"

    def test_ordinal_111_edge(self):
        assert number.ordinal(111) == "111th"
