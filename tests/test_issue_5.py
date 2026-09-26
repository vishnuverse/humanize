"""Tests for issue #5: typo in naturalsize docstring."""

from humanize.filesize import naturalsize


def test_typo_in_naturasize_docstring():
    """The docstring should say "human-readable" not "human-readble"."""
    assert "human-readable" in naturalsize.__doc__


def test_naturalsize_basic_usage():
    """Basic functionality still works."""
    assert naturalsize(3000000) == "3.0 MB"


def test_naturalsize_binary():
    """Binary mode works."""
    assert naturalsize(3000, binary=True) == "2.9 KiB"
