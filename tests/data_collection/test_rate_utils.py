from data_collection.utils.rate_utils import parse_rate_log

sample_rate_log = "2022-09-28T17:20:44,65411,GET /rate/it+happened+in+saint-tropez+2013=3"

def test_parse_rate_log():
    rate = parse_rate_log(sample_rate_log)

    expected_rate = new_log = {
        "time": "2022-09-28T17:20:44",
        "userid": "65411",
        "movieid": "it+happened+in+saint-tropez+2013",
        "rating": "3"
    }

    assert rate == expected_rate
