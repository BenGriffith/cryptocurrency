from pathlib import Path

from decouple import config

from crypto.utils.helpers import parse_service_account_file

LISTINGS_LATEST_URL = config("LISTINGS_LATEST_URL", cast=str)
CLOUD_STORAGE_ABSOLUTE = f"{Path.cwd().parent.parent.parent}{config('CLOUD_STORAGE')}"
CLOUD_STORAGE = parse_service_account_file(CLOUD_STORAGE_ABSOLUTE)
BUCKET = config("BUCKET", cast=str)