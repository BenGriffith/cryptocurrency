import json
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.bigquery import LoadJobConfig, QueryJob
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
    TAG_DIM
)
from crypto.utils.setup import DayDim, MonthDim, DateDim, NameDim, TagDim


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
        blob_name = "2023-07-12.json" #f"{datetime.today().strftime('%Y-%m-%d')}.json"
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
    
    def _query(self, query: str) -> QueryJob:
        job = self.bq_client.query(query=query)
        result = job.result()
        return result

    def _get_existing_symbols(self) -> list:
        symbol_query = """SELECT symbol FROM {name_dim}""".format(name_dim=NAME_DIM)
        result = self._query(query=symbol_query)
        return [row["symbol"] for row in result]

    def name_dim_rows(self, crypto_data: dict) -> list:
        existing_symbols = self._get_existing_symbols()
        rows = []
        for row in crypto_data:
            if row["symbol"] in existing_symbols:
                continue
            name_dim = NameDim(name_key=row["name"], symbol=row["symbol"], slug=row["slug"])
            rows.append(name_dim._asdict())
        return rows

    def _get_existing_tags(self) -> list:
        tag_query = """SELECT tag FROM {tag_dim}""".format(tag_dim=TAG_DIM)
        result = self._query(query=tag_query)
        return [row["tag"] for row in result]

    def _get_tags(self, crypto_data: dict, existing_tags: list) -> set:
        tags = set()
        for row in crypto_data:
            for tag in row["tags"]:
                if tag in existing_tags:
                    continue
                tags.add(tag)
        return tags
    
    def _get_tag_key_max(self):
        tag_query = """SELECT MAX(tag_key) AS max_key FROM {tag_dim}""".format(tag_dim=TAG_DIM)
        result = self._query(query=tag_query)
        return [row["max_key"] for row in result][0]
    
    def tag_dim_rows(self, crypto_data: dict) -> list:
        existing_tags = self._get_existing_tags()
        tags = self._get_tags(crypto_data=crypto_data, existing_tags=existing_tags)
        
        max_key = 0
        if tags and not INITIAL_LOAD:
            max_key = self._get_tag_key_max()

        rows = []
        start = max_key if max_key else 1        
        for key, tag in enumerate(tags, start=start):
            tag_dim = TagDim(tag_key=key, tag=tag)
            rows.append(tag_dim._asdict())
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
            transform.load_table(table_id=NAME_DIM, rows=name_dim_rows)

        # tag dimension
        tag_dim_rows = transform.tag_dim_rows(crypto_data=crypto_data)
        if tag_dim_rows:
            transform.load_table(table_id=TAG_DIM, rows=tag_dim_rows)