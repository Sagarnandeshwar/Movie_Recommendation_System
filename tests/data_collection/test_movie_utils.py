import pytest
import data_collection.utils.movie_utils as movie_utils

@pytest.fixture
def movie_store():
    return movie_utils.MovieStore()

def test_update_movie_info(movie_store):
    assert movie_store.get_movie_info() == {}

    movie_store.update_movie_info("pulp+fiction+1994")
    
    assert movie_store.get_movie_info() == {
        "pulp+fiction+1994": {
            "movie_length": 154,
            "tmdb_id": 680,
            "popularity": "140.950236",
            "vote_average": "8.3",
        }
    }

def test_update_duplicate_movie_info(movie_store):
    movie_store.update_movie_info("pulp+fiction+1994")
    
    assert movie_store.get_movie_info() == {
        "pulp+fiction+1994": {
            "movie_length": 154,
            "tmdb_id": 680,
            "popularity": "140.950236",
            "vote_average": "8.3",
        }
    }

def test_update_multiple_movie_info(movie_store):
    movie_store.update_movie_info("get+shorty+1995")
    movie_store.update_movie_info("finding+nemo+2003")

    assert movie_store.get_movie_info() == {
        "pulp+fiction+1994": {
            "movie_length": 154,
            "tmdb_id": 680,
            "popularity": "140.950236",
            "vote_average": "8.3",
        },
        "get+shorty+1995": {
            "movie_length": 105,
            "tmdb_id": 8012,
            "popularity": "12.669608",
            "vote_average": "6.4",
        },
        "finding+nemo+2003": {
            "movie_length": 100,
            "tmdb_id": 12,
            "popularity": "25.497794",
            "vote_average": "7.6",
        }
    }