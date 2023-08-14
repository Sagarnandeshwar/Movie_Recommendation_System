import requests
import json

user_info_url = "http://fall2022-comp585.cs.mcgill.ca:8080/user/"
movie_info_url = "http://fall2022-comp585.cs.mcgill.ca:8080/movie/"

# get request to provided {url} for {id}
def get_info_from_rest(url, id):
    type = url.rsplit('/', 2)[1]
    url = url+str(id)
    filepath = "../data/"+type+'_info.json'
    response = requests.get(url)
    json_item = response.json()

    return json_item

# gets info of {id} user
def get_user_info(id):
    return get_info_from_rest(user_info_url, id)

# gets info of {id} movie
def get_movie_info(id):
    movie = get_info_from_rest(movie_info_url, id)
    if movie == {'message': 'movie not found'}:
        return None
    return movie
