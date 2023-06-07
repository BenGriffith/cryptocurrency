import json
from typing import Dict
from datetime import datetime

from decouple import config
from google.cloud.storage import Client as GCSClient
from google.cloud.bigquery import Client as BQClient


class Loader:

    def __init__(self) -> None:
        self._gcs_client = GCSClient()
        self._bq_client = BQClient()
    
    def _get_bucket(self) -> str:
        bucket_name = config("BUCKET", cast=str)
        bucket = self._gcs_client.bucket(bucket_name)
        return bucket

    def create_blob(self, data: Dict) -> None:
        bucket = self._get_bucket()
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = bucket.blob(blob_name)

        with blob.open("w") as file:
            file.write(json.dumps(data))

    def load_tables():
        pass