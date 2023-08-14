from data_collection.utils.rest_api_utils import get_user_info, get_movie_info

def test_get_user_info():
    user = get_user_info(1)
    assert user["user_id"] == 1
    assert user["age"] == 34
    assert user["occupation"] == "sales/marketing"
    assert user["gender"] == "M"

def test_get_movie_info():
    id = "pulp+fiction+1994"
    movie = get_movie_info(id)
    assert movie["id"] == id
    assert movie["title"] == "Pulp Fiction"
