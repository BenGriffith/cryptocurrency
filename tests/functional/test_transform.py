from datetime import datetime

from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.transform import Transform


def test_bucket(mock_gcs_client, mock_bq_client, mock_bucket):
    transform = Transform(
        storage_client=mock_gcs_client, 
        bq_client=mock_bq_client,
        bucket_name="crypto-bucket"
        )

    mock_gcs_client.bucket.return_value = mock_bucket
    assert isinstance(transform.bucket, Bucket)


def test_blob(mock_gcs_client, mock_bq_client, mock_bucket, mock_blob):
    transform = Transform(
        storage_client=mock_gcs_client,
        bq_client=mock_bq_client,
        bucket_name="crypto-bucket"
    )

    mock_gcs_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    assert isinstance(transform.blob(blob_name="crypto-blob"), Blob)


def test_read_blob(mock_gcs_client, mock_bq_client, mock_bucket, mock_blob):
    transform = Transform(
        storage_client=mock_gcs_client,
        bq_client=mock_bq_client,
        bucket_name="crypto-bucket"
    )
    mock_gcs_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.exists.return_value = True

    mock_data = '{"name": "Ethereum"}'
    mock_blob.open.return_value.__enter__.return_value.read.return_value = mock_data

    value = transform.read_blob()

    assert isinstance(value, dict)

    mock_bucket.blob.assert_called_once_with(blob_name=f"{datetime.today().strftime('%Y-%m-%d')}.json")
    mock_blob.open.assert_called_once_with("r")