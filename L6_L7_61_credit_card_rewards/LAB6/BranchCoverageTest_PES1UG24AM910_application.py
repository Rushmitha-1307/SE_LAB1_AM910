
import pytest

from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status
)


# ==========================================
# BRANCH COVERAGE: REWARD POINTS
# ==========================================

def test_invalid_card_tier():
    with pytest.raises(ValueError):
        reward_points("diamond", 1000, "grocery", False)


def test_valid_card_tiers():
    assert reward_points("classic", 1000, "grocery", False) == 10
    assert reward_points("gold", 1000, "grocery", False) == 20
    assert reward_points("platinum", 1000, "grocery", False) == 40


def test_zero_amount():
    with pytest.raises(ValueError):
        reward_points("gold", 0, "grocery", False)


def test_negative_amount():
    with pytest.raises(ValueError):
        reward_points("gold", -100, "grocery", False)


def test_fuel_category():
    assert reward_points("gold", 1000, "fuel", False) == 0


def test_grocery_category():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_dining_category():
    assert reward_points("gold", 1000, "dining", False) == 40


def test_travel_category():
    assert reward_points("platinum", 1000, "travel", False) == 80


def test_weekend_gold():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_platinum():
    assert reward_points("platinum", 1000, "grocery", True) == 90


def test_weekend_classic():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_weekday_gold():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_weekend_dining():
    assert reward_points("gold", 1000, "dining", True) == 90


def test_amount_below_100():
    assert reward_points("classic", 99, "grocery", False) == 0


# ==========================================
# BRANCH COVERAGE: LATE PAYMENT FEE
# ==========================================

def test_zero_days_late():
    assert late_payment_fee(5000, 0) == 0


def test_negative_days_late():
    assert late_payment_fee(5000, -1) == 0


def test_zero_outstanding():
    assert late_payment_fee(0, 10) == 0


def test_negative_outstanding():
    assert late_payment_fee(-500, 10) == 0


def test_valid_payment_small_amount():
    assert late_payment_fee(500, 5) == 100


def test_boundary_outstanding_1000():
    assert late_payment_fee(1000, 5) == 100


def test_medium_outstanding():
    assert late_payment_fee(5000, 5) == 500


def test_boundary_outstanding_10000():
    assert late_payment_fee(10000, 5) == 500


def test_large_outstanding():
    assert late_payment_fee(10001, 5) == 1000


def test_late_payment_exactly_30_days():
    assert late_payment_fee(5000, 30) == 500


def test_late_payment_more_than_30_days():
    assert late_payment_fee(5000, 31) == 1250


def test_small_amount_more_than_30_days():
    assert late_payment_fee(500, 31) == 850


def test_large_amount_more_than_30_days():
    assert late_payment_fee(20000, 31) == 1750


# ==========================================
# BRANCH COVERAGE: CARD STATUS
# ==========================================

def test_frozen_card():
    assert card_status(50, 0, True) == "frozen"


def test_blocked_card():
    assert card_status(20, 3, False) == "blocked"


def test_more_than_three_missed_payments():
    assert card_status(20, 4, False) == "blocked"


def test_over_limit_risk():
    assert card_status(95, 0, False) == "over limit risk"


def test_utilisation_exactly_90():
    assert card_status(90, 0, False) == "watch"


def test_watch_due_to_utilisation():
    assert card_status(50, 0, False) == "watch"


def test_utilisation_exactly_30():
    assert card_status(30, 0, False) == "good"


def test_watch_due_to_missed_payment():
    assert card_status(20, 1, False) == "watch"


def test_good_card_status():
    assert card_status(20, 0, False) == "good"


def test_frozen_card_with_missed_payments():
    assert card_status(95, 3, True) == "frozen"


def test_blocked_card_with_high_utilisation():
    assert card_status(95, 3, False) == "blocked"
