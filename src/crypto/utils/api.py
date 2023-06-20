import os

import requests


class Connection:

    def __init__(self, limit: int = 5000) -> None:
        self._api_key = os.getenv("COINMARKET_API_KEY")
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": f"{self._api_key}"
        }
        self.parameters = {
            "start": 1,
            "limit": limit,
        }

    def request(self, url: str) -> dict:
        response = requests.get(url, headers=self._headers, params=self._parameters)
        data = response.json()
        return data