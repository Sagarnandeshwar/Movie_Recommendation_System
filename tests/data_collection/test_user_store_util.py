import pytest
import data_collection.utils.user_utils as user_utils
from datetime import datetime

dummy_prediction = {
    "0": "finding nemo",
    "1": "kill bill",
    "2": "inception",
    "3": "diplomacy",
    "4": "finding nemo",
    "5": "kill bill",
    "6": "inception",
    "7": "diplomacy",
    "8": "finding nemo",
    "9": "kill bill",
    "10": "inception",
    "11": "diplomacy",
    "12": "finding nemo",
    "13": "kill bill",
    "14": "inception",
    "15": "diplomacy",
    "16": "finding nemo",
    "17": "kill bill",
    "18": "inception",
    "19": "diplomacy"
}

dummy_time = "2022-10-04T01:34:16"

dummy_time2 = "2022-10-04T03:34:16"

dummy_rate_log = {
    "time": "2022-10-04T01:37:16",
    "userid": "1",
    "movieid": "diplomacy",
    "rating": 4
}

dummy_rate_log2 = {
    "time": "2022-10-05T01:37:16",
    "userid": "1",
    "movieid": "diplomacy",
    "rating": 5
}

dummy_watch_log = {
    "time": "2022-10-04T01:37:16",
    "userid": "1",
    "movieid": "diplomacy",
    "minute": 45
}

dummy_watch_log2 = {
    "time": "2022-11-04T01:37:16",
    "userid": "1",
    "movieid": "diplomacy",
    "minute": 65
}

dummy_request_log = {
    "timestamp": "2022-10-04T01:37:16",
    "userid": "1",
    "server": "fall2022-comp585-4.cs.mcgill.ca:8082",
    "code": "0",
    "predictions": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
    "response_time": "819 ms"
}

dummy_request_log2 = {
    "timestamp": "2022-10-04T03:34:16",
    "userid": "1",
    "server": "fall2022-comp585-4.cs.mcgill.ca:8082",
    "code": "0",
    "predictions": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
    "response_time": "819 ms"
}

@pytest.fixture
def user_store():
    return user_utils.UserPredictionStore()

def test_take_predictions(user_store):
    assert user_store.get_user_store() == {}

    user_store.take_predictions(dummy_request_log)

    assert user_store.get_user_store() == {
        "1": {
            "predictions": {
                "2022-10-04T01:37:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"]
            },
            "rate": {},
            "watch": {},
            "latest_prediction": "2022-10-04T01:37:16"
        }
    }

def test_add_rating(user_store):
    user_store.take_predictions(dummy_request_log)
    user_store.add_rating(dummy_rate_log)
    assert user_store.get_user_store() == {
        "1": {
            "predictions": {
                "2022-10-04T01:37:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"]
            },
            "rate": {
                "2022-10-04T01:37:16": {
                    dummy_rate_log['movieid']: dummy_rate_log['rating']
                }
            },
            "watch": {},
            "latest_prediction": "2022-10-04T01:37:16"
        }
    }

def test_add_new_rating_after_multiple_recommendations(user_store):
    user_store.take_predictions(dummy_request_log)
    user_store.add_rating(dummy_rate_log)
    user_store.take_predictions(dummy_request_log2)
    user_store.add_rating(dummy_rate_log2)
    assert user_store.get_user_store() == {
        "1": {
            "predictions": {
                "2022-10-04T01:37:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
                "2022-10-04T03:34:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"]
            },
            "rate": {
                "2022-10-04T01:37:16": {
                    dummy_rate_log['movieid']: dummy_rate_log['rating']
                },
                "2022-10-04T03:34:16": {
                    dummy_rate_log2['movieid']: dummy_rate_log2['rating']
                }
            },
            "watch": {},
            "latest_prediction": dummy_time2
        }
    }

def test_add_watching(user_store):
    user_store.empty_user_store()
    user_store.take_predictions(dummy_request_log)
    user_store.add_watch_data(dummy_watch_log)
    print(user_store.get_user_store())
    assert user_store.get_user_store() == {
        "1": {
            "predictions": {
                "2022-10-04T01:37:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
            },
            "rate": {},
            "watch": {
                "2022-10-04T01:37:16": {
                    dummy_watch_log['movieid']: dummy_watch_log['minute']
                }
            },
            "latest_prediction": "2022-10-04T01:37:16"
        }
    }

def test_add_new_watching_after_multiple_recommendations(user_store):
    user_store.empty_user_store()
    user_store.take_predictions(dummy_request_log)
    user_store.add_watch_data(dummy_watch_log)
    user_store.take_predictions(dummy_request_log2)
    user_store.add_watch_data(dummy_watch_log2)
    assert user_store.get_user_store() == {
        "1": {
            "predictions": {
                "2022-10-04T01:37:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"],
                "2022-10-04T03:34:16": ["glory+1989","pulp+fiction+1994","the+class+trip+1998","seven+samurai+1954","narco+2004","revenge+of+the+nerds+iv+nerds+in+love+1994","the+godfather+1972","the+shipping+news+2001","my+brother+the+devil+2012","the+godfather+1972","star+wars+1977","bill+hicks+revelations+1993","gigi+1958","lion+of+the+desert+1981","breach+2007","indiana+jones+and+the+last+crusade+1989","oceans+eleven+2001","dr.+strangelove+or+how+i+learned+to+stop+worrying+and+love+the+bomb+1964","kill+baby_+kill+1966","this+is+it+2009"]
            },
            "rate": {},
            "watch": {
                "2022-10-04T01:37:16": {
                    dummy_watch_log['movieid']: dummy_watch_log['minute']
                },
                "2022-10-04T03:34:16": {
                    dummy_watch_log2['movieid']: dummy_watch_log2['minute']
                }
            },
            "latest_prediction": "2022-10-04T03:34:16"
        }
    }