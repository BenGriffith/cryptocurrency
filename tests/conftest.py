import os

import pytest

from crypto.utils.api import Connection
from crypto.utils.constants import LISTINGS_LATEST_URL
from crypto.load import Load
from crypto.transform import Transform


@pytest.fixture
def coinmarket_response():
    connection = Connection(limit=100)
    response = connection.request(url=LISTINGS_LATEST_URL)
    return response


@pytest.fixture
def coinmarket_invalid_response():
    connection = Connection()
    connection._headers["X-CMC_PRO_API_KEY"] = ""
    response = connection.request(url=LISTINGS_LATEST_URL)
    return response


@pytest.fixture
def load():
    return Load()


@pytest.fixture
def gcs_client():
    return Load()._gcs_client


@pytest.fixture
def bucket(gcs_client):
    bucket_name = os.getenv("BUCKET")
    bucket = gcs_client.bucket(bucket_name)
    return bucket