"""Lab 6 line coverage tests.

Deeptanshu Kumar - PES1UG24AM357
Run this file explicitly for the independent line coverage measurement.
"""

import pytest

from visa_application import application_status, documents_complete, visa_fee


def test_unknown_visa_type():
    with pytest.raises(ValueError, match="^unknown visa type$"):
        visa_fee("work", 1, "normal", "B")


def test_negative_entries():
    with pytest.raises(ValueError, match="^invalid entries$"):
        visa_fee("tourist", -1, "normal", "B")


def test_included_entries_are_free():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_group_a_receives_one_extra_included_entry():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_normal_extra_entry_fee():
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_express_extra_entry_fee():
    assert visa_fee("tourist", 2, "express", "B") == 100


def test_express_bulk_surcharges():
    # Six extra entries, each charged at 100 + 20 + 10.
    assert visa_fee("tourist", 7, "express", "B") == 780


def test_renewal_needs_one_form():
    assert documents_complete(1, 0, True) is True


def test_new_application_needs_two_photos():
    assert documents_complete(3, 1, False) is False


def test_new_application_with_complete_documents():
    assert documents_complete(3, 2, False) is True


def test_normal_application_open_at_cutoff():
    assert application_status(30, False, False) == "open"


def test_express_peak_application_closing():
    assert application_status(24, True, True) == "closing"


def test_normal_application_closed():
    assert application_status(14, False, False) == "closed"
