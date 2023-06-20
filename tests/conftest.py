import pytest
from unittest.mock import MagicMock

from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob


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