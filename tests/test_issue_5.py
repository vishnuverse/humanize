"""Tests for issue #5: typo in naturalsize docstring."""

from __future__ import annotations

import humanize


def test_naturalsize_docstring_has_no_typo() -> None:
    """The naturalsize docstring must say 'human-readable', not 'human-readble'."""
    doc = humanize.naturalsize.__doc__
    assert doc is not None
    assert "human-readble" not in doc, "Typo 'human-readble' found in docstring"
    assert "human-readable" in doc, "Correct spelling 'human-readable' not found"


def test_naturalsize_docstring_starts_with_format() -> None:
    """The docstring should start with the expected format description."""
    doc = humanize.naturalsize.__doc__
    assert doc is not None
    assert doc.strip().startswith("Format a number of bytes")


def test_naturalsize_docstring_mentions_examples() -> None:
    """The docstring should contain Examples section."""
    doc = humanize.naturalsize.__doc__
    assert doc is not None
    assert "Examples" in doc
