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
DAY_DIM = f"{PROJECT_ID}.{DATASET}.{config('DAY_DIM')}"
MONTH_DIM = f"{PROJECT_ID}.{DATASET}.{config('MONTH_DIM')}"
DATE_DIM = f"{PROJECT_ID}.{DATASET}.{config('DATE_DIM')}"
NAME_DIM = f"{PROJECT_ID}.{DATASET}.{config('NAME_DIM')}"
TAG_DIM = f"{PROJECT_ID}.{DATASET}.{config('TAG_DIM')}"
NAME_TAG_BRIDGE = f"{PROJECT_ID}.{DATASET}.{config('NAME_TAG')}"
QUOTE_DIM = f"{PROJECT_ID}.{DATASET}.{config('QUOTE_DIM')}"
PRICE_FACT = f"{PROJECT_ID}.{DATASET}.{config('PRICE_FACT')}"
SUPPLY_FACT = f"{PROJECT_ID}.{DATASET}.{config('SUPPLY_FACT')}"
RANK_FACT = f"{PROJECT_ID}.{DATASET}.{config('RANK_FACT')}"
TRADING_VOLUME_DAY_FACT = f"{PROJECT_ID}.{DATASET}.{config('TRADING_VOLUME_DAY_FACT')}"
INITIAL_LOAD = config("INITIAL_LOAD", cast=bool)