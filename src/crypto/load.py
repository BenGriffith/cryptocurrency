import json
from typing import Dict
from datetime import datetime

from crypto.utils.api import Connection
from crypto.utils.constants import (
    LISTINGS_LATEST_URL, 
    CLOUD_STORAGE, 
    BUCKET, 
    Services,
)
from crypto.utils.helpers import client


class Load:

    def __init__(self, service: str, service_acct: dict, bucket: str) -> None:
        self.client = client(service=service, service_acct=service_acct)
        self.bucket = self.client.bucket(bucket)

    def create_blob(self, crypto_data: Dict) -> None:
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = self.bucket.blob(blob_name)
        with blob.open("w") as file:
            file.write(json.dumps(crypto_data))


if __name__ == "__main__":
    connection = Connection()
    coinmarket_response = connection.request(url=LISTINGS_LATEST_URL)

    load = Load(
        service=Services.GCS.value,
        service_acct=CLOUD_STORAGE,
        bucket=BUCKET,
    )
    load.create_blob(crypto_data=coinmarket_response)