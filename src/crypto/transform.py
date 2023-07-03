import json
import calendar
from datetime import datetime

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.helpers import service_credentials, time_period
from crypto.utils.constants import (
    BUCKET,
    CLOUD_STORAGE,
    BIGQUERY,
    DAY_DIM,
    MONTH_DIM,
    INITIAL_LOAD
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
    
    @time_period
    def day_dim_rows(self) -> list:
        return list(calendar.day_name)
    
    @time_period
    def month_dim_rows(self) -> list:
        return list(calendar.month_name)[1:]
    
    def _date_dim_row(self) -> list:
        pass
    
    def load_table(self, table_id: str, rows: list) -> None:
        table = self.bq_client.get_table(table=table_id)
        self.bq_client.insert_rows(table=table_id, rows=rows, selected_fields=table.schema)
        

if __name__ == "__main__":
    storage_client = CSClient(credentials=service_credentials(CLOUD_STORAGE))
    bq_client = BQClient(credentials=service_credentials(BIGQUERY))

    transform = Transform(storage_client=storage_client, bq_client=bq_client, bucket_name=BUCKET)

    if INITIAL_LOAD:
        day_dim_rows = transform.day_dim_rows()
        month_dim_rows = transform.month_dim_rows()
        transform.load_table(table_id=DAY_DIM, rows=day_dim_rows)
        transform.load_table(table_id=MONTH_DIM, rows=month_dim_rows)