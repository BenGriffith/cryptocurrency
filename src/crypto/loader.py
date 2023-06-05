import json
from typing import Dict
from datetime import datetime

from decouple import config
from google.cloud.storage import Client


class Loader:

    def __init__(self) -> None:
        self._storage_client = Client()
    
    def _get_bucket(self) -> str:
        bucket_name = config("BUCKET", cast=str)
        bucket = self._storage_client.bucket(bucket_name)
        return bucket

    def create_blob(self, data: Dict) -> None:
        bucket = self._get_bucket()
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = bucket.blob(blob_name)

        with blob.open("w") as file:
            file.write(json.dumps(data))