from decouple import config

from crypto.utils.helpers import (
    parse_service_account_file, 
    service_account_absolute_path,
)

LISTINGS_LATEST_URL = config("LISTINGS_LATEST_URL", cast=str)
CLOUD_STORAGE_ABSOLUTE = service_account_absolute_path("CLOUD_STORAGE")
CLOUD_STORAGE = parse_service_account_file(CLOUD_STORAGE_ABSOLUTE)
BIGQUERY_ABSOLUTE = service_account_absolute_path("BIGQUERY")
BIGQUERY = parse_service_account_file(BIGQUERY_ABSOLUTE)
BUCKET = config("BUCKET", cast=str)
PROJECT_ID = config("PROJECT_ID", cast=str)
DATASET = config("DATASET", cast=str)
DAY_DIM = f"{PROJECT_ID}.{DATASET}.{config('DAY_DIM', cast=str)}"
MONTH_DIM = f"{PROJECT_ID}.{DATASET}.{config('MONTH_DIM', cast=str)}"
DATE_DIM = f"{PROJECT_ID}.{DATASET}.{config('DATE_DIM', cast=str)}"
INITIAL_LOAD = config("INITIAL_LOAD", cast=bool)