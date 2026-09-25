"""Tests for issue #5: typo in naturalsize docstring."""

from humanize.filesize import naturalsize


def test_naturalsize_docstring_typo():
    """Verify that the docstring uses 'human-readable' not 'human-readble'."""
    doc = naturalsize.__doc__
    assert doc is not None, "naturalsize docstring should exist"
    # The typo exists in the current code
    assert "human-readble" not in doc, (
        "naturalsize docstring has a typo: 'human-readble' should be 'human-readable'"
    )
    assert "human-readable" in doc, (
        "naturalsize docstring should contain 'human-readable'"
    )


def test_naturalsize_basic():
    """Basic sanity check for naturalsize."""
    assert naturalsize(3000000) == "3.0 MB"
    assert naturalsize(300, False, True) == "300B"
