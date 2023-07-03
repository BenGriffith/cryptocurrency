from tests.conftest import DAYS, MONTHS


def test_time_period_days(time_period_days, days_keys_names):
    rows = time_period_days
    keys, names = days_keys_names
    assert isinstance(rows, list)
    assert len(rows) == 7
    assert keys == list(range(1, 8))
    assert names == DAYS


def test_time_period_months(time_period_months, months_keys_names):
    rows = time_period_months
    keys, names = months_keys_names
    assert isinstance(rows, list)
    assert len(rows) == 12
    assert keys == list(range(1, 13))
    assert names == MONTHS