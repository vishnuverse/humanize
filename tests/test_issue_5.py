#!/usr/bin/env python

"""Tests for the docstring fix for issue #5."""

from __future__ import annotations

import humanize


def test_naturalsize_docstring_no_typo():
    """The docstring of naturalsize should contain 'human-readable', not 'human-readble'."""
    doc = humanize.naturalsize.__doc__
    assert doc is not None
    # The typo 'human-readble' should NOT be present
    assert "human-readble" not in doc, f"Typo 'human-readble' found in docstring: {doc}"
    # The correct spelling must be present
    assert "human-readable" in doc, f"'human-readable' not found in docstring: {doc}"
