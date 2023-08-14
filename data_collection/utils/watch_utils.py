import pandas as pd

def parse_watch_log(log): 
    log_data = log.split(",")
    split_mpg = log_data[2].rsplit("/", 2)
    movieid = split_mpg[-2]
    minute = split_mpg[-1].replace(".mpg", "")

    new_log = {
        "time": log_data[0],
        "userid": log_data[1],
        "movieid": movieid,
        "minute": minute
    }

    return new_log

class WatchStore:
    watch_store = []
    watch_df = pd.DataFrame()

    def update_watch_store(self, log_str):
        log = parse_watch_log(log_str)
        self.watch_store.append(log)

        return log

    def get_watch_store(self):
        return self.watch_store

    def get_watch_store_df(self):
        self.watch_df = pd.DataFrame(self.watch_store)
        return self.watch_df
    
    def get_watch_store_csv(self, watch_filepath):
        df = self.get_watch_store_df()
        df.to_csv(watch_filepath, index=False, header=False)