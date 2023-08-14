import pandas as pd

class AssociationStore:
    association_store = {}

    def update_association_watch(self, log):
        key = str(log["userid"])+","+str(log["movieid"])
        
        if not key in self.association_store:
            self.association_store[key] = {
                "count": 0
            }
    
        self.association_store[key]["count"] += 1
        self.association_store[key]["time"] = log["time"]
    
    def update_association_rate(self, log):
        key = log["userid"]+","+log["movieid"]
        
        if not key in self.association_store:
            self.association_store[key] = {
                "count": 0,
                "rating": 0
            }
    
        self.association_store[key]["rating"] += int(log["rating"])
        self.association_store[key]["time"] = log["time"]
    
    def get_association_store(self):
        return self.association_store

    def get_association_series(self, movie_info):
        association_series = []
        count_err = 0

        for key in self.association_store.keys():
            
            try:
                key_split = key.split(",")
                movieid = key_split[1]
                count = self.association_store[key]["count"]
                
                rating = self.association_store[key].get("rating")
                flag_watch = count >= 0.5*movie_info[movieid]["movie_length"]
                flag = 0

                if (rating and rating >= 4) and (not rating and flag_watch):
                    flag = 1
                elif rating and rating < 4:
                    flag = 0

                item = {
                    "userid": key_split[0],
                    "movieid": movieid,
                    "count": count,
                    "time": self.association_store[key]["time"],
                    "tmdb_id": movie_info[movieid]["tmdb_id"],
                    "popularity": movie_info[movieid]["popularity"],
                    "vote_average": movie_info[movieid]["vote_average"],
                    "flag": flag
                }

                association_series.append(item)

            except:
                count_err += 1
                print("ERROR ASSOCIATION SERIES: " + str(key))
                continue
        
        print(str(count_err) + " errors detected")
        return association_series

    def get_association_csv(self, movie_info, filepath):
        series = self.get_association_series(movie_info)
        df = pd.DataFrame(series)
        df.to_csv(filepath, index=False)
