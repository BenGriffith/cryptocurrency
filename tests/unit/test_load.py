import os
from datetime import datetime

from google.cloud.storage.bucket import Bucket


def test_load_get_bucket(load):
    assert type(load._get_bucket()) == Bucket
    assert load._get_bucket().name == os.getenv("BUCKET")


def test_load_create_blob(coinmarket_response, load, bucket):
    blob_name = f"{datetime.today().strftime('%Y-%m-%d')}-unit-test.json"
    load.create_blob(name=blob_name, crypto_data=coinmarket_response)
    blob = bucket.blob(blob_name)
    blob_exists = blob.exists()
    assert blob_exists
    if blob_exists:
        blob.delete()