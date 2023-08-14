import pandas as pd
from util import convert

# def get_inter_from_raw(raw_csv_path="./movie/kafka_raw.csv"):
#     inter = pd.read_csv(raw_csv_path, header=None)
#     weight = 0.2
#     inter = pd.read_csv("./model/movie/inter.csv").sort_values("time") # sort by time
#     inter = inter.drop_duplicates(["user_id", "tmdb_id"], keep='last') # keep the latest watch data if watch the same movie twice
#     inter['grades'] = inter.apply(lambda row: row["popularity"]*row["vote_average"]*0.5*weight+row["rating"]*(1-weight), axis=1)
#     input_dict = {0:"user_id:token", 1:"tmdb_id:token", 2:"movie_id:token_seq", 3:"popularity:float", 4:"vote_average:float", 5:"rating:float", 6:"time:token", 7:"grades:float"}
#     convert(inter, input_dict, "./model/movie/movie.inter")

# def get_movie_from_inter(inter_path="./movie/inter_1M.csv"):
#     inter = pd.read_csv(inter_path)
#     movie = inter[['movie_id','rating']]
#     movie = movie.reset_index()
#     movie  = movie.rename(columns={"index": "movie_uid"})
#     movie = movie.groupby(['movie_uid','movie_id']).mean().sort_values(by="rating", ascending=False)
#     movie.to_csv("./movie/movie.csv")


def convert_inter_to_atom(inter_path="data/association.csv",  
    input_dict={0:"user_id:token", 1:"movie_id:token_seq", 2:"count:token", 3:"time:token_seq", 4:"tmdb_id:token", 5:"grade:float"},
    weight = 0.1):
    # process the inter
    inter = pd.read_csv(inter_path)
    inter["grade"] = inter.apply(lambda row: row["popularity"]*row["vote_average"]*0.5*weight+5*row["flag"]*(1-weight), axis=1)
    inter = inter.drop(["popularity", "vote_average", "flag"], axis=1)
    # convert the inter
    input_dict = input_dict
    convert(inter, input_dict, "model/movie/movie.inter")

if __name__ == "__main__":
    convert_inter_to_atom()