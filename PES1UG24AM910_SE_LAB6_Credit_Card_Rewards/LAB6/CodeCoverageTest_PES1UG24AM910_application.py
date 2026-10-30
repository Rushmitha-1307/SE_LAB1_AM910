
import pytest

from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status
)


# --------------------------------------------------
# CODE COVERAGE TESTS FOR REWARD POINTS
# --------------------------------------------------

def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_gold_grocery():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_platinum_grocery():
    assert reward_points("platinum", 1000, "grocery", False) == 40


def test_invalid_card_tier():
    with pytest.raises(ValueError):
        reward_points("diamond", 1000, "grocery", False)


def test_invalid_amount_zero():
    with pytest.raises(ValueError):
        reward_points("classic", 0, "grocery", False)


def test_invalid_amount_negative():
    with pytest.raises(ValueError):
        reward_points("classic", -100, "grocery", False)


def test_fuel_purchase():
    assert reward_points("gold", 1000, "fuel", False) == 0


def test_dining_purchase():
    assert reward_points("classic", 1000, "dining", False) == 20


def test_travel_purchase():
    assert reward_points("gold", 1000, "travel", False) == 40


def test_weekend_gold_bonus():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_platinum_bonus():
    assert reward_points("platinum", 1000, "grocery", True) == 90


def test_weekend_classic_no_bonus():
    assert reward_points("classic", 1000, "grocery", True) == 10


# --------------------------------------------------
# CODE COVERAGE TESTS FOR LATE PAYMENT FEE
# --------------------------------------------------

def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0


def test_negative_days_late():
    assert late_payment_fee(5000, -2) == 0


def test_zero_outstanding():
    assert late_payment_fee(0, 10) == 0


def test_small_outstanding():
    assert late_payment_fee(500, 5) == 100


def test_medium_outstanding():
    assert late_payment_fee(5000, 5) == 500


def test_large_outstanding():
    assert late_payment_fee(20000, 5) == 1000


def test_late_payment_over_30_days():
    assert late_payment_fee(5000, 35) == 1250


def test_late_payment_exactly_30_days():
    assert late_payment_fee(5000, 30) == 500


# --------------------------------------------------
# CODE COVERAGE TESTS FOR CARD STATUS
# --------------------------------------------------

def test_frozen_card():
    assert card_status(20, 0, True) == "frozen"


def test_blocked_card():
    assert card_status(20, 3, False) == "blocked"


def test_over_limit_risk():
    assert card_status(95, 0, False) == "over limit risk"


def test_watch_due_to_utilisation():
    assert card_status(50, 0, False) == "watch"


def test_watch_due_to_missed_payment():
    assert card_status(20, 1, False) == "watch"


def test_good_card_status():
    assert card_status(20, 0, False) == "good"
