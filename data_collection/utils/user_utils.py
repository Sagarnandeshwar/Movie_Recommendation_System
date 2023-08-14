from datetime import datetime
import pandas as pd

class UserPredictionStore:
    user_store = {}

    def take_predictions(self, request_log):
        if not request_log or "userid" not in request_log:
            return
        if request_log["userid"] not in self.user_store:
            self.user_store[request_log["userid"]] = {
                "predictions": {},
                "rate": {},
                "watch": {},
                "latest_prediction": ""
            }
        
        self.user_store[request_log["userid"]]['latest_prediction'] = request_log["timestamp"]
        self.user_store[request_log["userid"]]['predictions'][request_log["timestamp"]] = request_log["predictions"]
    
    ###

    # method take in ratings (self, ratelog)
        # if userid is not in userstore, skip
        # if user does exist in userstore,
            # if time is after latest prediction, add rate to user's rate dict

    # rate log looks like this:
    # log = {
    #     "time": log_data[0],
    #     "user_id": log_data[1],
    #     "movieid": movieid,
    #     "rating": rating
    # }

    def add_rating(self, ratelog):
        try:
            if ratelog["userid"] in self.user_store:
                user_id = ratelog['userid']
                latest_prediction = self.user_store[user_id]["latest_prediction"]

                if '.' in ratelog['time']:
                    ratelog['time'] = ratelog['time'][:ratelog['time'].find('.')]
                print(ratelog['time'])
                rate_time = datetime.strptime(ratelog['time'], '%Y-%m-%dT%H:%M:%S')

                if '.' in latest_prediction:
                    latest_prediction = latest_prediction[:latest_prediction.find('.')]
                print(latest_prediction)
                latest_prediction_time = datetime.strptime(latest_prediction, '%Y-%m-%dT%H:%M:%S')

                if rate_time >= latest_prediction_time:
                    if len(self.user_store[user_id]["rate"]) == 0:
                        self.user_store[user_id]["rate"][self.user_store[user_id]['latest_prediction']] = {}
                    if not self.user_store[user_id]["rate"].get(self.user_store[user_id]['latest_prediction']):
                        self.user_store[user_id]["rate"][self.user_store[user_id]['latest_prediction']] = {}    
                    self.user_store[user_id]["rate"][self.user_store[user_id]['latest_prediction']][ratelog["movieid"]] = ratelog['rating']
        
        except:
            return

    # new_log = {
    #     "time": log_data[0],
    #     "userid": log_data[1],
    #     "movieid": movieid,
    #     "minute": minute
    # }

    def add_watch_data(self, watch_log):
        try:
            if watch_log["userid"] in self.user_store:
                user_id = watch_log['userid']
                latest_prediction = self.user_store[user_id]["latest_prediction"]

                if '.' in watch_log['time']:
                    watch_log['time'] = watch_log['time'][:watch_log['time'].find('.')]
                print(watch_log['time'])
                watch_time = datetime.strptime(watch_log['time'], '%Y-%m-%dT%H:%M:%S')
                if '.' in latest_prediction:
                    latest_prediction = latest_prediction[:latest_prediction.find('.')]
                print(latest_prediction)
                latest_prediction_time = datetime.strptime(latest_prediction, '%Y-%m-%dT%H:%M:%S')

                if watch_time >= latest_prediction_time:
                    if len(self.user_store[user_id]["watch"]) == 0:
                        self.user_store[user_id]["watch"][self.user_store[user_id]['latest_prediction']] = {} 
                    if not self.user_store[user_id]["watch"].get(self.user_store[user_id]['latest_prediction']):
                        self.user_store[user_id]["watch"][self.user_store[user_id]['latest_prediction']] = {}    
                    self.user_store[user_id]["watch"][self.user_store[user_id]['latest_prediction']][watch_log["movieid"]] = watch_log['minute']
                
                for movie_time_stamp in self.user_store[user_id]["watch"]:
                    for movie_list in self.user_store[user_id]["watch"][movie_time_stamp]:
                        if watch_log["movieid"] in movie_list:
                            self.user_store[user_id]["watch"][movie_time_stamp][watch_log["movieid"]] = str(max(int(watch_log['minute']), int(self.user_store[user_id]["watch"][movie_time_stamp][watch_log["movieid"]])))

        except:
            return

    def get_user_store(self):
        return self.user_store
    
    def empty_user_store(self):
        self.user_store = {}

    def get_user_store_df(self):
        user_df = pd.DataFrame(self.user_store)
        return user_df

    def get_user_store_json(self, filepath):
        df = self.get_user_store_df()
        df.to_json(filepath)
