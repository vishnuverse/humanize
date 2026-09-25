"""Tests for issue #4: naturalday returns wrong result for today in extreme timezones."""

import datetime as dt
from unittest.mock import patch

import freezegun
import pytest

import humanize


@pytest.mark.parametrize(
    "frozen_utc_dt, local_today, date_input, expected",
    [
        # Honolulu-like: UTC 2026-09-26 09:00, local date is 2026-09-25
        (dt.datetime(2026, 9, 26, 9, 0, 0), dt.date(2026, 9, 25), dt.date(2026, 9, 25), "today"),
        # Kiritimati-like: UTC 2026-09-25 23:00, local date is 2026-09-26
        (dt.datetime(2026, 9, 25, 23, 0, 0), dt.date(2026, 9, 26), dt.date(2026, 9, 26), "today"),
        # Normal: UTC midday, same local date
        (dt.datetime(2026, 9, 26, 12, 0, 0), dt.date(2026, 9, 26), dt.date(2026, 9, 26), "today"),
        (dt.datetime(2026, 9, 26, 12, 0, 0), dt.date(2026, 9, 26), dt.date(2026, 9, 25), "yesterday"),
        (dt.datetime(2026, 9, 26, 12, 0, 0), dt.date(2026, 9, 26), dt.date(2026, 9, 27), "tomorrow"),
    ],
)
def test_naturalday_issue4(frozen_utc_dt, local_today, date_input, expected):
    """naturalday with a plain date should use local date.today(), not UTC date."""

    with freezegun.freeze_time(frozen_utc_dt, tz_offset=0):
        # freezegun patches datetime.now() -> frozen_utc_dt and date.today() -> frozen_utc_dt.date()
        # Override date.today() to return the LOCAL date (different from UTC date in extreme timezones)
        with patch("datetime.date.today", return_value=local_today):
            result = humanize.naturalday(date_input)
            assert result == expected, (
                f"frozen_utc={frozen_utc_dt}, local_today={local_today}, "
                f"date_input={date_input}, got={result!r}, expected={expected!r}"
            )
