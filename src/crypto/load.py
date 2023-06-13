import os
import json
from typing import Dict
from datetime import datetime

from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket
from google.oauth2 import service_account

from crypto.utils.api import Connection
from crypto.utils.constants import LISTINGS_LATEST_URL


class Load:

    def __init__(self) -> None:
        self._service_account = os.getenv("CLOUD_STORAGE")
        self._credentials = service_account.Credentials.from_service_account_file(self._service_account)
        self._gcs_client = Client(credentials=self._credentials)
    
    def _get_bucket(self) -> Bucket:
        bucket_name = os.getenv("BUCKET")
        bucket = self._gcs_client.bucket(bucket_name)
        return bucket

    def create_blob(self, name: str, crypto_data: Dict) -> None:
        bucket = self._get_bucket()
        blob_name = name
        blob = bucket.blob(blob_name)
        with blob.open("w") as file:
            file.write(json.dumps(crypto_data))


if __name__ == "__main__":
    connection = Connection()
    coinmarket_response = connection.request(url=LISTINGS_LATEST_URL)

    load = Load()
    blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
    load.create_blob(name=blob_name, crypto_data=coinmarket_response)