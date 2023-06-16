import pytest

from crypto.utils.api import Connection
from crypto.utils.constants import (
    CLOUD_STORAGE, 
    BUCKET, 
    Services,
)
from crypto.utils.helpers import client
from crypto.load import Load


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
def load():
    return Load(
        service=Services.GCS.value,
        service_acct=CLOUD_STORAGE,
        bucket=BUCKET,
    )


@pytest.fixture
def gcs_client():
    return client(service=Services.GCS.value, service_acct=CLOUD_STORAGE)


@pytest.fixture
def bucket(gcs_client):
    return gcs_client.bucket(BUCKET)