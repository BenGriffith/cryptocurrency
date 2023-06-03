def test_valid_api_request(coinmarket_response):
    status = coinmarket_response["status"]
    assert status["error_code"] == 0
    assert status["error_message"] == None
    assert status["credit_count"] == 25

    data = coinmarket_response["data"]
    assert len(data) == 5000

    for crypto in data:
        if crypto["name"] == "Bitcoin":
            assert crypto["symbol"] == "BTC"
            assert crypto["slug"] == "bitcoin"


def test_invalid_api_request(coinmarket_invalid_response):
    status = coinmarket_invalid_response["status"]
    assert status["error_code"] == 1002
    assert status["error_message"] == "API key missing."
    assert status["credit_count"] == 0