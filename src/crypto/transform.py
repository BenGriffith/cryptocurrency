import json
from datetime import datetime
from typing import Union

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.helpers import service_credentials
from crypto.utils.constants import (
    CLOUD_STORAGE,
    BIGQUERY,
)


class Transform:

    def __init__(self, storage_client: CSClient, bq_client: BQClient, bucket_name: str) -> None:
        self.storage_client = storage_client
        self.bq_client = bq_client
        self.bucket_name = bucket_name

    def bucket(self) -> Bucket:
        return self.storage_client.bucket(bucket_name=self.bucket_name)
    
    def blob(self, blob_name: str) -> Blob:
        return self.bucket().blob(blob_name=blob_name)

    def read_blob(self) -> dict:
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = self.blob(blob_name=blob_name)
        if blob.exists():
            with blob.open("r") as file:
                crypto_data = json.loads(file.read())
            return crypto_data
        return {}
    

if __name__ == "__main__":
    storage_client = CSClient(credentials=service_credentials(CLOUD_STORAGE))
    bq_client = BQClient(credentials=service_credentials(BIGQUERY))