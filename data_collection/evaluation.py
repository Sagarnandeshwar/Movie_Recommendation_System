import os
import json
import copy
import utils.user_utils
from datetime import datetime

user_preference_file_path = "telemetry_data.json"
model_performance_file_path = "model_performance.json"

def add_list_unique(list_1, list_2):
    result = []
    for element in list_1:
        if element not in list_2:
            result.append(element)
    result = result + list_2
    return result


def all_recommendations(dic_recomm, current_time_stamp):
    recomm_movie = []
    for time_stamp in dic_recomm:
        recomm_movie = add_list_unique(recomm_movie,dic_recomm[time_stamp])
        if time_stamp == current_time_stamp:
            break
    return recomm_movie


def movie_inter_in_recomm(recomm_list,inter_movie):
    result = []
    for movie in inter_movie:
        if movie in recomm_list:
            result.append(movie)
    return result


def calculate_sucess(recom_list, interacted_list):
    return len(recom_list) / max(len(interacted_list),1) * 100


def average_success_rate(success_rate_list):
    average = 0
    for lis in success_rate_list:
        if len(lis) == 0:
            continue
    return average


def average_list(lis):
    return sum(lis) / max(len(lis), 1)


def evaluate_model(user_store, log_path):
    dataframe = user_store.get_user_store()
    model_success_rate_list = []
    model_like_score_list = []
    model_average_rate_list = []
    model_average_watchtime_list = []
    model_rate_proportion_list = []
    model_watch_proportion_list = []

    people_not_interact = 0
    people_interacted = 0

    for user_id in dataframe:
        dictionary = dataframe[user_id]
        interaction_list_rate = []
        movie_in_recomm_rate = []

        interaction_list_watch = []
        movie_in_recomm_watch = []

        average_rating_list = []
        average_watchtime_list = []

        mov_rec_score = 0
        mov_rec_score_like = 0

        if dictionary["rate"]:
            for rate_time_stamp in dictionary["rate"]:
                rated_movie_list = []
                recomm_list = all_recommendations(dictionary["predictions"], rate_time_stamp)
                for rated_movies in dictionary["rate"][rate_time_stamp]:
                    rated_movie_list = add_list_unique(rated_movie_list, [rated_movies])
                    interaction_list_rate = add_list_unique(interaction_list_rate, [rated_movies])
                    if rated_movies in recomm_list:
                        mov_rec_score = mov_rec_score + 1
                        average_rating_list.append(int(dictionary["rate"][rate_time_stamp][rated_movies]))
                        if int(dictionary["rate"][rate_time_stamp][rated_movies]) > 2:
                            mov_rec_score_like = mov_rec_score_like + 1
                movie_in_recomm_rate = movie_inter_in_recomm(recomm_list, rated_movie_list)

        if dictionary["watch"]:
            for watch_time_stamp in dictionary["watch"]:
                watch_movie_list = []
                recomm_list = all_recommendations(dictionary["predictions"], watch_movie_list)
                for watched_movies in dictionary["watch"][watch_time_stamp]:
                    watch_movie_list = add_list_unique(watch_movie_list, [watched_movies])
                    interaction_list_watch = add_list_unique(interaction_list_watch, [watched_movies])
                    if watched_movies in recomm_list:
                        mov_rec_score = mov_rec_score + 1
                        average_watchtime_list.append(int(dictionary["watch"][watch_time_stamp][watched_movies]))
                        if int(dictionary["watch"][watch_time_stamp][watched_movies]) > 10:
                            mov_rec_score_like = mov_rec_score_like + 1
                movie_in_recomm_watch = movie_inter_in_recomm(recomm_list, watch_movie_list)

        interaction_list = add_list_unique(interaction_list_watch, interaction_list_rate)
        movie_in_recomm = add_list_unique(movie_in_recomm_rate, movie_in_recomm_watch)

        if len(interaction_list) == 0:
            people_not_interact = people_not_interact + 1
            continue

        people_interacted = people_interacted + 1
        rate_success_rate = calculate_sucess(movie_in_recomm_rate, interaction_list_rate)
        model_rate_proportion_list.append(rate_success_rate)

        watch_success_rate = calculate_sucess(movie_in_recomm_watch, interaction_list_watch)
        model_watch_proportion_list.append(watch_success_rate)

        success_rate = calculate_sucess(movie_in_recomm, interaction_list)
        model_success_rate_list.append(success_rate)

        like_score = mov_rec_score_like / max(mov_rec_score,1) * 100
        model_like_score_list.append(like_score)

        avg_rate = average_list(average_rating_list)
        model_average_rate_list.append(avg_rate)

        avg_watchtime = average_list(average_watchtime_list)
        model_average_watchtime_list.append(avg_watchtime)

    model_success_rate = round(average_list(model_success_rate_list),2)
    model_like_score = round(average_list(model_like_score_list),2)
    model_average_rate = round(average_list(model_average_rate_list),2)
    model_average_watchtime = round(average_list(model_average_watchtime_list),2)
    model_rate_proportion = round(average_list(model_rate_proportion_list),2)
    model_watch_proportion = round(average_list(model_watch_proportion_list),2)

    log_str = "*****System Performance*****\n"
    log_str += "Recommendation System Success Rate: " + str(model_success_rate) + "%\n"
    log_str += "Recommended movie like score: " + str(model_like_score) + "%\n"
    log_str += "Average Rating of recommended movies : " + str(model_average_rate) + "/5\n"
    log_str += "Average Watch time of recommended movies: " + str(model_average_watchtime) + " min\n"
    log_str += "Recommendation System Success proportion in user raring: " + str(model_rate_proportion) + " %\n"
    log_str += "Recommendation System Success proportion in user watch time: " + str(model_watch_proportion) + " %\n"
    log_str += "No. of people who stays: " + str(people_interacted) + "\n"
    log_str += "No. of people who left: " + str(people_not_interact) + "\n"
    print(log_str)
    
    current_time = str(int(datetime.now().timestamp()))
    save_path = os.path.join(log_path, current_time + ".log")

    with open(save_path, 'w') as log_file:
        log_file.write(log_str)
    
    model_per_path = os.path.join(log_path, model_performance_file_path)
    
    with open(model_per_path, 'r') as input_f:
        model_info_dict = json.load(input_f)
    
    cur_model_per_dict = {
        "Success_Rate": model_success_rate,
        "Like_Score": model_like_score,
        "Average_Rating": model_average_rate,
        "Average_WatchTime": model_average_watchtime,
        "Success_Rate_Rated_Movie": model_rate_proportion,
        "Success_Rate_Watched_Movie": model_watch_proportion,
        "Registered_People": people_interacted,
        "Unregistered_People": people_not_interact,
        "Timestamp": current_time
    }
    model_info_dict["data"].append(cur_model_per_dict)
    with open(model_per_path, 'w') as output:
        json.dump(model_info_dict, output, indent=1)
        

def telemetry_data(user_store, log_path):
    data = user_store.get_user_store()
    tel_data_path = os.path.join(log_path, user_preference_file_path)
    
    with open(tel_data_path, 'r') as input_f:
        user_preference_dict = json.load(input_f)
    
    new_json_dict = {}
    
    for user_info_i in user_preference_dict:
        new_json_dict[user_info_i] = user_preference_dict[user_info_i]
    
    for user_info in data:
        dic = data[user_info]
        liked_move = []

        if dic["rate"]:
            for r_time_stamp in dic["rate"]:
                for rated_movie in dic["rate"][r_time_stamp]:
                    if int(dic["rate"][r_time_stamp][rated_movie]) > 2:
                        liked_move = add_list_unique(liked_move, [rated_movie])

        if dic["watch"]:
            for w_time_stamp in dic["watch"]:
                for watched_movie in dic["watch"][w_time_stamp]:
                    if int(dic["watch"][w_time_stamp][watched_movie]) > 10:
                        liked_move = add_list_unique(liked_move, [watched_movie])
                        
        if len(liked_move) == 0:
            continue
            
        if user_info in new_json_dict:
            new_json_dict[user_info] = add_list_unique(user_preference_dict[user_info], liked_move)
        if user_info not in new_json_dict:
            new_json_dict[user_info] = liked_move
            
    tel_data_path = os.path.join(log_path, user_preference_file_path)
    with open(tel_data_path, "w") as outfile:
        json.dump(new_json_dict, outfile, indent=1)
