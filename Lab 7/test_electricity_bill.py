from hypothesis import given, strategies as st
from electricity_bill import units_consumed, daily_average, tariff_rate


# ---------- Fuzz tests: no function may crash on any input ----------
@given(st.text() | st.none())
def test_units_consumed_no_crash(s):
    try:
        units_consumed(s)
    except Exception as e:
        assert False, f"units_consumed crashed with: {e!r}"


@given(st.text() | st.none())
def test_daily_average_no_crash(s):
    try:
        daily_average(s)
    except Exception as e:
        assert False, f"daily_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_tariff_rate_no_crash(s):
    try:
        tariff_rate(s)
    except Exception as e:
        assert False, f"tariff_rate crashed with: {e!r}"


# ---------- Sanity checks: valid inputs must still work ----------
def test_units_consumed_valid():
    assert units_consumed("1200:1350") == 150


def test_daily_average_valid():
    assert daily_average("5,7,6") == 6.0


def test_tariff_rate_valid():
    assert tariff_rate("DOM-A") == 3
    assert tariff_rate("com-b") == 12