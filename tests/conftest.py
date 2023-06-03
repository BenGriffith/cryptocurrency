import pytest

from src.crypto.utils.api import Connection
from src.crypto.utils.constants import LISTINGS_LATEST_URL

@pytest.fixture
def coinmarket_response():
    connection = Connection()
    response = connection.request(url=LISTINGS_LATEST_URL)
    return response


@pytest.fixture
def coinmarket_invalid_response():
    connection = Connection()
    connection._headers["X-CMC_PRO_API_KEY"] = ""
    response = connection.request(url=LISTINGS_LATEST_URL)
    return response