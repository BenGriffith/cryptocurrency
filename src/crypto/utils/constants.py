import os
from enum import Enum

LISTINGS_LATEST_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
CLOUD_STORAGE = os.getenv("CLOUD_STORAGE")
BUCKET = os.getenv("BUCKET")

class Services(Enum):
    GCS = "storage"
    BQ = "bigquery"