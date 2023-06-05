from crypto.utils.api import Connection
from crypto.utils.constants import LISTINGS_LATEST_URL
from crypto.loader import Loader

# API data request
connection = Connection()
coinmarket_response = connection.request(url=LISTINGS_LATEST_URL)
data = coinmarket_response["data"]

# loader = Loader()
# loader.create_blob(data=coinmarket_response)