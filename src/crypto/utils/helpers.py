from typing import Union

from google.cloud.storage import Client as GCSClient
from google.cloud.bigquery import Client as BQClient
from google.oauth2 import service_account

from crypto.utils.constants import Services


def client(service: str, service_acct: dict) -> Union[GCSClient, BQClient]:
    credentials = service_account.Credentials.from_service_account_file(service_acct)
    if service == Services.GCS.value:
        return GCSClient(credentials=credentials)
    else:
        return BQClient(credentials=credentials)