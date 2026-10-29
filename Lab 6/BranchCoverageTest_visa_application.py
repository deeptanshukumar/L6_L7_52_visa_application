"""Lab 6 branch coverage and boundary tests.

Deeptanshu Kumar - PES1UG24AM357
This suite runs independently of the line coverage suite and starter tests.
"""

import pytest

from visa_application import application_status, documents_complete, visa_fee


@pytest.mark.parametrize(
    "visa_type,entries,message",
    [
        pytest.param("work", 1, "unknown visa type", id="unknown-type"),
        pytest.param("tourist", -1, "invalid entries", id="negative-entries"),
        pytest.param("work", -1, "unknown visa type", id="type-checked-first"),
    ],
)
def test_invalid_fee_inputs(visa_type, entries, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        visa_fee(visa_type, entries, "normal", "B")


@pytest.mark.parametrize(
    "visa_type,entries,speed,group,expected",
    [
        ("tourist", 0, "normal", "B", 0),
        ("tourist", 1, "normal", "B", 0),
        ("tourist", 2, "normal", "B", 40),
        ("tourist", 6, "normal", "B", 200),
        ("tourist", 7, "normal", "B", 360),
        ("tourist", 1, "express", "B", 0),
        ("tourist", 2, "express", "B", 100),
        ("tourist", 6, "express", "B", 500),
        ("tourist", 7, "express", "B", 780),
        ("tourist", 2, "normal", "A", 0),
        ("tourist", 3, "normal", "A", 40),
        ("tourist", 7, "normal", "A", 200),
        ("tourist", 8, "normal", "A", 360),
        ("tourist", 2, "express", "A", 0),
        ("tourist", 3, "express", "A", 100),
        ("tourist", 7, "express", "A", 500),
        ("tourist", 8, "express", "A", 780),
        ("business", 3, "normal", "B", 0),
        ("business", 4, "normal", "B", 40),
        ("business", 4, "normal", "A", 0),
        ("business", 5, "express", "A", 100),
        ("business", 10, "express", "A", 780),
        ("student", 2, "normal", "B", 0),
        ("student", 3, "normal", "B", 40),
        ("student", 2, "normal", "A", 0),
        ("student", 3, "normal", "A", 40),
        ("student", 7, "express", "A", 500),
        ("student", 8, "normal", "A", 360),
        ("student", 8, "express", "A", 780),
    ],
)
def test_fee_allowances_rates_and_bulk_boundaries(
    visa_type, entries, speed, group, expected
):
    # Five extra entries retain the base rate; six trigger the bulk surcharge.
    # Group A's extra allowance applies to tourist/business, but not student.
    assert visa_fee(visa_type, entries, speed, group) == expected


@pytest.mark.parametrize(
    "forms,photos,renewal,expected",
    [
        (0, 0, True, False),
        (0, 2, True, False),
        (1, 0, True, True),
        (1, 1, True, True),
        (1, 2, True, True),
        (2, 0, True, True),
        (3, 0, False, False),
        (3, 1, False, False),
        (3, 2, False, True),
        (3, 3, False, True),
        (2, 2, False, False),
        (0, 2, False, False),
        (4, 3, False, True),
    ],
)
def test_document_requirements_at_boundaries(forms, photos, renewal, expected):
    assert documents_complete(forms, photos, renewal) is expected


@pytest.mark.parametrize(
    "express,peak,cutoff",
    [
        pytest.param(False, False, 30, id="normal-off-peak"),
        pytest.param(False, True, 45, id="normal-peak"),
        pytest.param(True, False, 10, id="express-off-peak"),
        pytest.param(True, True, 25, id="express-peak"),
    ],
)
@pytest.mark.parametrize(
    "offset,expected",
    [
        pytest.param(-16, "closed", id="below-closing-boundary"),
        pytest.param(-15, "closing", id="at-closing-boundary"),
        pytest.param(-14, "closing", id="above-closing-boundary"),
        pytest.param(-1, "closing", id="below-open-boundary"),
        pytest.param(0, "open", id="at-open-boundary"),
        pytest.param(1, "open", id="above-open-boundary"),
    ],
)
def test_status_boundaries(express, peak, cutoff, offset, expected):
    # Check both boundaries in all four processing-speed/season combinations.
    assert application_status(cutoff + offset, express, peak) == expected
