# Usage:
# python3 collect_processed.py [path] [logs] (rating_only) (reuse_data)

# Parameters:
# [path] required: path to directory location of resulting processed data
# [logs] required: number of kafka logs to collect
# (rating_only) optional: "True" if only want to collect kafka logs of type "rate"
# (reuse_data) optional: "True" if already have kafka_raw and only request for movie info

# Outputs:
# association.csv:
    # csv with info on
    # user_id, tmdb_id, movie_id, popularity, vote_average, rating
    # for each kafka log of type "rate"
# kafka_raw.csv
    # every kafka log collected
# rate.csv
    # every kafka rate log collected
# watch.csv
    # every kafka watch log collected

import sys
import csv
import evaluation
import utils.kafka_utils as kafka_utils
import utils.movie_utils as movie_utils
import utils.user_utils as user_utils
import utils.watch_utils as watch_utils
import utils.rate_utils as rate_utils
import utils.association_utils as association_utils
from tqdm import tqdm
import os.path
import pandas as pd
import json
from tqdm import tqdm

def collect_parsed_log_action(log, args):
    movie_store = args[0]
    user_store = args[1]
    watch_store = args[2]
    rate_store = args[3]
    association_store = args[4]
    
    type = kafka_utils.get_log_type(log)
    content = None

    # if it's type is watch
    if type == "watch":
        content = watch_store.update_watch_store(log)
        association_store.update_association_watch(content)
        user_store.add_watch_data(content)
    # if it's type is rate
    if type == "rate":
        content = rate_store.update_rate_store(log)
        association_store.update_association_rate(content)
        user_store.add_rating(content)
    # if it's type is request
    if type == "request":
        content = kafka_utils.parse_request_log(log)
        user_store.take_predictions(content)
    
    if content:
        movie_store.update_movie_info(content.get("movieid"))

if __name__ == '__main__':
    # arguments
    if len(sys.argv[1:]) < 2:
        print("Not enough args")
        sys.exit(1)
    
    arg_data_path = sys.argv[1]

    if not (os.path.exists(arg_data_path) and os.path.isdir(arg_data_path)):
        print("path doesnt exist")
        sys.exit(1)

    if not sys.argv[2].isdigit():
        print("Number of logs to collect is not a positive integer")
        sys.exit(1)
    
    rating_only = False

    if len(sys.argv[1:]) >= 3 and sys.argv[3] == "True":
        rating_only = True

    start_from_raw = True
    if len(sys.argv[1:]) >= 4 and sys.argv[4] == "True":
        start_from_raw = False

    amt_logs_collect = int(sys.argv[2])

    # paths
    data_path = os.path.join(arg_data_path)
    raw_filepath = os.path.join(data_path, 'kafka_raw.csv')
    watch_filepath = os.path.join(data_path, 'watch.csv')
    watch_count_filepath = os.path.join(data_path, 'watch_count.csv')
    rate_filepath = os.path.join(data_path, 'rate.csv')
    association_filepath = os.path.join(data_path, 'association.csv')
    movie_store_filepath = os.path.join(data_path, 'movie_store.json')

    # create data directory
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # get log file and logs
    kafka_utils.get_log_file_from_kafka(raw_filepath, amt_logs_collect, rating_only)
    logs = kafka_utils.get_logs_from_file(raw_filepath)

    # create stores
    movie_store = movie_utils.MovieStore()
    user_store = user_utils.UserPredictionStore()
    watch_store = watch_utils.WatchStore()
    rate_store = rate_utils.RateStore()
    association_store = association_utils.AssociationStore()
    
    # action for every log
    if start_from_raw:
        kafka_utils.for_each_log(logs, collect_parsed_log_action, movie_store, user_store, watch_store, rate_store, association_store)
    else:
        movie_store = kafka_utils.get_movie_on_rate(rate_file, movie_store)

    print("---")

    watch_store.get_watch_store_csv(watch_filepath)
    rate_store.get_rate_store_csv(rate_filepath)
    movie_store.get_movie_store_json(movie_store_filepath)
    association_store.get_association_csv(movie_store.get_movie_info(), association_filepath)

    with open(os.path.join(data_path, 'user_store.json'), 'w') as openfile:
        json.dump(user_store.get_user_store(), openfile, indent=4, separators=(',', ': '))

    evaluation.evaluate_model(user_store, arg_data_path)