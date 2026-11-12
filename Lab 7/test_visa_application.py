"""Hypothesis fuzzing and regression checks for the three lab functions."""
import math
import pytest
from hypothesis import example, given, settings, strategies as st
from visa_application import parse_application, processing_average, payable_fee

settings.register_profile('lab', max_examples=300, derandomize=True, deadline=None)
settings.load_profile('lab')
invalid_types = st.none() | st.integers() | st.floats() | st.lists(st.integers()) | st.dictionaries(st.text(), st.integers())
inputs = st.text() | invalid_types

@given(inputs)
@example(None)
@example('tourist:0')
def test_parse_application_no_crash(s):
    result = parse_application(s)
    assert result is None or (isinstance(result, tuple) and len(result) == 2 and result[0] and result[1] > 0)

@given(inputs)
@example(None)
@example('')
def test_processing_average_no_crash(s):
    result = processing_average(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result) and result >= 0)

@given(inputs)
@example(None)
@example('NaN|0')
@example('1.7e308|0')
def test_payable_fee_no_crash(s):
    result = payable_fee(s)
    assert result is None or (math.isfinite(result) and result >= 0)

@given(st.sampled_from(['tourist', 'BUSINESS', ' student ']), st.integers(1, 10**12))
def test_valid_application(visa, entries):
    assert parse_application(f'{visa}:{entries}') == (visa.strip().title(), entries)

@given(st.lists(st.integers(0, 10**6), min_size=1, max_size=50))
def test_average_matches_arithmetic_mean(days):
    assert processing_average(','.join(map(str, days))) == pytest.approx(sum(days) / len(days))

@given(st.integers(0, 10**8), st.integers(0, 10**8))
def test_fee_formula(fee, discount):
    assert payable_fee(f'{fee}|{discount}') == pytest.approx(max(fee * 1.18 - discount, 0))

@pytest.mark.parametrize('s', ['', ':2', 'tourist:0', 'tourist:-1', 'tourist:1:2', 'tourist:1.5'])
def test_invalid_application(s):
    assert parse_application(s) is None

@pytest.mark.parametrize('s', ['', '1,,2', '-1,2', 'one,2', '1.5,2'])
def test_invalid_days(s):
    assert processing_average(s) is None

@pytest.mark.parametrize('s', ['', '1|2|3', '-1|0', '1|-1', 'NaN|0', 'inf|0', '1.7e308|0'])
def test_invalid_fee(s):
    assert payable_fee(s) is None
