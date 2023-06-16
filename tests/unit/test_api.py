import requests

def test_valid_api_request(mocker, coinmarket_valid_response):
    mocker.patch("requests.get", return_value=coinmarket_valid_response)
    response = requests.get("https://api.coinmarket.com/v2/cryptocurrency")
    assert response.status_code == 200

    status = response.json.return_value["status"]
    assert status["error_code"] == 0
    assert status["error_message"] == ""
    assert status["credit_count"] == 1

    data = response.json.return_value["data"]
    assert len(data) == 2

    for _, crypto_details in data.items():
        if crypto_details["name"] == "Bitcoin":
            assert crypto_details["symbol"] == "BTC"
            assert crypto_details["slug"] == "bitcoin"


def test_invalid_api_request(mocker, coinmarket_invalid_response):
    mocker.patch("requests.get", return_value=coinmarket_invalid_response)
    response = requests.get("https://api.coinmarket.com/v2/cryptocurrency")
    assert response.status_code == 401

    status = response.json.return_value["status"]
    assert status["error_code"] == 1002
    assert status["error_message"] == "API key missing."
    assert status["credit_count"] == 0