from .rest_api_utils import get_movie_info
import pandas as pd

class MovieStore:
    movie_info = {}
    movie_df = pd.DataFrame()

    def update_movie_info(self, id):
        if id not in self.movie_info:
            movie_raw = get_movie_info(id)

            if not movie_raw:
                self.movie_info[id] = None
                return
            
            movie = {
                "movie_length": movie_raw.get("runtime"),
                "tmdb_id": movie_raw.get("tmdb_id"),
                "popularity": movie_raw.get("popularity"),
                "vote_average": movie_raw.get("vote_average"),
            }

            self.movie_info[id] = movie
    
    def get_movie_info(self):
        return self.movie_info
    
    def get_movie_store_df(self):
        self.movie_df = pd.DataFrame(self.movie_info)
        return self.movie_df

    def get_movie_store_json(self, movie_filepath):
        df = self.get_movie_store_df()
        df.to_json(movie_filepath)
    