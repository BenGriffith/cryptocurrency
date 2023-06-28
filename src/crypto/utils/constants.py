from pathlib import Path

from decouple import config

from crypto.utils.helpers import (
    parse_service_account_file, 
    service_account_absolute_path,
)

LISTINGS_LATEST_URL = config("LISTINGS_LATEST_URL", cast=str)
CLOUD_STORAGE_ABSOLUTE = service_account_absolute_path("CLOUD_STORAGE")
CLOUD_STORAGE = parse_service_account_file(CLOUD_STORAGE_ABSOLUTE)
BIGQUERY_ABSOLUTE = service_account_absolute_path("BIGQUERY")
BIGQUERY = parse_service_account_file()
BUCKET = config("BUCKET", cast=str)