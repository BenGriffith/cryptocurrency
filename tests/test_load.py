from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.load import Load


def test_bucket(mock_gcs_client, mock_bucket):
    load = Load(client=mock_gcs_client, bucket_name="test-bucket")
    mock_gcs_client.bucket.return_value = mock_bucket
    assert isinstance(load.bucket(), Bucket)


def test_blob(mock_gcs_client, mock_bucket, mock_blob):
    load = Load(client=mock_gcs_client, bucket_name="test-bucket")
    mock_gcs_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    assert isinstance(load.blob(blob_name="test-blob"), Blob)


def test_create_blob(mock_gcs_client, mock_bucket, mock_blob, mock_blob_data):
    load = Load(client=mock_gcs_client, bucket_name="test-bucket")
    mock_gcs_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob_data.json.return_value = {"name": "Bitcoin"}
    load.create_blob(crypto_data=mock_blob_data.json.return_value)
    mock_bucket.blob.assert_called_once()
    mock_blob.open.assert_called_once_with("w")