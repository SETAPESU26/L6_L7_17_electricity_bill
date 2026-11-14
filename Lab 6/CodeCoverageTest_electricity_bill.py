import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge ----------
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


def test_mid_slab_domestic():
    # 300 + (200-100)*5 = 800, + 50 fixed
    assert energy_charge(200, "domestic") == 850


def test_high_slab_commercial():
    # (1300 + 100*8) * 2 + 150
    assert energy_charge(400, "commercial") == 4350


def test_unknown_connection():
    with pytest.raises(ValueError):
        energy_charge(10, "industrial")


def test_negative_units():
    with pytest.raises(ValueError):
        energy_charge(-1, "domestic")


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0


def test_late_within_15_days():
    assert late_fee(500, 10) == 50


def test_late_over_15_days_large_bill():
    # 100 + 3000 // 20
    assert late_fee(3000, 20) == 250


# ---------- subsidy ----------
def test_senior_low_usage_with_solar():
    assert subsidy(50, True, True) == 150


def test_solar_high_usage_loses_subsidy():
    assert subsidy(301, False, True) == 0
