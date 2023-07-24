from enum import Enum

from decouple import config

from crypto.utils.helpers import (
    parse_service_account_file, 
    service_account_absolute_path,
)

class Project(Enum):
    LISTINGS_LATEST_URL = config("LISTINGS_LATEST_URL", cast=str)
    CLOUD_STORAGE_ABSOLUTE = service_account_absolute_path("CLOUD_STORAGE")
    CLOUD_STORAGE = parse_service_account_file(CLOUD_STORAGE_ABSOLUTE)
    BIGQUERY_ABSOLUTE = service_account_absolute_path("BIGQUERY")
    BIGQUERY = parse_service_account_file(BIGQUERY_ABSOLUTE)
    BUCKET = config("BUCKET", cast=str)
    PROJECT_ID = config("PROJECT_ID", cast=str)
    DATASET = config("DATASET", cast=str)
    TABLE_QUALIFIER = f"{PROJECT_ID}.{DATASET}"
    INITIAL_LOAD = config("INITIAL_LOAD", cast=bool)


class Table(Enum):
    DAY_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('DAY_DIM')}"
    MONTH_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('MONTH_DIM')}"
    DATE_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('DATE_DIM')}"
    NAME_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('NAME_DIM')}"
    TAG_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('TAG_DIM')}"
    NAME_TAG_BRIDGE = f"{Project.TABLE_QUALIFIER.value}.{config('NAME_TAG')}"
    QUOTE_DIM = f"{Project.TABLE_QUALIFIER.value}.{config('QUOTE_DIM')}"
    PRICE_FACT = f"{Project.TABLE_QUALIFIER.value}.{config('PRICE_FACT')}"
    SUPPLY_FACT = f"{Project.TABLE_QUALIFIER.value}.{config('SUPPLY_FACT')}"
    RANK_FACT = f"{Project.TABLE_QUALIFIER.value}.{config('RANK_FACT')}"
    TRADING_VOLUME_DAY_FACT = f"{Project.TABLE_QUALIFIER.value}.{config('TRADING_VOLUME_DAY_FACT')}"
