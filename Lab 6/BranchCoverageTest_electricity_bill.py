import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge ----------
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


def test_slab1_upper_boundary():
    assert energy_charge(100, "domestic") == 350


def test_slab2_lower_boundary():
    assert energy_charge(101, "domestic") == 300 + 5 + 50


def test_mid_slab_domestic():
    assert energy_charge(200, "domestic") == 850


def test_slab2_upper_boundary():
    assert energy_charge(300, "domestic") == 1350


def test_high_slab_domestic():
    assert energy_charge(400, "domestic") == 2150


def test_low_usage_commercial():
    assert energy_charge(50, "commercial") == 450


def test_mid_slab_commercial():
    assert energy_charge(200, "commercial") == 1750


def test_high_slab_commercial():
    assert energy_charge(400, "commercial") == 4350


def test_zero_units():
    assert energy_charge(0, "domestic") == 50


def test_unknown_connection():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(10, "industrial")


def test_unknown_connection_checked_before_units():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(-5, "industrial")


def test_negative_units():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0


def test_paid_early_negative_days():
    assert late_fee(500, -3) == 0


def test_late_1_day():
    assert late_fee(500, 1) == 50


def test_late_15_days_boundary():
    assert late_fee(500, 15) == 50


def test_late_16_days_small_bill():
    assert late_fee(500, 16) == 100


def test_late_bill_exactly_2000_no_surcharge():
    assert late_fee(2000, 20) == 100


def test_late_bill_just_over_2000_surcharge():
    # 100 + 2001 // 20 = 100 + 100
    assert late_fee(2001, 20) == 200


def test_late_large_bill():
    assert late_fee(4000, 30) == 300


# ---------- subsidy ----------
def test_senior_low_usage_no_solar():
    assert subsidy(50, True, False) == 50


def test_senior_usage_boundary_100():
    assert subsidy(100, True, False) == 50


def test_senior_usage_just_over_100():
    assert subsidy(101, True, False) == 0


def test_non_senior_low_usage_no_solar():
    assert subsidy(50, False, False) == 0


def test_solar_only():
    assert subsidy(50, False, True) == 100


def test_senior_and_solar():
    assert subsidy(50, True, True) == 150


def test_solar_mid_usage():
    assert subsidy(200, False, True) == 100


def test_solar_usage_boundary_300_keeps_subsidy():
    assert subsidy(300, False, True) == 100


def test_solar_high_usage_loses_subsidy():
    assert subsidy(301, False, True) == 0


def test_senior_solar_high_usage():
    assert subsidy(301, True, True) == 0
