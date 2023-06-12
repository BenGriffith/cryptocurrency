import json
from datetime import datetime

from decouple import config
from google.cloud.storage import Client as BlobClient
from google.cloud.bigquery import Client as BigQueryClient
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob


class Transform:

    def __init__(self) -> None:
        self._blob_client = BlobClient()
        self._bq_client = BigQueryClient()
        self._blob = f"{datetime.today().strftime('%Y-%m-%d')}.json"

    def _get_bucket(self) -> Bucket:
        bucket_name = config("BUCKET", cast=str)
        bucket = self._blob_client.get_bucket(bucket_name)
        return bucket

    def _get_blob(self) -> Blob:
        bucket = self._get_bucket()
        blob = bucket.blob(self._blob)
        with blob.open("r") as file:
            crypto_data = json.loads(file.read())
        return crypto_data

    def _load_facts(self) -> None:
        pass

    def _load_dimensions(self) -> None:
        pass


if __name__ == "__main__":
    transform = Transform()
    transform._get_blob()