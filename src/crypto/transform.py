import json
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

from google.cloud.storage import Client as CSClient # Cloud Storage Client
from google.cloud.bigquery import Client as BQClient # BigQuery Client
from google.cloud.bigquery import LoadJobConfig
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob

from crypto.utils.helpers import service_credentials
from crypto.utils.constants import Project, Table, Queries, ROUNDING


class Transform:

    def __init__(self, storage_client: CSClient, bq_client: BQClient, bucket_name: str) -> None:
        self.storage_client = storage_client
        self.bq_client = bq_client
        self.bucket_name = bucket_name

    @property
    def bucket(self) -> Bucket:
        return self.storage_client.bucket(bucket_name=self.bucket_name)
    
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

        job_config = LoadJobConfig(
            schema=table.schema
        )

        job = self.bq_client.load_table_from_json(
            json_rows=rows,
            destination=table_id,
            project=Project.PROJECT_ID.value,
            job_config=job_config
        )

        job.result()
    
    def day_dim_rows(self) -> list:
        return [{"day_key": key, "name": day} for key, day in enumerate(calendar.day_name, start=1)]

    def month_dim_rows(self) -> list:
        return [{"month_key": key, "name": month} for key, month in enumerate(list(calendar.month_name)[1:], start=1)]
    
    def date_dim_row(self) -> list:
        d = datetime.today()
        row = {
            "date_key" : f"{d:%Y-%m-%d}",
            "year": d.year,
            "month_key": d.month,
            "day": d.day,
            "day_key": d.isoweekday(),
            "week_number": d.isocalendar().week,
            "week_end": d.fromisocalendar(d.year, d.isocalendar().week, 7).strftime('%Y-%m-%d'),
            "month_end": (d + relativedelta(day=31)).strftime("%Y-%m-%d"),
        }
        return [row]

    def name_dim_rows(self, crypto_data: dict) -> list:
        existing_symbols_query = Queries.symbols.value
        result = self.bq_client.query(query=existing_symbols_query).result()
        existing_symbols = set(row["symbol"] for row in result)

        rows = []
        for row in crypto_data:
            if row["symbol"] in existing_symbols:
                continue
            rows.append({"name_key": row["name"], "symbol": row["symbol"], "slug": row["slug"]})
        return rows

    def _get_tags(self, crypto_data: dict, existing_tags: set) -> set:
        tags = set()
        for row in crypto_data:
            for tag in row["tags"]:
                if tag in existing_tags:
                    continue
                tags.add(tag)
        return tags
    
    def tag_dim_rows(self, crypto_data: dict) -> list:
        existing_tags_query = Queries.tags.value
        result = self.bq_client.query(query=existing_tags_query).result()
        existing_tags = set(row["tag"] for row in result)

        tags = self._get_tags(crypto_data=crypto_data, existing_tags=existing_tags)
        
        max_key = 0
        if tags and not Project.INITIAL_LOAD.value:
            tag_query = Queries.max_key.value
            result = self.bq_client.query(query=tag_query).result()
            max_key = [row["max_key"] for row in result][0]

        rows = []
        start = max_key if max_key else 1        
        for key, tag in enumerate(tags, start=start):
            rows.append({"tag_key": key, "tag": tag})
        return rows

    def name_tag_bridge_table(self, date_key: date, crypto_data: dict) -> list:
        tag_query = Queries.tag_key.value
        result = self.bq_client.query(query=tag_query).result()
        tag_dim = {row["tag_key"]: row["tag"] for row in result}

        rows = []     
        for row in crypto_data:
            name = row["name"]
            tags = row["tags"]
            
            if not tags:
                continue
            
            for tag in tags:
                tag_key = [key for key, value in tag_dim.items() if value == tag][0]
                rows.append({"name_key": name, "date_key": date_key, "tag_key": tag_key})
        return rows
    
    def quote_dim_rows(self, date_key: date, crypto_data: dict) -> list:
        return [{"name_key": row["name"], "date_key": date_key, "quote": [row["quote"]]} for row in crypto_data]
    
    def price_fact_rows(self, date_key: date, crypto_data: dict) -> list:
        rows = []
        for row in crypto_data:
            price = round(row["quote"]["USD"]["price"], ROUNDING)
            rows.append({"name_key": row["name"], "date_key": date_key, "price": price})
        return rows
    
    def supply_fact_rows(self, date_key: date, crypto_data: dict) -> list:
        rows = []
        for row in crypto_data:
            circulating = round(row["circulating_supply"], ROUNDING)
            total = round(row["total_supply"], ROUNDING)
            rows.append({"name_key": row["name"], "date_key": date_key, "circulating": circulating, "total": total})
        return rows
    
    def rank_fact_rows(self, date_key: date, crypto_data: dict) -> list:
        return [{"name_key": row["name"], "date_key": date_key, "rank": row["cmc_rank"]} for row in crypto_data]
    
    def trading_volume_fact_rows(self, date_key: date, crypto_data: dict) -> list:
        rows = []
        for row in crypto_data:
            volume = round(row["quote"]["USD"]["volume_24h"], ROUNDING)
            rows.append({"name_key": row["name"], "date_key": date_key, "volume": volume})
        return rows
            

if __name__ == "__main__":
    storage_client = CSClient(credentials=service_credentials(Project.CLOUD_STORAGE.value))
    bq_client = BQClient(credentials=service_credentials(Project.BIGQUERY.value))
    transform = Transform(storage_client=storage_client, bq_client=bq_client, bucket_name=Project.BUCKET.value)

    if Project.INITIAL_LOAD.value:
        day_dim_rows = transform.day_dim_rows()
        month_dim_rows = transform.month_dim_rows()
        transform.load_table(table_id=Table.DAY_DIM.value, rows=day_dim_rows)
        transform.load_table(table_id=Table.MONTH_DIM.value, rows=month_dim_rows)

    # date dimension
    date_dim_row = transform.date_dim_row()
    date_key = date_dim_row[0]["date_key"]
    transform.load_table(table_id=Table.DATE_DIM.value, rows=date_dim_row)

    crypto_data = transform.read_blob()
    if crypto_data:
        crypto_data = crypto_data["data"]

        # name dimension
        if (name_dim_rows := transform.name_dim_rows(crypto_data=crypto_data)):
            transform.load_table(table_id=Table.NAME_DIM.value, rows=name_dim_rows)

        # tag dimension
        if (tag_dim_rows := transform.tag_dim_rows(crypto_data=crypto_data)):
            transform.load_table(table_id=Table.TAG_DIM.value, rows=tag_dim_rows)

        # name tag bridge
        if (name_tag_rows := transform.name_tag_bridge_table(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.NAME_TAG_BRIDGE.value, rows=name_tag_rows)

        # quote dimension
        if (quote_dim_rows := transform.quote_dim_rows(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.QUOTE_DIM.value, rows=quote_dim_rows)

        # price fact
        if (price_fact_rows := transform.price_fact_rows(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.PRICE_FACT.value, rows=price_fact_rows)

        # supply fact
        if (supply_fact_rows := transform.supply_fact_rows(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.SUPPLY_FACT.value, rows=supply_fact_rows)

        # rank fact
        if (rank_fact_rows := transform.rank_fact_rows(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.RANK_FACT.value, rows=rank_fact_rows)

        # trading volume fact
        if (trading_volume_fact_rows := transform.trading_volume_fact_rows(date_key=date_key, crypto_data=crypto_data)):
            transform.load_table(table_id=Table.TRADING_VOLUME_DAY_FACT.value, rows=trading_volume_fact_rows)