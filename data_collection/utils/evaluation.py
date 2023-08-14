import json

user_store_file_part = 'data/user_store.json'


def add_list(list_1, list_2):
    result = []
    for element in list_1:
        if element not in list_2:
            result.append(element)
    result = result + list_2
    return result


def average_list(list_1):
    if len(list_1) == 0:
        return 0
    return sum(list_1) / len(list_1)


def calculate_success_fail(list_recommendation, list_interaction):
    success = 0
    fail = 0
    for movie in list_recommendation:
        if movie in list_interaction:
            success = success + 1
        else:
            fail = fail + 1
    success_rate = success / len(list_recommendation) * 100
    fail_rate = fail / len(list_recommendation) * 100
    return [success_rate, fail_rate]


def calculate_irrelevance(list_recommendation, list_interaction):
    irrelevant = 0
    for movie in list_interaction:
        if movie not in list_recommendation:
            irrelevant = irrelevant + 1
    irrelevant_rate = irrelevant / len(list_interaction) * 100
    return irrelevant_rate


def evaluate_model():
    f = open(user_store_file_part)
    data = json.load(f)

    model_success_rate_list = []
    model_fail_rate_list = []
    model_irrelevance_rate_list = []
    model_average_rate_list = []
    model_average_watch_time_list = []
    model_per_movie_like = []
    people_not_interact = 0

    for user_info in data["user_store"]:
        for user in user_info:
            # print(user)
            dic = user_info[user]
            list_recommendation = []
            list_rated_movie = []
            list_watch_movie = []
            list_interaction = []
            success_rate = 0.0
            fail_rate = 100.0
            irrelevant_rate = 0.0
            movie_in_recomm = 0
            movie_liked = 0
            for time_stamp in dic["predictions"]:
                list_recommendation = add_list(list_recommendation, dic["predictions"][time_stamp])

            if len(list_recommendation) == 0:
                continue

            for rated_movie in dic["rate"][dic["latest_prediction"]]:
                list_rated_movie = add_list(list_rated_movie, [rated_movie])
                if rated_movie in list_recommendation:
                    model_average_rate_list.append(dic["rate"][dic["latest_prediction"]][rated_movie])
                    movie_in_recomm = movie_in_recomm + 1
                    if dic["rate"][dic["latest_prediction"]][rated_movie] > 3:
                        movie_liked = movie_liked + 1

            for watched_movie in dic["watch"][dic["latest_prediction"]]:
                list_watch_movie = add_list(list_watch_movie, [watched_movie])
                if watched_movie in list_recommendation:
                    model_average_watch_time_list.append(dic["watch"][dic["latest_prediction"]][watched_movie])
                    movie_in_recomm = movie_in_recomm + 1
                    if dic["watch"][dic["latest_prediction"]][watched_movie] > 24:
                        movie_liked = movie_liked + 1

            list_interaction = add_list(list_watch_movie, list_rated_movie)

            if len(list_interaction) == 0:
                people_not_interact = people_not_interact + 1
                continue

            # Calculating stats
            [success_rate, fail_rate] = calculate_success_fail(list_recommendation, list_interaction)
            irrelevant_rate = calculate_irrelevance(list_recommendation, list_interaction)

            # Appending list
            model_success_rate_list.append(success_rate)
            model_fail_rate_list.append(fail_rate)
            model_irrelevance_rate_list.append(irrelevant_rate)
            model_per_movie_like.append(movie_liked / movie_in_recomm * 100)

    model_success_rate = round(average_list(model_success_rate_list), 2)
    model_fail_rate = round(average_list(model_fail_rate_list), 2)
    model_irrelevance_rate = round(average_list(model_irrelevance_rate_list), 2)
    model_average_rate = round(average_list(model_average_rate_list), 2)
    model_average_watch_time = round(average_list(model_average_watch_time_list), 2)
    recommendation_likeliness = round(average_list(model_per_movie_like), 2)

    print("*****System Performance*****")
    print("Recommendation System Success Rate: " + str(model_success_rate) + "%")
    print("Recommendation System Failure Rate: " + str(model_fail_rate) + "%")
    print("Recommendation System Irrelevant Rate: " + str(model_irrelevance_rate) + "%")
    print("Recommended Movies Average Rating: " + str(model_average_rate) + "/5")
    print("Recommended Movies Average Watch time: " + str(model_average_watch_time) + " min")
    print("Recommended movie likeliness: " + str(recommendation_likeliness) + "%")
    print("No. of people who left: " + str(people_not_interact))

    f.close


def telemetry_data():
    f = open(user_store_file_part)
    data = json.load(f)

    telemetry_data_dic = {}

    for user_info in data["user_store"]:
        for user in user_info:
            dic = user_info[user]
            liked_move = []
            for rated_movie in dic["rate"][dic["latest_prediction"]]:
                if dic["rate"][dic["latest_prediction"]][rated_movie] > 3:
                    liked_move.append(rated_movie)

            for watched_movie in dic["watch"][dic["latest_prediction"]]:
                if dic["watch"][dic["latest_prediction"]][watched_movie] > 24:
                    liked_move.append(watched_movie)
            telemetry_data_dic[user] = liked_move
    f.close
    return telemetry_data_dic


if __name__ == "__main__":
    evaluate_model()
    #print(telemetry_data())
