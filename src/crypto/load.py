import json
from datetime import datetime

from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.api import Connection
from crypto.utils.constants import (
    LISTINGS_LATEST_URL, 
    CLOUD_STORAGE, 
    BUCKET,
)
from crypto.utils.helpers import service_credentials


class Load:

    def __init__(self, client: Client, bucket_name: str) -> None:
        self.client = client
        self._bucket = self.client.bucket(bucket_name=bucket_name)

    @property
    def bucket(self) -> Bucket:
        return self._bucket
    
    def blob(self, blob_name: str) -> Blob:
        return self.bucket.blob(blob_name=blob_name)

    def create_blob(self, crypto_data: dict) -> None:
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = self.blob(blob_name=blob_name)
        with blob.open("w") as file:
            file.write(json.dumps(crypto_data))


if __name__ == "__main__":
    connection = Connection()
    coinmarket_response = connection.request(url=LISTINGS_LATEST_URL)

    storage_client = Client(credentials=service_credentials(CLOUD_STORAGE))
    load = Load(client=storage_client, bucket_name=BUCKET)
    load.create_blob(crypto_data=coinmarket_response)