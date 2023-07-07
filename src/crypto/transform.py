import json
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.helpers import service_credentials
from crypto.utils.constants import (
    BUCKET,
    CLOUD_STORAGE,
    BIGQUERY,
    DAY_DIM,
    MONTH_DIM,
    DATE_DIM,
    INITIAL_LOAD,
)


class Transform:

    def __init__(self, storage_client: CSClient, bq_client: BQClient, bucket_name: str) -> None:
        self.storage_client = storage_client
        self.bq_client = bq_client
        self._bucket = self.storage_client.bucket(bucket_name=bucket_name)

    @property
    def bucket(self) -> Bucket:
        return self._bucket
    
    def blob(self, blob_name: str) -> Blob:
        return self.bucket.blob(blob_name=blob_name)

    def read_blob(self) -> dict:
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json"
        blob = self.blob(blob_name=blob_name)
        if blob.exists():
            with blob.open("r") as file:
                crypto_data = json.loads(file.read())
            return crypto_data
        return {}
    
    def load_table(self, table_id: str, rows: list) -> None:
        table = self.bq_client.get_table(table=table_id)
        self.bq_client.insert_rows(table=table_id, rows=rows, selected_fields=table.schema)
    
    def day_dim_rows(self) -> list:
        rows = [(key, day) for key, day in enumerate(calendar.day_name, start=1)]
        return rows

    def month_dim_rows(self) -> list:
        rows = [(key, month) for key, month in enumerate(list(calendar.month_name)[1:], start=1)]
        return rows
    
    def date_dim_row(self) -> list:
        d = datetime.today()
        date_key = f"{d:%Y-%m-%d}"
        year = d.year
        month_key = d.month
        day = d.day
        day_key = d.isoweekday()
        week_number = d.isocalendar().week
        week_end_date = d.fromisocalendar(year, week_number, 7).date()
        month_end_date = (d + relativedelta(day=31)).date()

        return [(date_key, year, month_key, day, day_key, week_number, week_end_date, month_end_date)]
        

if __name__ == "__main__":
    storage_client = CSClient(credentials=service_credentials(CLOUD_STORAGE))
    bq_client = BQClient(credentials=service_credentials(BIGQUERY))

    transform = Transform(storage_client=storage_client, bq_client=bq_client, bucket_name=BUCKET)

    if INITIAL_LOAD:
        day_dim_rows = transform.day_dim_rows()
        month_dim_rows = transform.month_dim_rows()
        transform.load_table(table_id=DAY_DIM, rows=day_dim_rows)
        transform.load_table(table_id=MONTH_DIM, rows=month_dim_rows)

    # date dimension
    date_dim_row = transform.date_dim_row()
    transform.load_table(table_id=DATE_DIM, rows=date_dim_row)

    crypto_data = transform.read_blob()

    # name dimension
