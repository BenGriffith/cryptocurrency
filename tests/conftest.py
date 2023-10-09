from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytest
from unittest.mock import MagicMock

from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob
from google.cloud.bigquery import Client as BQClient

from crypto.transform import Transform


@pytest.fixture
def coinmarket_valid_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": {
            "timestamp": "2023-06-13T19:30:34.499Z",
            "error_code": 0,
            "error_message": "",
            "elapsed": 10,
            "credit_count": 1,
            "notice": ""
        },
        "data": {
            "1": {
                "id": 1,
                "name": "Ethereum",
                "symbol": "ETH",
                "slug": "ethereum"
            },
            "2": {
                "id": 2,
                "name": "Bitcoin",
                "symbol": "BTC",
                "slug": "bitcoin",
            }
        }
    }
    return mock_response


@pytest.fixture
def coinmarket_invalid_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "status": {
            "timestamp": "2023-06-13T19:30:34.499Z",
            "error_code": 1002,
            "error_message": "API key missing.",
            "elapsed": 10,
            "credit_count": 0
            }
        }
    return mock_response


@pytest.fixture
def mock_blob_data():
    return MagicMock()


@pytest.fixture
def mock_gcs_client():
    return MagicMock(spec=Client)


@pytest.fixture
def mock_bucket():
    return MagicMock(spec=Bucket)


@pytest.fixture
def mock_blob():
    return MagicMock(spec=Blob)


@pytest.fixture
def mock_bq_client():
    return MagicMock(spec=BQClient)


@pytest.fixture
def transform(mock_gcs_client, mock_bq_client):
    return Transform(
        storage_client=mock_gcs_client,
        bq_client=mock_bq_client,
        bucket_name="project-cryptocurrency"
    )


@pytest.fixture
def date_dim_rows():
    today = datetime.today()
    return {
        "date_key": today.strftime("%Y-%m-%d"),
        "year": today.year,
        "month_key": today.month,
        "day": today.day,
        "day_key": today.isoweekday(),
        "week_number": today.isocalendar().week,
        "week_end": today.fromisocalendar(today.year, today.isocalendar().week, 7).strftime("%Y-%m-%d"),
        "month_end": (today + relativedelta(day=31)).strftime("%Y-%m-%d")
    }


@pytest.fixture
def crypto_data():
    sample = {
        "data": [
            {
                "id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "slug": "bitcoin",
                "cmc_rank": 5,
                "num_market_pairs": 500,
                "circulating_supply": 16950100,
                "total_supply": 16950100,
                "max_supply": 21000000,
                "infinite_supply": False,
                "last_updated": "2018-06-02T22:51:28.209Z",
                "date_added": "2013-04-28T00:00:00.000Z",
                "tags": [
                    "mineable", "top10"
                ],
                "platform": None,
                "self_reported_circulating_supply": None,
                "self_reported_market_cap": None,
                "quote": {
                    "USD": {
                        "price": 9283.92,
                        "volume_24h": 7155680000,
                        "volume_change_24h": -0.152774,
                        "percent_change_1h": -0.152774,
                        "percent_change_24h": 0.518894,
                        "percent_change_7d": 0.986573,
                        "market_cap": 852164659250.2758,
                        "market_cap_dominance": 51,
                        "fully_diluted_market_cap": 952835089431.14,
                        "last_updated": "2018-08-09T22:53:32.000Z"
                    },
                    "BTC": {
                        "price": 1,
                        "volume_24h": 772012,
                        "volume_change_24h": 0,
                        "percent_change_1h": 0,
                        "percent_change_24h": 0,
                        "percent_change_7d": 0,
                        "market_cap": 17024600,
                        "market_cap_dominance": 12,
                        "fully_diluted_market_cap": 952835089431.14,
                        "last_updated": "2018-08-09T22:53:32.000Z"
                    }
                }
            },
            {
                "id": 1027,
                "name": "Ethereum",
                "symbol": "ETH",
                "slug": "ethereum",
                "num_market_pairs": 6360,
                "circulating_supply": 16950100,
                "total_supply": 16950100,
                "max_supply": 21000000,
                "infinite_supply": False,
                "last_updated": "2018-06-02T22:51:28.209Z",
                "date_added": "2013-04-28T00:00:00.000Z",
                "tags": [
                    "mineable", "popular"
                ],
                "platform": None,
                "quote": {
                    "USD": {
                        "price": 1283.92,
                        "volume_24h": 7155680000,
                        "volume_change_24h": -0.152774,
                        "percent_change_1h": -0.152774,
                        "percent_change_24h": 0.518894,
                        "percent_change_7d": 0.986573,
                        "market_cap": 158055024432,
                        "market_cap_dominance": 51,
                        "fully_diluted_market_cap": 952835089431.14,
                        "last_updated": "2018-08-09T22:53:32.000Z"
                        },
                    "ETH": {
                        "price": 1,
                        "volume_24h": 772012,
                        "volume_change_24h": -0.152774,
                        "percent_change_1h": 0,
                        "percent_change_24h": 0,
                        "percent_change_7d": 0,
                        "market_cap": 17024600,
                        "market_cap_dominance": 12,
                        "fully_diluted_market_cap": 952835089431.14,
                        "last_updated": "2018-08-09T22:53:32.000Z"
                    }
                }
            }
            ],
        "status": {
            "timestamp": "2018-06-02T22:51:28.209Z",
            "error_code": 0,
            "error_message": "",
            "elapsed": 10,
            "credit_count": 1
            }
    }
    return sample.get("data")


@pytest.fixture
def tags_all_exist():
    return set(["mineable", "popular", "top10"])


@pytest.fixture
def tags_one_exist():
    return set(["mineable"])