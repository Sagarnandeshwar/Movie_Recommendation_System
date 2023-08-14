from data_collection.utils.kafka_utils import get_log_type, validate_log_data, log_set, parse_request_log

sample_watch_log = "2022-09-28T17:18:57,337106,GET /data/m/pulp+fiction+1994/9.mpg"
sample_rate_log = "2022-09-28T17:20:44,65411,GET /rate/it+happened+in+saint-tropez+2013=3"
sample_log_missing_fields = "2022-09-28T17:20:44,GET /rate/it+happened+in+saint-tropez+2013=3"
sample_request_log = "2022-10-29T21:54:35.854,231202,recommendation request fall2022-comp585-4.cs.mcgill.ca:8082, status 0, result: glory+1989,pulp+fiction+1994,the+class+trip+1998,seven+samurai+1954,narco+2004,revenge+of+the+nerds+iv+nerds+in+love+1994,the+godfather+1972,the+shipping+news+2001,my+brother+the+devil+2012,the+godfather+1972,star+wars+1977,bill+hicks+revelations+1993,gigi+1958,lion+of+the+desert+1981,breach+2007,indiana+jones+and+the+last+crusade+1989,oceans+eleven+2001,dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964,kill+baby_+kill+1966,this+is+it+2009, 819 ms"

def test_get_log_type():
    assert get_log_type(sample_watch_log) == "watch"
    assert get_log_type(sample_rate_log) == "rate"

def test_parse_request_log():
    request = parse_request_log(sample_request_log)

    expected_request = {
        "timestamp": "2022-10-29T21:54:35.854",
        "userid": "231202",
        "server": "fall2022-comp585-4.cs.mcgill.ca:8082",
        "code": "0",
        "predictions": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
        "response_time": "819 ms"
    }

    assert request == expected_request

def test_validate_log_data():
    log_set = set()
    log_data = sample_log_missing_fields.split(",")
    missing_field_outcome = validate_log_data(log_data)
    assert missing_field_outcome == False

    log_data = sample_watch_log.split(",")
    rating_only_outcome = validate_log_data(log_data, True)
    assert rating_only_outcome == False

    valid_outcome = validate_log_data(log_data)
    assert valid_outcome == True

    duplicate_outcome = validate_log_data(log_data)
    assert duplicate_outcome == False

