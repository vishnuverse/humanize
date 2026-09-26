"""Tests for issue #4: naturalday returns wrong day in off-UTC timezones."""

from __future__ import annotations

import datetime as dt
from unittest.mock import patch

import pytest
from freezegun import freeze_time

import humanize


class TestNaturaldayTimezone:
    """naturalday should handle dates consistently when local time ≠ UTC."""

    @freeze_time("2026-09-26 05:00")
    def test_today_in_honolulu_scenario(self):
        """In Honolulu (UTC-10) at 05:00 UTC, local date is still Sept 25.
        dt.date.today() returns Sept 25; naturalday should say 'today'."""
        with patch("datetime.date.today", return_value=dt.date(2026, 9, 25)):
            today = dt.date.today()
            result = humanize.naturalday(today)
            assert result == "today", f"Expected 'today', got '{result}'"

    @freeze_time("2026-09-26 10:00")
    def test_today_in_kiritimati_scenario(self):
        """In Kiritimati (UTC+14) at 10:00 UTC, local date is already Sept 27.
        dt.date.today() returns Sept 27; naturalday should say 'today'."""
        with patch("datetime.date.today", return_value=dt.date(2026, 9, 27)):
            today = dt.date.today()
            result = humanize.naturalday(today)
            assert result == "today", f"Expected 'today', got '{result}'"

    @freeze_time("2026-09-26 12:00")
    def test_relative_dates_still_work(self):
        """Relative dates (yesterday, tomorrow) should still work."""
        today = dt.date(2026, 9, 26)
        assert humanize.naturalday(today) == "today"
        assert humanize.naturalday(today + dt.timedelta(days=1)) == "tomorrow"
        assert humanize.naturalday(today - dt.timedelta(days=1)) == "yesterday"

    @freeze_time("2026-09-26 12:00")
    def test_explicit_date_in_past(self):
        """Explicitly provided past dates should return formatted string."""
        assert humanize.naturalday(dt.date(2026, 3, 5)) == "Mar 05"

    @freeze_time("2026-09-26 05:00")
    def test_honolulu_with_explicit_date(self):
        """Explicit date that matches local 'today' should say 'today'."""
        with patch("datetime.date.today", return_value=dt.date(2026, 9, 25)):
            result = humanize.naturalday(dt.date(2026, 9, 25))
            assert result == "today", f"Expected 'today', got '{result}'"

    @freeze_time("2026-09-26 10:00")
    def test_kiritimati_with_explicit_date(self):
        """Explicit date that matches local 'today' should say 'today'."""
        with patch("datetime.date.today", return_value=dt.date(2026, 9, 27)):
            result = humanize.naturalday(dt.date(2026, 9, 27))
            assert result == "today", f"Expected 'today', got '{result}'"
