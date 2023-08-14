import pandas as pd

def parse_rate_log(log):
    log_data = log.split(",")
    split_path = log_data[2].rsplit("/", 1)[1].split("=")
    movieid = split_path[0]
    rating = split_path[1]

    new_log = {
        "time": log_data[0],
        "userid": log_data[1],
        "movieid": movieid,
        "rating": rating
    }
    
    return new_log

class RateStore:
    rate_store = []
    rate_df = pd.DataFrame()

    def update_rate_store(self, log_str):
        log = parse_rate_log(log_str)
        self.rate_store.append(log)
        return log

    def get_rate_store(self):
        return self.rate_store

    def get_rate_store_df(self):
        self.rate_df = pd.DataFrame(self.rate_store)
        return self.rate_df
    
    def get_rate_store_csv(self, rate_filepath):
        df = self.get_rate_store_df()
        df.to_csv(rate_filepath, index=False, header=False)
    