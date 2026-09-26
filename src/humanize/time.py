"""Time humanizing functions.

These are largely borrowed from Django's `contrib.humanize`.
"""

from __future__ import annotations

__lazy_modules__ = {"humanize.i18n", "humanize.number"}

from enum import Enum
from functools import total_ordering

from .i18n import _gettext as _
from .i18n import _ngettext
from .number import intcomma

TYPE_CHECKING = False
if TYPE_CHECKING:
    import datetime as dt
    from collections.abc import Iterable
    from typing import Any

__all__ = [
    "naturaldate",
    "naturalday",
    "naturaldelta",
    "naturaltime",
    "precisedelta",
]


@total_ordering
class Unit(Enum):
    MICROSECONDS = 0
    MILLISECONDS = 1
    SECONDS = 2
    MINUTES = 3
    HOURS = 4
    DAYS = 5
    MONTHS = 6
    YEARS = 7

    def __lt__(self, other: Any) -> Any:
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def _now() -> dt.datetime:
    import datetime as dt

    return dt.datetime.now()


def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta:
    """Return an "absolute" value for a timedelta, always representing a time distance.

    Args:
        delta (datetime.timedelta): Input timedelta.

    Returns:
        datetime.timedelta: Absolute timedelta.
    """
    if delta.days < 0:
        now = _now()
        return now - (now + delta)
    return delta


def _date_and_delta(
    value: Any, *, now: dt.datetime | None = None, precise: bool = False
) -> tuple[Any, Any]:
    """Turn a value into a date and a timedelta which represents how long ago it was.

    If that's not possible, return `(None, value)`.
    """
    import datetime as dt

    if not now:
        now = _now()
    if isinstance(value, dt.datetime):
        date = value
        delta = now - value
    elif isinstance(value, dt.timedelta):
        date = now - value
        delta = value
    else:
        try:
            value = value if precise else round(value)
            delta = dt.timedelta(seconds=value)
            date = now - delta
        except (ValueError, TypeError):
            return None, value
    return date, _abs_timedelta(delta)


def naturaldelta(
    value: dt.timedelta | float,
    months: bool = True,
    minimum_unit: str = "seconds",
) -> str:
    """Return a natural representation of a timedelta or number of seconds.

    This is similar to `naturaltime`, but does not add tense to the result.

    The timedelta will be rounded to the nearest unit that makes sense.

    Args:
        value (datetime.timedelta, int or float): A timedelta or a number of seconds.
        months (bool): If `True`, then a number of months (based on 30.5 days) will be
            used for fuzziness between years.
        minimum_unit (str): The lowest unit that can be used.

    Returns:
        str (str or `value`): A natural representation of the amount of time
            elapsed unless `value` is not datetime.timedelta or cannot be
            converted to int (cannot be float due to 'inf' or 'nan').
            In that case, a `value` is returned unchanged.

    Raises:
        OverflowError: If `value` is too large to convert to datetime.timedelta.

    Examples:
        Compare two timestamps in a custom local timezone::

        ```pycon
        >>> import datetime as dt
        >>> from dateutil.tz import gettz

        >>> berlin = gettz("Europe/Berlin")
        >>> now = dt.datetime.now(tz=berlin)
        >>> later = now + dt.timedelta(minutes=30)

        >>> naturaldelta(later - now)
        '30 minutes'

        ```

    """
    import datetime as dt

    tmp = Unit[minimum_unit.upper()]
    if tmp not in (Unit.SECONDS, Unit.MILLISECONDS, Unit.MICROSECONDS):
        msg = f"Minimum unit '{minimum_unit}' not supported"
        raise ValueError(msg)
    min_unit = tmp

    if isinstance(value, dt.timedelta):
        delta = value
    else:
        try:
            int(value)  # Explicitly don't support string such as "NaN" or "inf"
            value = float(value)
            delta = dt.timedelta(seconds=value)
        except (ValueError, TypeError):
            return str(value)
        except OverflowError:
            # `int(value)` raises OverflowError for non-finite floats (inf/-inf),
            # which, like NaN, are returned unchanged. A too-large *finite* value
            # (whose OverflowError comes from `timedelta`) is still raised, per
            # the documented `OverflowError` contract.
            import math

            if not math.isfinite(value):
                return str(value)
            raise

    use_months = months

    delta = abs(delta)
    years = delta.days // 365
    days = delta.days % 365
    num_months = round(days / 30.5)

    if years == 0 and days < 1:
        if delta.seconds == 0:
            if min_unit == Unit.MICROSECONDS and delta.microseconds < 1000:
                return (
                    _ngettext("%d microsecond", "%d microseconds", delta.microseconds)
                    % delta.microseconds
                )

            if min_unit == Unit.MILLISECONDS or (
                min_unit == Unit.MICROSECONDS and 1000 <= delta.microseconds < 1_000_000
            ):
                milliseconds = delta.microseconds / 1000
                return (
                    _ngettext("%d millisecond", "%d milliseconds", int(milliseconds))
                    % milliseconds
                )
            return _("a moment")

        if delta.seconds == 1:
            return _("a second")

        if delta.seconds < 60:
            return _ngettext("%d second", "%d seconds", delta.seconds) % delta.seconds

        if 60 <= delta.seconds < 3600:
            minutes = round(delta.seconds / 60)
            if minutes == 1:
                return _("a minute")

            if minutes == 60:
                return _("an hour")

            return _ngettext("%d minute", "%d minutes", minutes) % minutes

        if 3600 <= delta.seconds:
            hours = round(delta.seconds / 3600)
            if hours == 1:
                return _("an hour")

            if hours == 24:
                return _("a day")

            return _ngettext("%d hour", "%d hours", hours) % hours

    elif years == 0:
        if days == 1:
            return _("a day")

        if not use_months:
            return _ngettext("%d day", "%d days", days) % days

        if num_months == 0:
            return _ngettext("%d day", "%d days", days) % days

        if num_months == 1:
            return _("a month")

        if num_months == 12:
            return _("a year")

        return _ngettext("%d month", "%d months", num_months) % num_months

    elif years == 1:
        if num_months == 0 and days == 0:
            return _("a year")

        if num_months == 0:
            return _ngettext("1 year, %d day", "1 year, %d days", days) % days

        if use_months:
            if num_months == 1:
                return _("1 year, 1 month")

            if num_months == 12:
                years += 1
                return _ngettext("%d year", "%d years", years) % years

            return (
                _ngettext("1 year, %d month", "1 year, %d months", num_months)
                % num_months
            )

        return _ngettext("1 year, %d day", "1 year, %d days", days) % days

    years = round(delta.days / 365)
    return _ngettext("%d year", "%d years", years).replace("%d", "%s") % intcomma(years)


def naturaltime(
    value: dt.datetime | dt.timedelta | float,
    future: bool = False,
    months: bool = True,
    minimum_unit: str = "seconds",
    when: dt.datetime | None = None,
) -> str:
    """Return a natural representation of a time in a resolution that makes sense.

    This is more or less compatible with Django's `naturaltime` filter.

    The time will be rounded to the nearest unit that makes sense.

    Args:
        value (datetime.datetime, datetime.timedelta, int or float): A `datetime`, a
            `timedelta`, or a number of seconds.
        future (bool): Ignored for `datetime`s and `timedelta`s, where the tense is
            always figured out based on the current time. For integers and floats, the
            return value will be past tense by default, unless future is `True`.
        months (bool): If `True`, then a number of months (based on 30.5 days) will be
            used for fuzziness between years.
        minimum_unit (str): The lowest unit that can be used.
        when (datetime.datetime): Point in time relative to which _value_ is
            interpreted.  Defaults to the current time in the local timezone.

    Returns:
        str: A natural representation of the input in a resolution that makes sense.
    """
    import datetime as dt

    value = _convert_aware_datetime(value)
    when = _convert_aware_datetime(when)

    now = when or _now()

    date, delta = _date_and_delta(value, now=now)
    if date is None:
        return str(value)
    # determine tense by value only if datetime/timedelta were passed
    if isinstance(value, (dt.datetime, dt.timedelta)):
        future = date > now

    ago = _("%s from now") if future else _("%s ago")
    delta = naturaldelta(delta, months, minimum_unit)

    if delta == _("a moment"):
        return _("now")

    return str(ago % delta)


def _convert_aware_datetime(
    value: dt.datetime | dt.timedelta | float | None,
) -> Any:
    """Convert aware datetime to naive datetime and pass through any other type."""
    if value is None:
        return None

    import datetime as dt

    if isinstance(value, dt.datetime) and value.tzinfo is not None:
        value = dt.datetime.fromtimestamp(value.timestamp())
    return value


def naturalday(value: dt.date | dt.datetime, format: str = "%b %d") -> str:
    """Return a natural day.

    For date values that are tomorrow, today or yesterday compared to
    present day return representing string. Otherwise, return a string
    formatted according to `format`.

    """
    import datetime as dt

    try:
        # When value is a tz-aware datetime, compute "today" in that timezone
        # so the comparison uses the correct local date.
        if isinstance(value, dt.datetime) and value.tzinfo is not None:
            today = dt.datetime.now(value.tzinfo).date()
        else:
            today = dt.date.today()
        value = dt.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return str(value)
    except (OverflowError, ValueError):
        # Date arguments out of range
        return str(value)
    delta = value - today

    if delta.days == 0:
        return _("today")

    if delta.days == 1:
        return _("tomorrow")

    if delta.days == -1:
        return _("yesterday")

    return value.strftime(format)