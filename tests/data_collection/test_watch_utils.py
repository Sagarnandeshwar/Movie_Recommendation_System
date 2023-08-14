from data_collection.utils.watch_utils import parse_watch_log

sample_watch_log = "2022-09-28T17:18:57,337106,GET /data/m/pulp+fiction+1994/9.mpg"

def test_parse_watch_log():
    watch = parse_watch_log(sample_watch_log)

    expected_watch = {
        "time": "2022-09-28T17:18:57",
        "userid": "337106",
        "movieid": "pulp+fiction+1994",
        "minute": "9"
    }

    assert watch == expected_watch
