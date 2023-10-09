import json
from pathlib import Path

from decouple import config

from google.oauth2 import service_account
from google.oauth2.service_account import Credentials


def service_credentials(service_acct: dict) -> Credentials:
    return service_account.Credentials.from_service_account_info(info=service_acct)

def parse_service_account_file(path: str) -> dict:
    with open(path, mode="r") as file:
        service_account_info = json.load(file)
    return service_account_info

def service_account_absolute_path(service_account: str) -> str:
    return f"{Path.cwd().parent.parent.parent}{config(service_account)}"