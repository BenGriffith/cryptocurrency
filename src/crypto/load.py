import json
from typing import Dict
from datetime import datetime

from decouple import config
from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket

from crypto.utils.api import Connection
from crypto.utils.constants import LISTINGS_LATEST_URL


class Load:

    def __init__(self) -> None:
        self._gcs_client = Client()
    
    def _get_bucket(self) -> Bucket:
        bucket_name = config("BUCKET", cast=str)
        bucket = self._gcs_client.bucket(bucket_name)
        return bucket

    def create_blob(self, crypto_data: Dict) -> None:
        bucket = self._get_bucket()
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = bucket.blob(blob_name)
        with blob.open("w") as file:
            file.write(json.dumps(crypto_data))


if __name__ == "__main__":
    connection = Connection()
    coinmarket_response = connection.request(url=LISTINGS_LATEST_URL)
    data = coinmarket_response["data"]

    load = Load()
    load.create_blob(crypto_data=coinmarket_response)