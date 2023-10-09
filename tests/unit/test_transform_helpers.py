def test_day_dim_rows(transform):
    rows = transform.day_dim_rows()
    assert rows == [
        {"day_key": 1, "name": "Monday"},
        {"day_key": 2, "name": "Tuesday"},
        {"day_key": 3, "name": "Wednesday"},
        {"day_key": 4, "name": "Thursday"},
        {"day_key": 5, "name": "Friday"},
        {"day_key": 6, "name": "Saturday"},
        {"day_key": 7, "name": "Sunday"},
    ]


def test_month_dim_rows(transform):
    rows = transform.month_dim_rows()
    assert rows == [
        {"month_key": 1, "name": "January"},
        {"month_key": 2, "name": "February"},
        {"month_key": 3, "name": "March"},
        {"month_key": 4, "name": "April"},
        {"month_key": 5, "name": "May"},
        {"month_key": 6, "name": "June"},
        {"month_key": 7, "name": "July"},
        {"month_key": 8, "name": "August"},
        {"month_key": 9, "name": "September"},
        {"month_key": 10, "name": "October"},
        {"month_key": 11, "name": "November"},
        {"month_key": 12, "name": "December"},
    ]


def test_date_dim_row(transform, date_dim_rows):
    rows = transform.date_dim_row()
    rows == [date_dim_rows]


def test_tags_exists(transform, crypto_data, tags_all_exist):
    tags = transform._get_tags(crypto_data, tags_all_exist)
    assert tags == set()


def test_tags_mixture(transform, crypto_data, tags_one_exist):
    tags = transform._get_tags(crypto_data, tags_one_exist)
    assert tags == set(["popular", "top10"])