import json
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.bigquery import LoadJobConfig
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.helpers import service_credentials
from crypto.utils.constants import (
    BUCKET,
    CLOUD_STORAGE,
    BIGQUERY,
    PROJECT_ID,
    DAY_DIM,
    MONTH_DIM,
    DATE_DIM,
    INITIAL_LOAD,
    NAME_DIM,
)
from crypto.utils.setup import DayDim, MonthDim, DateDim, NameDim


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
        blob_name = f"{datetime.today().strftime('%Y-%m-%d')}.json" # for testing
        blob = self.blob(blob_name=blob_name)
        if blob.exists():
            with blob.open("r") as file:
                crypto_data = json.loads(file.read())
            return crypto_data
        return {}
    
    def load_table(self, table_id: str, rows: list) -> None:
        table = self.bq_client.get_table(table=table_id)

        job_config = LoadJobConfig(
            schema=table.schema
        )

        job = self.bq_client.load_table_from_json(
            json_rows=rows,
            destination=table_id,
            project=PROJECT_ID,
            job_config=job_config
        )

        job.result()
    
    def day_dim_rows(self) -> list:
        rows = []
        for key, day in enumerate(calendar.day_name, start=1):
            row = DayDim(day_key=key, name=day)._asdict()
            rows.append(row)
        return rows

    def month_dim_rows(self) -> list:
        rows = []
        for key, month in enumerate(list(calendar.month_name)[1:], start=1):
            row = MonthDim(month_key=key, name=month)._asdict()
            rows.append(row)
        return rows
    
    def date_dim_row(self) -> list:
        d = datetime.today()
        row = DateDim(
            date_key=f"{d:%Y-%m-%d}",
            year=d.year,
            month_key=d.month,
            day=d.day,
            day_key=d.isoweekday(),
            week_number=d.isocalendar().week,
            week_end=d.fromisocalendar(d.year, d.isocalendar().week, 7).strftime('%Y-%m-%d'),
            month_end=(d + relativedelta(day=31)).strftime("%Y-%m-%d")
        )._asdict()
        return [row]
    
    def _get_name_dim_keys(self):
        query = """SELECT DISTINCT symbol FROM {name_dim}""".format(name_dim=NAME_DIM)
        job = self.bq_client.query(query=query)
        result = job.result()
        return result

    def name_dim_rows(self, crypto_data: dict) -> None:
        result = self._get_name_dim_keys()
        symbols = [row["symbol"] for row in result]

        rows = []
        for row in crypto_data:
            if row["symbol"] in symbols:
                continue
            name_dim = NameDim(name_key=row["name"], symbol=row["symbol"], slug=row["slug"])
            rows.append(name_dim._asdict())
        return rows


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
    if crypto_data:
        crypto_data = crypto_data["data"]

        # name dimension
        name_dim_rows = transform.name_dim_rows(crypto_data=crypto_data)
        if name_dim_rows:
            transform.load_table(table_id=NAME_DIM, rows=name_dim_rows